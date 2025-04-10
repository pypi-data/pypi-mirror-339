import os
import time
import logging
import binascii

from redis import (StrictRedis, 
				   ConnectionPool, 
				   BlockingConnectionPool, 
				   UnixDomainSocketConnection)

try:
	import eventlet.patcher
except ImportError:
	try:
		import gevent.socket
	except ImportError:
		from queue import LifoQueue
	else:
		from gevent.queue import LifoQueue	
else:
	from eventlet.queue import LifoQueue

from os import environ as env

logging = logging.getLogger('relock.rdbms')

class RDBMS(StrictRedis):

	def __init__(self, app=None, host='127.0.0.1', 
								 port=6379, 
								 db=2, 
								 decode_responses=False, 
								 corutine=False, **kwargs):

		self.host     = env.get('REDIS_HOST', host)
		self.port     = env.get('REDIS_PORT', port)
		self.corutine = corutine
		self.db       = env.get('REDIS_DB', db)
		self.decode_responses = bool(decode_responses)

		if not self.corutine:
			self.__pool = ConnectionPool(host=self.host,
										 port=self.port,
										 db=self.db,
										 socket_keepalive=True,
										 decode_responses=self.decode_responses)
		else:
			self.__pool = BlockingConnectionPool(**{'host': self.host, 
												    'port': self.port, 
												    'db': self.db,
												    'decode_responses': self.decode_responses,
												    'timeout': .500,
												    'socket_keepalive': True,
												    'retry_on_timeout': True,
												    'queue_class': LifoQueue,
												 	**kwargs})

		super().__init__(connection_pool=self.__pool, 
						 db=self.db, **kwargs)

		if app is not None:
			self.init_app(app)

	def init_app(self, app, *args, **kwargs):
		if not hasattr(app, 'extensions'):
			app.extensions = {}
		app.extensions['rdbms'] = self
		return self


	def __enter__(self):
		return self
 
	def __exit__(self, *args):
		pass

	@classmethod
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super().__new__(cls)
		return cls.instance

	""" 
	"""
	def __repr__(self):
		return '<RDBMS db:{0}>'.format(self.db)


with RDBMS() as db:
	
	from .models.config import Config
	from .models.ssl import SSL
	from .models.crt import Crt
	from .models.key import Key
	from .models.service import Service

