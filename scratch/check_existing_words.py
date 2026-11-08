import json
import urllib.request
import sys
import os

sys.path.append(os.getcwd())
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

words_to_check = [
    "田中", "佐藤", "鈴木", "山田", "主任", "係長",
    "商事", "物産", "電機",
    "各駅停車", "快速", "急行", "特急",
    "早割", "平日限定", "土日祝"
]

for w in words_to_check:
    res = call_mcp('cards_find', {'query': f'"{w}"'})
    txt = res['content'][0]['text']
    d = json.loads(txt)
    cids = d.get('cardIds', [])
    if cids:
        print(f"Word '{w}' exists in {len(cids)} cards")
    else:
        print(f"Word '{w}' NOT found")
