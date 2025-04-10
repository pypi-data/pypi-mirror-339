import logging

from typing import Any
from ..crypto import Signer

class KDM(object):

	def __init__(self):
		pass

	def random(self):
		with self('random') as _:
			if self.response is not None:
				return Signer(self.response)

