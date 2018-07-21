import requests
import json
import base64
import datetime
import logging
import inspect

logger = logging.getLogger('git-sdk')

class GitSession(requests.Session):
	API_DOMAIN = 'https://api.github.com'
	def __init__(self, user=None, password=None, client_id=None, client_secret=None, pat=None, **kwargs):
		super(GitSession, self).__init__(**kwargs)
		self.user = user
		self.password = password
		self.client_id = client_id
		self.client_secret = client_secret
		self.pat = pat
		self.closed = False
		self.authenticate()

	def authenticate(self):
		if self.pat:
			self.auth_type = 'PAT'
		elif self.client_id and self.client_secret and self.user and self.password:
			url = '%s/authorizations' % self.API_DOMAIN
			data = json.dumps({
				'client_id': self.client_id,
				'client_secret': self.client_secret,
				'note': 'sdk ' + datetime.datetime.now().isoformat()
			})
			headers = {
				'Authorization': 'Basic ' + base64.b64encode(bytearray('%s:%s' % (self.user, self.password), 'utf-8')).decode('utf-8')
			}
			resp = super(GitSession, self).post(url, data=data, headers=headers)
			if resp.status_code < 200 or resp.status_code > 299:
				raise Exception(resp.text)
			resp_json = json.loads(resp.text)
			logger.debug('Received oauth token %s', resp_json)
			self.oauth_authorization = resp_json
			self.auth_type = 'OAUTH'
		elif self.user and self.password:
			self.auth_type = 'BASIC'
		else:
			raise Exception('Either user, password or personal access token(pat) must be provided')

	def close(self):
		if self.auth_type == 'OAUTH':
			resp = self.delete('authorizations/%s' % self.oauth_authorization['id'], auth_type='BASIC')
			if resp.status_code >= 200 or resp.status_code <= 299:
				logger.debug('Successfully deleted oauth authorization %s', self.oauth_authorization['id'])
				self.closed = True
			else:
				logger.debug('Failed to delete oauth authorization %s: %s', self.oauth_authorization['id'], resp.text)

	def get_headers(self, auth_type=None, **kwargs):
		auth_type = auth_type if auth_type else self.auth_type
		if auth_type == 'BASIC':
			auth_str = 'Basic ' + base64.b64encode(bytearray('%s:%s' % (self.user, self.password), 'utf-8')).decode('utf-8')
		elif auth_type == 'OAUTH':
			auth_str = 'Basic ' + base64.b64encode(bytearray('%s:%s' % (self.user, self.oauth_authorization['token']), 'utf-8')).decode('utf-8')
		elif auth_type == 'PAT':
			auth_str = 'token ' + self.pat

		headers = {
			'Authorization': auth_str
		}

		headers.update(kwargs.get('headers', {}))

		return headers

	def make_request(self, endpoint, auth_type=None, data=None, **kwargs):
		if self.closed:
			logger.debug('Request on a closed session, Reauthenticating session')
			self.authenticate()
			self.closed = False

		current_frame = inspect.currentframe()
		caller_frame = inspect.getouterframes(current_frame, 2)
		caller_name = caller_frame[1][3]

		target_func = getattr(super(GitSession, self), caller_name)
		url = '%s/%s' % (self.API_DOMAIN, endpoint)
		if isinstance(data, (dict, list)):
			data=json.dumps(data)
		logger.debug('%s %s', caller_name.upper(), url)
		return target_func(url, data=data, headers=self.get_headers(auth_type=auth_type, **kwargs), **kwargs)

	def get(self, endpoint, auth_type=None, **kwargs):
		return self.make_request(endpoint, auth_type=auth_type, **kwargs)

	def put(self, endpoint, auth_type=None, **kwargs):
		return self.make_request(endpoint, auth_type=auth_type, **kwargs)

	def delete(self, endpoint, auth_type=None, **kwargs):
		return self.make_request(endpoint, auth_type=auth_type, **kwargs)

	def patch(self, endpoint, auth_type=None, **kwargs):
		return self.make_request(endpoint, auth_type=auth_type, **kwargs)

	def post(self, endpoint, auth_type=None, **kwargs):
		return self.make_request(endpoint, auth_type=auth_type, **kwargs)

