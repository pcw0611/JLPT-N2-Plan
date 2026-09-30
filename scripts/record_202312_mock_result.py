import sqlite3
import json
from datetime import datetime, timedelta

def record_result():
    conn = sqlite3.connect('database/jlpt_learning.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Load raw submission
    with open('scratch/raw_submission.json', 'r', encoding='utf-8') as f:
        sub = json.load(f)

    test_id = 'official-past-202312-full-mock-20260930'
    test_date = '2026-09-30'

    # Check if test already exists
    cur.execute("SELECT id FROM tests WHERE id = ?", (test_id,))
    if cur.fetchone():
        print(f"Test {test_id} already exists, deleting prior attempts and reviews to update cleanly...")
        cur.execute("DELETE FROM review_queue WHERE attempt_id IN (SELECT id FROM question_attempts WHERE test_id = ?)", (test_id,))
        cur.execute("DELETE FROM question_attempts WHERE test_id = ?", (test_id,))
        cur.execute("DELETE FROM tests WHERE id = ?", (test_id,))

    # Map item types
    def get_item_type(item_no):
        if 1 <= item_no <= 5: return 'kanji_reading'
        if 6 <= item_no <= 10: return 'kanji_orthography'
        if 11 <= item_no <= 13: return 'word_formation'
        if 14 <= item_no <= 20: return 'context_definition'
        if 21 <= item_no <= 25: return 'paraphrase'
        if 26 <= item_no <= 30: return 'word_usage'
        if 31 <= item_no <= 42: return 'grammar_form'
        if 43 <= item_no <= 47: return 'sentence_composition'
        if 48 <= item_no <= 51: return 'text_grammar'
        if 52 <= item_no <= 56: return 'short_content'
        if 57 <= item_no <= 65: return 'medium_content'
        if 66 <= item_no <= 67: return 'integrated_comprehension'
        if 68 <= item_no <= 70: return 'thematic_comprehension'
        if 71 <= item_no <= 72: return 'information_retrieval'
        if 73 <= item_no <= 77: return 'listening_task'
        if 78 <= item_no <= 83: return 'listening_point'
        if 84 <= item_no <= 88: return 'listening_summary'
        if 89 <= item_no <= 99: return 'listening_quick_response'
        if 100 <= item_no <= 102: return 'listening_integrated'
        return 'unknown'

    # Load 2023_12.json to get choice texts
    with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
        ref_data = json.load(f)
    ref_questions = {q['id']: q for q in ref_data['questions']}

    records = sub['questionsRecord']

    # Section counts
    vocab_items = records[:30]
    grammar_items = records[30:51]
    reading_items = records[51:72]
    listening_items = records[72:]

    v_c = sum(1 for q in vocab_items if q['isCorrect'])
    g_c = sum(1 for q in grammar_items if q['isCorrect'])
    r_c = sum(1 for q in reading_items if q['isCorrect'])
    l_c = sum(1 for q in listening_items if q['isCorrect'])

    lang_scaled = round(((v_c + g_c) / 51) * 60) # 29
    reading_scaled = round((r_c / 21) * 60) # 37
    listening_scaled = round((l_c / 30) * 60) # 26
    total_scaled = lang_scaled + reading_scaled + listening_scaled # 92

    wrong_item_nos = [q['id'] for q in records if not q['isCorrect']]

    notes_dict = {
        "source": "2023年 第2回 (12月) JLPT N2 本試験 原本対照 全領域 実戦模試",
        "provenance": "출제 원안: 2023年 第2回 (12月) JLPT N2 本試験 원문 대조 / 실제 본시험 전문 성우 원음(영상 숨김 순수 청해) / 공식 정답 일치",
        "total_score_scaled": total_scaled,
        "accuracy_percent": round((len(records) - len(wrong_item_nos)) / len(records) * 100, 1),
        "sections": {
            "vocab": {"total": 30, "correct": v_c, "pct": round(v_c/30*100, 1)},
            "grammar": {"total": 21, "correct": g_c, "pct": round(g_c/21*100, 1)},
            "language_knowledge": {"total": 51, "correct": v_c + g_c, "scaled": lang_scaled, "cutoff_met": lang_scaled >= 19},
            "reading": {"total": 21, "correct": r_c, "scaled": reading_scaled, "cutoff_met": reading_scaled >= 19},
            "listening": {"total": 30, "correct": l_c, "scaled": listening_scaled, "cutoff_met": listening_scaled >= 19}
        },
        "has_sectional_cutoff_risk": False,
        "is_passed": total_scaled >= 90 and lang_scaled >= 19 and reading_scaled >= 19 and listening_scaled >= 19,
        "wrong_items": wrong_item_nos,
        "unknown_items": [],
        "unanswered_items": []
    }

    # 1. Insert Test
    cur.execute("""
        INSERT INTO tests (
            id, test_date, title, source_class, target_level, difficulty_label,
            memory_timing, response_format, total_items, correct_items,
            unknown_items, unanswered_items, elapsed_seconds, time_limit_seconds,
            diagnostic_weight, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        test_id,
        test_date,
        "2023年 第2回 (12月) JLPT N2 本試験 全領域 実戦模試 (102問)",
        "official_mock",
        "N2",
        "official_high_difficulty",
        "full_mock_real",
        "multiple_choice_4",
        102,
        len(records) - len(wrong_item_nos),
        0,
        0,
        sub['elapsedSeconds'],
        9300,
        1.0,
        json.dumps(notes_dict, ensure_ascii=False)
    ))

    # 2. Insert Question Attempts & Review Queue
    exam_dt = datetime.strptime(test_date, '%Y-%m-%d')
    d1_str = (exam_dt + timedelta(days=1)).strftime('%Y-%m-%d')
    d3_str = (exam_dt + timedelta(days=3)).strftime('%Y-%m-%d')
    d7_str = (exam_dt + timedelta(days=7)).strftime('%Y-%m-%d')

    for q in records:
        item_no = q['id']
        item_type = get_item_type(item_no)
        is_corr = q['isCorrect']
        resp_state = 'correct' if is_corr else 'wrong'
        dwell_sec = q.get('dwellTimeSeconds', 0)

        ref_q = ref_questions.get(item_no, {})
        choices = ref_q.get('choices', [])

        user_ans_idx = q['userAnswer']
        off_ans_idx = q['officialAnswer']

        selected_text = choices[user_ans_idx] if (user_ans_idx is not None and user_ans_idx < len(choices)) else str(user_ans_idx)
        correct_text = choices[off_ans_idx] if (off_ans_idx is not None and off_ans_idx < len(choices)) else str(off_ans_idx)

        explanation = ref_q.get('explanation', '')
        trap_hypothesis = ""
        if not is_corr:
            # extract trap note from explanation if possible
            if '함정' in explanation:
                parts = explanation.split('함정')
                trap_hypothesis = parts[1].split('\n')[0].strip(': ·- ')[:100]
            else:
                trap_hypothesis = f"선택지 {user_ans_idx+1}번 오답 선택"

        cur.execute("""
            INSERT INTO question_attempts (
                test_id, item_no, item_type_id, level_label, response_state,
                response_seconds, audio_seconds, decision_seconds, play_count,
                selected_text, correct_text, trap_hypothesis, trap_confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_id,
            item_no,
            item_type,
            "N2",
            resp_state,
            dwell_sec,
            None,
            None,
            1 if item_no >= 73 else None,
            selected_text,
            correct_text,
            trap_hypothesis,
            "high" if not is_corr else None
        ))

        attempt_id = cur.lastrowid

        # Register to review_queue if wrong
        if not is_corr:
            for iv_label, iv_date in [('D+1', d1_str), ('D+3', d3_str), ('D+7', d7_str)]:
                cur.execute("""
                    INSERT INTO review_queue (
                        attempt_id, review_date, interval_label, status, result_state, result_seconds
                    ) VALUES (?, ?, ?, 'pending', NULL, NULL)
                """, (attempt_id, iv_date, iv_label))

    # 3. Update Study Intervals
    cur.execute("""
        INSERT INTO study_intervals (
            session_date, started_at, ended_at, duration_seconds, status, source, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        test_date,
        "2026-09-30T20:00:00+09:00",
        "2026-09-30T22:26:28+09:00",
        sub['elapsedSeconds'],
        "completed",
        "mock_exam_official_202312",
        "2023年 第2回 (12月) JLPT N2 本試験 全領域 実戦模試 (102問) 완본 응시 완료 (8,788초 / 146분 28초)"
    ))

    # 4. Update Study Sessions
    # Previous verified_minutes: 187. Now add 146 minutes = 333 minutes (or 334 with round)
    # Total seconds: Anki 7673s + Lecture 3600s + Exam 8788s = 20,061s = 334.35 minutes
    cur.execute("""
        UPDATE study_sessions
        SET verified_minutes = 334,
            summary = '[2026-09-30] 총 확인 학습시간 334분 (5시간 34분 / Anki 127분 53초 + N2 강의 60분 + 2023.12 실전모의고사 146분 28초). 1) 제2회 실전 모의고사 완주 (2023.12 기출 102문항, 환산 92/180점 합격, 전 영역 과락 0건 통과). 2) N2 정규강의 60분 수강. 3) Anki 1,111회 집중 회독 완료.',
            updated_at = datetime('now', 'localtime')
        WHERE session_date = ?
    """, (test_date,))

    conn.commit()
    conn.close()
    print("Successfully recorded 2023.12 mock exam in database/jlpt_learning.db!")

if __name__ == '__main__':
    record_result()
