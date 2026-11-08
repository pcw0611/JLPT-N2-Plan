import urllib.request
import json

req = urllib.request.Request(
    'http://127.0.0.1:3141/',
    data=json.dumps({
        'jsonrpc': '2.0', 'id': 1,
        'method': 'tools/list',
        'params': {}
    }).encode('utf-8'),
    headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
)
with urllib.request.urlopen(req, timeout=10) as resp:
    data = resp.read().decode('utf-8')
    for line in data.splitlines():
        if line.startswith('data: '):
            tools = json.loads(line[6:])['result']['tools']
            print("Tools available:")
            for t in tools:
                print(f" - {t['name']}")
