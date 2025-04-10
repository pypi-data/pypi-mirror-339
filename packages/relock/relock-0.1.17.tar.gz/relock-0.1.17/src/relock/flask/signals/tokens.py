import logging

from ..device import (token_invalid_fails_when_unpacking,
					  token_invalid_does_not_match_server,
					  token_invalid_reuse_of_token,
					  token_validation_successful,
					  the_signature_validation_has_failed,
					  the_signature_validation_was_successful)

class Tokens(object):

	@token_invalid_fails_when_unpacking.connect
	def _token_invalid_fails_when_unpacking(self, **kwargs):
		self.tcp.notify(**kwargs)

	@token_invalid_does_not_match_server.connect
	def _token_invalid_does_not_match_server(self, **kwargs):
		self.tcp.notify(**kwargs)

	@token_invalid_reuse_of_token.connect
	def _token_invalid_reuse_of_token(self, **kwargs):
		self.tcp.notify(**kwargs)

	@token_validation_successful.connect
	def _token_validation_successful(self, **kwargs):
		self.tcp.notify(**kwargs)

	@the_signature_validation_has_failed.connect
	def _the_signature_validation_has_failed(self, **kwargs):
		self.tcp.notify(**kwargs)

	@the_signature_validation_was_successful.connect
	def _the_signature_validation_was_successful(self, **kwargs):
		self.tcp.notify(**kwargs)
