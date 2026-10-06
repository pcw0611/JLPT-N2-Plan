import sys
import urllib.request
import json

sys.stdout.reconfigure(encoding='utf-8')

def mcp_call(name, args=None):
    req_body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": name,
            "arguments": args or {}
        }
    }
    data = json.dumps(req_body, ensure_ascii=False).encode('utf-8')
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
            return json.loads(line[6:]).get('result')
    return None

models = [
    "Basic",
    "Japanese Vocabulary",
    "JLPT 한권으로 끝내기 단어장"
]

for m in models:
    print(f"\n==================== MODEL: {m} ====================")
    style = mcp_call('model_styling', {'model_name': m})
    if style:
        txt = style['content'][0]['text']
        print("--- STYLING ---")
        print(txt[:600])
    
    tmpls = mcp_call('model_templates', {'model_name': m})
    if tmpls:
        txt = tmpls['content'][0]['text']
        print("--- TEMPLATES ---")
        print(txt[:800])
