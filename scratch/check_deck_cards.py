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

res = call_mcp('list_decks')
decks = json.loads(res['content'][0]['text'])['decks']
for d in decks:
    if '14' in d['name']:
        print("Deck:", d)
        find_res = call_mcp('find_notes', {'query': f"deck:\"{d['name']}\""})
        txt = find_res['content'][0]['text']
        data = json.loads(txt)
        note_ids = data.get('note_ids', [])
        print(f"Cards count in {d['name']}: {len(note_ids)}")
        if note_ids:
            info = call_mcp('notes_info', {'note_ids': note_ids})
            print("Notes:", info['content'][0]['text'])
