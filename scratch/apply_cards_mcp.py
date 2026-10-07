import os, sys, json, time, urllib.request

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


with open('scratch/final_updated_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

print(f"Loaded {len(cards)} final cards to update.")

success_count = 0
fail_count = 0

for i, c in enumerate(cards):
    nid = c['nid']
    exam = c['exam']
    qid = c['qid']
    front = c['front']
    back = c['back']
    is_audio = c['is_audio_only']
    
    print(f"[{i+1:2d}/25] Updating note {nid} ({exam} Q{qid:03d}, audio_only={is_audio})...")
    
    res = mcp_call('update_note_fields', {
        'id': nid,
        'fields': {
            'Front': front,
            'Back': back
        }
    })
    
    if res and not res.get('isError'):
        print(f"  -> SUCCESS")
        success_count += 1
    else:
        print(f"  -> FAILED: {res}")
        fail_count += 1
    time.sleep(0.1)

print("\n" + "="*60)
print(f"Update completed! Success: {success_count}, Failed: {fail_count}")
print("="*60)

# Trigger AnkiWeb sync
print("\nTriggering AnkiWeb sync...")
sync_res = mcp_call('sync')
print("Sync result:", sync_res)

job_id = None
if sync_res and sync_res.get('structuredContent'):
    job_id = sync_res.get('structuredContent', {}).get('job_id')

if job_id:
    for attempt in range(15):
        time.sleep(2)
        poll = mcp_call('sync', {'job_id': job_id})
        status = poll.get('structuredContent', {}).get('status')
        print(f"  Sync poll [{attempt+1}]: {status}")
        if status in ['success', 'error', 'conflict', 'cancelled']:
            break

print("\nAnki sync finished!")
