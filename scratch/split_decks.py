import json
import urllib.request
import time

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
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith("data: "):
            res = json.loads(line[6:])
            return res.get('result')
    return None

def main():
    old_deck = "JLPT N2::오답노트 모의고사 1·2회 (실전 음원·해설 완비)"
    deck_reading = "JLPT N2::오답노트 (언어지식·독해 62문항)"
    deck_listening = "JLPT N2::오답노트 (청해 25문항 · 실전 음원)"

    print("[1] Creating new separate decks...")
    res_r = mcp('create_deck', {'deck_name': deck_reading})
    print("Created reading deck:", res_r.get('structuredContent', {}).get('deckName'))
    res_l = mcp('create_deck', {'deck_name': deck_listening})
    print("Created listening deck:", res_l.get('structuredContent', {}).get('deckName'))

    print("[2] Fetching notes from existing deck...")
    find_res = mcp('find_notes', {'query': f'deck:"{old_deck}"'})
    note_ids = find_res.get('structuredContent', {}).get('noteIds', [])
    print(f"Total notes in existing deck: {len(note_ids)}")

    if not note_ids:
        # maybe already split?
        print("Checking if notes already moved...")
        r_notes = mcp('find_notes', {'query': f'deck:"{deck_reading}"'}).get('structuredContent', {}).get('noteIds', [])
        l_notes = mcp('find_notes', {'query': f'deck:"{deck_listening}"'}).get('structuredContent', {}).get('noteIds', [])
        print(f"Reading deck: {len(r_notes)}, Listening deck: {len(l_notes)}")
        return

    info_res = mcp('notes_info', {'notes': note_ids})
    notes = info_res.get('structuredContent', {}).get('notes', [])

    reading_card_ids = []
    listening_card_ids = []

    for n in notes:
        tags = n.get('tags', [])
        cards = n.get('cards', [])
        if '청해' in tags:
            listening_card_ids.extend(cards)
        else:
            reading_card_ids.extend(cards)

    print(f"Moving {len(reading_card_ids)} cards to '{deck_reading}'...")
    if reading_card_ids:
        mcp('card_management', {
            'params': {
                'action': 'change_deck',
                'card_ids': reading_card_ids,
                'deck': deck_reading
            }
        })

    print(f"Moving {len(listening_card_ids)} cards to '{deck_listening}'...")
    if listening_card_ids:
        mcp('card_management', {
            'params': {
                'action': 'change_deck',
                'card_ids': listening_card_ids,
                'deck': deck_listening
            }
        })

    print("[3] Verifying note counts in each deck...")
    r_check = mcp('find_notes', {'query': f'deck:"{deck_reading}"'}).get('structuredContent', {}).get('noteIds', [])
    l_check = mcp('find_notes', {'query': f'deck:"{deck_listening}"'}).get('structuredContent', {}).get('noteIds', [])
    old_check = mcp('find_notes', {'query': f'deck:"{old_deck}"'}).get('structuredContent', {}).get('noteIds', [])

    print(f"  -> 언어지식·독해 덱: {len(r_check)}개 문항 (목표: 62개)")
    print(f"  -> 청해 덱:         {len(l_check)}개 문항 (목표: 25개)")
    print(f"  -> 기존 덱 잔여:    {len(old_check)}개")

    assert len(r_check) == 62, f"Expected 62, got {len(r_check)}"
    assert len(l_check) == 25, f"Expected 25, got {len(l_check)}"
    assert len(old_check) == 0, f"Expected 0, got {len(old_check)}"

    print("[4] Triggering AnkiWeb sync...")
    sync_res = mcp('sync')
    job_id = sync_res.get('structuredContent', {}).get('job_id')
    if job_id:
        for _ in range(15):
            time.sleep(2)
            poll = mcp('sync', {'job_id': job_id})
            st = poll.get('structuredContent', {}).get('status')
            if st in ['success', 'error', 'conflict', 'cancelled']:
                print("Sync finished with status:", st)
                break

    print("\n>>> ALL CHECKS PASSED: 청해 덱 완전 분리 완료! <<<")

if __name__ == '__main__':
    main()
