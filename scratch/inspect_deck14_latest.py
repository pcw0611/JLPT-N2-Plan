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

if __name__ == '__main__':
    r = call_mcp('cards_stats', {'deck': 'JLPT N2::14 독해・기사・모의고사 어휘', 'limit': 1000})
    cards = json.loads(r['content'][0]['text']).get('cards', [])
    print(f"Total cards in Deck 14: {len(cards)}")
    nids = [c['nid'] for c in cards]
    n_info = call_mcp('notes_info', {'notes': nids[-5:]})
    raw = json.loads(n_info['content'][0]['text'])
    print("Raw keys:", list(raw.keys()) if isinstance(raw, dict) else type(raw))
    notes_list = raw.get('notes', []) if isinstance(raw, dict) else raw
    for n in notes_list:
        fields = n.get('fields', {})
        print(f"ID: {fields.get('id', {}).get('value')}, Kanji: {fields.get('kanji', {}).get('value')}, Kana: {fields.get('kana', {}).get('value')}")
