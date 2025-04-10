import re
import json
import os
import time
import hashlib
import xxhash
import binascii
import base64
import secrets
import logging
import pickle
import webauthn

from webauthn.helpers.cose import COSEAlgorithmIdentifier
from webauthn.helpers.structs import (
	AttestationConveyancePreference,
	AuthenticatorAttachment,
	AuthenticatorSelectionCriteria,
	PublicKeyCredentialDescriptor,
	UserVerificationRequirement,
	ResidentKeyRequirement,
)

from flask import current_app as app, url_for, redirect, request, session, Response
from flask_login import current_user as worker
from uuid import uuid4
from datetime import datetime
from datetime import timedelta

from typing import Any

from flask_login import (current_user,
						 UserMixin, 
						 login_user, 
						 logout_user)

from app.plugins.relock import KDM
from app.plugins.aes.gcm import GCM
from app.rdbms.models.user import User

from ..logic import Logic

import numpy as np

class Device(Logic):

	def __init__(self, key: str, 
					   value: Any = None, 
					   pattern: str = 'default', **kwargs):
		super().__init__(key, value, pattern, **kwargs)
		self.__kdm = KDM(self.value,	 	 #signing private key
						 self.client,	 	 #client public key
						 self.session,	 	 #last session key
						 self.secret,		 #actual secret key
						 power=128)
		self.__cache = list()
		if not self.addr:
			self.addr  = request.remote_addr #actual remote_addr

	def __enter__(self):
		return self
 
	def __exit__(self, *args):
		pass

	@property
	def kdm(self):
		return self.__kdm

	@property
	def addr(self):
		if hasattr(self, 'ip'):
			return self.ip

	@addr.setter
	def addr(self, value:str = str()):
		self.ip = value

	@property
	def nonce(self):
		if hasattr(self, 'nonce_bytes'):
			return getattr(self, 'nonce_bytes')
		return bytes()

	@nonce.setter
	def nonce(self, value:bytes = bytes()):
		setattr(self, 'nonce_bytes', value)

	@property
	def associated(self):
		if app.config.get('ASSOCIATE_SERVER'):
			if app.config.get('SERVER_HOST') != app.config.get('ASSOCIATE_SERVER'):
				return app.config.get('ASSOCIATE_SERVER')

	@property
	def associator(self):
		if hasattr(self, 'associator_secret_key'):
			return getattr(self, 'associator_secret_key')
		return bytes()

	@associator.setter
	def associator(self, value:bytes = bytes()):
		setattr(self, 'associator_secret_key', value)
		self.update()

	@property
	def signature(self):
		if hasattr(self, 'associator_signature_key'):
			return getattr(self, 'associator_signature_key')
		return bytes()

	@signature.setter
	def signature(self, value:bytes = bytes()):
		setattr(self, 'associator_signature_key', value)
		self.update()

	@property
	def approved(self):
		if hasattr(self, 'approved_key'):
			return getattr(self, 'approved_key')
		return bytes()

	@approved.setter
	def approved(self, value:Any = True):
		setattr(self, 'approved_key', value)

	@approved.deleter
	def approved(self):
		delattr(self, 'approved_key', value)

	@property
	def authenticated(self):
		return session.get('authenticated')

	@authenticated.setter
	def authenticated(self, value:Any = True):
		session['authenticated'] = True

	@authenticated.deleter
	def authenticated(self):
		if 'authenticated' in session:
			del session['authenticated']

	@property
	def challange(self) -> bytes():
		if challange := session.get('challange', bytes()):
			if self.associator:
				with GCM(self.associator) as gcm:
					print(request.url)
					return gcm.encrypt((challange, app.config.get('SERVER_HOST')))

	@challange.setter
	def challange(self, value:bytes = bytes()):
		if self.associator:
			session['return'] = value
			session['challange'] = os.urandom(16)

	@challange.deleter
	def challange(self):
		if 'challange' in session:
			del session['challange']
		if 'return' in session:
			del session['return']

	@property
	def grind(self):
		if hasattr(self, 'grind_bytes'):
			return getattr(self, 'grind_bytes')
		return bytes()

	@grind.setter
	def grind(self, value:bytes = bytes()):
		setattr(self, 'grind_bytes', value)

	@property
	def inner(self):
		if not hasattr(self, 'inner_key'):
			self.inner_key = os.urandom(32)
		return self.inner_key

	@inner.setter
	def inner(self, value:bytes):
		self.inner_key = value

	@property
	def client(self):
		if not hasattr(self, 'client_key'):
			self.client_key = bytes()
		return self.client_key

	@client.setter
	def client(self, value:bytes):
		self.client_key = value

	@property
	def session(self):
		return session.get('x25519', bytes())

	@session.setter
	def session(self, value:bytes):
		session['x25519'] = value

	@property
	def auth(self):
		if not hasattr(self, 'auth_key'):
			self.auth_key = os.urandom(32)
			self.update()
		with GCM(self.inner) as gcm:
			return base64.urlsafe_b64encode(gcm.encrypt(self.auth_key)).decode()

	@auth.setter
	def auth(self, value:bytes):
		if not hasattr(self, 'auth_key'):
			self.auth_key = value
			self.update()

	@auth.deleter
	def auth(self):
		delattr(self, 'auth_key')

	def confirm(self, value:bytes):
		if hasattr(self, 'auth_key'):
			with GCM(self.inner) as gcm:
				if bytes := base64.urlsafe_b64decode(value):
					if _ := gcm.decrypt(bytes):
						if _ == self.auth_key:
							del self.auth
							return True

	@property
	def autologin(self):
		if not hasattr(self, 'auto_login'):
			setattr(self, 'auto_login', False)
		return self.auto_login

	@autologin.setter
	def autologin(self, value:bytes):
		setattr(self, 'auto_login', value)

	@autologin.deleter
	def autologin(self):
		delattr(self, 'auto_login')

	@property
	def recovery(self):
		return session.get('recovery', bytes())

	@recovery.setter
	def recovery(self, value:bytes):
		session['recovery'] = value

	@recovery.deleter
	def recovery(self):
		del session['recovery']

	@property
	def user(self):
		if hasattr(self, 'user_id'):
			return self.user_id

	@user.setter
	def user(self, value:int):
		self.user_id = value

	@property
	def cookie(self):
		return hasattr(self, '__fresh_cookie')

	@cookie.setter
	def cookie(self, value:bool = True):
		setattr(self, '__fresh_cookie', True)

	@property
	def secret(self):
		if not hasattr(self, 'secret_key'):
			self.secret_key = bytes()
		if not hasattr(self, '__secret'):
			self.__secret = bytes()
			# With quick open and close tab in the browser
			# the browser will restore the session, thus session
			# cookie is not deleted imidietly
			if self.session or self.recovery and self.secret_key:
				try:
					with GCM(self.recovery or self.session) as gcm:		
						self.__secret = gcm.decrypt(self.secret_key)
				except:
					logging.error('Secret decryption faild with %s', self.recovery or self.session)
				else:
					pass
					# print(np.frombuffer(self.__secret, np.uint8))
		return self.__secret

	@secret.setter
	def secret(self, value:bytes):
		if not self.session and value:
			raise SystemError('No session key to encrypt')
		if self.session and value:
			with GCM(self.session) as gcm:
				self.secret_key = gcm.encrypt(value)
				self.__secret = value	
			# logging.trace('New secret by: %s', self.session)
			# print(np.frombuffer(value, np.uint8))
		elif not value:
			self.secret_key = bytes()


	@property
	def stamp(self):
		return session.get('stamp', bytes())

	@stamp.setter
	def stamp(self, value:bytes):
		session['stamp'] = value

	@stamp.deleter
	def stamp(self):
		del session['stamp']

	@property
	def hash(self):
		if hasattr(self, 'secret_key') and self.secret_key:
			return hashlib.blake2b(self.secret, salt=bytes(16),
												digest_size=16).digest()
		return bytes()

	def exchange(self, key:bytes = bytes(), 
					   token:bytes = bytes(), 
					   recovery:bytes = bytes()):
		if public := self.kdm.exchange(key):
			# logging.trace('Client public key %s', np.frombuffer(key, dtype=np.uint8))
			# logging.trace('Server public key %s', np.frombuffer(public, dtype=np.uint8))
			if token == self.hash:
				token = str()
				# Make sure to load last session key from cookie
				# if request.cookies.get('auto_login'):
				# 	with GCM(app.config.get('SECRET_KEY')) as gcm:
				# 		if data := gcm.decrypt(base64.b64decode(request.cookies.get('auto_login'))):
				# 			logging.attent(self.recovery == data.get('session'))
				# 			self.recovery = data.get('session')
				# 		else:
				# 			logging.error('Wrong secret key - cookie decryption faild.')
				if not self.secret:
					self.client   = bytes(self.kdm.client)
					self.session  = bytes(self.kdm.session)
					self.stamp    = bytes(self.hash)
					self.secret   = bytes(self.kdm.secret)
					self.addr 	  = request.remote_addr
					if recovery := bytes(self.kdm.session):
						if not bool(self):
							self.save()
				elif recovery := bytes(self.recovery):
					self.session = bytes(self.kdm.session)
					self.addr 	 = request.remote_addr
					if token := self.rekeying():
						self.recovery = self.session
						self.stamp    = self.hash

				self.cookie = True

				with GCM(self.session) as gcm:
					return dict(key=list(public),
								signer=list(bytes(self.kdm.signer)),
								token=token if isinstance(token, str) else list(token),
								recovery=list(gcm.encrypt(recovery, True)),
								error=str())
		logging.error('Key agreement invalid STAMP.')
		return dict(key=list(),
					signer=list(),
					token=str(),
					recovery=list(),
					error='Invalid stamp.')

	def rekeying(self, salt=bytes(), token=bytes(), hexlify=True):
		if isinstance(salt, str):
			try:
				salt = binascii.unhexlify(salt)
			except:
				return False
			else:
				if len(salt) != 32:
					return False
		if nonce := self.kdm.rekeying(salt, token):
			self.secret = bytes(self.kdm.secret)
			self.stamp  = self.hash
			session['re-keying'] = time.time()
			logging.verbose(time.time())
			session['re-rolls'] = session.get('re-rolls', 0) + 1
			# print(np.frombuffer(self.kdm.secret, np.uint8))
			if self.update():
				logging.info('re-keying finalized, device object updated.')
				self.recovery = self.session
				self.cookie = True
				if isinstance(nonce, bool):
					return nonce
				if hexlify:
					return binascii.hexlify(nonce).decode()
				return nonce
		return False

	def clear(self):
		self.client = bytes()
		self.secret = bytes()
		self.session = bytes()
		self.recovery = bytes()
		self.nonce = bytes()
		setattr(self, '__clear', True)
		setattr(self, '__fresh_cookie', True)
		session.pop('recovery', None)
		session.pop('x25519', None)
		session.pop('device', None)
		if self.logout():
			return bool(self.delete())
		return False

	def login(self, user:object = None) -> bool:
		if not user:
			user = User(self.user)
		if user and login_user(user, remember=False, 
									 duration=timedelta(minutes=app.config.get('SESSION_MAX_TIME')),
									 force=True):
			self.seen = time.time()
			if self.update():
				return worker.is_authenticated
		return worker.is_authenticated

	def logout(self) -> bool:
		self.seen = time.time()
		if device := self.update() if logout_user() else None:
			del self.challange
			return True
		return False

	def register(self, user:object = None) -> bool:
		if user and self.user:
			return user.get_id() == self.user
		if user and user.get_id() and not self.user:
			self.user = user.get_id()
			if self.update():
				return user.get_id() == self.user
		return False

	def verify(self, data:bytes, signature:bytes, valid:bool = False) -> bool:
		try:
			if isinstance(data, str) and int(data, 16):
				data = binascii.unhexlify(data)
			if isinstance(signature, str) and int(signature, 16):
				signature = binascii.unhexlify(signature)
			valid = self.kdm.verify(data, signature)
		except:
			logging.error('Invalid signature. The transferred data are not signed with the correct key.')
		else:
			logging.debug('Signature is correct.')
		finally:
			return valid

	def validate(self, token:bytes, valid:bool = False) -> bool:
		try:
			if isinstance(token, str) and int(token, 16):
				token = binascii.unhexlify(token)
		except:
			logging.error('Invalid token. The validated token cannot be unpacked.')
		else:
			try:
				valid = self.kdm.validate(token)
			except: 
				logging.error('Invalid token. The validated token does not match the secret.')
			else:
				logging.debug('Token match the server side.')
		finally:
			if cache := app.config.get('SESSION_CACHE'):
				if not cache in session:
					session[cache] = list()
				if token in session[cache]:
					logging.error('Token re-use, same token was seen before. %s', token)
					valid = False
				else:
					session[cache].append(token)
		return valid


	def token(self) -> bool:
		return self.kdm.token()

	def sign(self, value:bytes) -> bool:
		return self.kdm.sign(value)

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
		if self.user and not options:
			if options := webauthn.generate_registration_options(
				rp_id=app.config.get('SERVER_HOST'),
				rp_name=app.config.get('NAME', 'relock'),
				# user_id=bytes([1, 2, 3, 4]),
				user_name=self.user,
				user_display_name=self.user,
				# attestation=AttestationConveyancePreference.DIRECT,
				authenticator_selection=AuthenticatorSelectionCriteria(
					authenticator_attachment=AuthenticatorAttachment.PLATFORM,
					resident_key=ResidentKeyRequirement.REQUIRED,
					user_verification=UserVerificationRequirement.REQUIRED,
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
				timeout=12000,
			):
				if str := webauthn.options_to_json(options):
					self.passkey = json.loads(str)
					if self.update():
						return str
		elif self.user and options:
			# try:
			registration = webauthn.verify_registration_response(
				# Demonstrating the ability to handle a plain dict version of the WebAuthn response
				credential=options['credential'],
				expected_challenge=webauthn.base64url_to_bytes(self.passkey['challenge']),
				expected_origin=app.config.get('SERVER_SCHEME') + "://" + app.config.get('SERVER_HOST'),
				expected_rp_id=app.config.get('SERVER_HOST'),
				require_user_verification=True,
			)
			# except:
			# 	logging.error('Faild to register passkey for %s', self.user)
			# else:
			self.credential_id = registration.credential_id
			self.credential_public_key = registration.credential_public_key
			# finally:
			self.passkey = base64.urlsafe_b64encode(os.urandom(16)).decode()
			if self.update():
				return dict(id=list(registration.credential_id),
							url=session.get('url'),
							token=self.passkey)
		return dict(id=list())

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

	def authenticate(self, credential=None, verification=object()) -> str:
		# del self.credential_id
		# del self.credential_public_key
		logging.info(self.user)
		logging.info(credential)
		if self.user and not credential:
			if credential := webauthn.generate_authentication_options(
							rp_id=app.config.get('SERVER_HOST'),
							challenge=os.urandom(32),
							allow_credentials=[PublicKeyCredentialDescriptor(id=self.credential_id)],
							user_verification=UserVerificationRequirement.REQUIRED):
				if str := webauthn.options_to_json(credential):
					self.passkey = json.loads(str)
					if self.update():
						return str
		elif self.user and credential:
			try:
				verification = webauthn.verify_authentication_response(
					# Demonstrating the ability to handle a stringified JSON version of the WebAuthn response
					credential=credential,
					expected_challenge=webauthn.base64url_to_bytes(self.passkey['challenge']),
					expected_rp_id=app.config.get('SERVER_HOST'),
					expected_origin=app.config.get('SERVER_SCHEME') + "://" + app.config.get('SERVER_HOST'),
					credential_public_key=self.credential_public_key,
					credential_current_sign_count = 0,
					require_user_verification = True,
				)
			except:
				logging.error('Faild to authenticate user %s', self.user)
			else:
				self.counter = 1
			finally:
				logging.info('authentication sucess.')
				# del self.credential_id
				# del self.credential_public_key
				self.passkey = base64.urlsafe_b64encode(os.urandom(16)).decode()
				if self.update():
					return dict(id=list(verification.credential_id),
								url=session.get('url'),
								token=self.passkey,
								counter=self.counter)
				else:
					logging.error('update faild.')
		return dict()

	@property
	def credential(self):
		if hasattr(self, 'credential_id'):
			return base64.urlsafe_b64encode(self.credential_id).decode()
		return str()

	def passkey_login(self, token):
		if hasattr(self, 'passkey'):
			if token == self.passkey:
				del self.passkey
				if self.update():
					return True
		return False

	@property
	def id(self):
		return self.kdm.identity.decode()

	@Logic.timer
	def set_cookie(self, response):
		logging.info('set cookie in progress...')
		if name := app.config.get('LOGIN_COOKIE_NAME'):
			if stamp := app.config.get('STAMP_COOKIE_NAME'):
				if hasattr(self, '__clear'):
					logging.trace('Clear cookie event')
					response.set_cookie(name, value=base64.b64encode(bytes()).decode(),
											  expires=datetime.now(),
											  max_age=timedelta(seconds=1),
											  path='/',
											  secure=True, 
											  httponly=True,
											  samesite=app.config.get('LOGIN_COOKIE_SAMESITE', 'lax'))
				else:
					logging.debug('Exit recovery key established.')
					if random := os.urandom(32):
						with GCM(random) as gcm:
							if _ := dict(key=self.key,
										 stamp=self.hash,
										 session=self.session):
								if bytearray := base64.b64encode(gcm.encrypt(_)).decode():
									if key := xxhash.xxh128(bytearray).digest():
										if self.associate(key, random):
											response.set_cookie(name, value=bytearray,
																	  expires=datetime.now() + timedelta(days=365),
																	  max_age=timedelta(days=365),
																	  path='/',
																	  secure=True, 
																	  httponly=True,
																	  samesite=app.config.get('LOGIN_COOKIE_SAMESITE', 'lax'))
											print('STAMP COOKIE SAMESITE', app.config.get('STAMP_COOKIE_SAMESITE', 'lax'))
											response.set_cookie(stamp,value=binascii.hexlify(self.hash).decode(),
																	  expires=datetime.now() + timedelta(days=365),
																	  max_age=timedelta(days=365),
																	  path='/',
																	  secure=True, 
																	  httponly=True,
																	  samesite=app.config.get('STAMP_COOKIE_SAMESITE', 'lax'))
		session[app.config.get('SESSION_CACHE')] = list()
		return response

	@classmethod
	# @Logic.timer
	def load_cookie(cls, stamp=bytes()):
		# session.modified = True
		if not '/static' in request.url and \
		   not '.mp3' in request.url and \
		   not '.js' in request.url and \
		   not '.css' in request.url:
			# print(request.headers)
			if name := app.config.get('LOGIN_COOKIE_NAME'):
				if stamp := app.config.get('STAMP_COOKIE_NAME'):
					if cookie := request.cookies.get(name):	
						if stamp := request.cookies.get(stamp):
							stamp = binascii.unhexlify(stamp)
						if key := Device.associate(xxhash.xxh128(cookie).digest()):
							if session.get('x25519') == session.get('recovery'):
								if device := Device(key=session.get('device')):
									if stamp and worker.is_authenticated:
										if worker.is_authenticated and stamp != session.get('stamp') or stamp != device.stamp:
											logging.error('STAMP identyfication error. Worker session was terminated.')
											logout_user()									
									return setattr(request, 'device', device)
							if cookie := base64.b64decode(cookie):
								with GCM(key) as gcm:
									try:
										if dict := gcm.decrypt(cookie):
											session['device'] = dict.get('key')
											session['stamp'] = dict.get('stamp')
											session['recovery'] = dict.get('session')
									except:
										logging.attent('Cookie has invalid content, hacking attempt?')
									else:
										if device := Device(key=session.get('device')):
											logging.debug('Device recovered from valid cookie.')
											return setattr(request, 'device', device)
									finally:
										logging.debug('Load device from cookie.')
					else:
						logging.debug('Cookie is not attached to the request.')
						print(request.url)
						print(request.headers)
						print(request.cookies)
			# else:
			with KDM() as kdm:
				session['device'] = bytes(kdm.signer)
				session['recovery'] = bytes()
				session['stamp'] = bytes()
				setattr(request, 'device', Device(key=bytes(kdm.signer),
												  value=abs(kdm.signer),
												  auto_commit=False))

	@classmethod
	def update_cookie(cls, response):
		if app.config.SESSION_COOKIE_NAME in request.cookies:
			if hasattr(request, 'device') and worker.is_authenticated:
				request.device.login()
		if hasattr(request, 'device') and request.device.cookie:
			return request.device.set_cookie(response)
		return response