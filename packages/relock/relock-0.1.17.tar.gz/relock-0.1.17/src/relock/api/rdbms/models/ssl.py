import os
import ssl
import secrets
import logging

from ..logic import Logic
from typing import Any
from ssl import Purpose

from .key import Key
from .crt import Crt

class SSL(Logic):

	__context  = None
	__location = None

	__key = None
	__crt = None

	PROTOCOL_TLS_CLIENT, PROTOCOL_TLS_SERVER, CLIENT_AUTH, SERVER_AUTH = (ssl.PROTOCOL_TLS_CLIENT, ssl.PROTOCOL_TLS_SERVER, ssl.Purpose.CLIENT_AUTH, ssl.Purpose.SERVER_AUTH)

	def __init__(self, key: str = None, 
					   value: Any = secrets.token_urlsafe(32).encode(), 
					   pattern: str = 'default', **kwargs):
		if pattern != None:
			self.pattern = pattern
		if not self.key and key and not self.value and value:
			self.key, self.value, self.__context, self.__location = (str(key)[:512], value, None, None)
			self.save()
		
		if not self.rsa:
			self.rsa = kwargs.get('key') if 'key' in kwargs else None
		if not self.crt:
			self.crt = kwargs.get('ip') if 'ip' in kwargs else None
 
	def __call__(self, purpose: object = ssl.PROTOCOL_TLS_SERVER, add: str = None, ip: tuple = ()):
		if not self.crt and ip:
			self.crt = ip
		if purpose in (ssl.PROTOCOL_TLS_CLIENT, ssl.PROTOCOL_TLS_SERVER, ssl.Purpose.CLIENT_AUTH, ssl.Purpose.SERVER_AUTH):
			with self.rsa as key:
				with self.crt as crt:
					with crt.tmp as crt:
						with key.tmp as key:
							# print(os.popen('openssl x509 -noout -modulus -in %s' % crt.name).read())
							# print(os.popen('openssl rsa -noout -modulus -in %s' % key.name).read())
							self.__context = self.tls(purpose)
							self.__context.load_cert_chain(certfile=crt.name, 
														   keyfile=key.name,
														   password=self.value)
		# with Crt(add) as crt:
		# 	if bool(crt):
		# 		self.location = crt
		# 		with crt.tmp as crt:
		# 			self.__context.load_verify_locations(crt.name)
		return self

	def __enter__(self):
		return self.__context if self.__context else self

	def tls(self, mode: object = ssl.PROTOCOL_TLS_SERVER):
		if context := ssl.SSLContext(mode):
		# if context := ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert):
			#SSL version 2, 3 are insecure so they have been blocked
			context.options |= ssl.OP_NO_SSLv2
			context.options |= ssl.OP_NO_SSLv3
			# context.verify_mode = ssl.CERT_REQUIRED
		return context

	def encrypt(self, input: bytes) -> bytes:
		return self.crt.encrypt(input)

	def verify(self, input: bytes, signature: bytes) -> bool:
		return self.crt.verify(input, signature)

	@property
	def location(self) -> object:
		return self.__location

	@location.setter
	def location(self, crt: object) -> None:
		self.__location = crt

	@property
	def rsa(self) -> object:
		if not self.__key:
			self.__key = Key(self.key, password=self.value)
		return self.__key()

	@rsa.setter
	def rsa(self, bytes: bytes = bytes()) -> None:
		Key(self.key, bytes, password=self.value)

	@property
	def crt(self) -> object:
		if not self.__crt and self.key:
			self.__crt = Crt(self.key)
		return self.__crt

	@crt.setter
	def crt(self, ip: tuple = ()) -> None:
		self.__crt = Crt.create(self.key, ip=ip, key=self.rsa())
