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

res = call_mcp('find_notes', {'query': 'deck:"JLPT 한끝 Voca::4-N2"'})
txt = res['content'][0]['text']
data = json.loads(txt)
note_ids = data.get('note_ids', [])
print(f"Total notes in 4-N2: {len(note_ids)}")
if note_ids:
    info = call_mcp('notes_info', {'note_ids': [note_ids[0]]})
    print(info['content'][0]['text'])

# Also check if '駆け足', '巡り', '妻' already exist in any deck!
for word in ['駆け足', '巡り', '妻']:
    w_res = call_mcp('find_notes', {'query': word})
    w_txt = w_res['content'][0]['text']
    w_ids = json.loads(w_txt).get('note_ids', [])
    print(f"Search for '{word}': {len(w_ids)} notes found: {w_ids}")
    if w_ids:
        w_info = call_mcp('notes_info', {'note_ids': w_ids[:1]})
        print(w_info['content'][0]['text'])
