import os
import sys
import json
import re
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

ENDPOINT = "http://127.0.0.1:3141/"
MEDIA_DIR = os.path.join(os.environ['APPDATA'], 'Anki2', '사용자 1', 'collection.media')

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

def verify_all():
    deck_read = "JLPT N2::오답노트 (언어지식·독해 62문항)"
    res_read = mcp_call('find_notes', {'query': f'deck:"{deck_read}"'})
    read_ids = res_read.get('structuredContent', {}).get('noteIds', [])
    print(f"Total notes in '{deck_read}': {len(read_ids)}")

    deck_name = "JLPT N2::오답노트 (청해 25문항 · 실전 음원)"
    res = mcp_call('find_notes', {'query': f'deck:"{deck_name}"'})
    note_ids = res.get('structuredContent', {}).get('noteIds', [])
    print(f"Total notes found in deck '{deck_name}': {len(note_ids)}")
    assert len(note_ids) == 25, f"Expected 25 notes, found {len(note_ids)}"

    info_res = mcp_call('notes_info', {'notes': note_ids})
    notes = info_res.get('structuredContent', {}).get('notes', [])

    print("\n" + "="*80)
    print("VERIFYING ALL 25 LISTENING NOTES IN ANKI")
    print("="*80)

    for i, n in enumerate(sorted(notes, key=lambda x: (x.get('tags', []), x['noteId'])), 1):
        nid = n['noteId']
        tags = n.get('tags', [])
        front = n['fields']['Front']['value']
        back = n['fields']['Back']['value']

        sound_match = re.search(r'\[sound:([^\]]+)\]', front)
        sound_fn = sound_match.group(1) if sound_match else None

        media_path = os.path.join(MEDIA_DIR, sound_fn) if sound_fn else None
        media_exists = os.path.exists(media_path) if media_path else False
        media_size = os.path.getsize(media_path) if media_exists else 0

        # Check script in back
        has_script = '問題本文' in back or 'スクリプト' in back
        has_choices = '選択肢' in back or '①' in back or '1.' in back or '1번' in back
        has_answer = '정답' in back or '正解' in back

        print(f"[{i:02d}/25] Note ID: {nid} | Tags: {tags}")
        print(f"       Sound: {sound_fn} (Exists in collection.media: {media_exists}, Size: {media_size:,} bytes)")
        print(f"       Back has Script: {has_script} | Choices: {has_choices} | Answer: {has_answer}")

        if not media_exists or media_size < 1000:
            print(f"       [ERROR] Audio file missing or empty: {sound_fn}")

    # Detailed inspection of Q80
    q80_note = [n for n in notes if 'Q80' in n.get('tags', []) and '1회_공식제2집' in n.get('tags', [])]
    if q80_note:
        n = q80_note[0]
        print("\n" + "="*80)
        print("DETAILED VERIFICATION FOR EXAM 1 Q80 (USER'S SCREENSHOT)")
        print("="*80)
        print(f"Note ID: {n['noteId']}")
        st_matches = re.findall(r'\[sound:[^\]]+\]', n['fields']['Front']['value'])
        print(f"Front Sound Tag: {st_matches}")
        print("\n--- FRONT TEXT (Question / Choices if any) ---")
        clean_front = re.sub(r'<[^>]+>', ' ', n['fields']['Front']['value'])
        clean_front = ' '.join(clean_front.split())
        print(clean_front[:300])

        print("\n--- BACK TEXT (Script / Dialogue / Answer) ---")
        clean_back = re.sub(r'<[^>]+>', '\n', n['fields']['Back']['value'])
        lines = [line.strip() for line in clean_back.splitlines() if line.strip()]
        for l in lines[:15]:
            print("  ", l)

if __name__ == '__main__':
    verify_all()
