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

from flask import current_app as app, url_for, redirect, request, session, Response
from flask_login import current_user as worker
from uuid import uuid4
from datetime import datetime
from datetime import timedelta

from typing import Any

from ..logic import Logic


from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends.openssl.backend import backend

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.kdf.x963kdf import X963KDF
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.asymmetric import ed25519

from cryptography.hazmat.primitives.asymmetric.ed25519 import (Ed25519PrivateKey, 
															   Ed25519PublicKey)
from cryptography.hazmat.primitives.asymmetric.x25519 import (X25519PrivateKey, 
															  X25519PublicKey)
from cryptography.hazmat.primitives.serialization import (Encoding, 
														  NoEncryption, 
														  PrivateFormat, 
														  PublicFormat)
from fe25519 import fe25519
from ge25519 import ge25519, ge25519_p3

class Service(Logic):

	def __init__(self, key: str = None, 
					   value: Any = None, 
					   pattern: str = 'default', **kwargs):
		if pattern != None:
			self.pattern = pattern
		if key and not value:
			if _ := ed25519.Ed25519PrivateKey.generate():
				value = _.private_bytes(encoding=serialization.Encoding.Raw,
									    format=serialization.PrivateFormat.Raw,
									    encryption_algorithm=serialization.NoEncryption())
		if not self.key and key != None and value != None:
			self.key, self.value = (key, value); self.save()

		self.__private = ed25519.Ed25519PrivateKey.from_private_bytes(self.value)
		self.__public = self.__private.public_key()

	def __enter__(self):
		return self
 
	def __exit__(self, *args):
		pass

	@staticmethod
	def x25519_from_ed25519_private_bytes(private_bytes):
		if not backend.x25519_supported():
			raise UnsupportedAlgorithm(
				"X25519 is not supported by this version of OpenSSL.",
				_Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM,
			)

		hasher = hashes.Hash(hashes.SHA512())
		hasher.update(private_bytes)
		h = bytearray(hasher.finalize())
		# curve25519 clamping
		h[0] &= 248
		h[31] &= 127
		h[31] |= 64

		return x25519.X25519PrivateKey.from_private_bytes(h[0:32])

	@staticmethod
	def x25519_from_ed25519_public_bytes(public_bytes) -> X25519PublicKey:
		if not backend.x25519_supported():
			raise UnsupportedAlgorithm(
				"X25519 is not supported by this version of OpenSSL.",
				_Reasons.UNSUPPORTED_EXCHANGE_ALGORITHM,
			)

		# This is libsodium's crypto_sign_ed25519_pk_to_curve25519 translated into
		# the Pyton module ge25519.
		if ge25519.has_small_order(public_bytes) != 0:
			raise ValueError("Doesn't have small order")

		# frombytes in libsodium appears to be the same as
		# frombytes_negate_vartime; as ge25519 only implements the from_bytes
		# version, we have to do the root check manually.
		A = ge25519_p3.from_bytes(public_bytes)
		if A.root_check:
			raise ValueError("Root check failed")

		if not A.is_on_main_subgroup():
			raise ValueError("It's on the main subgroup")

		one_minus_y = fe25519.one() - A.Y
		x = A.Y + fe25519.one()
		x = x * one_minus_y.invert()

		return bytes(x.to_bytes())

	def exchange(self, key):
		self.service_key = key
		if bytes := self.x25519_from_ed25519_public_bytes(key):
			if public := x25519.X25519PublicKey.from_public_bytes(bytes):
				if private := self.x25519_from_ed25519_private_bytes(self.value):
					self.secret_key = private.exchange(public)
		return self.secret

	@property
	def secret(self):
		if hasattr(self, 'secret_key'):
			return self.secret_key

	@property
	def public(self):
		if bytes := self.__public.public_bytes(
			encoding=serialization.Encoding.Raw,
			format=serialization.PublicFormat.Raw
		):
			return bytes

	@property
	def service(self):
		if hasattr(self, 'service_key'):
			return ed25519.Ed25519PublicKey.from_public_bytes(self.service_key)

	def sign(self, data:bytes) -> bytes:
		return self.__private.sign(data)

	def verify(self, data:bytes, signature:bytes) -> bool:
		try:
			self.service.verify(signature, data)
		except:
			return False
		else:
			return True

	def __bytes__(self):
		return self.public

	def __abs__(self):
		return self.value