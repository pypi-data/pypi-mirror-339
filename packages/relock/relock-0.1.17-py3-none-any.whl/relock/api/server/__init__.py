import os
import sys
import logging
import binascii
import logging

logging = logging.getLogger(__name__)

class Server(object):

	def __init__(self, app=None):
		if app is not None:
			self.init_app(app)

	def init_app(self, app, add_context_processor=True):
		"""

		:param app: The :class:`flask.Flask` object to configure.
		:type app: :class:`flask.Flask`
		:param add_context_processor: Whether to add a context processor to
			the app that adds a `current_user` variable to the template.
			Defaults to ``True``.
		:type add_context_processor: bool
		"""
		app.key_manager = self

		with app.app_context():

			from .routes import bp; app.register_blueprint(bp)