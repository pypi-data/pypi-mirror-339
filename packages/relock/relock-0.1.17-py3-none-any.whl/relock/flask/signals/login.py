import binascii
import logging
import time

from flask import (current_app as app,
				   request,
				   Response,
				   session,
				   redirect,
				   url_for,
				   abort)

from flask_login import (current_user as worker,
						 logout_user,
						 user_logged_in,
						 user_logged_out,
						 user_loaded_from_cookie,
						 user_loaded_from_request,
						 user_login_confirmed,
						 user_unauthorized,
						 user_needs_refresh,
						 user_accessed,
						 session_protected)

from ..device import (user_has_logged_in_to_the_system,
					  owner_has_been_assigned_to_the_device,
					  user_has_loggeded_out_from_the_system,
					  user_is_unauthorized_to_get_response,
					  user_logged_out_as_all_tabs_have_been_closed,
					  user_new_tab_has_been_blocked_as_not_allowed,
					  user_tab_has_been_closed_on_server_side)

class Login(object):

	#: Sent when a user is logged in. In addition to the app (which is the
	#: sender), it is passed `user`, which is the user being logged in.
	@user_logged_in.connect
	def _user_logged_in(self, *args, **kwargs):
		if user := kwargs.get('user'):
			if not request.device.owner:
				request.device.owner = user.get_id()
				owner_has_been_assigned_to_the_device.send()
		if 'screens' in session:
			session['screens'] = dict()
			session['screens'][binascii.hexlify(request.device.screen).decode()] = -1
		user_has_logged_in_to_the_system.send()

	#: Sent when a user is logged out. In addition to the app (which is the
	#: sender), it is passed `user`, which is the user being logged out.
	@user_logged_out.connect
	def _user_logged_out(self, *args, **kwargs):
		session.clear()
		if request.device.previous_addr != request.remote_addr:
			request.device.previous_addr = request.remote_addr
			request.device.update()
		user_has_loggeded_out_from_the_system.send()

	#: Sent when the user is loaded from the cookie. In addition to the app (which
	#: is the sender), it is passed `user`, which is the user being reloaded.
	@user_loaded_from_cookie.connect
	def _user_loaded_from_cookie(self, *args, **kwargs):
		logging.debug('_user_loaded_from_cookie')

	#: Sent when the user is loaded from the request. In addition to the app (which
	#: is the #: sender), it is passed `user`, which is the user being reloaded.
	@user_loaded_from_request.connect
	def _user_loaded_from_request(self, *args, **kwargs):
		logging.debug('user_loaded_from_request')

	#: Sent when a user's login is confirmed, marking it as fresh. (It is not
	#: called for a normal login.)
	#: It receives no additional arguments besides the app.
	@user_login_confirmed.connect
	def _user_login_confirmed(self, *args, **kwargs):
		logging.debug('_user_login_confirmed')

	#: Sent when the `unauthorized` method is called on a `LoginManager`. It
	#: receives no additional arguments besides the app.
	@user_unauthorized.connect
	def _user_unauthorized(self, *args, **kwargs):
		user_is_unauthorized_to_get_response.send()
		
	#: Sent when the `needs_refresh` method is called on a `LoginManager`. It
	#: receives no additional arguments besides the app.
	@user_needs_refresh.connect
	def _user_needs_refresh(self, *args, **kwargs):
		logging.debug('_user_needs_refresh')

	#: Sent whenever the user is accessed/loaded
	#: receives no additional arguments besides the app.
	@user_accessed.connect
	def _user_accessed(self, *args, **kwargs):
		session.modified = True
		# print(request.headers)
		if screens := session.get('screens', dict()):
			for screen, timer in screens.copy().items():
				if timer > 0 and timer < time.monotonic():
					del session['screens'][screen]
					user_tab_has_been_closed_on_server_side.send()
		if app.config.get('SESSION_SENTINEL_TAB_LOGOUT', True):
			if session.get('_user_id'):
				if not len(session.get('screens', dict())):
					#: logout user from session if all tabs in browser
					#: were close before session re-initialisation
					if 'screens' in session:
						del session['screens']
					del session['_user_id']
					user_logged_out_as_all_tabs_have_been_closed.send()

	#: Sent whenever session protection takes effect, and a session is either
	#: marked non-fresh or deleted. It receives no additional arguments besides
	#: the app.
	@session_protected.connect
	def _session_protected(self, *args, **kwargs):
		pass


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