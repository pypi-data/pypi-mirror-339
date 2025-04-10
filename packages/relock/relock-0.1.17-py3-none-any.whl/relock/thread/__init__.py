import time
import logging
import threading

from functools import wraps

class Thread(object):

	counter = 0

	@classmethod
	def daemon(cls, function):
		@wraps(function)
		def daemon(*args, **kwargs):
			cls.counter = cls.counter + 1
			if _ := threading.Thread(target=function, 
									 name=function.__name__ + str(cls.counter), 
									 args=args, 
									 kwargs=kwargs, 
									 daemon=True):
				_.start()
		return daemon

	@classmethod
	def thread(cls, function):
		@wraps(function)
		def thread(*args, **kwargs):
			cls.counter = cls.counter + 1
			if _ := threading.Thread(target=function, 
									 name=function.__name__ + str(cls.counter), 
									 args=args,
									 kwargs=kwargs):
				_.start()
				return _.join()
		return thread