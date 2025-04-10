import os
import sys
import logging
import binascii
import bleach

logging = logging.getLogger(__name__)

from flask import (Blueprint,
				   current_app as app, 
				   has_request_context,
				   request,
				   session)

from flask_login import (current_user as worker,
						 user_logged_in,
					     user_logged_out,
					     user_loaded_from_cookie,
					     user_loaded_from_request,
					     user_login_confirmed,
					     user_unauthorized,
					     user_needs_refresh,
					     user_accessed,
					     session_protected)

from ..tcp import TCP
from ..thread import Thread
from ..javascript import *
from .device import Device

bp = os.environ.get('SENTINEL_ROUTE', 'relock')
bp = Blueprint(bp, __name__, url_prefix='/%s' % bp,
							 template_folder='templates',
							 static_folder='static',
							 static_url_path='/static/%s' % bp)

class Cloud(object):

	def __init__(self, app=None, host=None,
								 port=None,
								 pool=1,
								 ping=False,
								 timeout=30):
		if app is not None:
			self.init_app(app)
		self.tcp = None

	def init_app(self, app, add_context_processor=True):
		"""
		Configures an application. This registers an `before_request` call, and
		attaches this `SessionSentinel` to it as `app.session_sentinel`.

		:param app: The :class:`flask.Flask` object to configure.
		:type app: :class:`flask.Flask`
		:param add_context_processor: Whether to add a context processor to
			the app that adds a `current_user` variable to the template.
			Defaults to ``True``.
		:type add_context_processor: bool
		"""
		app.relock = self

		app.config.setdefault('SESSION_SENTINEL_HOST', str(os.environ.get('SESSION_SENTINEL_HOST', '127.0.0.1')))
		app.config.setdefault('SESSION_SENTINEL_PORT', int(os.environ.get('SESSION_SENTINEL_PORT', 8111)))
		app.config.setdefault('SESSION_SENTINEL_POOL', int(os.environ.get('SESSION_SENTINEL_POOL', 1)))
		app.config.setdefault('SESSION_SENTINEL_PING', bool(os.environ.get('SESSION_SENTINEL_PING', False)))
		app.config.setdefault('SESSION_SENTINEL_TIMEOUT', int(os.environ.get('SESSION_SENTINEL_TIMEOUT', 30)))

		with app.app_context():
			try:
				self.tcp = TCP(host=app.config.get('SESSION_SENTINEL_HOST'),
							   port=app.config.get('SESSION_SENTINEL_PORT'),
							   pool=app.config.get('SESSION_SENTINEL_POOL'),
							   ping=app.config.get('SESSION_SENTINEL_PING'),
							   timeout=app.config.get('SESSION_SENTINEL_TIMEOUT'))
			except (SystemExit, KeyboardInterrupt):
				sys.exit()
			except Exception as e:
				raise RuntimeError('Session Sentinel host is not available.')
			else:
				app.before_request(Device.before)
				app.after_request(Device.after)

		self.tcp.expose('/')
		self.tcp.expose('/auth/device')
		self.tcp.expose('/auth/clear')
		self.tcp.expose('/favicon.ico')
