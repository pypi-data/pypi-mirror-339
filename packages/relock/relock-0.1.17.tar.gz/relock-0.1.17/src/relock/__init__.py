""" Active API Armour TCP/HTTP client.
"""

# By Marcin Sznyra, marcin(at)relock.id, 2024.
#    re:lock B.V. Blaak 16, 3011TA, Rotterdam. KVK: 91870879.

__author__ = 'Marcin Sznyra'
__credits__ = 'relock Inc.'

from .crypto import *
from .tcp import TCP
from .tcp.socket import Socket
from .thread import Thread
from .cloud import Cloud
try:
	from flask import session
except Exception as e:
	pass
else:
	from .flask import Flask
	from .nobody import Nobody