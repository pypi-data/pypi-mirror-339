import logging

from ..device import (origin_authentication_empty_signature,
					  origin_authentication_empty_token,
					  origin_authentication_key_collision,
					  origin_authentication_failure_invalid_signature,
					  origin_authentication_is_successful,
					  origin_authentication_remote_addr_change,
					  origin_authentication_user_agent_change,
					  origin_authentication_rekeying_demand,
					  origin_authentication_rekeying_nonce_mismatch,
					  origin_authentication_rekeying_nonce_created)

class Origin(object):

	@origin_authentication_empty_signature.connect
	def _origin_authentication_empty_signature(self, **kwargs):
		self.tcp.notify(**kwargs)

	@origin_authentication_empty_token.connect
	def _origin_authentication_empty_token(self, **kwargs):
		self.tcp.notify(**kwargs)

	@origin_authentication_key_collision.connect
	def _origin_authentication_key_collision(self, **kwargs):
		self.tcp.notify(**kwargs)

	@origin_authentication_failure_invalid_signature.connect
	def _origin_authentication_failure_invalid_signature(self, **kwargs):
		self.tcp.notify(**kwargs)

	@origin_authentication_is_successful.connect
	def _origin_authentication_is_successful(self, **kwargs):
		self.tcp.notify(**kwargs)

	@origin_authentication_remote_addr_change.connect
	def _origin_authentication_remote_addr_change(self, **kwargs):
		self.tcp.notify(**kwargs)

	@origin_authentication_user_agent_change.connect
	def _origin_authentication_user_agent_change(self, **kwargs):
		self.tcp.notify(**kwargs)

	@origin_authentication_rekeying_demand.connect
	def _origin_authentication_rekeying_demand(self, **kwargs):
		self.tcp.notify(**kwargs)

	@origin_authentication_rekeying_nonce_mismatch.connect
	def _origin_authentication_rekeying_nonce_mismatch(self, **kwargs):
		self.tcp.notify(**kwargs)

	@origin_authentication_rekeying_nonce_created.connect
	def _origin_authentication_rekeying_nonce_created(self, **kwargs):
		self.tcp.notify(**kwargs)