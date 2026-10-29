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

r = call_mcp('cards_stats', {'deck': 'JLPT N2::14 독해・기사・모의고사 어휘', 'limit': 2})
txt = r['content'][0]['text']
d = json.loads(txt)
cards = d.get('cards', [])
if cards:
    nid = cards[0]['nid']
    n_info = call_mcp('notes_info', {'notes': [nid]})
    print(n_info['content'][0]['text'])
