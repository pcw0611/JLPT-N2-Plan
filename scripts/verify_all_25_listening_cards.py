import os
import sys
import json
import re
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

ENDPOINT = "http://127.0.0.1:3141/"
DECK_LISTENING = "JLPT N2::오답노트 (청해 25문항 · 실전 음원)"

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

def verify():
    res = mcp_call('find_notes', {'query': f'deck:"{DECK_LISTENING}"'})
    note_ids = res.get('structuredContent', {}).get('noteIds', [])
    print(f"Total notes in listening deck: {len(note_ids)}")
    assert len(note_ids) == 25, f"Expected 25 notes, got {len(note_ids)}"

    info_res = mcp_call('notes_info', {'notes': note_ids})
    notes = info_res.get('structuredContent', {}).get('notes', [])

    print("\n" + "="*80)
    print(f"{'No':<3} | {'Exam':<12} | {'QID':<5} | {'Note ID':<14} | {'Script Len':<10} | {'Status'}")
    print("="*80)

    all_passed = True

    for i, n in enumerate(notes, 1):
        nid = n['noteId']
        tags = n.get('tags', [])
        front = n['fields']['Front']['value']
        back = n['fields']['Back']['value']

        exam = '1회_공식제2집' if '1회_공식제2집' in tags else '2회_202312'
        qid = [t for t in tags if t.startswith('Q')][0]

        # Checks
        has_script_box = '📜 청해 대본 (발화 스크립트 전문)' in back
        has_speaker_tags = any(s in back for s in ['男', '女', '先生', '店員', '上司', '研究者', 'アナウンサー', '中山さん', '村職員', '農園の人', '職人', '店長', '先輩', '幹事', '同僚', '取引先', '案内'])
        has_correct_banner = '공식 정답 및 대본 완비' in back and '番:' in back
        has_user_mistake = '❌ 내 선택:' in back
        has_ruby = '<ruby>' in back

        # Script length
        script_match = re.search(r'<span>📜 청해 대본 \(발화 스크립트 전문\)</span>\s*</div>\s*<div[^>]*>(.*?)</div>\s*</div>', back, re.DOTALL)
        script_text = script_match.group(1).strip() if script_match else ""
        script_len = len(re.sub(r'<[^>]+>', '', script_text))

        is_ok = has_script_box and has_speaker_tags and has_correct_banner and has_user_mistake and has_ruby and script_len > 30

        status = "✅ PASS" if is_ok else "❌ FAIL"
        if not is_ok:
            all_passed = False

        print(f"{i:<3} | {exam:<12} | {qid:<5} | {nid:<14} | {script_len:<10} | {status}")

    print("="*80)
    if all_passed:
        print(">>> ALL 25 CARDS PASSED INDEPENDENT VERIFICATION 100%! <<<")
    else:
        print(">>> SOME CARDS FAILED VERIFICATION! <<<")

if __name__ == '__main__':
    verify()
