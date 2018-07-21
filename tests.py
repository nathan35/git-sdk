from sdk import GitSession
import json

def test_with_user_password(username, password):
	session = GitSession(username, password)
	resp = session.get('user')
	assert resp.status_code >= 200 and resp.status_code <= 299
	resp_json = json.loads(resp.text)
	assert resp_json['login'] == username

	session.close()

	resp = session.get('user')
	assert resp.status_code >= 200 and resp.status_code <= 299
	resp_json = json.loads(resp.text)
	assert resp_json['login'] == username
	

def test_with_client_secret(username, password, client_id, client_secret):
	session = GitSession(username, password, client_id, client_secret)
	resp = session.get('user')
	assert resp.status_code >= 200 and resp.status_code <= 299
	resp_json = json.loads(resp.text)
	assert resp_json['login'] == username

	session.close()

	resp = session.get('user')
	assert resp.status_code >= 200 and resp.status_code <= 299
	resp_json = json.loads(resp.text)
	assert resp_json['login'] == username

def test_with_personal_access_token(username, pat):
	session = GitSession(pat=pat)
	resp = session.get('user')
	assert resp.status_code >= 200 and resp.status_code <= 299
	resp_json = json.loads(resp.text)
	assert resp_json['login'] == username

	session.close()

	resp = session.get('user')
	assert resp.status_code >= 200 and resp.status_code <= 299
	resp_json = json.loads(resp.text)
	assert resp_json['login'] == username


