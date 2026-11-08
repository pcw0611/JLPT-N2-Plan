import sys, json, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

def call_mcp(name, arguments=None):
    req = urllib.request.Request(
        'http://127.0.0.1:3141/',
        data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': name, 'arguments': arguments or {}}}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        for line in resp.read().decode('utf-8').splitlines():
            if line.startswith('data: '):
                return json.loads(line[6:])['result']

r1 = call_mcp('find_notes', {'query': 'kanji:稼ぐ'})
print("稼ぐ in Anki:", r1['content'][0]['text'])
r2 = call_mcp('find_notes', {'query': 'kanji:経済'})
print("経済 in Anki:", r2['content'][0]['text'])
