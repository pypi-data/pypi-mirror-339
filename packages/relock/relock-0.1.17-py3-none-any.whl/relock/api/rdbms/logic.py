import sys
import time
import subprocess
import pickle
import base64
import tempfile
import ujson as json
import random
import binascii
import xxhash
import hashlib
import logging

from functools import wraps
from typing import Any
from uuid import uuid4

from . import db

class Logic(object):

	def __init__(self, key: str = None, 
					   value: Any = None, 
					   pattern: str = 'default', auto_commit=True, **kwargs):
		if pattern != None:
			self.pattern = pattern
		if not self.key and key != None and value != None:
			self.key, self.value = (key, value); 
			if auto_commit:
				self.save()
		elif self.key and value != None:
			self.value = value
			if auto_commit:
				self.update()

	def __enter__(self):
		return self
 
	def __exit__(self, *args):
		pass

	@property
	def key(self) -> Any:
		if hasattr(self, '_key'):
			return self._key

	@key.setter
	def key(self, input: Any) -> None:
		if hasattr(self, '_key') and self.delete():
			self._key = input
			self.save()
		else:
			self._key = input
				
	@property
	def value(self) -> Any:
		if hasattr(self, '_value'):
			return self._value

	@value.setter
	def value(self, value: Any) -> None:
		self._value = value

	def __abs__(self):
		""" returns true if object is fresh and never loaded from db,
			returns false if object was restored from database,
		"""
		return 1 if not hasattr(self, '__coerce') else 0

	def __bool__(self):
		if not abs(self):
			return True
		return True if db.exists('%s:%s:%s' % (self.__class__.__name__, self.pattern, self.codec(self.key))) and hasattr(self, '_value') else False

	def __bytes__(self):
		if not self.value:
			return bytes()
		return self.value.encode() if isinstance(self.value, str) else bytes(self.value)

	def __iter__(self):
		return iter(db.keys('%s:%s:*' % (self.__class__.__name__, self.pattern)))

	@classmethod
	def keys(cls, pattern: str = 'default'):
		return db.keys('%s:%s:*' % (cls.__name__, pattern))

	@classmethod
	def count(cls, pattern: str = 'default'):
		return len(cls.keys(pattern))

	@classmethod
	def random(cls, pattern: str = 'default'):
		return random.choice(cls.keys(pattern)).decode().replace(':%s' % pattern, '').replace('%s:' % cls.__name__, '')

	def delete(self):
		if bool(self):
			if hash := str(self):
				return db.delete(hash)

	def save(self):
		if hash := str(self):
			return db.set(hash, pickle.dumps(self))

	@classmethod
	def flush(cls, key:str, pattern:str = 'default'):
		if pattern := '%s:%s:%s' % (cls.__name__, pattern, cls.codec(key)):
			if db.exists(pattern):
				db.delete(pattern)
		return True

	@classmethod
	def associate(cls, key:str, value:bytes = bytes(), pattern:str = 'default-associate'):
		if pattern := '%s:%s:%s' % (cls.__name__, pattern, cls.codec(key)):
			if value:
				return db.set(pattern, pickle.dumps(value))
			if db.exists(pattern):
				return pickle.loads(db.get(pattern))
		return bytes()

	def update(self, value:Any = None):
		if value is not None:
			self.value = value
		# if bool(self):
		db.set(str(self), pickle.dumps(self))
		return self

	@staticmethod
	def codec(data:bytes) -> hex:
		if data is not None:
			if _ := hashlib.blake2b(binascii.hexlify(data.encode() if isinstance(data, str) else data),
								    salt=bytes(), 
								    digest_size=16).hexdigest():
				return _

	@classmethod
	def destroy(cls, key:bytes, **kwargs):
		if key is not None:
			if pattern := '%s:%s:%s' % (cls.__name__, 
										kwargs.get('pattern', 'default'), 
										cls.codec(key)):
				if db.exists(pattern):
					return db.delete(pattern)

	def __str__(self):
		return '%s:%s:%s' % (self.__class__.__name__, 
							 self.pattern, 
							 self.codec(self.key))

	@classmethod
	def __hex__(cls, key: bytes = None, **kwargs):
		if key is not None:
			if pattern := '%s:%s:%s' % (cls.__name__, 
										kwargs.get('pattern', 'default'), 
										cls.codec(key)):
				return pattern

	@classmethod
	def __(cls, key: bytes, **kwargs):
		if db.exists(key):
			return pickle.loads(db.get(key)).__coerce__(**kwargs)

	@classmethod
	def __new__(cls, *args, **kwargs):
		""" If object is re-created (has only one argument, key)
			let's it use internal cache, object is saved in the 
			pool so it not need to be produced from scratch.
		"""
		if _ := cls.__hex__(*args[1:], **kwargs) if len(args) == 2 or len(kwargs) == 1 and kwargs.get('key') else None:
			if object := cls.__(_):
				return object
		return super().__new__(cls)

	def __coerce__(self, **kwargs):
		if kwargs.get('pattern'):
			self.pattern = kwargs.get('pattern')
		self.__coerce = True
		return self

	def __getnewargs__(self):
		""" For new-style classes, you can influence what arguments get passed to __new__ 
			upon unpickling. This method should also return a tuple of arguments that will 
			then be passed to __new__.
		"""
		return (self.key, None)

	def __getstate__(self) -> dict:
		# Copy the object's state from self.__dict__ which contains
		# all our instance attributes. Always use the dict.copy()
		# method to avoid modifying the original state.
		_ = dict()
		for key in filter(lambda i: i not in ['_sa_instance_state', '_RSA__private', '_RSA__public'], self.__dict__.keys()):
			if key in self.__dict__:
				if not key.startswith('_') or '_key' in key or '_value' in key:
					if bytes := getattr(self, key):
						_[key] = pickle.dumps(bytes)
		return _

	def __setstate__(self, state):
		# Restore instance attributes (i.e., passwd and time).
		for item in state:
			if _ := state.get(item):
				try:
					bytes = pickle.loads(_)
				except Exception as error:
					logging.error('Recovery faild with %s', item)
				else:
					setattr(self, item, bytes)
