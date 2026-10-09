# -*- coding: utf-8 -*-
"""
Record Anki study stats for 2026-10-09 in database/jlpt_learning.db.
- Anki: 662 reviews, 5,746.74s (95m 46.74s / 95.78m), 437 distinct cards (10:16 ~ 17:32 KST)
  Including new session: JLPT N2::05 조건형 비교 30 reviews (11.2m)
- Online quizzes (4 sessions): 3,786s (63m 6s)
  1) 動詞活用 SPEED RUN 100: 321s (5m 21s, 30/30)
  2) 청해 실전음원 25제 [7문항 중간완료]: 1403s (23m 23s, 7/7)
  3) 청해 실전음원 25제 [3문항 중간완료]: 630s (10m 30s, 2/3)
  4) 청해 실전음원 25제 [11문항 풀이]: 1432s (23m 52s, 4/11)
- Total verified time: 9,532.74s = 158m 52.74s (approx 2h 38m, verified_minutes = 158, remaining 52.74s preserved)
"""

import sqlite3
import shutil
import sys
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'database' / 'jlpt_learning.db'

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1009')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TEMP_DIR / 'collection.anki2-shm')

con_anki = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur_anki = con_anki.cursor()

cur_anki.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur_anki.fetchall())
new_rem = queue_counts.get(0, 0)
learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
rev_rem = queue_counts.get(2, 0)

cur_anki.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur_anki.fetchall()}

KST = timezone(timedelta(hours=9))
d_str = '2026-10-09'

s_dt = datetime(2026, 10, 9, 4, 0, 0, tzinfo=KST)
e_dt = s_dt + timedelta(days=1)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s_ms, e_ms))
cnt, total_time_ms, distinct_cards, min_id, max_id = cur_anki.fetchone()
cnt = cnt or 0
anki_sec = (total_time_ms or 0) / 1000.0
anki_mins = anki_sec / 60.0
sec_per_card = round(anki_sec / cnt, 2) if cnt else 0

min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST) if min_id else s_dt
max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST) if max_id else s_dt
min_dt_str = min_dt.strftime('%H:%M')
max_dt_str = max_dt.strftime('%H:%M')

# Ratings
cur_anki.execute('''
    SELECT ease, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY ease
''', (s_ms, e_ms))
rating_map = dict(cur_anki.fetchall())
again_c = rating_map.get(1, 0)
hard_c = rating_map.get(2, 0)
good_c = rating_map.get(3, 0)
easy_c = rating_map.get(4, 0)
again_pct = round((again_c / cnt * 100), 2) if cnt else 0.0

# Types
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s_ms, e_ms))
type_map = dict(cur_anki.fetchall())
learn_revs = type_map.get(0, 0) + type_map.get(2, 0)
revs_done = type_map.get(1, 0) + type_map.get(3, 0)

# Decks
cur_anki.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s_ms, e_ms))
deck_breakdown = []
deck_lines = []
for did, d_cnt, d_dist, d_tms in cur_anki.fetchall():
    d_sec = (d_tms or 0) / 1000.0
    d_min = round(d_sec / 60.0, 1)
    d_name = deck_names.get(did, f"Deck {did}")
    deck_breakdown.append({
        'deckId': did,
        'deckName': d_name,
        'reviews': d_cnt,
        'distinctCards': d_dist,
        'studyMinutes': d_min,
        'seconds': round(d_sec, 1)
    })
    deck_lines.append(f"{d_name} {d_cnt:,}회({d_min}분)")

# Grammar reviewed
cur_anki.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ? AND c.did IN (
        SELECT id FROM decks WHERE name LIKE '%문법%' OR name LIKE '%05%' OR name LIKE '%조건형%'
    )
''', (s_ms, e_ms))
grammar_reviewed_today = cur_anki.fetchone()[0] or 0

con_anki.close()

# SQLite Database calculations
con_db = sqlite3.connect(DB)
cur_db = con_db.cursor()

# 1. Update Anki study interval (id=17)
cur_db.execute('''
    UPDATE study_intervals
    SET started_at = ?,
        ended_at = ?,
        duration_seconds = ?,
        notes = ?
    WHERE id = 17 AND session_date = '2026-10-09' AND source = 'anki'
''', (
    min_dt.strftime('%Y-%m-%d %H:%M:%S'),
    max_dt.strftime('%Y-%m-%d %H:%M:%S'),
    int(round(anki_sec)),
    f"[2026-10-09 Anki 회독 세션] {int(anki_sec//60)}분 {round(anki_sec%60, 2)}초 (총 {cnt:,}회 실측, 고유 카드 {distinct_cards}장, 카드당 평균 {sec_per_card}초, {min_dt_str}~{max_dt_str} KST)"
))

# 2. Sum all intervals for 2026-10-09
cur_db.execute('SELECT source, duration_seconds, notes FROM study_intervals WHERE session_date = "2026-10-09"')
all_intervals = cur_db.fetchall()

total_quiz_sec = 0
quiz_summaries = []
for src, dur, note in all_intervals:
    if src != 'anki':
        total_quiz_sec += dur
        m = dur // 60
        s = dur % 60
        t_str = f"{m}분 {s}초" if m > 0 else f"{s}초"
        quiz_summaries.append(f"{note.split(']')[0].replace('[', '')}: {t_str}")

# Total time: exact anki seconds + quiz seconds
grand_total_sec = anki_sec + total_quiz_sec
whole_mins = int(grand_total_sec // 60)
rem_sec = round(grand_total_sec % 60, 2)

deck_summary_str = ", ".join(deck_lines[:5])
if len(deck_lines) > 5:
    deck_summary_str += f" 외 {len(deck_lines)-5}개 덱"

session_summary = (
    f"[{d_str}] 당일 현재 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(grand_total_sec/60.0, 2)}분, 진행 중). "
    f"1) ★Anki 집중 회독 세션 {cnt:,}회 실측 ({int(anki_sec//60)}분 {round(anki_sec%60, 2)}초 / {anki_sec:.2f}초, {min_dt_str}~{max_dt_str} KST 완수, 고유 카드 {distinct_cards}장, 카드당 평균 {sec_per_card}초)★: "
    f"주요 덱 {deck_summary_str}. "
    f"학습 반응: Again {again_c:,} ({again_pct}%), Hard {hard_c} ({round(hard_c/cnt*100, 2)}%), "
    f"Good {good_c} ({round(good_c/cnt*100, 2)}%), Easy {easy_c} ({round(easy_c/cnt*100, 2)}%). "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장). "
    f"2) ★실전 훈련 및 모의고사 오답 복습 4세션 실측 ({total_quiz_sec//60}분 {total_quiz_sec%60}초 / {total_quiz_sec}초)★: "
    f"① 動詞活用 SPEED RUN 100 30제 (5분 21초, 30/30, 100%), "
    f"② 청해 실전음원 25제 [7문항 중간완료] (23분 23초, 7/7, 100%), "
    f"③ 청해 실전음원 25제 [3문항 중간완료] (10분 30초, 2/3, 67%), "
    f"④ 청해 실전음원 25제 [11문항 풀이] (23분 52초, 4/11, 36%). "
    f"잔여 {rem_sec}초 보존."
)

source_note = (
    f"Anki revlog 2026-10-09 실측치 ({cnt:,}회, {round(anki_mins, 2)}분) + 온라인 시험 4건({round(total_quiz_sec/60.0, 2)}분) 합산치 (총 {whole_mins}분 {rem_sec}초)."
)

summary_payload = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks',
    'scopeLabel': '전체 덱',
    'answeredCards': cnt,
    'studyMinutes': round(anki_mins, 2),
    'secondsPerCard': sec_per_card,
    'againCount': again_c,
    'againPct': again_pct,
    'learningReviews': learn_revs,
    'reviewsDone': revs_done,
    'ratings': {
        'again': again_c,
        'hard': hard_c,
        'good': good_c,
        'easy': easy_c
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'decks': deck_breakdown,
    'studyDay': d_str,
    'ankiResourceStudyDayRaw': d_str,
    'sourceNote': source_note,
    'inventory': {
        'n3_unseen': 0,
        'n2_unseen': 0,
        'n2_new_today': 0,
        'n3_new_today': 0,
        'grammar_new_today': 0,
        'grammar_reviewed_today': grammar_reviewed_today,
        'grammar_unseen': 0,
        'new_cards_exposed_today': 0
    }
}

# 3. Update study_sessions
cur_db.execute('''
    INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
    VALUES (?, ?, 0, ?)
    ON CONFLICT(session_date) DO UPDATE SET
        verified_minutes = excluded.verified_minutes,
        summary = excluded.summary,
        updated_at = CURRENT_TIMESTAMP
''', (d_str, whole_mins, session_summary))

# 4. Update anki_daily_stats
cur_db.execute('''
    INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at)
    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(snapshot_date) DO UPDATE SET
        scope_label = excluded.scope_label,
        payload_json = excluded.payload_json,
        source_filename = excluded.source_filename,
        captured_at = CURRENT_TIMESTAMP,
        updated_at = CURRENT_TIMESTAMP
''', (d_str, '전체 덱', json.dumps(summary_payload, ensure_ascii=False), f'Anki revlog snapshot {d_str}'))

con_db.commit()

print(f"[{d_str}] DB Updated Successfully!")
print(f"  - Anki: {cnt:,} reviews, {round(anki_mins, 2)}m ({int(anki_sec//60)}m {round(anki_sec%60, 2)}s, {min_dt_str}~{max_dt_str} KST)")
print(f"  - Online Quizzes: {len(all_intervals)-1} sessions, {round(total_quiz_sec/60.0, 2)}m ({total_quiz_sec//60}m {total_quiz_sec%60}s)")
print(f"  - Grand Total: {whole_mins}m {rem_sec}s ({round(grand_total_sec/60.0, 2)}m / approx {whole_mins//60}h {whole_mins%60}m)")
print(f"  - DB verified_minutes: {whole_mins}")

assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
print("Integrity check & Foreign key check passed!")
