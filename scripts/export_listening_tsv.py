import os
import sys
import json
import csv
import urllib.request

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
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith("data: "):
            res = json.loads(line[6:])
            return res.get('result')
    return None

def export():
    deck_name = "JLPT N2::오답노트 (청해 25문항 · 실전 음원)"
    res = mcp_call('find_notes', {'query': f'deck:"{deck_name}"'})
    nids = res.get('structuredContent', {}).get('noteIds', [])
    info = mcp_call('notes_info', {'notes': nids})
    notes = info.get('structuredContent', {}).get('notes', [])

    out_path = os.path.abspath('scratch/anki_error_notes_listening_25.tsv')
    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        for n in sorted(notes, key=lambda x: (x.get('tags', []), x['noteId'])):
            front = n['fields']['Front']['value'].replace('\n', ' ')
            back = n['fields']['Back']['value'].replace('\n', ' ')
            tags = ' '.join(n.get('tags', []))
            writer.writerow([front, back, tags])

    print(f"Exported {len(notes)} listening notes to {out_path}")

if __name__ == '__main__':
    export()
