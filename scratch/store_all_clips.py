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

def store_all_clips():
    clips = [76, 80, 90, 94, 97, 99, 102, 106]
    for qid in clips:
        fn = f"vol2_q{qid}.mp3"
        path = os.path.abspath(f"scratch/audio_clips/{fn}")
        res = mcp('store_media_file', {'filename': fn, 'path': path})
        if res and not res.get('isError'):
            print(f"[STORED] {fn}")
        else:
            print(f"[ERROR] {fn}: {res}")

if __name__ == '__main__':
    store_all_clips()
