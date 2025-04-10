import base64
import zlib
import pickle
import logging
import tempfile
import sys

from typing import Any
from uuid import uuid4 as uuid

from . import db
from .logic import Logic

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

class RSA(Logic):

	__padding = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
				    	     algorithm=hashes.SHA256(),
				    	     label=None)
	__public  = None
	__private = None
	_password = None

	def __init__(self, key: str = str(), 
					   value: bytes = bytes(), 
					   pattern: str = 'default',
					   password: str = str(), **kwargs):
		if pattern:
			self.pattern = pattern
		if password:
			self._password = password.encode() if isinstance(password, str) else password
		if not self.key and key and not value:
			self.key, self.value = (str(key), rsa.generate_private_key(public_exponent=65537, 
																			 key_size=4096,
																			 backend=default_backend()).private_bytes(
																									encoding=serialization.Encoding.PEM,
																									format=serialization.PrivateFormat.PKCS8,
																									encryption_algorithm=serialization.BestAvailableEncryption(self._password) if self._password else serialization.NoEncryption()
																								))
			self.save()
		elif not self.key and key and value and not self.value and isinstance(value, bytes):
			self.key, self.value = (str(key), bytes(value))
			if self().__public:
				self.save()
		elif self.key and value and value != self.value and value is not None and isinstance(value, bytes):
			self.value = bytes(value)
			if self().__public:
				self.update()

	@property
	def public(self) -> object:
		if self.__public:
			return self.__public.public_bytes(encoding=serialization.Encoding.PEM,
											  format=serialization.PublicFormat.SubjectPublicKeyInfo)

	@property
	def _public(self) -> object:
		if self.__public:
			return self.__public

	@property
	def private(self) -> object:
		if self.__private:
			return self.__private.private_bytes(encoding=serialization.Encoding.PEM,
												format=serialization.PrivateFormat.PKCS8,
												encryption_algorithm=serialization.BestAvailableEncryption(self._password) if self._password else serialization.NoEncryption())

	@property
	def _private(self) -> object:
		if self.__private:
			return self.__private

	def encrypt(self, input: bytes, size:int = 256, offset:int = 0, _ = bytes()) -> bytes:
		if input := zlib.compress(pickle.dumps(input)):
			while not offset >= len(input):
				if chunk := input[offset:offset + size]:
					if len(chunk) % size != 0:
						chunk += bytes(bytearray((size - len(chunk))))
					_ += self.__public.encrypt(chunk, self.__padding); offset += size
		return base64.b64encode(_)

	def decrypt(self, input: bytes, size:int = 512, offset:int = 0, _ = bytes()) -> bytes:
		if self.__private:
			if input := base64.b64decode(input):
				while offset != len(input):
					if chunk := input[offset:offset + size]:
						_ += self.__private.decrypt(chunk, self.__padding); offset += size
			return pickle.loads(zlib.decompress(_))
		return bytes()

	def sign(self, input: bytes) -> str():
		if self.__private:
			if input := input.encode() if isinstance(input, str) else pickle.dumps(input):
				return self.__private.sign(data=input,
									       padding=padding.PSS(
										 	  mgf=padding.MGF1(hashes.SHA256()),
											  salt_length=padding.PSS.MAX_LENGTH
										   ), 
								 		   algorithm=hashes.SHA256())
		return bytes()

	def verify(self, input: bytes, signature: bytes) -> bool:
		try:
			self.__public.verify(data=input.encode() if isinstance(input, str) else pickle.dumps(input),
								 signature=signature,
								 padding=padding.PSS(
									mgf=padding.MGF1(hashes.SHA256()),
									salt_length=padding.PSS.MAX_LENGTH
								 ),
								 algorithm=hashes.SHA256())
		except InvalidSignature:
			return False
		else:
			return True
		return False

	@property
	def tmp(self, tmp = None):
		if tmp := tempfile.NamedTemporaryFile(prefix=self.key, dir='/dev/shm' if sys.platform.startswith('linux') else None, suffix='.pem', delete=True, mode='wb+'):
			if self.__private:
				tmp.write(self.private)
			else:
				tmp.write(self.public)
			tmp.seek(0)
		return tmp

	def __enter__(self):
		return self()

	def __call__(self):
		if not self.__public and self.value:
			load_pem_private_key(self.value, password=self._password if self._password else None)
			try:
				self.__private = load_pem_private_key(self.value, password=self._password if self._password else None)
			except ValueError:
				try: 
					self.__public = load_pem_public_key(self.value)
				except ValueError:
					pass
			else:
				self.__public = self.__private.public_key()
		return self

	def __bytes__(self):
		if self.__private:
			return self.private
		else:
			return self.public
		return bytes()

	def __coerce__(self, **kwargs):
		if kwargs.get('password'):
			self._password = kwargs.get('password').encode() if isinstance(kwargs.get('password'), str) else kwargs.get('password')
		if kwargs.get('pattern'):
			self.pattern = kwargs.get('pattern')
		return self