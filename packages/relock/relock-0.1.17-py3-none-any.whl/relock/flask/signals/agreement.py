import logging

from ..device import (evo_key_decryption_faild,
					  session_key_does_not_exists,
					  key_agreement_success_for_new_device,
					  key_agreement_freeze_recovery_wrong_stamp,
					  key_agreement_failed_rekeying_token,
					  key_agreement_failed_rekeying_salt,
					  key_agreement_failed_rekeying_save,
					  key_agreement_failed_wrong_key,
					  key_agreement_success_exchange,
					  key_agreement_success_rekeying)

class Agreement(object):

	@key_agreement_success_for_new_device.connect
	def _key_agreement_success_for_new_device(self, **kwargs):
		self.tcp.notify(**kwargs)

	@key_agreement_success_exchange.connect
	def _key_agreement_success_exchange(self, **kwargs):
		self.tcp.notify(**kwargs)

	@key_agreement_freeze_recovery_wrong_stamp.connect
	def _key_agreement_freeze_recovery_wrong_stamp(self, **kwargs):
		self.tcp.notify(**kwargs)

	@key_agreement_failed_rekeying_token.connect
	def _key_agreement_failed_rekeying_token(self, **kwargs):
		self.tcp.notify(**kwargs)

	@key_agreement_failed_rekeying_salt.connect
	def _key_agreement_failed_rekeying_salt(self, **kwargs):
		self.tcp.notify(**kwargs)

	@key_agreement_failed_rekeying_save.connect
	def _key_agreement_failed_rekeying_save(self, **kwargs):
		self.tcp.notify(**kwargs)

	@key_agreement_failed_wrong_key.connect
	def _key_agreement_failed_wrong_key(self, **kwargs):
		self.tcp.notify(**kwargs)

	@key_agreement_success_rekeying.connect
	def _key_agreement_success_rekeying(self, **kwargs):
		self.tcp.notify(**kwargs)

	@evo_key_decryption_faild.connect
	def _evo_key_decryption_faild(self, **kwargs):
		self.tcp.notify(**kwargs)

	@session_key_does_not_exists.connect
	def _session_key_does_not_exists(self, **kwargs):
		self.tcp.notify(**kwargs)