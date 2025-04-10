import time
import threading

from functools import wraps

from blinker import Signal, NamedSignal
from flask import (current_app as app,
				   has_request_context,
				   request,
				   session)
from flask_login import current_user as worker

class Thread(object):

	counter = 0

	@classmethod
	def daemon(cls, function):
		@wraps(function)
		def daemon(*args, **kwargs):
			if has_request_context() and worker:
				kwargs = {'service_host': app.config.get('SERVER_HOST'),
						  'caep_enabled': app.config.get('CAEP_ENABLED'),
						  'otel_enabled': app.config.get('OTEL_ENABLED'),
						  'name': args[0].name,
						  'host': request.headers.get('Host'),
						  'agent': request.headers.get('User-Agent'),
						  'addr': request.remote_addr,
						  'method': request.method,
						  'url': request.url,
						  'path': request.path,
						  'user': worker.get_id(),
						  'email': worker.get_email(),
						  'authenticated': worker.is_authenticated,
						  'active': worker.is_active,
						  'anonymous': worker.is_anonymous,
						  'device': session.get('device', bytes()),
						  'stamp': session.get('stamp', bytes()),
						  **kwargs}
			if _ := threading.Thread(target=function, 
									 name=args[0].name, 
									 args=(*args,
									 	   app._get_current_object().session_sentinel),
									 kwargs=kwargs):
				return _.start()
		return daemon


class SentinelSignal(Signal):
	"""A named generic notification emitter."""

	def __init__(self, name, doc=None):
		Signal.__init__(self, doc)

		#: The name of this signal.
		self.name = name

	@Thread.daemon
	def send(self, *args, **kwargs):
		"""
		Emit this signal on behalf of *sender*, passing on **kwargs.
		Returns a list of 2-tuples, pairing receivers with their return
		value. The ordering of receiver notification is undefined.
		:param self:
		"""
		# Using '*args' rather than 'sender=None' allows 'sender' to be
		# used as a keyword argument- i.e. it's an invisible name in the
		# function signature.
		if len(args) > 1:
			raise TypeError('send() accepts only one positional argument, '
							'%s given' % len(args))
		if not self.receivers:
			return []
		
			
		return [(receiver, receiver(args[0], **kwargs))
				for receiver in self.receivers_for(args[0])]

class Namespace(dict):
	"""A mapping of signal names to signals."""

	def signal(self, name, doc=None):
		"""Return the :class:`NamedSignal` *name*, creating it if required.

		Repeated calls to this function will return the same signal object.

		"""
		try:
			return self[name]
		except KeyError:
			return self.setdefault(name, SentinelSignal(name, doc))

_signals = Namespace()

#: Sent when the device is loaded from the cookie. In addition to the app (which
#: is the sender), it is passed `device`, which is the device being reloaded.
device_loaded_from_cookie = _signals.signal("device-loaded-from-cookie")

#: Sent when the new version of the device cookie and stamp cookie is sent to the 
#: user's browser. Typically indicates that the re-keying / re-establishment process 
#: has been completed correctly.
device_cookie_and_stamp_set = _signals.signal("device_cookie_and_stamp_set")

#: Sent when the new version of the device cookie and stamp cookie is sent to the 
#: user's browser, before sending the cookie previous keys are erased on server side.
device_cookie_deprecated_keys_removed = _signals.signal("device_cookie_deprecated_keys_removed")

#: Sent when an incoming request does not have a `device cookie` attached, or 
#: when cookie encrypted data cannot be accessed. Typically this is a session start.
blank_device_object_created = _signals.signal("blank_device_object_created")

#: Sent when an incoming request does not have a `device cookie` attached. Typically 
#: this is a clean session start.
request_without_device_cookie = _signals.signal("request-without-device-cookie")

#: Sent if the 'device session' exists and the incoming request does not have a 
#: `device cookie` attached. Abnormal behaviour of the user's browser or incorrect 
#: settings for cookies - may occur if the user manually deletes cookies.
session_request_without_cookie = _signals.signal("session_request_without_cookie")

#: Sent when the cookie attached to the request is not properly decoded
#: with base64 encoder. Critical signal, someone manipultes the cookie data.
device_cookie_base64_decode_failure = _signals.signal("device_cookie_base64_decode_failure")

#: Sent when the request has device cookie attached but there is no corresponding
#: decryption key on server side. This can indicate session hijacking, as the 
#: corresponding server-side keys are expired when a new version of the Evolution Key 
#: is generated.
device_cookie_key_not_exists = _signals.signal("device-cookie-key-not-exists")

#: Sent when the request has a device cookie attached and the associated key exists 
#: in storage, and despite that decryption faild. Theoretically this should never 
#: happen.
device_cookie_decryption_faild = _signals.signal("device_cookie_decryption_faild")

#: Sent when a device cookie is attached to the request, but there is no corresponding 
#: data in session on the server side. Server session has expired.
device_session_no_longer_exists = _signals.signal("device_session_no_longer_exists")

#: Sent when the stamp cookie attached to request is not hex encoded and cannot
#: be loaded. Cookie exists and is not valid. Critical signal.
stamp_cookie_decode_failure = _signals.signal("stamp_cookie_decode_failure")

#: Sent when the request has stamp cookie attached but on the server side stamp
#: does not match the attached value. This might be a sign of credential theft or
#: abnormal behaviour of browser (cookie was not updated fast enough).
device_cookie_invalid_stamp = _signals.signal("device_cookie_invalid_stamp")

#: Sent if the request has a device cookie attached to it but does not have a stamp 
#: cookie attached. This is abnormal and may indicate that the credentials have been 
#: stolen.
device_cookie_stamp_cookie_not_exists = _signals.signal("device_cookie_stamp_cookie_not_exists")

#: Sent if a stamp cookie is attached to the request and the stamp matches the 
#: session stamp and the server-side device stamp. This means that the basic 
#: credentials have been validated.
device_cookie_session_confirmed = _signals.signal("device_cookie_session_confirmed")

#: Sent when the request has began to be processed. Sends core information about request 
#: agent and basic data possible to get from request object.
request_processing_has_started = _signals.signal("request_processing_has_started")

#: Sent when the request processing has been completed. This signal means the end 
#: of data processing.
request_processing_has_been_completed = _signals.signal("request_processing_has_been_completed")

#: Sent when the incoming user device does not have a cookie and new key agreement 
#: have been done. Determines the moment when a new user device is has been detected 
#: and the session key establishment for that specific device.
key_agreement_success_for_new_device = _signals.signal("key-agreement-success-for_new-device")

#: Sent when the incoming exchange request has a STAMP that does not match the 
#: server side. If no one has tampered with the secret material, and has access to 
#: all the credentials, this should never happen.
key_agreement_freeze_recovery_wrong_stamp = _signals.signal("key_agreement_freeze_recovery_wrong_stamp")

#: Sent when the incoming new session agreement request fails due to salt byte 
#: mismatch and verification token collision. Can only happen if someone has tampered 
#: with the secret material.
key_agreement_failed_rekeying_token = _signals.signal("key_agreement_failed_rekeying_token")

#: Sent when the incoming new session agreement request fails due to an incorrect 
#: hexadecimal string containing salt bytes. This can only happen if someone has 
#: tampered with the secret material.
key_agreement_failed_rekeying_salt = _signals.signal("key_agreement_failed_rekeying_salt")

#: Sent when the incoming new session agreement request fails due to save error. 
#: The socket connection with Sentinel has been broken or host is down.
key_agreement_failed_rekeying_save = _signals.signal("key_agreement_failed_rekeying_save")

#: Sent when the incoming new session agreement request fails due to incorrect random 
#: key material. This can only happen if someone has deliberately sent the wrong 
#: public ed25519 key.
key_agreement_failed_wrong_key = _signals.signal("key_agreement_failed_wrong_key")

#: Sent when the incoming new session agreement re-keying of the evolving key has been 
#: correctly completed. The new evolving key has been stored on the server side and the 
#: operation has been confirmed by the incoming token.
key_agreement_success_rekeying = _signals.signal("key_agreement_success_rekeying")

#: Sent when the incoming new session agreement has been correctly completed. The 
#: new session key has been stored on the server side and the operation has been 
#: confirmed by the incoming token.
key_agreement_success_exchange = _signals.signal("key_agreement_success_exchange")

#: Sent when the incoming new session agreement has correct stamp and the session_key 
#: already exists on server-side. If multiscreen is allowed the server will send the 
#: existing key.
key_agreement_session_restored = _signals.signal("key_agreement_session_restored")


#: Sent when the unknown error occurs. Decryption of the evolving key is impossible 
#: because there is no valid SESSION_KEY or the previous SESSION_KEY (RECOVERY) is 
#: invalid.
evo_key_decryption_faild = _signals.signal("evo_key_decryption_faild")

#: Sent when the program attempts to encrypt an evolving key when no session key 
#: exists. This should never happen and indicates a logical problem or a very 
#: strange flow of data.
session_key_does_not_exists = _signals.signal("session_key_does_not_exists")


#: Sent when the browser sends an invalid verification token that cannot be unhexed. 
#: This means that someone is manipulating the data flow and deliberately sending 
#: invalid data.
token_invalid_fails_when_unpacking = _signals.signal("token_invalid_fails_when_unpacking")

#: Sent when the browser sends an invalid verification token that does not match the 
#: server side. This can happen if the browser side has expired credentials - the key 
#: has been rotated outside the legitimate sandbox.
token_invalid_does_not_match_server = _signals.signal("token_invalid_does_not_match_server")

#: Sent when the browser sends an valid token with was already used before. Token 
#: re-use typically means that exact token was intercepted in-the-middle and TLS 
#: connection is eavesdropped.
token_invalid_reuse_of_token = _signals.signal("token_invalid_reuse_of_token")

#: Sent when the browser sends an valid token with was correctly validatad an match 
#: the server-side credentials.
token_validation_successful = _signals.signal("token_validation_successful")

#: Sent when the browser sends an token with was not-correctly validated and the parser 
#: throws an ValueError. This should never happen.
token_validation_throw_error = _signals.signal("token_validation_throw_error")

#: Sent when the browser sends a token with an associated signature and signature 
#: validation fails. The browser has an invalid signature key that is not associated 
#: with a server-side device credential.
the_signature_validation_has_failed = _signals.signal("the_signature_validation_has_failed")

#: Sent when the browser sends an signature with was not-correctly validated and the parser 
#: throws a ValueError. This should never happen.
the_signature_validation_throws_error = _signals.signal("the_signature_validation_throws_error")

#: Sent when the browser sends a token with an associated signature and the signature 
#: validation is correct. This means that the origin of the request is confirmed.
the_signature_validation_was_successful = _signals.signal("the_signature_validation_was_successful")

#: Sent when the browser sends a verification token and empty signature (no data). 
#: This is a generic critical error and means that the user device cannot be 
#: authenticated and the user should be logged out.
origin_authentication_empty_signature = _signals.signal("origin_authentication_empty_signature")

#: Sent when the browser sends an empty verification token. This is a generic 
#: critical error and means that the user device cannot be authenticated and the 
#: user should be logged out.
origin_authentication_empty_token = _signals.signal("origin_authentication_empty_token")

#: Sent when the browser sends a verification token that is signed with the appropriate key, but 
#: the token does not match the server-side token or is corrupt. This is a generic 
#: critical error and means that the user device cannot be authenticated and the user 
#: should be logged out.
origin_authentication_key_collision = _signals.signal("origin_authentication_key_collision")

#: Sent when the browser sends a verification token that is signed with an invalid key, token 
#: cannot be validated and origin confirmed. This is a generic critical error and means that the 
#: user device cannot be authenticated and user should be logged-out.
origin_authentication_failure_invalid_signature = _signals.signal("origin_authentication_failure_invalid_signature")

#: Sent when the incoming request comes from a remote address that is different from 
#: the one assigned to the device. The user may have left the secure network or they 
#: may have changed their location.
origin_authentication_remote_addr_change = _signals.signal("origin_authentication_remote_addr_change")

#: Sent when the incoming request comes from an user agent that is different from 
#: the one assigned to the device. The user may have upgraded the browser, or this 
#: may be an indication of session hijacking.
origin_authentication_user_agent_change = _signals.signal("origin_authentication_user_agent_change")

#: Sent when the browser sends a verification token signed with an appropriate key 
#: and the credentials are successfully verified. The user device is authenticated 
#: and the origin of the request is confirmed.
origin_authentication_is_successful = _signals.signal("origin_authentication_is_successful")

#: Sent before the server begins credential validation only if a re-keying nonce is 
#: assigned to the server-side device. This means that the server's evolution key is 
#: renewed before token validation, and is verified with the incoming token after 
#: rotation.
origin_authentication_rekeying_demand = _signals.signal("origin_authentication_rekeying_demand")

#: Sent when the program generates the new re-keying nonce on the server side. The 
#: nonce is delivered to the user's browser, but the re-keying moment is delayed until 
#: the browser returns for validation.
origin_authentication_rekeying_nonce_created = _signals.signal("origin_authentication_rekeying_created")

#: Sent when the incoming credential validation request has a re-keying nonce that 
#: does not match the server-side nonce assigned to the device. This is typically an 
#: indication of stolen credentials and inevitable key collision error.
origin_authentication_rekeying_nonce_mismatch = _signals.signal("origin_authentication_rekeying_nonce_mismatch")


user_has_logged_in_to_the_system = _signals.signal("user_has_logged_in_to_the_system")
owner_has_been_assigned_to_the_device = _signals.signal("owner_has_been_assigned_to_the_device")
user_has_loggeded_out_from_the_system = _signals.signal("user_has_loggeded_out_from_the_system")
user_is_unauthorized_to_get_response = _signals.signal("user_is_unauthorized_to_get_response")

user_has_opened_a_new_tab_in_the_browser = _signals.signal("user_has_opened_a_new_tab_in_the_browser")
user_tab_has_been_purged_unload_effect = _signals.signal("user_tab_has_been_purged_unload_effect")
user_tab_has_been_closed_on_server_side = _signals.signal("user_tab_has_been_destroyed_on_server_side")
user_logged_out_as_all_tabs_have_been_closed = _signals.signal("user_logged_out_as_all_tabs_have_been_closed")
user_new_tab_has_been_blocked_as_not_allowed = _signals.signal("user_new_tab_has_been_blocked_as_not_allowed")
user_keys_has_been_ereased_as_being_invalid = _signals.signal("user_keys_has_been_ereased_as_being_invalid")

device_has_been_deleted_as_being_unnecessary = _signals.signal("device_has_been_deleted_as_being_unnecessary") 
device_has_been_registered_in_the_system = _signals.signal("device_has_been_registered_in_the_system")  

abort_as_protected_route_require_device_owner = _signals.signal("abort_as_protected_route_require_device_owner") 
abort_as_this_is_cookie_hijacking_incident = _signals.signal("abort_as_this_is_cookie_hijacking_incident") 
abort_as_network_location_has_been_change = _signals.signal("abort_as_network_location_has_been_change") 