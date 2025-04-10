import logging
import binascii
import base64

from flask import (current_app as app, 
				   has_request_context,
				   session)

from .signals import (token_invalid_fails_when_unpacking,
					  token_invalid_does_not_match_server,
					  token_invalid_reuse_of_token,
					  token_validation_throw_error,
					  token_validation_successful)

class Tokens(object):

	def token(self) -> bytes:
		# if self.upgrade():
		return binascii.hexlify(self.kdm.token()).decode()

	def validate(self, token:bytes, reuse: bool = False, valid:bool = False, hash:str = str()) -> bool:
		if hash := token:
			try:
				if isinstance(token, str) and int(token, 16):
					token = binascii.unhexlify(token)
			except:
				token_invalid_fails_when_unpacking.send()
			else:
				try:
					valid = self.kdm.validate(token)
				except:
					token_validation_throw_error.send()
				else:
					if valid:
						token_validation_successful.send()
					else:
						token_invalid_does_not_match_server.send()
			finally:
				if cache := app.config.get('SESSION_CACHE', 'cache'):
					if not cache in session:
						session[cache] = list()
					if hash and hash in session[cache]:
						if not reuse:
							valid = False; token_invalid_reuse_of_token.send()
		return valid

	def sign(self, value:bytes) -> bool:
		"""
		This will sign the passed `value' with a private ed25519 key unique to that device. The signature key is random and only available on the server side for the correct user and user device.

		:param value: The data to be singed.
		:type value: bytes
		"""
		return self.kdm.sign(value)

	def verify(self, data:bytes, signature:bytes, valid:bool = False) -> bool:
		"""
		This will sign the passed `value' with a private ed25519 key unique to that device. The signature key is random and only available on the server side for the correct user and user device.

		:param data: The data to be veryficated against signature.
		:type data: bytes
		:param signature: The signature material.
		:type signature: bytes
		:param valid: By default assumed invalid signature.
					   Defaults to ``False``.
		:type valid: bool
		"""
		try:
			if isinstance(data, str) and int(data, 16):
				data = binascii.unhexlify(data)
			if isinstance(signature, str) and int(signature, 16):
				signature = binascii.unhexlify(signature)
			valid = self.kdm.verify(data, signature)
		except:
			the_signature_validation_throws_error.send()
		else:
			if valid:
				the_signature_validation_was_successful.send()
			else:
				the_signature_validation_has_failed.send()
		finally:
			return valid