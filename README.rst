Git-sdk : Python sdk to access github via github REST api
===============================================

.. code-block:: python
>>> from sdk import GitSession
>>> session = GitSession(user='USER', password='PASSWORD')
>>> session.get('user')
<Response [200]>
>>> resp = session.get('user')
>>> resp.text
'{"login":"USER","id":34100649,...
>>> session.close()

If you have an app with client_id and client_secret

.. code-block:: python
>>> session = GitSession(user='USER', password='PASSWORD', client_id='9db6e44220ce9asd3e5', client_secret='0df6e5h54b4bac4fb6fb29e2asc2541df815lc546')
>>> session.get('user')
<Response [200]>

If you have a personal access token(pat)

.. code-block:: python
>>> session = GitSession(pat='0df6e5h54b4bac4fb6fb29e2asc2541df815lc546')

If you want to force Basic authentication for endpoints, which do not allow any other authentication

.. code-block:: python
>>> session.get('authorizations', auth_type='BASIC')
<Response [200]>

POST eg.

.. code-block:: python
>>> session.post('authorizations', data={'client_id': '9db6e44220ce9313f3e5', 'client_secret': '0ff6e554b4bdc4fb6fb29e2a1c2541df815ac506'}, auth_type='BASIC')
<Response [201]>
>>> 
>>> session.post('authorizations', data={'client_id': '9db6e44220ce9313f3e5', 'client_secret': '0ff6e554b4bdc4fb6fb29e2a1c2541df815ac506'}, auth_type='BASIC', headers={'Content-Encoding':'gzip'})
<Response [201]>
