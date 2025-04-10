from flask import (current_app as app, 
				   session, 
				   request, 
				   Response, 
				   url_for, 
				   json,
				   render_template, 
				   flash, 
				   jsonify, 
				   redirect, 
				   abort, 
				   make_response, 
				   session)

from flask_login import (current_user as worker, 
						 login_required)

from . import bp, logging

import bleach
import random, os
import time
import pickle
import base64
import hashlib
import binascii
import subprocess

from datetime import datetime
from datetime import timedelta
from jsmin import jsmin

from urllib.parse import urlparse

from .device import (origin_authentication_key_collision,
					 origin_authentication_failure_invalid_signature,
					 origin_authentication_is_successful,
					 origin_authentication_rekeying_demand,
					 origin_authentication_rekeying_nonce_mismatch,
					 origin_authentication_empty_token,
					 origin_authentication_empty_signature,
					 token_invalid_fails_when_unpacking,
					 the_signature_validation_throws_error,
					 user_has_opened_a_new_tab_in_the_browser,
					 user_tab_has_been_purged_unload_effect,
					 user_logged_out_as_all_tabs_have_been_closed,
					 user_new_tab_has_been_blocked_as_not_allowed)

@bp.route('/remote', methods=['POST'])
def remote():
	if ip := ".".join(map(str, (random.randint(35, 200) 
                        		  for _ in range(4)))):
		if request.device.rekeying():
			request.device.addr = ip
	return dict(addr=request.device.addr, id=binascii.hexlify(request.device.hash).decode())

@bp.route('/register', methods=['POST'])
def register():
	if request.method == 'POST' and request.json.get('credential'):
		return request.device.webauthn(request.json)
	return request.device.webauthn()

@bp.route('/authenticate', methods=['POST'])
def authenticate():
	if request.method == 'POST' and 'credential' in request.json:
		return request.device.authenticate(request.json.get('credential'))
	return request.device.authenticate()

@bp.route('/identity/<string:token>', methods=['GET'])
def identity(token=None):
	return binascii.hexlify(os.urandom(64))

@bp.route("/screen", methods=['POST'])
def screen(token=None):
	return ('', 204)

@bp.route("/close", methods=['POST'])
def close(token=None, delay=1.5):
	if screen := bleach.clean(request.form.get('screen')):
		if screens := session.get('screens', dict()):
			if screen in session['screens']:
				session['screens'][screen] = time.monotonic() + delay
				user_tab_has_been_purged_unload_effect.send(screen=screen,
															origin=bleach.clean(request.form.get('origin')),
															path=bleach.clean(request.form.get('path')))
	return ('', 204)

@bp.route("/exchange", methods=['POST'])
def exchange():
	if not isinstance(request.json.get('key'), list):
		return dict()
	if not isinstance(request.json.get('hash'), list):
		return dict()
	with app.app_context():
		if keys := request.device.exchange(bytes(request.json.get('key')),
										   bytes(request.json.get('hash')),
										   bytes(request.json.get('xsid')),
										   bytes(request.json.get('screen'))):
			return keys
	return dict()

@bp.route("/validate", methods=['POST'])
def validate(token=None, signature=None):
	if not worker.is_authenticated:
		session['screens'] = dict()
	if screen := bleach.clean(request.json.get('screen')):
		if not session.get('screens'):
			session['screens'] = dict()
		if not screen in session['screens']:
			user_has_opened_a_new_tab_in_the_browser.send()
		session['screens'][screen] = -1
	if request.device.nonce:
		if request.json.get('nonce') and bytes(request.json.get('nonce')) != request.device.nonce:
			origin_authentication_rekeying_nonce_mismatch.send(json=request.json.get('nonce'),
															   device=request.device.nonce)
		origin_authentication_rekeying_demand.send()
		if token := request.device.rekeying(request.device.nonce):
			request.device.nonce = bytes()

	if token := request.headers.get('X-Key-Token', str()):
		try:
			if isinstance(token, str) and int(token, 16):
				token = binascii.unhexlify(token)
		except:
			token_invalid_fails_when_unpacking.send()
	else:
		origin_authentication_empty_token.send()

	if signature := request.headers.get('X-Key-Signature', str()):
		try:
			if isinstance(signature, str) and int(signature, 16):
				signature = binascii.unhexlify(signature)
		except:
			the_signature_validation_throws_error.send()
	else:
		origin_authentication_empty_signature.send()

	if signature := request.device.verify(token,
										  signature):
		if token := request.device.validate(token):
			origin_authentication_is_successful.send(signature=signature,
													 token=token)
			return dict(status=True, 
						authenticated=worker.is_authenticated, 
						credential=True if request.device.credential else False,
						url=None,
						reprocess=False,
						timeout=0,
						owner=True if request.device.owner else False)
		origin_authentication_key_collision.send(signature=signature,
												 token=token)
		return dict(status=False, 
					authenticated=worker.is_authenticated, 
					credential=True if request.device.credential else False,
					url=None,
					reprocess=app.config.get('SESSION_SENTINEL_REPROCESS'), 
					timeout=0,
					owner=True if request.device.owner else False)
	origin_authentication_failure_invalid_signature.send(signature=signature)
	return dict(status=False, 
				authenticated=worker.is_authenticated,
				credential=True if request.device.credential else False,
				url=None,
				reprocess=app.config.get('SESSION_SENTINEL_REPROCESS'), 
				timeout=0,
				owner=True if request.device.owner else False)

@bp.route('/relock.js', methods=['GET'])
def js(content=bytes(), cache='package.py'):
	__static__ = os.path.join(os.path.dirname(__file__), '../javascript')
	if app.config.get('APP_DEBUG'):
		for file in ('passkey.js', 'noble-hashes.js', 'noble-curves.js', 'utils.js', 'gcm.js', 'relock.js', 'forms.js'):
			if os.path.exists(os.path.join(__static__, file)):
				with open(os.path.join(__static__, file)) as js_file:
					content += bytes(js_file.read(),'utf-8')
	if not app.extensions.get('relock_js'):
		if content:
			with open(os.path.join(__static__, cache), 'wb') as js_file:
				js_file.write(content)
		elif os.path.exists(os.path.join(__static__, cache)):
			with open(os.path.join(__static__, cache), 'rb') as js_file:
				content += js_file.read()
		app.extensions['relock_js'] = jsmin(content.decode())
	return Response(app.extensions.get('relock_js'), status=200, 
													 content_type='text/javascript; charset=utf-8')

@bp.route("/clear", methods=['POST', 'GET'])
def clear():
	return dict(status=request.device.clear())