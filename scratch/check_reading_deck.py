# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def call_mcp(name, arguments={}):
    req = urllib.request.Request(
        'http://127.0.0.1:3141/',
        data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': name, 'arguments': arguments}}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith('data: '):
            return json.loads(line[6:])['result']
    return None

res = call_mcp('find_notes', {'query': '取り組み or 取り組む'})
print("Search results:", res['structuredContent'])
if res['structuredContent']['noteIds']:
    info_res = call_mcp('notes_info', {'notes': res['structuredContent']['noteIds']})
    for n in info_res['structuredContent']['notes']:
        print(f"Deck: {n['modelName']}, kanji: {n['fields'].get('kanji', {}).get('value')}")
