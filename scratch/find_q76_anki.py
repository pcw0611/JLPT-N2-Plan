import json, urllib.request, sys

sys.stdout.reconfigure(encoding='utf-8')

ENDPOINT = "http://127.0.0.1:3141/"

def mcp_call(name: str, arguments: dict = None):
    req_body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": name,
            "arguments": arguments or {}
        }
    }
    data = json.dumps(req_body, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith("data: "):
            res = json.loads(line[6:])
            return res.get('result')
    return None

res = mcp_call('execute_anki_action', {
    'action': 'findCards',
    'params': {'query': 'e2_q76.mp3'}
})
print("Cards matching e2_q76.mp3:", res)

if res and 'result' in res and res['result']:
    card_ids = res['result']
    info = mcp_call('execute_anki_action', {
        'action': 'cardsInfo',
        'params': {'cards': card_ids}
    })
    print("Found cards info count:", len(info['result']))
    for c in info['result']:
        print(f"Card ID: {c['cardId']} | Note ID: {c['noteId']}")
        fields = c['fields']
        for fn, fv in fields.items():
            if '青葉市' in fv['value']:
                print(f"  Field {fn} contains 青葉市!")
