import urllib.request
import json

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

print("Models:", call_mcp('model_names'))
print("Field names of 'JLPT 한권으로 끝내기 단어장':", call_mcp('model_field_names', {'model_name': 'JLPT 한권으로 끝내기 단어장'}))
print("Decks:", call_mcp('list_decks'))
