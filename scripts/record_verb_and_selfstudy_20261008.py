# -*- coding: utf-8 -*-
"""
Record Verb Speed Run 100 and Self-Study (1h 30m) for 2026-10-08 in database/jlpt_learning.db.
- Test result: 100 / 100 (100%), 24m 13s (1,453s)
- Self-study: 1h 30m (90m, 5,400s)
- Previous total seconds: 10,653.23s (177m 33.23s)
- Added seconds: 1,453s + 5,400s = 6,853s
- New total seconds: 17,506.23s (291m 46.23s / ~4h 51m 46s)
- verified_minutes = 291
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

# 1. Insert into tests table
test_id = 'verb-speedrun-20261008-100'
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
    '2026-10-08 動詞活用 SPEED RUN 100 (100제 완주)',
    '자체 제작',
    'N2',
    '동사 활용 훈련',
    '즉시 훈련',
    '웹 퀴즈 (인앱 브라우저)',
    100,
    100,
    0,
    0,
    1453,
    None,
    0.4,
    json.dumps({
        'course': '전체 100문항 완주 코스',
        'score': '100/100',
        'accuracy': '100%',
        'wrong_items': [],
        'notes': '동사 활용 100문항 100% 전원 정답 퍼펙트 완주 달성 (24분 13초, 문항당 평균 14.5초).'
    }, ensure_ascii=False)
))
print("Tests table updated successfully.")

# 2. Insert study_intervals for Verb Speed Run
cur.execute('''
    INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    '2026-10-08',
    '2026-10-08 21:32:00',
    '2026-10-08 21:56:13',
    1453,
    'completed',
    'quiz',
    '[2026-10-08 動詞活用 SPEED RUN 100] 24분 13초 (동사 활용 100문항 완주, 정답 100/100, 정답률 100%)'
))
print("study_intervals row for Verb Speed Run inserted.")

# 3. Insert study_intervals for Self-Study (1h 30m = 5,400s)
cur.execute('''
    INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    '2026-10-08',
    '2026-10-08 19:30:00',
    '2026-10-08 21:00:00',
    5400,
    'completed',
    'self_study',
    '[2026-10-08 개인 공부] 1시간 30분 (90분 / 5,400초, 일본어 문법·어휘·독해 자율 집중 학습)'
))
print("study_intervals row for Self-Study inserted.")

# 4. Update study_sessions
# Previous: 10,653.23s + 1,453s + 5,400s = 17,506.23s (291m 46.23s)
total_sec = 10653.23 + 1453.00 + 5400.00
whole_mins = int(total_sec // 60) # 291
rem_sec = round(total_sec % 60, 2) # 46.23

session_summary = (
    f"[2026-10-08] 당일 현재 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(total_sec/60.0, 2)}분, 진행 중). "
    f"1) ★動詞活用 SPEED RUN 100 퍼펙트 완주 (24분 13초 / 1,453초 실측 완료, tests 등록)★: 100문항 전원 정답 100/100 (100%), 평균 14.5초/문항 쾌속 마스터. "
    f"2) ★N2 文法 SPEED RUN — 문형 저격 퀴즈 v2 완주 (58분 41초 / 3,521초 실측 완료, tests 등록)★: N2 전범위 150제 종합 코스 100문항 완주 (정답 100/107, 정답률 93.5%). "
    f"3) ★形容詞活用 SPEED RUN 100 완주 (21분 1초 / 1,261초 실측 완료, tests ID adj-speedrun-20261008-30)★: N2 필수 함정 코스 30제 (정답 81/83, 98%). "
    f"4) ★JLPT N2 模試 間違いノート 復習 (총 3회차 누적 13분 27초 / 14문항 13정답 92.9%)★: 1차 필기 8제(3분 37초, 8/8) + 2차 청해 실전음원 2제(5분 6초, 2/2) + 3차 청해 실전음원 4제(4분 44초, 3/4, Q99 복습 큐 등록). "
    f"5) ★개인 공부 집중 세션 (90분 / 1시간 30분 / 5,400초 실측 추가 반영)★: 문법·어휘·독해 자율 보강. "
    f"6) Anki 집중 회독 세션 559회 실측 (84.40분 / 1시간 24분 24.23초, 고유 카드 303장). 잔여 {rem_sec}초 보존."
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
