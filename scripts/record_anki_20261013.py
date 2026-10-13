# -*- coding: utf-8 -*-
"""
Record Anki study stats for 2026-10-13 in database/jlpt_learning.db.
- Total study time: Common (all decks) = 6,043.77s (100m 43.77s / 100.73m / ~1h 40m 44s)
- Accuracy & ratings: Voca only (JLPT 한끝 Voca series) = 426 reviews, Again 124 (29.11%), Hard 15, Good 7, Easy 280
- New reading vocabulary deck (독해・기사・모의고사 어휘): 286 reviews, 51.88m (42 cards intensive memorization)
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
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1013_voca_filter')
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
d_str = '2026-10-13'

s_dt = datetime(2026, 10, 13, 4, 0, 0, tzinfo=KST)
e_dt = s_dt + timedelta(days=1)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

# 1. TOTAL (Common Time & Overall Reviews across ALL decks)
cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s_ms, e_ms))
total_cnt, total_time_ms, total_distinct_cards, min_id, max_id = cur_anki.fetchone()
total_cnt = total_cnt or 0
common_sec = (total_time_ms or 0) / 1000.0
common_mins = common_sec / 60.0

min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST) if min_id else s_dt
max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST) if max_id else s_dt
min_dt_str = min_dt.strftime('%H:%M')
max_dt_str = max_dt.strftime('%H:%M')

# 2. VOCA ONLY (Accuracy, Ratings, Speed metrics)
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
''', (s_ms, e_ms))
voca_cnt, voca_time_ms, voca_distinct_cards = cur_anki.fetchone()
voca_cnt = voca_cnt or 0
voca_sec = (voca_time_ms or 0) / 1000.0
voca_mins = voca_sec / 60.0
voca_sec_per_card = round(voca_sec / voca_cnt, 2) if voca_cnt else 0

# Voca Ratings
cur_anki.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s_ms, e_ms))
voca_rating_map = dict(cur_anki.fetchall())
again_c = voca_rating_map.get(1, 0)
hard_c = voca_rating_map.get(2, 0)
good_c = voca_rating_map.get(3, 0)
easy_c = voca_rating_map.get(4, 0)
again_pct = round((again_c / voca_cnt * 100), 2) if voca_cnt else 0.0

# Voca Review Types
cur_anki.execute('''
    SELECT r.type, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.type
''', (s_ms, e_ms))
voca_type_map = dict(cur_anki.fetchall())
voca_learn_revs = voca_type_map.get(0, 0) + voca_type_map.get(2, 0)
voca_revs_done = voca_type_map.get(1, 0) + voca_type_map.get(3, 0)

# 3. All Decks Breakdown
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

# Grammar/Theme Deck count
cur_anki.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ? AND c.did IN (
        SELECT id FROM decks WHERE name LIKE '%문법%' OR name LIKE '%JLPT N2%'
    )
''', (s_ms, e_ms))
grammar_reviewed_today = cur_anki.fetchone()[0] or 0

con_anki.close()

# SQLite Database calculations
con_db = sqlite3.connect(DB)
cur_db = con_db.cursor()

# 1. Update or insert Anki study interval for 2026-10-13 (Time: Common All Decks)
cur_db.execute('''
    SELECT id FROM study_intervals WHERE session_date = ? AND source = 'anki'
''', (d_str,))
existing_anki_interval = cur_db.fetchone()

anki_interval_note = (
    f"[2026-10-13 Anki 회독 세션] {int(common_sec//60)}분 {round(common_sec%60, 2)}초 "
    f"(시간 공통: 총 {total_cnt:,}회 실측 [한끝 Voca {voca_cnt:,}회 + 신규 독해·기사 어휘 286회], "
    f"고유 카드 {total_distinct_cards}장, {min_dt_str}~{max_dt_str} KST)"
)

if existing_anki_interval:
    cur_db.execute('''
        UPDATE study_intervals
        SET started_at = ?,
            ended_at = ?,
            duration_seconds = ?,
            notes = ?
        WHERE id = ?
    ''', (
        min_dt.strftime('%Y-%m-%d %H:%M:%S'),
        max_dt.strftime('%Y-%m-%d %H:%M:%S'),
        int(round(common_sec)),
        anki_interval_note,
        existing_anki_interval[0]
    ))
else:
    cur_db.execute('''
        INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
        VALUES (?, ?, ?, ?, 'completed', 'anki', ?)
    ''', (
        d_str,
        min_dt.strftime('%Y-%m-%d %H:%M:%S'),
        max_dt.strftime('%Y-%m-%d %H:%M:%S'),
        int(round(common_sec)),
        anki_interval_note
    ))

# 2. Sum all intervals for 2026-10-13
cur_db.execute('SELECT source, duration_seconds, notes FROM study_intervals WHERE session_date = ?', (d_str,))
all_intervals_1013 = cur_db.fetchall()

total_quiz_sec_1013 = 0
quiz_summaries_1013 = []
for src, dur, note in all_intervals_1013:
    if src != 'anki':
        total_quiz_sec_1013 += dur
        m = dur // 60
        s = dur % 60
        t_str = f"{m}분 {s}초" if m > 0 else f"{s}초"
        quiz_summaries_1013.append(f"{note.split(']')[0].replace('[', '')}: {t_str}")

grand_total_sec = common_sec + total_quiz_sec_1013
whole_mins = int(grand_total_sec // 60)
rem_sec = round(grand_total_sec % 60, 2)

deck_summary_str = ", ".join(deck_lines[:6])

quiz_part_str = ""
if quiz_summaries_1013:
    quiz_part_str = f" 2) ★실전 훈련 {len(quiz_summaries_1013)}세션 실측 ({total_quiz_sec_1013//60}분 {total_quiz_sec_1013%60}초 / {total_quiz_sec_1013}초)★: " + ", ".join(quiz_summaries_1013) + "."

session_summary = (
    f"[{d_str}] 당일 현재 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(grand_total_sec/60.0, 2)}분, 진행 중). "
    f"1) ★Anki 회독 세션 {total_cnt:,}회 실측 ({int(common_sec//60)}분 {round(common_sec%60, 2)}초 / {common_sec:.2f}초, {min_dt_str}~{max_dt_str} KST 완수, 고유 카드 {total_distinct_cards}장)★: "
    f"[시간 공통 반영: 총 {round(common_mins, 1)}분] "
    f"[정확도·반응 지표: 한끝 Voca 기준] {voca_cnt:,}회({round(voca_mins, 1)}분, 고유 카드 {voca_distinct_cards}장, 카드당 {voca_sec_per_card}초) ➔ "
    f"Again {again_c:,} ({again_pct}%), Hard {hard_c} ({round(hard_c/voca_cnt*100, 2)}%), "
    f"Good {good_c} ({round(good_c/voca_cnt*100, 2)}%), Easy {easy_c} ({round(easy_c/voca_cnt*100, 2)}%). "
    f"신규 단어장 암기 ➔ 독해・기사・모의고사 어휘 286회(51.9분, 42장 집중 회독). "
    f"주요 덱: {deck_summary_str}. "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장)."
    f"{quiz_part_str} "
    f"잔여 {rem_sec}초 보존."
)

source_note = (
    f"Anki revlog 2026-10-13 실측치 (시간 공통: {total_cnt:,}회 {round(common_mins, 2)}분 / 정확도: 한끝 Voca {voca_cnt:,}회 {again_pct}% Again)."
)

summary_payload = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks_time_voca_ratings',
    'scopeLabel': '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)',
    'answeredCards': voca_cnt,                  # Accuracy & reaction scope: Voca only
    'totalAnsweredCardsAllDecks': total_cnt,     # Common total count
    'studyMinutes': round(common_mins, 2),       # Common total study time
    'secondsPerCard': voca_sec_per_card,         # Voca speed
    'againCount': again_c,                       # Voca ratings
    'againPct': again_pct,                       # Voca accuracy
    'learningReviews': voca_learn_revs,
    'reviewsDone': voca_revs_done,
    'ratings': {
        'again': again_c,
        'hard': hard_c,
        'good': good_c,
        'easy': easy_c
    },
    'allDecksStats': {
        'totalReviews': total_cnt,
        'totalStudyMinutes': round(common_mins, 2),
        'distinctCards': total_distinct_cards,
        'newReadingDeckReviews': 286,
        'newReadingDeckMinutes': 51.88
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
        'new_cards_exposed_today': 42
    }
}

# 3. Update study_sessions for 2026-10-13
cur_db.execute('''
    INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
    VALUES (?, ?, 0, ?)
    ON CONFLICT(session_date) DO UPDATE SET
        verified_minutes = excluded.verified_minutes,
        summary = excluded.summary,
        updated_at = CURRENT_TIMESTAMP
''', (d_str, whole_mins, session_summary))

# 4. Update anki_daily_stats for 2026-10-13
cur_db.execute('''
    INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at)
    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(snapshot_date) DO UPDATE SET
        scope_label = excluded.scope_label,
        payload_json = excluded.payload_json,
        source_filename = excluded.source_filename,
        captured_at = CURRENT_TIMESTAMP,
        updated_at = CURRENT_TIMESTAMP
''', (d_str, '전체 덱 (시간 공통 / 정확도: 한끝 Voca)', json.dumps(summary_payload, ensure_ascii=False), f'Anki revlog snapshot {d_str}'))

con_db.commit()

print(f"[{d_str}] DB Updated Successfully!")
print(f"  - Common Time (All Decks): {common_sec:.2f}s ({round(common_mins, 2)}m / {int(common_sec//60)}m {round(common_sec%60, 2)}s, {min_dt_str}~{max_dt_str} KST)")
print(f"  - DB verified_minutes: {whole_mins}m (rem: {rem_sec}s)")
print(f"  - Accuracy & Ratings (Voca only): {voca_cnt:,} reviews, Again {again_c} ({again_pct}%), Hard {hard_c}, Good {good_c}, Easy {easy_c}")
print(f"  - New Reading Deck: 286 reviews (51.88m, 42 cards)")
print(f"  - Decks Breakdown: {deck_lines}")

assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
print("Integrity check & Foreign key check passed!")
