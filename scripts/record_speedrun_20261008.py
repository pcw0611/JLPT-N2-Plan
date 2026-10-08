# -*- coding: utf-8 -*-
"""
Record N2 Grammar Speed Run result for 2026-10-08 in database/jlpt_learning.db.
1) Test result: 100 / 107 (93.5%), 58m 41s (3,521s)
2) Study intervals: ID for Speed Run added (3,521s)
3) Study sessions updated: Anki 84m 24.23s + Speed Run 58m 41.00s = 143m 5.23s (DB verified_minutes = 143)
"""

import sqlite3
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'database' / 'jlpt_learning.db'

con = sqlite3.connect(DB)
cur = con.cursor()

# 1. Insert or update tests table
test_id = 'n2-grammar-speedrun-20261008'
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
    'N2 文法 SPEED RUN — 문형 저격 퀴즈 v2 (N2 전범위 150제 종합)',
    '자체 제작',
    'N2',
    'standard',
    'immediate',
    'multiple_choice_4',
    107,
    100,
    0,
    0,
    3521,
    None,
    0.3,
    json.dumps({
        'course': 'all',
        'courseName': 'N2 전범위 150제 종합',
        'accuracy': 93.46,
        'score': 100,
        'attempts': 107,
        'elapsedSec': 3521,
        'timeFormatted': '58분 41초',
        'sourceNote': '루틴 트레이너 N2 文法 SPEED RUN v2 100문항 완주'
    }, ensure_ascii=False)
))
print("Tests table updated successfully.")

# 2. Insert or update study_intervals
cur.execute("SELECT id FROM study_intervals WHERE session_date = '2026-10-08' AND notes LIKE '%SPEED RUN%'")
existing_interval = cur.fetchone()
if existing_interval:
    cur.execute('''
        UPDATE study_intervals
        SET duration_seconds = 3521,
            started_at = '2026-10-08T15:07:00+09:00',
            ended_at = '2026-10-08T16:05:41+09:00',
            notes = 'N2 文法 SPEED RUN — 문형 저격 퀴즈 v2 (N2 전범위 150제 종합 코스 100문항 완주 100/107, 93.5%, 58분 41초 실측)'
        WHERE id = ?
    ''', (existing_interval[0],))
    print(f"Updated existing study_intervals ID {existing_interval[0]}.")
else:
    cur.execute('''
        INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
        VALUES ('2026-10-08', '2026-10-08T15:07:00+09:00', '2026-10-08T16:05:41+09:00', 3521, 'completed', 'chat_confirmed', 'N2 文法 SPEED RUN — 문형 저격 퀴즈 v2 (N2 전범위 150제 종합 코스 100문항 완주 100/107, 93.5%, 58분 41초 실측)')
    ''')
    print("Inserted new study_intervals row for Speed Run.")

# 3. Update study_sessions
# Anki: 5,064.23s (84.40m) + Speed Run: 3,521.00s (58.68m) = 8,585.23s (143.09m)
total_sec = 5064.23 + 3521.00
whole_mins = int(total_sec // 60)
rem_sec = round(total_sec % 60, 2)

session_summary = (
    f"[2026-10-08] 당일 현재 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(total_sec/60.0, 2)}분, 진행 중). "
    f"1) ★N2 文法 SPEED RUN — 문형 저격 퀴즈 v2 완주 (58분 41초 / 3,521초 실측 완료, tests 및 study_intervals 등록)★: "
    f"N2 전범위 150제 종합 코스 100문항 완주 (정답 100/107, 정답률 93.5%), 전 문형 빈칸 뉘앙스 저격 및 1초 킬러 포인트 오답 회수 완료. "
    f"2) Anki 집중 회독 세션 559회 실측 (84.40분 / 1시간 24분 24.23초, 09:15~14:29 진행, 고유 카드 303장, 카드당 평균 9.06초): "
    f"주요 덱 JLPT 한끝 Voca::4-N2 300회(48.7분), JLPT 한끝 Voca::2-N4 129회(20.5분), JLPT 한끝 Voca::3-N3 82회(10.4분), JLPT 한끝 Voca::1-N5 42회(4.0분) 등. "
    f"학습 반응: Again 256 (45.80%), Hard 10 (1.79%), Good 19 (3.40%), Easy 274 (49.02%). "
    f"잔여 {rem_sec}초 보존."
)

cur.execute('''
    UPDATE study_sessions
    SET verified_minutes = ?,
        summary = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE session_date = '2026-10-08'
''', (whole_mins, session_summary))
print(f"Updated study_sessions for 2026-10-08: {whole_mins}m {rem_sec}s.")

con.commit()

# Assert integrity
assert cur.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not cur.execute('PRAGMA foreign_key_check').fetchall()
print("DB integrity check passed ok.")

con.close()
