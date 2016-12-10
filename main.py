#!/usr/bin/python
import re
import time
import json
import requests
from config import MACKEREL_URL, MACKEREL_API_KEY

SX9_URL = 'http://sx9.jp/weather/kyoto-yoshida.js'

def main():
    r = requests.get(SX9_URL)
    p = re.compile(r'\((\d), (\d+), (\d+)\)')
    data = [x.strip() for x in r.text.splitlines() if 'data.setValue(5,' in x][1:]
    poe = []
    for line in data:
        m = p.search(line)
        poe.append(int(m.group(3)))
    headers = {
        'X-Api-Key': MACKEREL_API_KEY,
        'Content-Type': 'application/json'
        }
    payload = [
        {
            'name': 'sx9.yoshida', 
            'time': int(time.strftime('%s', time.localtime())),
            'value': max(poe)
        }
    ]
    r = requests.post(MACKEREL_URL, data=json.dumps(payload), headers=headers)
    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    main()
