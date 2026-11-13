import urllib.request, json, re, sys
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
        body = resp.read().decode('utf-8')
        m = re.search(r'^data:\s*(.+)$', body, re.MULTILINE)
        if m:
            return json.loads(m.group(1))['result']
        raise ValueError('Could not parse SSE response')

queries = ['kanji:塾', 'kanji:*塾*', 'kana:じゅく', '塾']
for q in queries:
    res = call_mcp('find_notes', {'query': q})
    txt = res['content'][0]['text']
    data = json.loads(txt)
    notes = data.get('notes', [])
    print(f"Query: '{q}' -> {len(notes)} notes found")
    for n in notes[:5]:
        fields = n.get('fields', {})
        print(" ", fields.get('id', {}).get('value', ''), fields.get('kanji', {}).get('value', ''), fields.get('kana', {}).get('value', ''), fields.get('meaning', {}).get('value', '')[:40])
