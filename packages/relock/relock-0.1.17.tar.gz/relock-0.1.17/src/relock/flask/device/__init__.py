import re
import json
import os
import time
import hashlib
import xxhash
import binascii
import base64
import secrets
import logging
import pickle

from flask import (current_app as app, 
				   url_for, 
				   redirect,
				   request,
				   has_request_context,
				   session, 
				   Response)

from flask_login import (current_user as worker,
						 UserMixin, 
						 login_user, 
						 logout_user)

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

from datetime import (datetime,
					  timedelta)
from uuid import uuid4
from typing import Any

from ...crypto import KDM
from ...crypto import GCM

from .logic import Logic
from .core import Core
from .passkey import Passkey
from .system import System
from .signals import *

class Device(Logic, Core, System, Passkey):

	def __init__(self, key: str, 
					   value: Any = None,
					   addr: str = str(),
					   pattern: str = 'default', 
					   **kwargs):

		super().__init__(key, 				 #server side public key
						 value, 			 #server side private key
						 pattern, 
						 **kwargs)

		self.__cache = list()
		if kwargs.get('addr') or has_request_context():
			if addr := kwargs.get('addr', request.remote_addr):
				if self.addr != addr:
					self.addr  = addr #actual remote_addr

		if not self.platform and has_request_context():
			self.platform = self.os + '+' + self.kind

	def __enter__(self):
		return self
 
	def __exit__(self, *args):
		pass

	@property
	def kdm(self):
		if not hasattr(self, '__kdm'):
			setattr(self, '__kdm', KDM(self.value,	 	 #ed25519 private key
									   self.client,	 	 #client ed25519 public key
									   self.session,	 #last session key
									   self.secret,		 #actual secret key
									   power=128))
		return getattr(self, '__kdm')

	@property
	def id(self):
		return self.kdm.identity.decode()

	def confirm(self, reuse=False, token=None):
		if token := request.form.get('X-Key-Token') or \
					request.headers.get('X-Key-Token'):
			if signature := request.form.get('X-Key-Signature') or \
							request.headers.get('X-Key-Signature'):
				if request.device.verify(token, signature) and \
				   request.device.validate(token, reuse=bool(reuse)):
					return True

	@classmethod
	def exposed(cls, path:str = str()):
		for route in app.expose:
			if route in path:
				return True

	def authorized(self, path:str = str()):
		if app.config.get('SESSION_SENTINEL_PROTECTED') and \
		   (self.exposed(request.path) or self.owner):
		   return True

	@property
	def xsid(self, size:int = 32) -> str:
		return HKDF(algorithm=hashes.SHA512(),
					length=size,
					salt=self.value,
					info=self.key,
				).derive(session.sid.encode())

	@property
	def screen(self) -> bytes:
		if has_request_context():
			return session.get('screen', bytes())

	@screen.setter
	def screen(self, value:bytes):
		if has_request_context():
			session['screen'] = value

	@property
	def owner(self) -> [int|str]:
		if hasattr(self, 'owner_id'):
			return self.owner_id
		return False

	@owner.setter
	def owner(self, value:[int|str]) -> None:
		if not hasattr(self, 'owner_id'):
			setattr(self, 'owner_id', value)
		self.update()

	@owner.deleter
	def owner(self) -> None:
		if hasattr(self, 'owner_id'):
			delattr(self, 'owner_id')
		self.update()