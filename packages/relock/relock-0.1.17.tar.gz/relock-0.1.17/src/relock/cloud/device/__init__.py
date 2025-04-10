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
from flask_login import current_user as worker

from datetime import (datetime,
					  timedelta)
from uuid import uuid4
from typing import Any

class Device(object):

	def __init__(self, connection=None):
		self.tcp = connection
		if not hasattr(request, 'id'):
			setattr(request, 'id', str(uuid4()))
		with self.tcp(**{'route': 'before',
						 'sid': session.sid,
						 'rid': request.id,
						 'cookies': request.cookies,
						 'host': request.headers.get('Host'),
						 'agent': request.headers.get('User-Agent'),
						 'addr': request.remote_addr,
						 'method': request.method,
						 'url': request.url,
						 'path': request.path,
						 'user': worker.get_id(),
						 'email': worker.get_email(),
						 'authenticated': worker.is_authenticated,
						 'active': worker.is_active,
						 'anonymous': worker.is_anonymous,
						 'X-Key-Token': request.headers.get('X-Key-Token', str()) or 
						 		  		request.form.get('X-Key-Token', str()),
						 'X-Key-Signature': request.headers.get('X-Key-Signature', str()) or 
						 		  	  		request.form.get('X-Key-Signature', str()),
						 'host': app.config.get('SERVER_HOST')}) as tcp:
			print(request.id)

	def confirm(self):
		pass

	def clear(self):
		pass

	def unlink(self):
		pass

	def exchange(self, key:bytes, hash:bytes, xsid:bytes, screen:bytes):
		with self.tcp(**{'route': 'exchange',
						 'sid': session.sid,
						 'rid': request.id,
						 'key': key,
						 'hash': hash,
						 'xsid': xsid,
						 'screen': screen,
						 'host': app.config.get('SERVER_HOST')}) as tcp:
			print(tcp.response)

	def validation(self):
		pass

	def webauthn(self):
		pass

	def authenticate(self):
		pass

	def rekeying(self):
		pass

	def verify(self):
		pass

	def validate(self):
		pass

	@classmethod
	def before(cls) -> None:
		if not hasattr(request, 'relock'):
			with app.session_sentinel.tcp.servers as server:
				with app.session_sentinel.tcp.lock:
					with server.pool as conn:
						setattr(request, 'relock', Device(conn))

	@classmethod
	def after(cls, response) -> object:
		with app.session_sentinel.tcp(**{'route': 'after',
								  		 'sid': session.sid,
								   		 'rid': request.id,
							  	   		 'host': app.config.get('SERVER_HOST')}) as tcp:
			print(tcp.response)
		return response

