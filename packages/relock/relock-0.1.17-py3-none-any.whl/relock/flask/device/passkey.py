import os
import base64
import ujson as json
import logging
import webauthn

from typing import Any
from .base import Base

from flask import (current_app as app, 
				   has_request_context,
				   request,
				   session)

from webauthn.helpers.cose import COSEAlgorithmIdentifier
from webauthn.helpers.structs import (
	AttestationConveyancePreference,
	AuthenticatorAttachment,
	AuthenticatorSelectionCriteria,
	PublicKeyCredentialDescriptor,
	UserVerificationRequirement,
	ResidentKeyRequirement,
)

from .signals import (origin_authentication_user_agent_change,
					  origin_authentication_rekeying_nonce_created,
					  origin_authentication_remote_addr_change)
from .logic import Logic

class Credential(Logic):

	def __init__(self, key: str, 
					   value: Any = None,
					   public: bytes = bytes(),
					   pattern: str = 'Unknown+Desktop', 
					   **kwargs):
		if public is not bytes():
			self.public = public
		super().__init__(key, 		#user ID/email
						 value, 	#credential ID
						 pattern,   #os system + device kind
						 **kwargs)
		if public:
			self.public = public
			self.update()

	def __bool__(self):
		return True if hasattr(self, 'public') else False

	def __delete__(self):
		return self.delete()

	def __enter__(self):
		return self
 
	def __exit__(self, *args):
		pass

class Passkey(object):

	@property
	def credential(self):
		if not hasattr(self, '__credential') or not getattr(self, '__credential'):
			setattr(self, '__credential', Credential(session.get('email'),
													 pattern=self.platform))
		return getattr(self, '__credential')

	@property
	def counter(self):
		if not hasattr(self, 'signins'):
			self.signins = 0
		return self.signins

	@counter.setter
	def counter(self, value=None) -> int:
		if not hasattr(self, 'signins'):
			self.signins = 0
		self.signins = self.signins + 1

	def webauthn(self, options=None, registration=dict()) -> dict:
		"""Generate options for registering a credential via navigator.credentials.create()

		Args:
		    `rp_id`: A unique, constant identifier for this Relying Party.
		    `rp_name`: A user-friendly, readable name for the Relying Party.
		    `user_name`: A value that will help the user identify which account this credential is associated with. Can be an email address, etc...
		    (optional) `user_id`: A collection of random bytes that identify a user account. For privacy reasons it should NOT be something like an email address. Defaults to 64 random bytes.
		    (optional) `user_display_name`: A user-friendly representation of their account. Can be a full name ,etc... Defaults to the value of `user_name`.
		    (optional) `challenge`: A byte sequence for the authenticator to return back in its response. Defaults to 64 random bytes.
		    (optional) `timeout`: How long in milliseconds the browser should give the user to choose an authenticator. This value is a *hint* and may be ignored by the browser.
		    (optional) `attestation`: The level of attestation to be provided by the authenticator.
		    (optional) `authenticator_selection`: Require certain characteristics about an authenticator, like attachment, support for resident keys, user verification, etc...
		    (optional) `exclude_credentials`: A list of credentials the user has previously registered so that they cannot re-register them.
		    (optional) `supported_pub_key_algs`: A list of public key algorithm IDs the RP chooses to restrict support to. Defaults to all supported algorithm IDs.

		Returns:
		    Registration options ready for the browser. Consider using `helpers.options_to_json()` in this library to quickly convert the options to JSON.
		"""
		if session.get('email') and not options:
			if options := webauthn.generate_registration_options(
				rp_id=app.config.get('SERVER_HOST'),
				rp_name=app.config.get('NAME', 'relock'),
				# user_id=bytes([1, 2, 3, 4]),
				user_name=session.get('email'),
				user_display_name=session.get('email'),
				attestation=AttestationConveyancePreference.DIRECT,
				authenticator_selection=AuthenticatorSelectionCriteria(
					authenticator_attachment=AuthenticatorAttachment.PLATFORM,
					resident_key=ResidentKeyRequirement.REQUIRED,
					user_verification=UserVerificationRequirement.DISCOURAGED,
					require_resident_key=True
				),
				challenge=os.urandom(16),
				# exclude_credentials=[
				# 	PublicKeyCredentialDescriptor(id=b"1234567890"),
				# ],
				supported_pub_key_algs=[COSEAlgorithmIdentifier.ECDSA_SHA_256,
									    COSEAlgorithmIdentifier.EDDSA,
									    COSEAlgorithmIdentifier.ECDSA_SHA_512,
									    COSEAlgorithmIdentifier.RSASSA_PSS_SHA_256,
									    COSEAlgorithmIdentifier.RSASSA_PSS_SHA_384,
									    COSEAlgorithmIdentifier.RSASSA_PSS_SHA_512,
									    COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
									    COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_384,
									    COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_512,
									],
				timeout=60000,
			):
				if str := webauthn.options_to_json(options):
					session['passkey'] = json.loads(str)
					return str
		elif session.get('email') and options:
			try:
				registration = webauthn.verify_registration_response(
					# Demonstrating the ability to handle a plain dict version of the WebAuthn response
					credential=options['credential'],
					expected_challenge=webauthn.base64url_to_bytes(session['passkey']['challenge']),
					expected_origin=app.config.get('SERVER_SCHEME', 'https') + "://" + app.config.get('SERVER_HOST'),
					expected_rp_id=app.config.get('SERVER_HOST'),
					require_user_verification=True,
				)
			except:
				logging.error('Faild to register passkey for %s', self.user)
			else:
				if _ := Credential(session.get('email'),
								   registration.credential_id,
								   public=registration.credential_public_key,
								   pattern=self.platform,
								   auto_commit=True):
					setattr(self, '__credential', _)
			finally:
				return dict(id=list(registration.credential_id))
		return dict(id=list())

	def authenticate(self, credential=None, verification=object()) -> str:
		if not session.get('challenge'):
			session['challenge'] = os.urandom(32)	
		if session.get('email') and not credential:
			try:
				credential = webauthn.generate_authentication_options(
					rp_id=app.config.get('SERVER_HOST'),
					challenge=session.get('challenge'),
					allow_credentials=[PublicKeyCredentialDescriptor(id=bytes(self.credential))],
					user_verification=UserVerificationRequirement.DISCOURAGED)
			except:
				logging.error('Faild to create passkey.')
			else:
				if credential := webauthn.options_to_json(credential):
					session['passkey'] = json.loads(credential)
			finally:
				return credential
		elif session.get('email') and credential and session.get('passkey'):
			if _ := session.get('passkey'):
				try:
					verification = webauthn.verify_authentication_response(
						# Demonstrating the ability to handle a stringified JSON version of the WebAuthn response
						credential=credential,
						expected_challenge=webauthn.base64url_to_bytes(_.get('challenge')),
						expected_rp_id=app.config.get('SERVER_HOST'),
						expected_origin=app.config.get('SERVER_SCHEME', 'https') + "://" + app.config.get('SERVER_HOST'),
						credential_public_key=self.credential.public,
						credential_current_sign_count = 0,
						require_user_verification = False,
					)
				except:
					logging.error('Faild to authenticate user %s', session.get('identity'))
				else:
					session['passkey'] = webauthn.base64url_to_bytes(_.get('challenge'))
				finally:
					if hasattr(verification, 'credential_id'):
						return dict(id=list(verification.credential_id))
		return dict()

	@property
	def passkey(self):
		if has_request_context():
			if _ := session.get('challenge', bytes):
				if session.get('passkey', bytes()) == _:
					session.pop('passkey')
					session.pop('challenge')
					return True
		return False
