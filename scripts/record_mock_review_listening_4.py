# -*- coding: utf-8 -*-
"""
Record JLPT N2 模試 間違いノート 復習 (청해 실전음원 4제 중간완료) for 2026-10-08 in database/jlpt_learning.db.
- Test result: 3 / 4 (75%), 4m 44s (284s)
- Mistake: Q99 (청해 문제4 即時応答 8번: 壁の色変えたせいか、広く見えるんじゃない？)
- D+1/D+3/D+7 review queue registered
- Total study time updated to 177m 33.23s (verified_minutes = 177)
"""

import sqlite3
import json
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'database' / 'jlpt_learning.db'

con = sqlite3.connect(DB)
cur = con.cursor()

# 1. Insert tests table
test_id = 'machigai-review-20261008-listening-4'
cur.execute('''
    INSERT INTO tests (
        id, test_date, title, source_class, target_level, difficulty_label,
        memory_timing, response_format, total_items, correct_items, unknown_items,
        unanswered_items, elapsed_seconds, time_limit_seconds, diagnostic_weight, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        total_items = excluded.total_items,
        correct_items = excluded.correct_items,
        elapsed_seconds = excluded.elapsed_seconds,
        notes = excluded.notes
''', (
    test_id,
    '2026-10-08',
    '2026-10-08 JLPT N2 模試 間違いノート 復習 (청해 실전음원 4문항 중간완료)',
    '공식 모의고사',
    'N2',
    '오답노트 복습',
    '지연 복습',
    '웹 퀴즈 (실전 음원 플레이어)',
    4,
    3,
    0,
    0,
    284,
    None,
    0.5,
    json.dumps({
        'course': '청해 실전음원 25제 [4문항 중간완료]',
        'score': '3/4',
        'accuracy': '75%',
        'wrong_items': ['Q99'],
        'notes': '청해 실전 원본 음원 4문항 응시 3정답 1오답. Q99(공식 제2집 청해 문제4 즉시응답 8번: 壁の色変えたせいか、広く見えるんじゃない？) 오답.'
    }, ensure_ascii=False)
))
print("Tests table updated successfully.")

# 2. Insert study_intervals
cur.execute('''
    INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    '2026-10-08',
    '2026-10-08 21:25:28',
    '2026-10-08 21:30:12',
    284,
    'completed',
    'quiz',
    '[2026-10-08 JLPT N2 模試 間違いノート 復習] 4분 44초 (코스: 청해 실전음원 25제 [4문항 중간완료], 점수: 3/4, 정답률: 75%, 오답: Q99)'
))
print("study_intervals row inserted successfully.")

# 3. Insert question_attempts for Q99
cur.execute('''
    INSERT INTO question_attempts (
        test_id, item_no, item_type_id, level_label, response_state,
        response_seconds, audio_seconds, decision_seconds, play_count,
        selected_text, correct_text, trap_hypothesis, trap_confidence
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    test_id,
    99,
    'listening_quick_response',
    'N2',
    'wrong',
    71,
    25,
    46,
    1,
    '1번 (分かりました。そうしてみます。)',
    '2번 (ほんと、変えて、正解ですね。)',
    '이미 벽 색을 바꾼 상태(変えたせいか)에서의 의견 동조를 요청·제안으로 오인하여 시제 및 화행 오류 발생',
    0.95
))
attempt_id = cur.lastrowid
print(f"question_attempts row inserted with ID {attempt_id}.")

# 4. Insert review_queue for Q99 (D+1, D+3, D+7)
review_schedules = [
    ('2026-10-09', 'D+1'),
    ('2026-10-11', 'D+3'),
    ('2026-10-15', 'D+7')
]
for r_date, r_interval in review_schedules:
    cur.execute('''
        INSERT INTO review_queue (attempt_id, review_date, interval_label, status)
        VALUES (?, ?, ?, 'pending')
    ''', (attempt_id, r_date, r_interval))
print("review_queue rows inserted successfully.")

# 5. Update study_sessions
# Previous: 10,369.23s + 284.00s = 10,653.23s (177m 33.23s)
total_sec = 10369.23 + 284.00
whole_mins = int(total_sec // 60) # 177
rem_sec = round(total_sec % 60, 2) # 33.23

session_summary = (
    f"[2026-10-08] 당일 현재 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(total_sec/60.0, 2)}분, 진행 중). "
    f"1) ★N2 文法 SPEED RUN — 문형 저격 퀴즈 v2 완주 (58분 41초 / 3,521초 실측 완료, tests 등록)★: N2 전범위 150제 종합 코스 100문항 완주 (정답 100/107, 정답률 93.5%). "
    f"2) ★形容詞活用 SPEED RUN 100 완주 (21분 1초 / 1,261초 실측 완료, tests ID adj-speedrun-20261008-30)★: N2 필수 함정 코스 30제 (정답 81/83, 98%). "
    f"3) ★JLPT N2 模試 間違いノート 復習 (총 3회차 누적 13분 27초 / 14문항 13정답 92.9%)★: 1차 필기 8제(3분 37초, 8/8 100%) + 2차 청해 실전음원 2제(5분 6초, 2/2 100%) + 3차 청해 실전음원 4제(4분 44초, 3/4 75%, 오답: Q99). "
    f"4) Anki 집중 회독 세션 559회 실측 (84.40분 / 1시간 24분 24.23초, 고유 카드 303장). 잔여 {rem_sec}초 보존."
)

cur.execute('''
    UPDATE study_sessions
    SET verified_minutes = ?,
        summary = ?,
        updated_at = ?
    WHERE session_date = '2026-10-08'
''', (whole_mins, session_summary, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
print(f"study_sessions updated to {whole_mins} minutes.")

con.commit()
con.close()
print("All DB operations committed successfully.")
