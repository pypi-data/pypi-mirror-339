import logging

from ..device import (stamp_cookie_decode_failure,
					  blank_device_object_created,
					  device_loaded_from_cookie,
					  request_without_device_cookie,
					  session_request_without_cookie,
					  device_cookie_and_stamp_set,
					  device_cookie_key_not_exists,
					  device_cookie_invalid_stamp,
					  device_cookie_deprecated_keys_removed,
					  device_cookie_stamp_cookie_not_exists,
					  device_cookie_session_confirmed,
					  device_cookie_base64_decode_failure,
					  device_session_no_longer_exists,
					  device_cookie_decryption_faild,
					  device_has_been_deleted_as_being_unnecessary)

class Device(object):

	@stamp_cookie_decode_failure.connect
	def _stamp_cookie_decode_failure(self, **kwargs):
		self.tcp.notify(**kwargs)

	@blank_device_object_created.connect
	def _blank_device_object_created(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_loaded_from_cookie.connect
	def _device_loaded_from_cookie(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_cookie_session_confirmed.connect
	def _device_cookie_session_confirmed(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_cookie_stamp_cookie_not_exists.connect
	def _device_cookie_stamp_cookie_not_exists(self, **kwargs):
		self.tcp.notify(**kwargs)

	@request_without_device_cookie.connect
	def _request_without_device_cookie(self, **kwargs):
		self.tcp.notify(**kwargs)

	@session_request_without_cookie.connect
	def _session_request_without_cookie(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_cookie_deprecated_keys_removed.connect
	def _device_cookie_deprecated_keys_removed(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_cookie_and_stamp_set.connect
	def _device_cookie_and_stamp_set(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_cookie_key_not_exists.connect
	def _device_cookie_key_not_exists(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_cookie_invalid_stamp.connect
	def _device_cookie_invalid_stamp(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_cookie_base64_decode_failure.connect
	def _device_cookie_base64_decode_failure(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_session_no_longer_exists.connect
	def _device_session_no_longer_exists(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_cookie_decryption_faild.connect
	def _device_cookie_decryption_faild(self, **kwargs):
		self.tcp.notify(**kwargs)

	@device_has_been_deleted_as_being_unnecessary.connect
	def _device_has_been_deleted_as_being_unnecessary(self, **kwargs):
		self.tcp.notify(**kwargs)