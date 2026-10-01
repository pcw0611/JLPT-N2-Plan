import json
import urllib.request
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith("data: "):
            res = json.loads(line[6:])
            result = res.get('result', {})
            if 'structuredContent' in result:
                return result['structuredContent']
            if 'content' in result and result['content']:
                try:
                    return json.loads(result['content'][0]['text'])
                except:
                    return result['content'][0]['text']
            return result
    return None

if __name__ == '__main__':
    decks = mcp('list_decks')
    print("Decks:", decks)
    
    # Query notes in listening deck
    res = mcp('find_notes', {'query': 'deck:"JLPT N2::오답노트 (청해 25문항 · 실전 음원)"'})
    nids = res.get('notes', []) if isinstance(res, dict) else res
    print(f"Notes count in listening deck: {len(nids)}")
    
    notes_info = mcp('notes_info', {'notes': nids})
    notes_list = notes_info.get('notes', []) if isinstance(notes_info, dict) else notes_info
    
    for n in sorted(notes_list, key=lambda x: x.get('tags', [])):
        nid = n['noteId']
        tags = n.get('tags', [])
        front = n['fields']['Front']['value']
        back = n['fields']['Back']['value']
        print(f"\n==========================================")
        print(f"NOTE {nid} | Tags: {tags}")
        print("--- FRONT ---")
        print(front[:300])
        print("--- BACK ---")
        print(back[:500])
