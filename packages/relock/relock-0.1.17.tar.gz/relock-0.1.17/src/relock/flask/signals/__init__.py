import logging 

from flask import (current_app as app,  
				   request)

from .agreement import Agreement
from .device import Device
from .login import Login
from .origin import Origin
from .tokens import Tokens
from .user import User

logging = logging.getLogger(__name__)

from ..device import (request_processing_has_started,
					  request_processing_has_been_completed)

class Signals(Agreement, Device, Login, Origin, Tokens, User):

	def __init__(self):
		logging.info('Starting signals engine...')

	@request_processing_has_started.connect
	def _request_processing_has_started(self, **kwargs):
		self.tcp.notify(**kwargs)

	@request_processing_has_been_completed.connect
	def _request_processing_has_been_completed(self, **kwargs):
		self.tcp.notify(**kwargs)