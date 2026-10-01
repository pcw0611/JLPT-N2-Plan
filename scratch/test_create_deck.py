import json
import urllib.request

ENDPOINT = "http://127.0.0.1:3141/"

def mcp(name: str, arguments: dict = None):
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

if __name__ == '__main__':
    deck_name = "JLPT N2::오답노트 모의고사 1·2회 (실전 음원·해설 완비)"
    res = mcp('create_deck', {'deck_name': deck_name})
    print("create_deck result:", res)
