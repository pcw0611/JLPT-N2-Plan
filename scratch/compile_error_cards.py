import json
import re
import sqlite3

def load_exam1_data():
    with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', html, re.DOTALL)
    raw_questions = json.loads(m.group(1))
    q_map = {q['id']: q for q in raw_questions}

    with open('database/results/official-vol2-full-mock-20260920.json', 'r', encoding='utf-8') as f:
        res = json.load(f)

    conn = sqlite3.connect('database/jlpt_learning.db')
    conn.row_factory = sqlite3.Row
    attempts = conn.execute("""
        SELECT item_no, selected_text, correct_text, response_seconds
        FROM question_attempts
        WHERE test_id = 'official-vol2-full-mock-20260920' AND response_state = 'wrong'
        ORDER BY item_no
    """).fetchall()

    items = []
    for att in attempts:
        qid = att['item_no']
        q = q_map.get(qid, {})
        items.append({
            'exam': '제1회 실전 모의고사 (공식 제2집)',
            'exam_short': '제1회',
            'id': qid,
            'section': q.get('sectionName', '言語知識・読解' if qid < 76 else '聴解'),
            'problemNo': q.get('problemNo', ''),
            'subtype': q.get('subtype', ''),
            'category': q.get('category', ''),
            'instruction': q.get('instruction', ''),
            'prompt': q.get('prompt', ''),
            'choices': q.get('choices', []),
            'answer': q.get('answer', 0),
            'translation': q.get('translation', ''),
            'connection': q.get('connection', ''),
            'meaning': q.get('meaning', ''),
            'trap': q.get('trap', ''),
            'contrast': q.get('contrast', ''),
            'example': q.get('example', ''),
            'user_selected': att['selected_text'],
            'correct_text': att['correct_text'],
            'response_seconds': att['response_seconds'],
            'audio_clip': f"vol2_q{qid}.mp3" if qid in [76, 80, 90, 94, 97, 99, 102, 106] else None
        })
    return items

def load_exam2_data():
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

        items.append({
            'exam': '제2회 실전 모의고사 (2023.12 기출)',
            'exam_short': '제2회',
            'id': qid,
            'section': ref.get('sectionName', '言語知識・読解' if qid < 73 else '聴解'),
            'problemNo': ref.get('problemNo', r.get('problemNo', '')),
            'subtype': ref.get('subtype', ''),
            'category': ref.get('category', r.get('category', '')),
            'instruction': ref.get('instruction', ''),
            'prompt': ref.get('prompt', ''),
            'choices': choices,
            'answer': off_ans,
            'translation': ref.get('translation', ''),
            'connection': ref.get('connection', ''),
            'meaning': ref.get('meaning', ''),
            'trap': ref.get('trap', ''),
            'contrast': ref.get('contrast', ''),
            'example': ref.get('example', ''),
            'user_selected': user_text,
            'correct_text': off_text,
            'response_seconds': dwell,
            'audio_clip': None
        })
    return items

if __name__ == '__main__':
    e1 = load_exam1_data()
    e2 = load_exam2_data()
    print(f"Exam 1 wrong items: {len(e1)}")
    print(f"Exam 2 wrong items: {len(e2)}")
    print(f"Total: {len(e1) + len(e2)}")
    assert len(e1) == 36, f"Expected 36, got {len(e1)}"
    assert len(e2) == 51, f"Expected 51, got {len(e2)}"
    print("Verification passed! All 87 items loaded cleanly.")
