import os
import sys
import jwt
import ssl
import time
import base64
import ujson as json
import tempfile
import logging
import binascii
import requests
import urllib3

urllib3.disable_warnings()

from tempfile import NamedTemporaryFile

from urllib.parse import urlparse
from urllib.parse import urlencode

from os import environ as env
from uuid import uuid4

logging = logging.getLogger('relock.api')

from .rdbms import Service, Config, db

class reLock(object):

	def __init__(self, app=None, origin='localhost',
								 client_id=str(uuid4()),
								 client_secret=str(uuid4()),
								 redirect_uri='/',
								 corutine=False, **kwargs):

		self.origin        = env.get('HOST_ORIGIN', origin)
		self.client_id     = env.get('CLIENT_ID', client_id)
		self.client_secret = env.get('CLIENT_SECRET', client_secret)
		self.redirect_uri  = env.get('REDIRECT_URI', redirect_uri)
		self.service       = Service(self.origin)
		self.url 	       = 'https://relock.service/api/'

		if _origin := urlparse(self.url).netloc:
			if origin := Config(_origin):
				self.__certyficate = origin
			else:
				try:
					certyficate = ssl.get_server_certificate((_origin, 443))
				except:
					certyficate = bytes()
				else:
					certyficate = certyficate.encode()
				finally:
					self.__certyficate = Config(_origin, certyficate)

		if app is not None:
			self.init_app(app)

		if not self.service.secret:
			if response := self('establish', key=binascii.hexlify(bytes(self.service)).decode()):
				if key := response.get('key'):
					try:
						key = binascii.unhexlify(key)
					except:
						logging.error('Key agreement faild, wrong data.')
					else:
						try:
							self.service.exchange(key)
						except:
							logging.error('Key agreement faild, wrong key.')
						else:
							logging.info('Key establishment for service has been done.')
						finally:
							self.service.update()

		print(self(endpoint='authorization/123456789', 
				      token='123456789'))

	def init_app(self, app, *args, **kwargs):
		if not hasattr(app, 'extensions'):
			app.extensions = {}
		app.extensions['relock'] = self
		return self

	@property
	def crt(self, tmp = None):
		if self.__certyficate:
			if tmp := NamedTemporaryFile(prefix=self.__certyficate.key, 
										 dir='/dev/shm' if sys.platform.startswith('linux') else None, 
										 suffix='.crt', 
										 delete=True, 
										 mode='wb+'):
				tmp.write(self.__certyficate.value); tmp.seek(0);
			return tmp
		return False

	def __call__(self, endpoint='info', 
					   js=dict(), 
					   **kwargs):
		# encoded = jwt.encode({"Some":"Key"}, private, algorithm='EdDSA')
		# decoded = jwt.decode(encoded, public, algorithms='EdDSA', verify=True)

		with self.crt as crt:
			headers = { "Client-ID" : self.client_id,
						"User-Agent": "re:lock:api",
						"X-Client-Host": self.origin,
			            "Content-Type" : "application/json"}
			if response := requests.post(self.url + endpoint, 
										 headers=headers,
										 json=kwargs, 
										 verify=crt.name):
				try:
					js = json.loads(response.content)
				except:
					logging.error('Can\'t load json from response')
				else:
					pass
		return js

	def __enter__(self):
		return self
 
	def __exit__(self, *args):
		pass

	def auth_url(self, *args, **kwargs):
		kwargs = dict(state = base64.b64encode(os.urandom(12)).decode(),
					  code_challenge = "xxx",
        			  code_challenge_method = "S256",
					  **kwargs)
		return '&'.join(["{}={}".format(k, v) for k, v in kwargs.items()])
		# return urlencode(kwargs)

	def state(self):
		return base64.urlsafe_b64encode(os.urandom(12)).decode()

	def verifier(self):
		code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
		# code_verifier = re.sub('[^a-zA-Z0-9]+', '', code_verifier)
		return code_verifier

	def challange(self, code_verifier):
		code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
		code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
		return code_challenge.replace('=', '')

	@classmethod
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super().__new__(cls)
		return cls.instance

	""" 
	"""
	def __repr__(self):
		return '<relock:API db:{0}>'.format(db.db)
