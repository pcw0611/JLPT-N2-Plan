import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

def call_mcp(name, arguments=None):
    if arguments is None:
        arguments = {}
    req = urllib.request.Request(
        'http://127.0.0.1:3141/',
        data=json.dumps({
            'jsonrpc': '2.0', 'id': 1,
            'method': 'tools/call',
            'params': {'name': name, 'arguments': arguments}
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        for line in resp.read().decode('utf-8').splitlines():
            if line.startswith('data: '):
                return json.loads(line[6:])['result']

decks = [
    'TOEIC 900+::1-기초 (600점 도달)',
    'TOEIC 900+::2-중급 (700~800점)',
    'TOEIC 900+::3-고급 (900+)',
    'TOEIC 900+::4-문법'
]

for deck in decks:
    r = call_mcp('find_notes', {'query': f'deck:"{deck}"'})
    cnt = 0
    if r and 'content' in r:
        txt = r['content'][0]['text']
        data = json.loads(txt)
        cnt = len(data.get('notes', []))
    print(f'{deck}: {cnt} notes')
