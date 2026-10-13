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

res = call_mcp('find_notes', {'query': 'tag:독해_어휘'})
txt = res['content'][0]['text']
note_ids = json.loads(txt).get('note_ids', [])
print(f"Notes with tag:독해_어휘: {note_ids}")

if note_ids:
    info = call_mcp('notes_info', {'notes': note_ids})
    for n in json.loads(info['content'][0]['text'])['notes']:
        print(f"ID: {n['noteId']} | Kanji: {n['fields']['kanji']['value']} | Cards: {n['cards']}")

# Check card info
if note_ids:
    # Check which deck card belongs to
    pass
