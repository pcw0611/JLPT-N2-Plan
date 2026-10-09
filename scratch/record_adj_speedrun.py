import sqlite3
import json
from datetime import datetime

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

# 1. Insert into tests
test_id = 'adj-speedrun-20261008-30'
cur.execute("""
INSERT OR REPLACE INTO tests (
    id, test_date, title, source_class, target_level, difficulty_label,
    memory_timing, response_format, total_items, correct_items, unknown_items,
    unanswered_items, elapsed_seconds, time_limit_seconds, diagnostic_weight, notes
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    test_id,
    '2026-10-08',
    '2026-10-08 形容詞活用 SPEED RUN 100 (N2 필수 함정 30제)',
    '자체 제작',
    'N2',
    '형용사 활용 훈련',
    '즉시 훈련',
    '웹 퀴즈 (인앱 브라우저)',
    83,
    81,
    0,
    0,
    1261,
    None,
    0.4,
    json.dumps({
        "course": "★ N2 필수 함정 코스 (30제)",
        "score": "81/83",
        "accuracy": "98%",
        "notes": "오답 재시도 2회 포함 총 81개 정답 달성 (정답률 98%), 21분 1초 완주."
    }, ensure_ascii=False)
))

# 2. Insert into study_intervals
cur.execute("""
INSERT INTO study_intervals (
    session_date, started_at, ended_at, duration_seconds, status, source, notes
) VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    '2026-10-08',
    '2026-10-08 17:58:00',
    '2026-10-08 18:19:01',
    1261,
    'completed',
    'quiz',
    '[2026-10-08 形容詞活用 SPEED RUN 100] 21분 1초 (★ N2 필수 함정 코스 30제, 정답 81/83, 정답률 98%)'
))

# 3. Update study_sessions id=44
new_summary = (
    "[2026-10-08] 당일 현재 누적 순수 학습시간 172분 49.23초 (약 2시간 52분 49초 / 172.82분, 진행 중). "
    "1) ★N2 文法 SPEED RUN — 문형 저격 퀴즈 v2 완주 (58분 41초 / 3,521초 실측 완료, tests 등록)★: N2 전범위 150제 종합 코스 100문항 완주 (정답 100/107, 정답률 93.5%). "
    "2) ★形容詞活用 SPEED RUN 100 완주 (21분 1초 / 1,261초 실측 완료, tests ID adj-speedrun-20261008-30)★: N2 필수 함정 코스 30제 (정답 81/83, 98%). "
    "3) ★JLPT N2 模試 間違いノート 復習 (총 2회차 누적 8분 43초 / 10문항 전원 정답 100%)★: 1차 필기 8제(3분 37초, 8/8) + 2차 청해 실전음원 2제(5분 6초, 2/2). "
    "4) Anki 집중 회독 세션 559회 실측 (84.40분 / 1시간 24분 24.23초, 고유 카드 303장). 잔여 49.23초 보존."
)

cur.execute("""
UPDATE study_sessions
SET verified_minutes = 172,
    summary = ?,
    updated_at = ?
WHERE session_date = '2026-10-08'
""", (new_summary, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

con.commit()
print("DB update successful! Total minutes: 172m, test ID:", test_id)
