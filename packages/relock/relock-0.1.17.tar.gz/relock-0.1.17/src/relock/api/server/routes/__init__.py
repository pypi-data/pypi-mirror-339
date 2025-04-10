from flask import Blueprint
import os, logging

logging = logging.getLogger(__name__)

_ = os.environ.get('API_ROUTE', 'api')
_ = Blueprint(_, __name__, url_prefix='/%s' % _,
						   template_folder='templates',
						   static_folder='static',
						   static_url_path='/static/%s' % _)
from .routes import *