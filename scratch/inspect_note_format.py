import sys, json, urllib.request
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
    with urllib.request.urlopen(req, timeout=10) as resp:
        for line in resp.read().decode('utf-8').splitlines():
            if line.startswith('data: '):
                return json.loads(line[6:])['result']

res = call_mcp('find_notes', {'query': 'note:"JLPT 한권으로 끝내기 단어장"'})
text = json.loads(res['content'][0]['text'])
note_ids = text.get('note_ids', [])[:1]
print("Found note:", note_ids)
info_res = call_mcp('notes_info', {'notes': note_ids})
info = json.loads(info_res['content'][0]['text'])
print(json.dumps(info, ensure_ascii=False, indent=2))
