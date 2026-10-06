import sys
import urllib.request
import json

sys.stdout.reconfigure(encoding='utf-8')

req_body = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
}
data = json.dumps(req_body).encode('utf-8')
req = urllib.request.Request(
    "http://127.0.0.1:3141/",
    data=data,
    headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=10) as resp:
    body = resp.read().decode('utf-8')
for line in body.splitlines():
    if line.startswith("data: "):
        tools = json.loads(line[6:]).get('result', {}).get('tools', [])
        for t in tools:
            if t['name'] in ['find_notes', 'add_note', 'create_deck', 'notes_info']:
                print(f"=== {t['name']} ===")
                print(json.dumps(t['inputSchema'], indent=2))
