from sdk import GitSession
import json

def test_with_user_password(username, password):
	session = GitSession(username, password, headers= {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
	})
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
	session = GitSession(username, password, client_id, client_secret, headers= {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    })
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
	session = GitSession(pat=pat, headers= {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    })
	resp = session.get('user')
	assert resp.status_code >= 200 and resp.status_code <= 299
	resp_json = json.loads(resp.text)
	assert resp_json['login'] == username

	session.close()

	resp = session.get('user')
	assert resp.status_code >= 200 and resp.status_code <= 299
	resp_json = json.loads(resp.text)
	assert resp_json['login'] == username


