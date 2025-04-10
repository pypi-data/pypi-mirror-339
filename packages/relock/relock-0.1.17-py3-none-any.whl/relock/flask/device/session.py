import base64
from flask import (current_app as app, 
				   has_request_context,
				   session)

from ...crypto import GCM

class Session(object):

	@property
	def prev(self):
		if has_request_context():
			return session.get('prev', bytes())

	@prev.setter
	def prev(self, value:bytes):
		if has_request_context():
			session['prev'] = value

	@property
	def stamp(self):
		if has_request_context():
			return session.get('stamp', bytes())

	@stamp.setter
	def stamp(self, value:bytes):
		if has_request_context():
			if self.stamp:
				self.prev = self.stamp
			session['stamp'] = value

	@stamp.deleter
	def stamp(self):
		if has_request_context() and 'stamp' in session:
			del session['stamp']

	@property
	def recovery(self):
		if has_request_context():
			return session.get('recovery', bytes())

	@recovery.setter
	def recovery(self, value:bytes):
		if has_request_context():
			session['recovery'] = value

	@recovery.deleter
	def recovery(self):
		if has_request_context() and 'recovery' in session:
			del session['recovery']

	@property
	def session(self):
		if has_request_context():
			return session.get('x25519', bytes())
		return bytes()

	@session.setter
	def session(self, value:bytes):
		if has_request_context():
			session['x25519'] = value
