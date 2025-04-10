import logging

from typing import Any
from .base import Base

from flask import (current_app as app, 
				   has_request_context,
				   request,
				   session)

from .signals import (origin_authentication_user_agent_change,
					  origin_authentication_rekeying_nonce_created,
					  origin_authentication_remote_addr_change)

class System(object):

	@property
	def platform(self):
		if hasattr(self, 'device_platform'):
			return getattr(self, 'device_platform')
		return str()

	@platform.setter
	def platform(self, value:str = str()):
		if value != self.platform:
			setattr(self, 'device_platform', value)

	@property
	def os(self):
		if os := request.headers.get('User-Agent', str()).lower():
			if 'win' in os:
				return 'Windows'
			elif 'mac' in os:
				return 'MacOS'
			elif 'x11' in os:
				return 'Linux'
			elif 'android' in os:
				return 'Android'
			elif 'ipad' in os or 'iphone' in os:
				return 'iOS'
		return 'Unknown'

	@property
	def kind(self):
		if agent := request.headers.get('User-Agent', str()).lower():
			if 'mobi' in agent or 'android' in agent:
				return 'Mobile'
			elif 'tablet' in agent or 'ipad' in agent:
				return 'Tablet'
		return 'Desktop'
