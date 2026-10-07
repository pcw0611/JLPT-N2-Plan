# -*- coding: utf-8 -*-
"""Generate and add 60 exception verb cards to Anki using single add_note calls."""
import os, sys, json, time, urllib.request

sys.path.insert(0, os.path.abspath('.'))
from scratch.build_exception_verbs_master import CSS_BLOCK, EXCEPTION_VERBS

sys.stdout.reconfigure(encoding='utf-8')

ENDPOINT = "http://127.0.0.1:3141/"
DECK_NAME = "JLPT N2::예외 1그룹 동사"
MODEL_NAME = "Basic"

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

def build_card_pair(v, idx):
    cards = []
    
    # Card A: 그룹 판별 및 기본 활용 (ます/ない/て/た)
    front_a = f"""{CSS_BLOCK}
<div class="vt-wrap">
  <div class="vt-center">
    <div class="vt-badge vt-badge-grp">예외 1그룹 동사 마스터 #{idx:02d}-A</div>
    <div class="vt-title">{v['kanji']}（{v['reading']}）</div>
    <div class="vt-sub">이 동사는 몇 그룹 동사인가? (ます형 / ない형 / て형은?)</div>
  </div>
</div>"""

    back_a = f"""{CSS_BLOCK}
<div class="vt-wrap">
  <div class="vt-ans-head">1그룹 동사 (예외 5단 활용!)</div>
  <div class="vt-sec">
    <div class="vt-meaning">＝ {v['meaning']}</div>
    <div style="font-size:13.5px; color:#475569; margin-top:2px; font-weight:600;">{v['category']}</div>
    <div class="vt-ex-ja"><span class="vt-tag">예문:</span> {v['ex_ja']}</div>
    <div class="vt-ex-ko">{v['ex_ko']}</div>
  </div>

  <div class="vt-sec-contrast">
    <div style="font-size:12px; font-weight:700; color:#b45309; margin-bottom:2px;">⚠️ 혼동 방지 & 시험 포인트</div>
    <div style="font-size:13.5px; color:#92400e; line-height:1.5;">{v['contrast']}</div>
  </div>

  <div class="vt-rule-box">
    <div class="vt-rule-title">📌 3대 기본 활용형 (1그룹 어미 변화)</div>
    <div class="vt-grid">
      <div class="vt-grid-item"><b>ます형:</b> {v['masu']}</div>
      <div class="vt-grid-item"><b>ない형:</b> {v['nai']}</div>
      <div class="vt-grid-item"><b>て형:</b> {v['te']}</div>
      <div class="vt-grid-item"><b>た형:</b> {v['ta']}</div>
    </div>
  </div>
</div>"""

    cards.append({
        "fields": {"Front": front_a, "Back": back_a},
        "tags": ["JLPT_N2", "동사활용", "1그룹예외", "그룹판별", f"단어_{v['kanji']}"]
    })

    # Card B: 심화 파생형 (가능형 / 가정형 / 사역형 / 수동형)
    front_b = f"""{CSS_BLOCK}
<div class="vt-wrap">
  <div class="vt-center">
    <div class="vt-badge vt-badge-irreg">예외 1그룹 동사 활용 완성 #{idx:02d}-B</div>
    <div class="vt-title">{v['kanji']}（{v['reading']}）</div>
    <div class="vt-sub">「{v['meaning']}」의 <b>가능형 / 가정형(ば) / 사역형 / 수동형</b>은?</div>
  </div>
</div>"""

    back_b = f"""{CSS_BLOCK}
<div class="vt-wrap">
  <div class="vt-ans-head" style="color:#1d4ed8; background:#eff6ff; border-color:#bfdbfe;">{v['kanji']}（{v['reading']}） 1그룹 파생 활용</div>
  
  <div class="vt-sec">
    <div class="vt-meaning">＝ {v['meaning']}</div>
    <div style="font-size:13px; color:#475569;">1그룹(5단) 규칙: 어미 る가 あ/い/う/え/お 각 단으로 전개!</div>
  </div>

  <div class="vt-rule-box">
    <div class="vt-rule-title">🎯 4대 핵심 문법 파생형</div>
    <div class="vt-grid">
      <div class="vt-grid-item"><b>가능형:</b> <span style="color:#059669; font-weight:700;">{v['kanou']}</span></div>
      <div class="vt-grid-item"><b>가정(ば)형:</b> <span style="color:#2563eb; font-weight:700;">{v['ba']}</span></div>
      <div class="vt-grid-item"><b>사역형:</b> <span style="color:#d97706; font-weight:700;">{v['shieki']}</span></div>
      <div class="vt-grid-item"><b>수동형:</b> <span style="color:#dc2626; font-weight:700;">{v['ukemi']}</span></div>
    </div>
  </div>

  <div class="vt-sec-contrast" style="margin-top:10px;">
    <div style="font-size:12px; font-weight:700; color:#b45309; margin-bottom:2px;">💡 2그룹 오답 함정 비교</div>
    <div style="font-size:13px; color:#92400e; line-height:1.5;">
      • 2그룹식 가능형(× {v['kanji']}られる)이 아니라 1그룹 가능형 <b>{v['kanou']}</b><br>
      • 2그룹식 사역형(× {v['kanji']}させる)이 아니라 1그룹 사역형 <b>{v['shieki']}</b>
    </div>
  </div>
</div>"""

    cards.append({
        "fields": {"Front": front_b, "Back": back_b},
        "tags": ["JLPT_N2", "동사활용", "1그룹예외", "심화활용", f"단어_{v['kanji']}"]
    })

    return cards

def main():
    print("="*65)
    print(">>> 1. Creating/Verifying Deck: " + DECK_NAME)
    print("="*65)
    deck_res = mcp_call('create_deck', {'deck_name': DECK_NAME})
    print("Deck status:", deck_res.get('structuredContent', {}).get('message', 'OK'))

    all_notes = []
    for i, v in enumerate(EXCEPTION_VERBS):
        pair = build_card_pair(v, i + 1)
        all_notes.extend(pair)

    print(f"\n>>> 2. Total generated notes: {len(all_notes)} (30 verbs x 2 cards = 60 cards)")

    # Save TSV backup for repository persistence
    tsv_path = "scratch/anki_exception_verbs_60.tsv"
    with open(tsv_path, "w", encoding="utf-8") as out:
        for n in all_notes:
            f_clean = n['fields']['Front'].replace('"', '""')
            b_clean = n['fields']['Back'].replace('"', '""')
            tags_str = " ".join(n['tags'])
            out.write(f'"{f_clean}"\t"{b_clean}"\t{tags_str}\n')
    print(f"Saved local TSV backup: {tsv_path}")

    # Add each note via single add_note
    print(f"\n>>> 3. Adding {len(all_notes)} notes to Anki via add_note...")
    added_count = 0
    fail_count = 0
    for idx, n in enumerate(all_notes):
        payload = {
            "deck_name": DECK_NAME,
            "model_name": MODEL_NAME,
            "fields": n['fields'],
            "tags": n['tags'],
            "allow_duplicate": True
        }
        res = mcp_call('add_note', payload)
        if res and not res.get('isError'):
            nid = res.get('structuredContent', {}).get('note_id')
            added_count += 1
            if (idx + 1) % 10 == 0 or idx == len(all_notes) - 1:
                print(f"  [{idx+1:2d}/{len(all_notes)}] Added note {nid}...")
        else:
            print(f"  [{idx+1:2d}/{len(all_notes)}] FAILED:", res)
            fail_count += 1
        time.sleep(0.05)

    print(f"\nCompleted: {added_count} added, {fail_count} failed")

    # AnkiWeb Sync
    print("\n>>> 4. Triggering AnkiWeb sync...")
    sync_res = mcp_call('sync')
    job_id = sync_res.get('structuredContent', {}).get('job_id') if sync_res else None
    if job_id:
        for _ in range(15):
            time.sleep(2)
            poll = mcp_call('sync', {'job_id': job_id})
            st = poll.get('structuredContent', {}).get('status')
            print(f"  Sync status: {st}")
            if st in ['success', 'error', 'conflict', 'cancelled']:
                break

    print("\n" + "="*65)
    print(">>> All 60 Exception Group 1 Verb Cards Created & Synced to Anki! <<<")
    print("="*65)

if __name__ == '__main__':
    main()
