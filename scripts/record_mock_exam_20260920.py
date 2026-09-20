import sqlite3
import json
import re
from datetime import datetime

DB_PATH = 'database/jlpt_learning.db'
RESULT_PATH = 'database/results/official-vol2-full-mock-20260920.json'
HTML_PATH = 'quiz_sites/n2-midterm-mock-exam-20260920.html'

def run():
    with open(RESULT_PATH, 'r', encoding='utf-8') as f:
        result_data = json.load(f)

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);\s*\n\s*let sessionQuestions', html, re.DOTALL)
    if not m:
        # fallback match
        m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', html, re.DOTALL)
    raw_questions = json.loads(m.group(1))
    q_map = {q['id']: q for q in raw_questions}

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # 1. Register missing official item_types
    official_types = [
        ('kanji_orthography', 'vocabulary', '한자 표기', '表記', 1, 20, 35, 'N2 문자·어휘 문제2'),
        ('word_formation', 'vocabulary', '파생어·합성어', '語形成', 1, 20, 35, 'N2 문자·어휘 문제3'),
        ('context_definition', 'vocabulary', '문맥규정', '文脈規定', 1, 25, 40, 'N2 문자·어휘 문제4'),
        ('word_usage', 'vocabulary', '단어 용법', '用法', 1, 40, 70, 'N2 문자·어휘 문제6'),
        ('medium_content', 'reading', '중문 내용이해', '中文内容理解', 1, 150, 240, 'N2 독해 문제11'),
        ('integrated_comprehension', 'reading', '통합 이해', '統合理解', 1, 240, 360, 'N2 독해 문제12'),
        ('thematic_comprehension', 'reading', '장문 주장 이해', '長文主張理解', 1, 240, 360, 'N2 독해 문제13'),
        ('information_retrieval', 'reading', '정보 검색', '情報検索', 1, 120, 180, 'N2 독해 문제14'),
        ('listening_summary', 'listening', '개요이해', '概要理解', 1, 5, 20, 'N2 청해 문제3'),
        ('listening_integrated', 'listening', '통합이해', '統合理解', 1, 10, 25, 'N2 청해 문제5')
    ]
    for it in official_types:
        cur.execute('''
            INSERT OR IGNORE INTO item_types (id, domain, label_ko, label_ja, is_official_type, recommended_min_sec, recommended_max_sec, timing_note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', it)

    # Map problemNo / category to item_type_id
    def get_item_type_id(q_id, prob_no, category):
        if 1 <= q_id <= 5: return 'kanji_reading'
        if 6 <= q_id <= 10: return 'kanji_orthography'
        if 11 <= q_id <= 15: return 'word_formation'
        if 16 <= q_id <= 22: return 'context_definition'
        if 23 <= q_id <= 27: return 'paraphrase'
        if 28 <= q_id <= 32: return 'word_usage'
        if 33 <= q_id <= 44: return 'grammar_form'
        if 45 <= q_id <= 49: return 'sentence_composition'
        if 50 <= q_id <= 54: return 'text_grammar'
        if 55 <= q_id <= 59: return 'short_content'
        if 60 <= q_id <= 68: return 'medium_content'
        if 69 <= q_id <= 70: return 'integrated_comprehension'
        if 71 <= q_id <= 73: return 'thematic_comprehension'
        if 74 <= q_id <= 75: return 'information_retrieval'
        if 76 <= q_id <= 80: return 'listening_task'
        if 81 <= q_id <= 86: return 'listening_point'
        if 87 <= q_id <= 91: return 'listening_summary'
        if 92 <= q_id <= 103: return 'listening_quick_response'
        if 104 <= q_id <= 107: return 'listening_integrated'
        return 'grammar_form'

    test_id = 'official-vol2-full-mock-20260920'
    cur.execute('DELETE FROM tests WHERE id=?', (test_id,))
    cur.execute('DELETE FROM question_attempts WHERE test_id=?', (test_id,))

    notes_dict = {
        'source': '日本語能力試験 公式問題集 第2集 (2018) 原本対照 · 個人学習用 実戦模試 (ブラウザTTS聴解演習)',
        'provenance': result_data.get('provenanceNote'),
        'total_score_scaled': result_data.get('scoreScaledEstimate'),
        'accuracy_percent': result_data.get('accuracyPercent'),
        'sections': result_data.get('sections'),
        'has_sectional_cutoff_risk': result_data.get('hasSectionalCutoffRisk'),
        'section1_elapsed_seconds': 5263, # 87m 43s (어휘 18m18s + 문법 21m56s + 독해 47m29s = 5263s)
        'section2_elapsed_seconds': 1768, # 29m 28s (청해)
        'wrong_items': [q['id'] for q in result_data['questionsRecord'] if not q['isCorrect']],
        'unknown_items': [],
        'unanswered_items': []
    }

    cur.execute('''
        INSERT INTO tests (
            id, test_date, title, source_class, target_level, difficulty_label,
            memory_timing, response_format, total_items, correct_items, unknown_items,
            unanswered_items, elapsed_seconds, time_limit_seconds, diagnostic_weight, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        test_id,
        '2026-09-20',
        'JLPT N2 공식 문제집 제2집 전 영역 완본 실전모의고사 (107문항)',
        'official_mock',
        'N2',
        'official_standard',
        'full_mock_real',
        'multiple_choice_4',
        result_data['totalQuestions'],
        result_data['correctCount'],
        result_data['unknownCount'],
        result_data['unansweredCount'],
        result_data['elapsedSeconds'],
        9300, # 155 minutes standard
        1.0,
        json.dumps(notes_dict, ensure_ascii=False)
    ))

    # Insert question attempts and collect wrong attempt IDs
    wrong_attempt_records = []
    for q_rec in result_data['questionsRecord']:
        qid = q_rec['id']
        raw_q = q_map.get(qid, {})
        choices = raw_q.get('choices', [])
        ans_idx = q_rec['officialAnswer']
        user_idx = q_rec['userAnswer']
        
        user_text = choices[user_idx] if (user_idx is not None and user_idx < len(choices)) else str(user_idx)
        correct_text = choices[ans_idx] if (ans_idx is not None and ans_idx < len(choices)) else str(ans_idx)
        
        state = 'correct' if q_rec['isCorrect'] else 'wrong'
        dwell = q_rec.get('dwellTimeSeconds', 0)
        item_type = get_item_type_id(qid, q_rec.get('problemNo'), q_rec.get('category'))
        
        trap_info = raw_q.get('trap', '')

        cur.execute('''
            INSERT INTO question_attempts (
                test_id, item_no, item_type_id, level_label, response_state,
                response_seconds, audio_seconds, decision_seconds, play_count,
                selected_text, correct_text, trap_hypothesis, trap_confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            test_id,
            qid,
            item_type,
            'N2',
            state,
            dwell,
            None,
            None,
            1 if item_type.startswith('listening') else None,
            user_text,
            correct_text,
            trap_info,
            'high'
        ))
        attempt_id = cur.lastrowid
        if state == 'wrong':
            wrong_attempt_records.append((attempt_id, qid, raw_q, q_rec))

    # Insert review queue for wrong attempts: D+1 (2026-09-21), D+3 (2026-09-23), D+7 (2026-09-27)
    for att_id, qid, raw_q, q_rec in wrong_attempt_records:
        for interval, r_date in [('D+1', '2026-09-21'), ('D+3', '2026-09-23'), ('D+7', '2026-09-27')]:
            cur.execute('''
                INSERT INTO review_queue (attempt_id, review_date, interval_label, status)
                VALUES (?, ?, ?, 'pending')
            ''', (att_id, r_date, interval))

    # Study session upsert
    session_summary = (
        f"[2026-09-20] 총 순수 시험시간 115분 36초 (6,936초 / 115.6분). "
        f"★JLPT N2 공식 문제집 제2집 전 영역 완본 실전모의고사 (107문항) 완주★: "
        f"1) 종합 점수: 119/180점 (정답률 66.4%, 71/107). "
        f"2) 영역별: 언어지식 31/54 (문자·어휘 21/32 66%, 문법 10/22 45%), 독해 16/21 (76%), 청해 24/32 (75%). "
        f"3) 과락(19점) 위험 전 영역 0건(안전 통과). "
        f"4) 지구력 분석: 1교시 62.7% 대비 2교시 청해 75.0%(+12.3%p)로 후반부 고집중 완주. 잔여 36초 보존."
    )
    cur.execute('SELECT id, verified_minutes FROM study_sessions WHERE session_date="2026-09-20"')
    existing_sess = cur.fetchone()
    if existing_sess:
        cur.execute('''
            UPDATE study_sessions
            SET verified_minutes = ?, summary = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (115, session_summary, existing_sess[0]))
    else:
        cur.execute('''
            INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
            VALUES ('2026-09-20', 115, 0, ?)
        ''', (session_summary,))

    # Pass probability snapshot insert
    reason_text = (
        "[2026-09-20 공식 모의고사 완주 반영] 공식 문제집 제2집 107문항 전 영역 실전모의고사(155분 규격) 완주 및 119/180점(정답률 66.4%, 71/107) 달성. "
        "1) 영역별: 언어지식 31/54(57.4%), 독해 16/21(76.2%), 청해 24/32(75.0%)로 독해·청해에서 N2 고득점권 실력 실증. "
        "2) 전 영역 과락 기준점(19점) 위험 0건(안전 통과). "
        "3) 1교시(62.7%) 대비 2교시 청해(75.0%, +12.3%p)로 후반부 실전 멘탈 지구력 검증. "
        "공식 종합 시험 첫 완주 실측치이므로 신뢰도를 low에서 medium으로 상향하고, 현재 응시 가능 범위를 45~60%(중간값 약 52.5%), 12월 시험일 예상 전망을 75%로 대폭 상향 조정."
    )
    cur.execute('''
        INSERT INTO pass_probability_snapshots (
            snapshot_date, level, current_low_pct, current_high_pct, projected_exam_pct, daily_change_pp, confidence, reason
        ) VALUES ('2026-09-20', 'N2', 45.0, 60.0, 75.0, 25.0, 'medium', ?)
    ''', (reason_text,))

    con.commit()
    con.close()
    print(f"Successfully recorded mock exam! Wrong items: {len(wrong_attempt_records)}, Review items inserted: {len(wrong_attempt_records)*3}")

if __name__ == '__main__':
    run()
