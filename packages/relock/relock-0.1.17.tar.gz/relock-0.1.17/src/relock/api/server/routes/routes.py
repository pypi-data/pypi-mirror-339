import binascii
import base64
import os

from . import _ as bp, logging

from flask import render_template, request, Response, redirect, url_for, session, abort
from flask_login import current_user as worker, login_required
from flask import current_app as app
from urllib.parse import urlparse

# from app.rdbms import User
from ...rdbms import Service

from ....crypto import GCM
# from app.plugins.mail import Mail as Compose
# from app.plugins.relock import Montgomery

# from email_validator import validate_email, EmailNotValidError

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

@bp.route('/info/<string:uuid>', methods=['GET', 'POST'])
@bp.route('/info', methods=['POST', 'GET'])
def info(uuid=None):
	return dict(request.headers)

@bp.route('/authorization/<string:token>', methods=['GET', 'POST'])
@bp.route('/authorization', methods=['GET', 'POST'])
def authorization(token=None):
    # params={
    #     "response_type": "code",
    #     "client_id": client_id,
    #     "scope": "openid",
    #     "redirect_uri": redirect_uri,
    #     "state": state,
    #     "code_challenge": code_challenge,
    #     "code_challenge_method": "S256",
    # },
	print(request.args)
	print(request.json)
	print('client_id' in request.args or token is not None)
	# {'code': ['478296a3-c3ea-4a2f-bd2e-69f3181fb78c.af09d80d-9901-445f-b789-c6dfa33ec175.294e60a6-9596-406b-9eae-1912aebe04dd'],
	#  'session_state': ['af09d80d-9901-445f-b789-c6dfa33ec175'],
	#  'state': ['fooobarbaz']}
	return dict(request.headers)

@bp.route('/token', methods=['GET'])
def token(uuid=None):
    # data={
    #     "grant_type": "authorization_code",
    #     "client_id": client_id,
    #     "redirect_uri": redirect_uri,
    #     "code": auth_code,
    #     "code_verifier": code_verifier,
    # },
	print(request.args)
	# {'access_token': 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJjd05fNm5WaEQyM0U4WWVnUGJob1pBU2c2Ynd4a2ktSkNsMHJlWFdJUEE4In0.eyJqdGkiOiIyZDA3OTBhNS1hNjMwLTQ2MDYtOTI5Ni1kNGQ0Y2M4NDg5NDgiLCJleHAiOjE1NjkzOTg0OTksIm5iZiI6MCwiaWF0IjoxNTY5Mzk4NDM5LCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjkwOTAvYXV0aC9yZWFsbXMvbWFzdGVyIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjEwMzMzNmJmLWM0NzEtNGRkNS1iMzllLTQ2NTJhMDAzMmJlOCIsInR5cCI6IkJlYXJlciIsImF6cCI6InBrY2UtdGVzdCIsImF1dGhfdGltZSI6MTU2OTM5ODQzOCwic2Vzc2lvbl9zdGF0ZSI6ImFmMDlkODBkLTk5MDEtNDQ1Zi1iNzg5LWM2ZGZhMzNlYzE3NSIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6ImpvaG4ifQ.C0723Ejex8k8dVGzTT2IRtEYXymAONBMkpoRCAGwd_E253L8WZGsEJ5-qkGgzpafgen85XpAD6c_x44QsD_q0P74J_9FqQPikY6JmpcUMNYD9eXjzZo21USVD2DKV7JOZ9Wp3N9GwcV50KCYZIcoIgHfGpHbCnhVppdHn5tuH936WsBGQL7tQ5zDFuT3fO1Op01XdJBg77LT91HTDq1zh42kH1fzgTO3zDzKKxlOJN6d7yBiMDCSIdZ3CVDRMSl65FK-7433SLWoJmNAQHIlH8RYrtvkNIfUZmABXe3CVBWQ2HJXG4Y-gocxkaiFxDoRwoYC6YfwiXKmjnita2vfSw',
	#  'expires_in': 60,
	#  'id_token': 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJjd05fNm5WaEQyM0U4WWVnUGJob1pBU2c2Ynd4a2ktSkNsMHJlWFdJUEE4In0.eyJqdGkiOiI5NmFkMmFiOS02ZDU0LTRjYmItYTIzYi01Y2ZkYWY1MDI0OTciLCJleHAiOjE1NjkzOTg0OTksIm5iZiI6MCwiaWF0IjoxNTY5Mzk4NDM5LCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjkwOTAvYXV0aC9yZWFsbXMvbWFzdGVyIiwiYXVkIjoicGtjZS10ZXN0Iiwic3ViIjoiMTAzMzM2YmYtYzQ3MS00ZGQ1LWIzOWUtNDY1MmEwMDMyYmU4IiwidHlwIjoiSUQiLCJhenAiOiJwa2NlLXRlc3QiLCJhdXRoX3RpbWUiOjE1NjkzOTg0MzgsInNlc3Npb25fc3RhdGUiOiJhZjA5ZDgwZC05OTAxLTQ0NWYtYjc4OS1jNmRmYTMzZWMxNzUiLCJhY3IiOiIxIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJqb2huIn0.HAPQmX_ZxmTNxhxOst4U5STJZEEP-GgSfOh303p5oCYZ4y-jhk1SG4BMXW1dU7GWaTh9ccI2aVt8kYjOOsqin3jYvELoZRUxnMk0VftgARNcmb0vb-v2uCdSftSYUGvxmqU0TXeYL2hz7lELIJQSbH3C_DGg476yvRzWh7LEk2bdx8K3yS07jA6w0clDoB79uztfSrwnmtsB1S0soIsE14CaNwI93kiD40m6p9WU5EdPfIu0VaNqQrsCzQrt4LojqN5zAIwDLdBScZBukhWYn0WKmTqcw1djGZBWKHvwV9kP4m27T_0DKpa9Bwi0AomlFjhDK_b41ERuE-3-7MNH5A',
	#  'not-before-policy': 0,
	#  'refresh_expires_in': 1800,
	#  'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwZjBlNjZiZS1hOWNkLTRhMjktODdiNS00NTAwMGZjYzk1NjcifQ.eyJqdGkiOiJiOGYxZDJmZi1mNmYzLTRiYTEtYjU3OC0zMmMxZDZlMjllN2IiLCJleHAiOjE1Njk0MDAyMzksIm5iZiI6MCwiaWF0IjoxNTY5Mzk4NDM5LCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjkwOTAvYXV0aC9yZWFsbXMvbWFzdGVyIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo5MDkwL2F1dGgvcmVhbG1zL21hc3RlciIsInN1YiI6IjEwMzMzNmJmLWM0NzEtNGRkNS1iMzllLTQ2NTJhMDAzMmJlOCIsInR5cCI6IlJlZnJlc2giLCJhenAiOiJwa2NlLXRlc3QiLCJhdXRoX3RpbWUiOjAsInNlc3Npb25fc3RhdGUiOiJhZjA5ZDgwZC05OTAxLTQ0NWYtYjc4OS1jNmRmYTMzZWMxNzUiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUifQ.KmzF-T3meYK1m72ShHQGA3G0VGVA6GYXNIMZVoHkx9Q',
	#  'scope': 'openid email profile',
	#  'session_state': 'af09d80d-9901-445f-b789-c6dfa33ec175',
	#  'token_type': 'bearer'}
	return dict(request.headers)

@bp.route('/establish/<string:_key>', methods=['GET'])
@bp.route('/establish', methods=['POST'])
def establish(key=None, origin=None):
	if request.method == 'POST' and request.json.get('key'):
		key = request.json.get('key')
	try:
		key = binascii.unhexlify(key)
	except:
		abort(401, 'Data format is invalid.')
	else:
		try:
			if origin := urlparse(request.headers.get('X-Client-Host')):
				origin = origin.netloc or origin.path
		except:
			key = None
		else:
			if service := Service(origin):
				try:		
					service.exchange(key)
				except:
					abort(401, 'Key establishment faild.')
				else:
					key = binascii.hexlify(bytes(service)).decode()
				finally:
					logging.info('Key establishment for %s', origin)
	finally:
		return dict(key=key, origin=origin)

# https://relock.service/api/authorization
# ?client_id=my_client_id
# &redirect_uri=http%3A%2F%2Flocalhost%callback
# &response_type=code
# &state=kHWL4VwcbUbtPR4mtht6yMAGG_S-ZcBh5RxI_IGDmJc
# &nonce=mSGOS1M3LYU9ncTvvutoqUR4n1EtmaC_sQ3db4dyMAc
# &scope=openid+email+profile
# &code_challenge=W3n02f6xUKoDVbmhWEWz3h780b-Ci6ucnBS_d7nogmQ
# &code_challenge_method=S256
# &resource=https%3A%2F%2Fmy.resource.local%2Fapi