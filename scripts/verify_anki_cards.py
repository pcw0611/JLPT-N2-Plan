import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
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
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith("data: "):
            res = json.loads(line[6:])
            return res.get('result')
    return None

def verify():
    # 1. Find notes in the new deck
    query = '"deck:JLPT N2::오답노트 모의고사 1·2회 (실전 음원·해설 완비)"'
    res = mcp('find_notes', {'query': query})
    structured = res.get('structuredContent', {})
    note_ids = structured.get('noteIds', [])
    print(f"Total notes found in deck: {len(note_ids)}")
    assert len(note_ids) == 87, f"Expected 87 notes, but found {len(note_ids)}"

    # 2. Get info on notes
    info_res = mcp('notes_info', {'notes': note_ids[:10]})
    notes_info = info_res.get('structuredContent', {}).get('notes', [])
    print(f"Inspected first {len(notes_info)} notes successfully.")

    # 3. Check audio tags
    all_info_res = mcp('notes_info', {'notes': note_ids})
    all_notes = all_info_res.get('structuredContent', {}).get('notes', [])
    audio_notes = [n for n in all_notes if '[sound:vol2_' in n.get('fields', {}).get('Front', {}).get('value', '')]
    print(f"Notes with official audio clips: {len(audio_notes)} (Expected 8)")
    assert len(audio_notes) == 8, f"Expected 8 audio notes, got {len(audio_notes)}"

    # 4. Check domain distribution
    domains = {'문자어휘': 0, '문법': 0, '독해': 0, '청해': 0}
    exams = {'1회_공식제2집': 0, '2회_202312': 0}
    for n in all_notes:
        tags = n.get('tags', [])
        for d in domains:
            if d in tags:
                domains[d] += 1
        for e in exams:
            if e in tags:
                exams[e] += 1

    print("Domain distribution:", domains)
    print("Exam distribution:", exams)
    assert exams['1회_공식제2집'] == 36, f"Expected 36, got {exams['1회_공식제2집']}"
    assert exams['2회_202312'] == 51, f"Expected 51, got {exams['2회_202312']}"

    # 5. Check TSV file
    with open('anki_error_notes_exams_1_2.tsv', 'r', encoding='utf-8') as f:
        tsv_lines = f.readlines()
    print(f"TSV backup card count: {len(tsv_lines)}")
    assert len(tsv_lines) == 87, f"Expected 87 TSV rows, got {len(tsv_lines)}"

    print("\n>>> ALL VERIFICATION CHECKS PASSED PERFECTLY (100% MATCH)! <<<")

if __name__ == '__main__':
    verify()
