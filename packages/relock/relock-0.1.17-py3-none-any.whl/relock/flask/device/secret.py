import os
import logging
import binascii
import hashlib

import numpy as np

from flask import (current_app as app, 
				   has_request_context,
				   request,
				   session)

from ...crypto import GCM

from .session import Session
from .tokens import Tokens
from .signals import (key_agreement_success_for_new_device,
					  key_agreement_freeze_recovery_wrong_stamp,
					  key_agreement_failed_rekeying_token,
					  key_agreement_failed_rekeying_salt,
					  key_agreement_failed_rekeying_save,
					  key_agreement_failed_wrong_key,
					  key_agreement_success_exchange,
					  key_agreement_success_rekeying,
					  key_agreement_session_restored,
					  evo_key_decryption_faild,
					  session_key_does_not_exists)

class Secret(Session, Tokens):

	@property
	def secret(self):
		#: The secret_key variable is stored in encrypted form on the server side. 
		#: The evolving key (secret_key) is encrypted by a current session key.
		if not hasattr(self, 'secret_key'):
			self.secret_key = bytes()
 
		#: Private variables are not stored in the database and live only in the 
		#: memory on the application server. They are allocated and decrypted from 
		#: storaged variable only once.
		if not hasattr(self, '__secret'):
			self.__secret = bytes()
			#: If you quickly open and close a tab in your browser, the browser 
			#: re-creates the old session. This means that the session cookie file 
			#: is not immediately deleted by the browser.
			if self.recovery and self.secret_key:
				try:
					with GCM(self.session or self.recovery) as gcm:		
						self.__secret = gcm.decrypt(self.secret_key)
						self.session = self.session or self.recovery
				except:
					evo_key_decryption_faild.send()
				else:
					pass
		return self.__secret

	@secret.setter
	def secret(self, value:bytes):
		if not self.session and value:
			session_key_does_not_exists.send()
		if self.session and value:
			with GCM(self.session) as gcm:
				self.secret_key = gcm.encrypt(value)
				self.__secret = value
		elif not value:
			self.secret_key = bytes()

	@property
	def hash(self):
		if hasattr(self, 'secret_key') and self.secret_key:
			return hashlib.blake2b(self.secret, salt=bytes(16),
												digest_size=16).digest()
		return bytes()

	def exchange(self, key:bytes = bytes(),
					   stamp:bytes = bytes(),
					   xsid:bytes = bytes(),
					   screen: bytes = bytes(),
					   token:str = str(),
					   recovery:bytes = bytes(),
					   restore:bool = False):
		id = stamp == self.hash == session.get('stamp')
		# print(id, stamp, self.hash, session.get('stamp'))
		if public := self.kdm.exchange(key):
			# logging.trace('Client public key %s', np.frombuffer(key, dtype=np.uint8))
			# logging.trace('Server public key %s', np.frombuffer(public, dtype=np.uint8))
			if not self.secret and not self.recovery:
				self.client   = bytes(self.kdm.client)
				self.session  = bytes(self.kdm.session)
				self.stamp    = bytes(self.hash)
				self.secret   = bytes(self.kdm.secret)
				self.addr 	  = request.remote_addr
				if recovery := bytes(self.kdm.session):
					if not bool(self):
						if self.save():
							key_agreement_success_for_new_device.send()
			elif self.session and self.xsid == xsid and self.addr == request.remote_addr:
				recovery = self.session
				restore = True
				if token := self.rekeying():
					key_agreement_session_restored.send()
			elif recovery := bytes(self.recovery):
				self.session = bytes(self.kdm.session)
				self.addr 	 = request.remote_addr
				if token := self.rekeying():
					self.recovery = self.session
					key_agreement_success_exchange.send()
			if not id:
				key_agreement_freeze_recovery_wrong_stamp.send()
				recovery = os.urandom(32)
			self.cookie = True
			self.screen = screen
			with GCM(self.kdm.session) as gcm:
				return dict(key=list(public),
							signer=list(bytes(self.kdm.signer)),
							token=token if isinstance(token, str) else list(token),
							xsid=list(self.xsid),
							recovery=list(gcm.encrypt(recovery, True)),
							restore=restore,
							error=str())
		else:
			key_agreement_failed_wrong_key.send(key=key)
		return dict(key=list(),
					signer=list(),
					token=str(),
					recovery=list(),
					error='Key agreement faild.')

	def rekeying(self, salt=bytes(), token=bytes(), hexlify=True):
		if isinstance(salt, str):
			try:
				salt = binascii.unhexlify(salt)
			except:
				key_agreement_failed_rekeying_salt.send(salt=salt); return False
			else:
				if len(salt) != 32:
					key_agreement_failed_rekeying_salt.send(salt=salt); return False
		if nonce := self.kdm.rekeying(salt, token):
			self.secret = bytes(self.kdm.secret)
			self.stamp  = self.hash
			if self.update():
				self.recovery = self.session
				self.cookie = True
				key_agreement_success_rekeying.send()
				if isinstance(nonce, bool):
					return nonce
				if hexlify:
					return binascii.hexlify(nonce).decode()
				return nonce
			else:
				key_agreement_failed_rekeying_save.send()
		else:
			key_agreement_failed_rekeying_token.send(token=token)
		return False

