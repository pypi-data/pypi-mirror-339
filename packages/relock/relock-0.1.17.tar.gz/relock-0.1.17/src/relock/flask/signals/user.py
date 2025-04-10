import logging

from ..device import (user_has_logged_in_to_the_system,
					  owner_has_been_assigned_to_the_device,
					  user_has_loggeded_out_from_the_system,
					  user_is_unauthorized_to_get_response,
					  user_has_opened_a_new_tab_in_the_browser,
					  user_tab_has_been_purged_unload_effect,
					  user_logged_out_as_all_tabs_have_been_closed,
					  user_new_tab_has_been_blocked_as_not_allowed,
					  user_tab_has_been_closed_on_server_side,
					  user_keys_has_been_ereased_as_being_invalid,
					  abort_as_protected_route_require_device_owner,
					  abort_as_this_is_cookie_hijacking_incident,
					  abort_as_network_location_has_been_change)

class User(object):

	@user_has_logged_in_to_the_system.connect
	def _user_has_logged_in_to_the_system(self, **kwargs):
		self.tcp.notify(**kwargs)

	@owner_has_been_assigned_to_the_device.connect
	def _owner_has_been_assigned_to_the_device(self, **kwargs):
		self.tcp.notify(**kwargs)

	@user_has_loggeded_out_from_the_system.connect
	def _user_has_loggeded_out_from_the_system(self, **kwargs):
		self.tcp.notify(**kwargs)

	@user_is_unauthorized_to_get_response.connect
	def _user_is_unauthorized_to_get_response(self, **kwargs):
		self.tcp.notify(**kwargs)

	@user_has_opened_a_new_tab_in_the_browser.connect
	def _user_has_opened_a_new_tab_in_the_browser(self, **kwargs):
		self.tcp.notify(**kwargs)

	@user_tab_has_been_purged_unload_effect.connect
	def _user_tab_has_been_purged_unload_effect(self, **kwargs):
		self.tcp.notify(**kwargs)

	@user_logged_out_as_all_tabs_have_been_closed.connect
	def _user_logged_out_as_all_tabs_have_been_closed(self, **kwargs):
		self.tcp.notify(**kwargs)

	@user_new_tab_has_been_blocked_as_not_allowed.connect
	def _user_new_tab_has_been_blocked_as_not_allowed(self, **kwargs):
		self.tcp.notify(**kwargs)

	@user_tab_has_been_closed_on_server_side.connect
	def _user_tab_has_been_closed_on_server_side(self, **kwargs):
		self.tcp.notify(**kwargs)

	@user_keys_has_been_ereased_as_being_invalid.connect
	def _user_keys_has_been_ereased_as_being_invalid(self, **kwargs):
		self.tcp.notify(**kwargs)

	@abort_as_protected_route_require_device_owner.connect
	def _abort_as_protected_route_require_device_owner(self, **kwargs):
		self.tcp.notify(**kwargs)

	@abort_as_this_is_cookie_hijacking_incident.connect
	def _abort_as_this_is_cookie_hijacking_incident(self, **kwargs):
		self.tcp.notify(**kwargs)

	@abort_as_network_location_has_been_change.connect
	def _abort_as_network_location_has_been_change(self, **kwargs):
		self.tcp.notify(**kwargs)