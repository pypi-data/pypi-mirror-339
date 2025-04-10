import logging

from typing import Any
from .base import Base

from flask import (current_app as app, 
				   has_request_context,
				   session)

from .signals import (origin_authentication_user_agent_change,
					  origin_authentication_rekeying_nonce_created,
					  origin_authentication_remote_addr_change)

class Core(Base):

	@property
	def addr(self):
		if hasattr(self, 'current_addr'):
			return self.current_addr
		return str()

	@addr.setter
	def addr(self, value:str = str()):
		if value != self.addr:
			origin_authentication_remote_addr_change.send(previous_addr=self.addr or value,
														  current_addr=value)
			self.previous_addr = self.addr or value
			self.current_addr = value
			self.update()

	@property
	def agent(self):
		if hasattr(self, 'current_agent'):
			return self.current_agent
		return str()

	@agent.setter
	def agent(self, value:str = str()):
		if value != self.agent:
			if self.agent:
				origin_authentication_user_agent_change.send(previous_agent=self.agent,
															 current_agent=value)
			self.previous_agent = self.agent or value
			self.current_agent = value

	@property
	def nonce(self):
		if hasattr(self, 'nonce_bytes'):
			return getattr(self, 'nonce_bytes')
		return bytes()

	@nonce.setter
	def nonce(self, value:bytes = bytes()):
		setattr(self, 'nonce_bytes', value)
		if self.save():
			if value is not bytes():
				origin_authentication_rekeying_nonce_created.send()

	@property
	def inner(self):
		if not hasattr(self, 'inner_key'):
			self.inner_key = os.urandom(32)
		return self.inner_key

	@inner.setter
	def inner(self, value:bytes):
		self.inner_key = value