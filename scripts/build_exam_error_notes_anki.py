import os
import sys
import json
import re
import sqlite3
import urllib.request

ENDPOINT = "http://127.0.0.1:3141/"
DECK_NAME = "JLPT N2::오답노트 모의고사 1·2회 (실전 음원·해설 완비)"
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

def parse_error_note_markdown():
    with open('JLPT_ERROR_NOTE.md', 'r', encoding='utf-8') as f:
        text = f.read()

    entries = re.split(r'### \[(2026-09-\d+)\] Q(\d+)', text)
    items_map = {}
    for i in range(1, len(entries), 3):
        date = entries[i]
        qid = int(entries[i+1])
        content = entries[i+2]
        items_map[(date, qid)] = content

    parsed_map = {}
    for (date, qid), content in items_map.items():
        m_cat = re.search(r'\*\*카테고리:\s*([^\n]+)\*\*', content)
        cat = m_cat.group(1).strip() if m_cat else ''

        def get_field(pat):
            m = re.search(pat, content, re.DOTALL)
            return m.group(1).strip() if m else ''

        parsed_map[(date, qid)] = {
            'category': cat,
            'prompt_raw': get_field(r'1\.\s*\*\*문제 원문\*\*:\s*\n?(.*?)(?=2\.|\Z)'),
            'translation': get_field(r'2\.\s*\*\*자연스러운 번역\*\*:\s*(.*?)(?=3\.|\Z)'),
            'answer_line': get_field(r'3\.\s*\*\*선택 답 ➔ 공식 정답\*\*:\s*(.*?)(?=4\.|\Z)'),
            'connection_meaning': get_field(r'4\.\s*\*\*접속·핵심 의미\*\*:\s*(.*?)(?=5\.|\Z)'),
            'trap': get_field(r'5\.\s*\*\*사용자 상태 및 함정 분석\*\*:\s*(.*?)(?=6\.|\Z)'),
            'contrast': get_field(r'6\.\s*\*\*유사 문형 및 표현 비교\*\*:\s*(.*?)(?=7\.|\Z)'),
            'example': get_field(r'7\.\s*\*\*추가 예문\*\*:\s*(.*?)(?=8\.|\Z)'),
            'next_review': get_field(r'8\.\s*\*\*다음 복습일\*\*:\s*(.*?)(?=9\.|\Z)'),
            'procedure': get_field(r'9\.\s*\*\*다음번 풀이 절차\*\*:\s*(.*?)(?=10\.|\Z)'),
            'check': get_field(r'10\.\s*\*\*제출 직전 체크\*\*:\s*(.*?)(?=\n---|<!--|\Z)'),
        }
    return parsed_map

def load_exam1_items(error_note_data):
    with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', html, re.DOTALL)
    raw_questions = json.loads(m.group(1))
    q_map = {q['id']: q for q in raw_questions}

    conn = sqlite3.connect('database/jlpt_learning.db')
    conn.row_factory = sqlite3.Row
    attempts = conn.execute("""
        SELECT item_no, selected_text, correct_text, response_seconds
        FROM question_attempts
        WHERE test_id = 'official-vol2-full-mock-20260920' AND response_state = 'wrong'
        ORDER BY item_no
    """).fetchall()

    items = []
    audio_clips_set = {76, 80, 90, 94, 97, 99, 102, 106}

    for att in attempts:
        qid = att['item_no']
        q = q_map.get(qid, {})
        en = error_note_data.get(('2026-09-20', qid), {})

        items.append({
            'exam_title': '제1회 실전 모의고사 (공식 제2집)',
            'exam_tag': '1회_공식제2집',
            'id': qid,
            'domain': '청해' if qid >= 76 else ('독해' if qid >= 55 else ('문법' if qid >= 33 else '문자어휘')),
            'problemNo': q.get('problemNo', ''),
            'subtype': q.get('subtype', ''),
            'category': en.get('category') or q.get('category', ''),
            'instruction': q.get('instruction', ''),
            'prompt': q.get('prompt', ''),
            'choices': q.get('choices', []),
            'answer_idx': q.get('answer', 0),
            'correct_text': att['correct_text'],
            'user_selected': att['selected_text'],
            'dwell_sec': att['response_seconds'],
            'translation': en.get('translation') or q.get('translation', ''),
            'connection_meaning': en.get('connection_meaning') or f"{q.get('connection', '')} — {q.get('meaning', '')}",
            'trap': en.get('trap') or q.get('trap', ''),
            'contrast': en.get('contrast') or q.get('contrast', ''),
            'example': en.get('example') or q.get('example', ''),
            'check': en.get('check') or '표기/접속/기능어 형태의 미세한 차이를 확인했는가?',
            'procedure': en.get('procedure') or '문맥 키워드 포착 ➔ 핵심 조건 대조 ➔ 오답 소거 ➔ 정답 확정',
            'audio_clip': f"vol2_q{qid}.mp3" if qid in audio_clips_set else None
        })
    return items

def load_exam2_items(error_note_data):
    with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
        ref_data = json.load(f)
    ref_map = {q['id']: q for q in ref_data['questions']}

    with open('scratch/raw_submission.json', 'r', encoding='utf-8') as f:
        sub = json.load(f)

    records = [r for r in sub['questionsRecord'] if not r['isCorrect']]

    items = []
    for r in records:
        qid = r['id']
        ref = ref_map.get(qid, {})
        user_ans = r['userAnswer']
        off_ans = r['officialAnswer']
        dwell = r.get('dwellTimeSeconds', 0)
        choices = ref.get('choices', [])

        user_text = choices[user_ans] if (user_ans is not None and user_ans < len(choices)) else str(user_ans)
        off_text = choices[off_ans] if (off_ans is not None and off_ans < len(choices)) else str(off_ans)
        en = error_note_data.get(('2026-09-30', qid), {})

        items.append({
            'exam_title': '제2회 실전 모의고사 (2023.12 기출)',
            'exam_tag': '2회_202312',
            'id': qid,
            'domain': '청해' if qid >= 73 else ('독해' if qid >= 52 else ('문법' if qid >= 31 else '문자어휘')),
            'problemNo': ref.get('problemNo', r.get('problemNo', '')),
            'subtype': ref.get('subtype', ''),
            'category': en.get('category') or ref.get('category', ''),
            'instruction': ref.get('instruction', ''),
            'prompt': ref.get('prompt', ''),
            'choices': choices,
            'answer_idx': off_ans,
            'correct_text': off_text,
            'user_selected': user_text,
            'dwell_sec': dwell,
            'translation': en.get('translation') or ref.get('translation', ''),
            'connection_meaning': en.get('connection_meaning') or f"{ref.get('connection', '')} — {ref.get('meaning', '')}",
            'trap': en.get('trap') or ref.get('trap', ''),
            'contrast': en.get('contrast') or ref.get('contrast', ''),
            'example': en.get('example') or ref.get('example', ''),
            'check': en.get('check') or '표기/접속/기능어 형태의 미세한 차이를 확인했는가?',
            'procedure': en.get('procedure') or '문맥 키워드 포착 ➔ 핵심 조건 대조 ➔ 오답 소거 ➔ 정답 확정',
            'audio_clip': None
        })
    return items

def build_card_html(item):
    qid = item['id']
    exam_tag = item['exam_title']
    problem_no = item['problemNo']
    subtype = item['subtype']
    category = item['category']
    instruction = item['instruction']
    prompt = item['prompt'].strip()
    choices = item['choices']
    user_sel = item['user_selected']
    corr_text = item['correct_text']
    dwell = item['dwell_sec']
    trans = item['translation']
    conn_mean = item['connection_meaning']
    trap = item['trap']
    contrast = item['contrast']
    example = item['example']
    check = item['check']
    audio_clip = item['audio_clip']
    domain = item['domain']

    # --- FRONT ---
    audio_html = ""
    if audio_clip:
        audio_html = f"""
        <div style="margin:12px 0 16px 0; padding:12px; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; text-align:center;">
          <div style="font-size:12px; font-weight:700; color:#166534; margin-bottom:6px;">🎧 공식 원본 시험 음원</div>
          [sound:{audio_clip}]
        </div>
        """

    choices_html = ""
    if choices:
        ch_list = []
        for i, c in enumerate(choices, 1):
            ch_list.append(f"""
            <div style="padding:10px 14px; border:1px solid #e2e8f0; border-radius:8px; font-size:16px; color:#1e293b; background:#f8fafc; line-height:1.45;">
              <b style="color:#64748b; margin-right:8px;">{i}.</b> {c}
            </div>
            """)
        choices_html = "".join(ch_list)

    inst_html = f'<div style="font-size:13px; color:#64748b; margin-bottom:12px; line-height:1.4;">{instruction}</div>' if instruction else ''

    front_html = f"""
<div style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Hiragino Sans', sans-serif; max-width:620px; margin:0 auto; padding:6px 2px;">
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:8px; margin-bottom:12px;">
    <span style="font-size:12px; font-weight:700; color:#2563eb; background:#eff6ff; padding:3px 8px; border-radius:6px;">{exam_tag} · Q{qid:02d}</span>
    <span style="font-size:12px; font-weight:600; color:#475569;">{problem_no} ({subtype})</span>
  </div>

  {inst_html}
  {audio_html}

  <div style="font-size:20px; font-weight:700; color:#0f172a; line-height:1.6; margin-bottom:16px; word-break:keep-all;">
    {prompt}
  </div>

  <div style="display:flex; flex-direction:column; gap:8px;">
    {choices_html}
  </div>
</div>
"""

    # --- BACK ---
    ans_num_str = f"{item['answer_idx'] + 1}番: " if isinstance(item['answer_idx'], int) and item['answer_idx'] >= 0 else ""
    correct_display = f"{ans_num_str}{corr_text}"

    contrast_html = ""
    if contrast:
        contrast_html = f"""
        <div style="margin-top:10px; padding-top:10px; border-top:1px dashed #e2e8f0; font-size:13px; line-height:1.5;">
          <b style="color:#0891b2;">🔍 유사 문형·표현 비교:</b><br>{contrast}
        </div>
        """

    example_html = ""
    if example:
        example_html = f"""
        <div style="border:1px solid #e2e8f0; border-radius:8px; padding:12px 14px; margin-bottom:12px; background:#fafafa;">
          <div style="font-size:12px; font-weight:700; color:#475569; margin-bottom:4px;">📖 추가 예문 (실전 훈련)</div>
          <div style="font-size:17px; line-height:1.6; color:#0f172a;">{example}</div>
        </div>
        """

    category_html = f'<div style="font-size:11px; color:#64748b; margin-top:2px;">분류: {category}</div>' if category else ''

    back_html = f"""
<div style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Hiragino Sans', sans-serif; max-width:620px; margin:0 auto; padding:6px 2px;">
  
  <!-- Header -->
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:8px; margin-bottom:12px;">
    <span style="font-size:12px; font-weight:700; color:#16a34a; background:#f0fdf4; padding:3px 8px; border-radius:6px;">공식 정답 및 해설</span>
    <span style="font-size:12px; font-weight:600; color:#475569;">{exam_tag} · Q{qid:02d}</span>
  </div>

  <!-- Correct Answer Banner -->
  <div style="background:#f0fdf4; border-left:4px solid #16a34a; padding:12px 14px; border-radius:0 8px 8px 0; margin-bottom:12px;">
    <div style="font-size:11px; font-weight:700; color:#166534; text-transform:uppercase;">공식 정답</div>
    <div style="font-size:22px; font-weight:800; color:#14532d; margin:4px 0 6px;">{correct_display}</div>
    <div style="font-size:14px; color:#334155; line-height:1.5;">{trans}</div>
    {category_html}
  </div>

  <!-- User Mistake & Trap Analysis Box -->
  <div style="background:#fff1f2; border:1px solid #fecdd3; border-radius:8px; padding:12px 14px; margin-bottom:12px;">
    <div style="font-size:13px; font-weight:700; color:#9f1239; margin-bottom:6px;">
      ❌ 내 선택: <span style="font-weight:800; color:#be123c;">{user_sel}</span>
      <span style="font-size:11px; font-weight:500; color:#881337; margin-left:6px;">(풀이 체류: {dwell}초)</span>
    </div>
    <div style="font-size:13px; color:#9f1239; line-height:1.5;">
      <b>⚠️ 함정 분석:</b> {trap}
    </div>
  </div>

  <!-- Connection & Meaning Box -->
  <div style="border:1px solid #e2e8f0; border-radius:8px; padding:12px 14px; margin-bottom:12px; background:#ffffff;">
    <div style="font-size:13px; color:#1e293b; line-height:1.55;">
      <b style="color:#2563eb;">📌 접속·핵심 의미:</b><br>{conn_mean}
    </div>
    {contrast_html}
  </div>

  <!-- Example Box -->
  {example_html}

  <!-- Exam Signal & Pre-submission Check -->
  <div style="background:#eff6ff; border-left:4px solid #2563eb; padding:10px 14px; border-radius:0 8px 8px 0; font-size:13px; color:#1e40af; line-height:1.5;">
    <b>💡 직전 체크 & 시험 신호:</b><br>{check}
  </div>

</div>
"""
    return front_html.strip(), back_html.strip()

def build_all_cards():
    print("[1/5] Loading and parsing JLPT_ERROR_NOTE.md...")
    en_data = parse_error_note_markdown()
    print(f"      Parsed {len(en_data)} error note entries.")

    print("[2/5] Compiling Exam 1 and Exam 2 items...")
    e1_items = load_exam1_items(en_data)
    e2_items = load_exam2_items(en_data)
    all_items = e1_items + e2_items
    print(f"      Exam 1: {len(e1_items)} items")
    print(f"      Exam 2: {len(e2_items)} items")
    print(f"      Total:  {len(all_items)} items")
    assert len(all_items) == 87, f"Expected 87, got {len(all_items)}"

    print("[3/5] Ensuring deck exists in Anki...")
    mcp_call('create_deck', {'deck_name': DECK_NAME})

    print("[4/5] Adding cards to Anki...")
    added_count = 0
    tsv_rows = []

    for i, item in enumerate(all_items, 1):
        front, back = build_card_html(item)
        tags = [
            'JLPT_N2',
            '오답노트',
            item['exam_tag'],
            item['domain'],
            f"Q{item['id']:02d}"
        ]
        if item.get('audio_clip'):
            tags.append('음원포함')

        # Add note to Anki
        res = mcp_call('add_note', {
            'deck_name': DECK_NAME,
            'model_name': MODEL_NAME,
            'fields': {
                'Front': front,
                'Back': back
            },
            'tags': tags,
            'allow_duplicate': True
        })
        if res and not res.get('isError'):
            added_count += 1
            if added_count % 20 == 0 or added_count == 87:
                print(f"      Progress: {added_count}/87 cards added to Anki...")
        else:
            print(f"      [WARN] Card {i} (Q{item['id']}) error: {res}")

        # TSV row (Front \t Back \t Tags)
        clean_front = front.replace('\t', ' ').replace('\n', '<br>')
        clean_back = back.replace('\t', ' ').replace('\n', '<br>')
        clean_tags = " ".join(tags)
        tsv_rows.append(f"{clean_front}\t{clean_back}\t{clean_tags}")

    # Write TSV backup
    with open('anki_error_notes_exams_1_2.tsv', 'w', encoding='utf-8') as f:
        f.write("\n".join(tsv_rows))
    print(f"[5/5] Saved standalone backup to anki_error_notes_exams_1_2.tsv ({len(tsv_rows)} cards).")

    print(f"\n==========================================")
    print(f"★ COMPLETE: Successfully added {added_count}/87 cards to Anki deck:")
    print(f"    '{DECK_NAME}'")
    print(f"==========================================")

if __name__ == '__main__':
    build_all_cards()
