import os
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
    abs_path = os.path.abspath('scratch/audio_clips/vol2_q94.mp3')
    print("Testing store_media_file for:", abs_path)
    res = mcp('store_media_file', {'filename': 'vol2_q94.mp3', 'path': abs_path})
    print("store_media_file result:", res)
