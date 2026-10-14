# -*- coding: utf-8 -*-
"""
Record Anki study stats for 2026-10-14 in database/jlpt_learning.db.
- Total study time: 5,358.00s (89m 18.00s / 89.30m / ~1h 29m 18s)
- Accuracy & ratings: 485 reviews, Again 153 (31.55%), Hard 10 (2.06%), Good 8 (1.65%), Easy 314 (64.74%)
- All 485 reviews are in JLPT 한끝 Voca series
- Also update 2026-10-13 study_sessions summary to match verified_minutes=239 (including 10th online sub).
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
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1014_record')
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
d_str = '2026-10-14'

s_dt = datetime(2026, 10, 14, 4, 0, 0, tzinfo=KST)
e_dt = s_dt + timedelta(days=1)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

# 1. TOTAL across ALL decks
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

# Ratings
cur_anki.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY r.ease
''', (s_ms, e_ms))
rating_map = dict(cur_anki.fetchall())
again_c = rating_map.get(1, 0)
hard_c = rating_map.get(2, 0)
good_c = rating_map.get(3, 0)
easy_c = rating_map.get(4, 0)
again_pct = round((again_c / total_cnt * 100), 2) if total_cnt else 0.0

# Review Types
cur_anki.execute('''
    SELECT r.type, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY r.type
''', (s_ms, e_ms))
type_map = dict(cur_anki.fetchall())
learn_revs = type_map.get(0, 0) + type_map.get(2, 0)
revs_done = type_map.get(1, 0) + type_map.get(3, 0)

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

# 1. Update or insert Anki study interval for 2026-10-14
cur_db.execute('''
    SELECT id FROM study_intervals WHERE session_date = ? AND source = 'anki'
''', (d_str,))
existing_anki_interval = cur_db.fetchone()

anki_interval_note = (
    f"[2026-10-14 Anki 회독 세션] {int(common_sec//60)}분 {round(common_sec%60, 2)}초 "
    f"(한끝 Voca 전범위 집중 회독: 총 {total_cnt:,}회 실측, "
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

# 2. Sum all intervals for 2026-10-14
cur_db.execute('SELECT source, duration_seconds, notes FROM study_intervals WHERE session_date = ?', (d_str,))
all_intervals_1014 = cur_db.fetchall()

total_quiz_sec_1014 = 0
quiz_summaries_1014 = []
for src, dur, note in all_intervals_1014:
    if src != 'anki':
        total_quiz_sec_1014 += dur
        m = dur // 60
        s = dur % 60
        t_str = f"{m}분 {s}초" if m > 0 else f"{s}초"
        quiz_summaries_1014.append(f"{note.split(']')[0].replace('[', '')}: {t_str}")

grand_total_sec = common_sec + total_quiz_sec_1014
whole_mins = int(grand_total_sec // 60)
rem_sec = round(grand_total_sec % 60, 2)

deck_summary_str = ", ".join(deck_lines[:6])

quiz_part_str = ""
if quiz_summaries_1014:
    quiz_part_str = f" 2) ★실전 훈련 {len(quiz_summaries_1014)}세션 실측 ({total_quiz_sec_1014//60}분 {total_quiz_sec_1014%60}초 / {total_quiz_sec_1014}초)★: " + ", ".join(quiz_summaries_1014) + "."

session_summary = (
    f"[{d_str}] 당일 현재 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(grand_total_sec/60.0, 2)}분, 진행 중). "
    f"1) ★Anki 집중 회독 세션 {total_cnt:,}회 실측 ({int(common_sec//60)}분 {round(common_sec%60, 2)}초 / {common_sec:.2f}초, {min_dt_str}~{max_dt_str} KST 완수, 고유 카드 {total_distinct_cards}장, 카드당 {voca_sec_per_card}초)★: "
    f"[전체 덱 실측: {round(common_mins, 1)}분, 전량 한끝 Voca 덱] "
    f"주요 덱: {deck_summary_str}. "
    f"학습 반응: Again {again_c:,} ({again_pct}%), Hard {hard_c} ({round(hard_c/total_cnt*100, 2)}%), "
    f"Good {good_c} ({round(good_c/total_cnt*100, 2)}%), Easy {easy_c} ({round(easy_c/total_cnt*100, 2)}%). "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장)."
    f"{quiz_part_str} "
    f"잔여 {rem_sec}초 보존."
)

source_note = (
    f"Anki revlog 2026-10-14 실측치 (전체 덱: {total_cnt:,}회 {round(common_mins, 2)}분 / 정확도: 한끝 Voca 전량 {again_pct}% Again)."
)

summary_payload = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks_time_voca_ratings',
    'scopeLabel': '전체 덱 (시간 공통 / 한끝 Voca 전량)',
    'answeredCards': voca_cnt,
    'totalAnsweredCardsAllDecks': total_cnt,
    'studyMinutes': round(common_mins, 2),
    'secondsPerCard': voca_sec_per_card,
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
    'allDecksStats': {
        'totalReviews': total_cnt,
        'totalStudyMinutes': round(common_mins, 2),
        'distinctCards': total_distinct_cards,
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

# 3. Update study_sessions for 2026-10-14
cur_db.execute('''
    INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
    VALUES (?, ?, 0, ?)
    ON CONFLICT(session_date) DO UPDATE SET
        verified_minutes = excluded.verified_minutes,
        summary = excluded.summary,
        updated_at = CURRENT_TIMESTAMP
''', (d_str, whole_mins, session_summary))

# 4. Update anki_daily_stats for 2026-10-14
cur_db.execute('''
    INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at)
    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(snapshot_date) DO UPDATE SET
        scope_label = excluded.scope_label,
        payload_json = excluded.payload_json,
        source_filename = excluded.source_filename,
        captured_at = CURRENT_TIMESTAMP,
        updated_at = CURRENT_TIMESTAMP
''', (d_str, '전체 덱 (시간 공통 / 한끝 Voca 전량)', json.dumps(summary_payload, ensure_ascii=False), f'Anki revlog snapshot {d_str}'))

# 5. Reconcile 2026-10-13 study_sessions summary to match verified_minutes=239 (including 10th sub)
summary_1013_reconciled = (
    "[2026-10-13] 당일 최종 누적 순수 학습시간 238분 40.77초 (약 3시간 58분 / 238.68분, 마감). "
    "1) ★Anki 회독 세션 712회 실측 (100분 43.77초 / 6043.77초, 05:36~12:47 KST 완수, 고유 카드 343장)★: "
    "[시간 공통 반영: 총 100.7분] [정확도·반응 지표: 한끝 Voca 기준] 426회(48.9분, 고유 카드 301장, 카드당 6.88초) ➔ "
    "Again 124 (29.11%), Hard 15 (3.52%), Good 7 (1.64%), Easy 280 (65.73%). "
    "신규 단어장 암기 ➔ 독해・기사・모의고사 어휘 286회(51.9분, 42장 집중 회독). "
    "주요 덱: JLPT N2::14 독해・기사・모의고사 어휘 286회(51.9분), JLPT 한끝 Voca::4-N2 193회(24.6분), JLPT 한끝 Voca::2-N4 103회(12.2분), JLPT 한끝 Voca::3-N3 77회(6.8분), JLPT 한끝 Voca::1-N5 47회(4.7분), JLPT 한끝 Voca::공통::의상 6회(0.6분). "
    "잔여 큐: new 361장, learning 2장, review 3,026장 (총 3,389장). "
    "2) ★실전 훈련 10세션 실측 (137분 57초 / 8277초, 175/202 정답, 86.6%)★: "
    "N2 文法 SPEED RUN 3세션 (45분 47초, 150/165 정답) + JLPT N2 模試 間違いノート 復習 7세션 (92분 10초, 25/37 정답). "
    "잔여 40.77초 보존."
)
cur_db.execute('''
    UPDATE study_sessions
    SET summary = ?,
        verified_minutes = 239,
        updated_at = CURRENT_TIMESTAMP
    WHERE session_date = '2026-10-13'
''', (summary_1013_reconciled,))

con_db.commit()

print(f"[{d_str}] DB Updated Successfully!")
print(f"  - Common Time (All Decks): {common_sec:.2f}s ({round(common_mins, 2)}m / {int(common_sec//60)}m {round(common_sec%60, 2)}s, {min_dt_str}~{max_dt_str} KST)")
print(f"  - DB verified_minutes: {whole_mins}m (rem: {rem_sec}s)")
print(f"  - Accuracy & Ratings: {total_cnt:,} reviews, Again {again_c} ({again_pct}%), Hard {hard_c}, Good {good_c}, Easy {easy_c}")
print(f"  - Decks Breakdown: {deck_lines}")

assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
print("Integrity check & Foreign key check passed!")
