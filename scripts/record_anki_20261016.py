# -*- coding: utf-8 -*-
"""
Record Anki study stats for 2026-10-16 (and reconcile 2026-10-15 final stats) in database/jlpt_learning.db.

2026-10-15 (Reconciled Final):
- Anki: 843 reviews, 10,079.11s (167m 59.11s / 167.99m / ~2h 47m 59s), 315 distinct cards (10:07 ~ 00:38 KST)
- Voca only: 485 reviews, 6,374.29s (106m 14.29s), 271 cards, Again 214 (44.12%), Hard 6, Good 7, Easy 258
- Reading vocab deck (14 독해・기사・모의고사 어휘): 358 reviews, 3,704.83s (61m 44.83s), 44 cards
- Total learning time: 10,079.11s = 167m 59.11s (verified_minutes = 167m, rem: 59.11s, reconciled)

2026-10-16 (Current In-Progress Session):
- Anki: 543 reviews, 7,323.83s (122m 3.83s / 122.06m / ~2h 2m 4s), 269 distinct cards (10:22 ~ 14:37 KST)
- Voca only: 543 reviews, 7,323.83s (122m 3.83s), 269 cards, Again 274 (50.46%), Hard 0, Good 1 (0.18%), Easy 268 (49.36%)
- Queue: new 332, learning 20, review 3,090 (total 3,442)
- Total learning time: 7,323.83s = 122m 3.83s (verified_minutes = 122m, rem: 3.83s, in progress)
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
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1016_record')
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

con_db = sqlite3.connect(DB)
cur_db = con_db.cursor()

# ==========================================
# 1. Reconcile 2026-10-15 Final
# ==========================================
d15_str = '2026-10-15'
s15_dt = datetime(2026, 10, 15, 4, 0, 0, tzinfo=KST)
e15_dt = s15_dt + timedelta(days=1)
s15_ms = int(s15_dt.timestamp() * 1000)
e15_ms = int(e15_dt.timestamp() * 1000)

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s15_ms, e15_ms))
t15_cnt, t15_tms, t15_dist, min15_id, max15_id = cur_anki.fetchone()
t15_sec = (t15_tms or 0) / 1000.0
t15_min = t15_sec / 60.0
min15_dt = datetime.fromtimestamp(min15_id / 1000.0, tz=KST)
max15_dt = datetime.fromtimestamp(max15_id / 1000.0, tz=KST)

# Ratings 10-15 (Voca only for accuracy metric)
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
''', (s15_ms, e15_ms))
voca15_cnt, voca15_tms, voca15_dist = cur_anki.fetchone()
voca15_sec = (voca15_tms or 0) / 1000.0
voca15_min = voca15_sec / 60.0
voca15_sec_per_card = round(voca15_sec / voca15_cnt, 2) if voca15_cnt else 0

cur_anki.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s15_ms, e15_ms))
r15_voca = dict(cur_anki.fetchall())
again15_c = r15_voca.get(1, 0)
hard15_c = r15_voca.get(2, 0)
good15_c = r15_voca.get(3, 0)
easy15_c = r15_voca.get(4, 0)
again15_pct = round((again15_c / voca15_cnt * 100), 2) if voca15_cnt else 0.0

# Reading deck stats
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
''', (s15_ms, e15_ms))
read15_row = cur_anki.fetchone()
read15_cnt = read15_row[0] or 0
read15_sec = (read15_row[1] or 0) / 1000.0
read15_min = read15_sec / 60.0
read15_dist = read15_row[2] or 0

# Types (overall)
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s15_ms, e15_ms))
type15_map = dict(cur_anki.fetchall())
learn15_revs = type15_map.get(0, 0)
revs15_done = type15_map.get(1, 0)
relearn15_revs = type15_map.get(2, 0)

# First time cards exposed
cur_anki.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    WHERE r.id >= ? AND r.id < ?
      AND r.cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
''', (s15_ms, e15_ms, s15_ms))
first15_cards = cur_anki.fetchone()[0] or 0

# 10-15 Decks breakdown
cur_anki.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s15_ms, e15_ms))
deck15_breakdown = []
deck15_lines = []
for did, d_cnt, d_dist, d_tms in cur_anki.fetchall():
    d_sec = (d_tms or 0) / 1000.0
    d_m = round(d_sec / 60.0, 1)
    d_name = deck_names.get(did, f"Deck {did}")
    deck15_breakdown.append({
        'deckId': did,
        'deckName': d_name,
        'reviews': d_cnt,
        'distinctCards': d_dist,
        'studyMinutes': d_m,
        'seconds': round(d_sec, 1)
    })
    deck15_lines.append(f"{d_name} {d_cnt:,}회({d_m}분)")

# Update 10-15 Anki interval
anki15_note = (
    f"[2026-10-15 Anki 회독 세션] {int(t15_sec//60)}분 {round(t15_sec%60, 2)}초 "
    f"(한끝 Voca 및 N2 독해어휘 회독: 총 {t15_cnt:,}회 실측, "
    f"고유 카드 {t15_dist}장, {min15_dt.strftime('%H:%M')}~{max15_dt.strftime('%H:%M')} KST)"
)
cur_db.execute('''
    UPDATE study_intervals
    SET started_at = ?,
        ended_at = ?,
        duration_seconds = ?,
        notes = ?
    WHERE session_date = '2026-10-15' AND source = 'anki'
''', (
    min15_dt.strftime('%Y-%m-%d %H:%M:%S'),
    max15_dt.strftime('%Y-%m-%d %H:%M:%S'),
    int(round(t15_sec)),
    anki15_note
))

# Sum 10-15 intervals
cur_db.execute('SELECT source, duration_seconds, notes FROM study_intervals WHERE session_date = ?', (d15_str,))
int15 = cur_db.fetchall()
q15_sec = sum(dur for src, dur, note in int15 if src != 'anki')
total15_sec = t15_sec + q15_sec
whole15_mins = int(total15_sec // 60)
rem15_sec = round(total15_sec % 60, 2)

session15_summary = (
    f"[{d15_str}] 당일 최종 누적 순수 학습시간 {whole15_mins}분 {rem15_sec}초 (약 {whole15_mins//60}시간 {whole15_mins%60}분 / {round(total15_sec/60.0, 2)}분, 마감). "
    f"1) ★Anki 회독 세션 {t15_cnt:,}회 실측 ({int(t15_sec//60)}분 {round(t15_sec%60, 2)}초 / {t15_sec:.2f}초, {min15_dt.strftime('%H:%M')}~{max15_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t15_dist}장)★: "
    f"[시간 공통 반영: 총 {round(t15_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {voca15_cnt:,}회({round(voca15_min, 1)}분, 고유 카드 {voca15_dist}장, 카드당 {voca15_sec_per_card}초) ➔ "
    f"Again {again15_c:,} ({again15_pct}%), Hard {hard15_c} ({round(hard15_c/voca15_cnt*100, 2)}%), "
    f"Good {good15_c} ({round(good15_c/voca15_cnt*100, 2)}%), Easy {easy15_c} ({round(easy15_c/voca15_cnt*100, 2)}%). "
    f"신규 단어장 암기 ➔ 독해 어휘 {read15_cnt}회({round(read15_min, 1)}분, {read15_dist}장 집중 회독). "
    f"주요 덱: {', '.join(deck15_lines[:6])}. "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장). "
    f"잔여 {rem15_sec}초 보존."
)

cur_db.execute('''
    UPDATE study_sessions
    SET verified_minutes = ?,
        summary = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE session_date = '2026-10-15'
''', (whole15_mins, session15_summary))

payload15 = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks_time_voca_ratings',
    'scopeLabel': '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)',
    'answeredCards': voca15_cnt,
    'totalAnsweredCardsAllDecks': t15_cnt,
    'studyMinutes': round(t15_min, 2),
    'secondsPerCard': voca15_sec_per_card,
    'againCount': again15_c,
    'againPct': again15_pct,
    'learningReviews': learn15_revs,
    'reviewsDone': revs15_done,
    'ratings': {
        'again': again15_c,
        'hard': hard15_c,
        'good': good15_c,
        'easy': easy15_c
    },
    'allDecksStats': {
        'totalReviews': t15_cnt,
        'totalStudyMinutes': round(t15_min, 2),
        'distinctCards': t15_dist,
        'readingVocabReviews': read15_cnt,
        'readingVocabMinutes': round(read15_min, 2),
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'decks': deck15_breakdown,
    'studyDay': d15_str,
    'ankiResourceStudyDayRaw': d15_str,
    'sourceNote': f"Anki revlog 2026-10-15 실측치 (시간 공통: {t15_cnt:,}회 {round(t15_min, 2)}분 / 정확도: 한끝 Voca {voca15_cnt:,}회 {again15_pct}% Again).",
    'inventory': {
        'n3_unseen': 0,
        'n2_unseen': 0,
        'n2_new_today': 0,
        'n3_new_today': 0,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 0,
        'grammar_unseen': 0,
        'new_cards_exposed_today': first15_cards
    }
}

cur_db.execute('''
    UPDATE anki_daily_stats
    SET scope_label = ?,
        payload_json = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE snapshot_date = '2026-10-15'
''', ('전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)', json.dumps(payload15, ensure_ascii=False)))


# ==========================================
# 2. Record 2026-10-16 (Current In-Progress Session)
# ==========================================
d16_str = '2026-10-16'
s16_dt = datetime(2026, 10, 16, 4, 0, 0, tzinfo=KST)
e16_dt = s16_dt + timedelta(days=1)
s16_ms = int(s16_dt.timestamp() * 1000)
e16_ms = int(e16_dt.timestamp() * 1000)

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s16_ms, e16_ms))
t16_cnt, t16_tms, t16_dist, min16_id, max16_id = cur_anki.fetchone()
t16_sec = (t16_tms or 0) / 1000.0
t16_min = t16_sec / 60.0
min16_dt = datetime.fromtimestamp(min16_id / 1000.0, tz=KST)
max16_dt = datetime.fromtimestamp(max16_id / 1000.0, tz=KST)

# Voca only for accuracy metrics
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
''', (s16_ms, e16_ms))
voca16_cnt, voca16_tms, voca16_dist = cur_anki.fetchone()
voca16_sec = (voca16_tms or 0) / 1000.0
voca16_min = voca16_sec / 60.0
voca16_sec_per_card = round(voca16_sec / voca16_cnt, 2) if voca16_cnt else 0

cur_anki.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s16_ms, e16_ms))
r16_voca = dict(cur_anki.fetchall())
again16_c = r16_voca.get(1, 0)
hard16_c = r16_voca.get(2, 0)
good16_c = r16_voca.get(3, 0)
easy16_c = r16_voca.get(4, 0)
again16_pct = round((again16_c / voca16_cnt * 100), 2) if voca16_cnt else 0.0

# Reading deck stats
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
''', (s16_ms, e16_ms))
read16_row = cur_anki.fetchone()
read16_cnt = read16_row[0] or 0
read16_sec = (read16_row[1] or 0) / 1000.0
read16_min = read16_sec / 60.0
read16_dist = read16_row[2] or 0

# Types (overall)
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s16_ms, e16_ms))
type16_map = dict(cur_anki.fetchall())
learn16_revs = type16_map.get(0, 0)
revs16_done = type16_map.get(1, 0)
relearn16_revs = type16_map.get(2, 0)

# First time cards exposed
cur_anki.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    WHERE r.id >= ? AND r.id < ?
      AND r.cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
''', (s16_ms, e16_ms, s16_ms))
first16_cards = cur_anki.fetchone()[0] or 0

# Decks breakdown
cur_anki.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s16_ms, e16_ms))
deck16_breakdown = []
deck16_lines = []
for did, d_cnt, d_dist, d_tms in cur_anki.fetchall():
    d_sec = (d_tms or 0) / 1000.0
    d_m = round(d_sec / 60.0, 1)
    d_name = deck_names.get(did, f"Deck {did}")
    deck16_breakdown.append({
        'deckId': did,
        'deckName': d_name,
        'reviews': d_cnt,
        'distinctCards': d_dist,
        'studyMinutes': d_m,
        'seconds': round(d_sec, 1)
    })
    deck16_lines.append(f"{d_name} {d_cnt:,}회({d_m}분)")

# 1. study_intervals for 2026-10-16
cur_db.execute('SELECT id FROM study_intervals WHERE session_date = ? AND source = "anki"', (d16_str,))
existing16_anki = cur_db.fetchone()
anki16_note = (
    f"[2026-10-16 Anki 회독 세션] {int(t16_sec//60)}분 {round(t16_sec%60, 2)}초 "
    f"(한끝 Voca 전량 집중 회독: 총 {t16_cnt:,}회 실측, "
    f"고유 카드 {t16_dist}장, {min16_dt.strftime('%H:%M')}~{max16_dt.strftime('%H:%M')} KST)"
)

if existing16_anki:
    cur_db.execute('''
        UPDATE study_intervals
        SET started_at = ?,
            ended_at = ?,
            duration_seconds = ?,
            notes = ?
        WHERE id = ?
    ''', (
        min16_dt.strftime('%Y-%m-%d %H:%M:%S'),
        max16_dt.strftime('%Y-%m-%d %H:%M:%S'),
        int(round(t16_sec)),
        anki16_note,
        existing16_anki[0]
    ))
else:
    cur_db.execute('''
        INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
        VALUES (?, ?, ?, ?, 'completed', 'anki', ?)
    ''', (
        d16_str,
        min16_dt.strftime('%Y-%m-%d %H:%M:%S'),
        max16_dt.strftime('%Y-%m-%d %H:%M:%S'),
        int(round(t16_sec)),
        anki16_note
    ))

# 2. Sum all intervals for 2026-10-16
cur_db.execute('SELECT source, duration_seconds, notes FROM study_intervals WHERE session_date = ?', (d16_str,))
int16 = cur_db.fetchall()
q16_sec = sum(dur for src, dur, note in int16 if src != 'anki')
total16_sec = t16_sec + q16_sec
whole16_mins = int(total16_sec // 60)
rem16_sec = round(total16_sec % 60, 2)

session16_summary = (
    f"[{d16_str}] 당일 현재 누적 순수 학습시간 {whole16_mins}분 {rem16_sec}초 (약 {whole16_mins//60}시간 {whole16_mins%60}분 / {round(total16_sec/60.0, 2)}분, 진행 중). "
    f"1) ★Anki 회독 세션 {t16_cnt:,}회 실측 ({int(t16_sec//60)}분 {round(t16_sec%60, 2)}초 / {t16_sec:.2f}초, {min16_dt.strftime('%H:%M')}~{max16_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t16_dist}장)★: "
    f"[시간 공통 반영: 총 {round(t16_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {voca16_cnt:,}회({round(voca16_min, 1)}분, 고유 카드 {voca16_dist}장, 카드당 {voca16_sec_per_card}초) ➔ "
    f"Again {again16_c:,} ({again16_pct}%), Hard {hard16_c} ({round(hard16_c/voca16_cnt*100, 2)}%), "
    f"Good {good16_c} ({round(good16_c/voca16_cnt*100, 2)}%), Easy {easy16_c} ({round(easy16_c/voca16_cnt*100, 2)}%). "
    f"주요 덱: {', '.join(deck16_lines[:6])}. "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장). "
    f"잔여 {rem16_sec}초 보존."
)

cur_db.execute('''
    INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
    VALUES (?, ?, 0, ?)
    ON CONFLICT(session_date) DO UPDATE SET
        verified_minutes = excluded.verified_minutes,
        summary = excluded.summary,
        updated_at = CURRENT_TIMESTAMP
''', (d16_str, whole16_mins, session16_summary))

payload16 = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks_time_voca_ratings',
    'scopeLabel': '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)',
    'answeredCards': voca16_cnt,
    'totalAnsweredCardsAllDecks': t16_cnt,
    'studyMinutes': round(t16_min, 2),
    'secondsPerCard': voca16_sec_per_card,
    'againCount': again16_c,
    'againPct': again16_pct,
    'learningReviews': learn16_revs,
    'reviewsDone': revs16_done,
    'ratings': {
        'again': again16_c,
        'hard': hard16_c,
        'good': good16_c,
        'easy': easy16_c
    },
    'allDecksStats': {
        'totalReviews': t16_cnt,
        'totalStudyMinutes': round(t16_min, 2),
        'distinctCards': t16_dist,
        'readingVocabReviews': read16_cnt,
        'readingVocabMinutes': round(read16_min, 2),
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'decks': deck16_breakdown,
    'studyDay': d16_str,
    'ankiResourceStudyDayRaw': d16_str,
    'sourceNote': f"Anki revlog 2026-10-16 실측치 (시간 공통: {t16_cnt:,}회 {round(t16_min, 2)}분 / 정확도: 한끝 Voca {voca16_cnt:,}회 {again16_pct}% Again).",
    'inventory': {
        'n3_unseen': 0,
        'n2_unseen': 0,
        'n2_new_today': 0,
        'n3_new_today': 0,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 0,
        'grammar_unseen': 0,
        'new_cards_exposed_today': first16_cards
    }
}

cur_db.execute('''
    INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at)
    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(snapshot_date) DO UPDATE SET
        scope_label = excluded.scope_label,
        payload_json = excluded.payload_json,
        source_filename = excluded.source_filename,
        captured_at = CURRENT_TIMESTAMP,
        updated_at = CURRENT_TIMESTAMP
''', (d16_str, '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)', json.dumps(payload16, ensure_ascii=False), f'Anki revlog snapshot {d16_str}'))

con_db.commit()

# Assertions
assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
con_anki.close()

print("=" * 60)
print("[2026-10-15 Reconciled Successfully]")
print(f"  - Anki: {t15_cnt:,} reviews, {t15_sec:.2f}s ({round(t15_min, 2)}m / {int(t15_sec//60)}m {round(t15_sec%60, 2)}s, {min15_dt.strftime('%H:%M')}~{max15_dt.strftime('%H:%M')} KST)")
print(f"  - DB verified_minutes: {whole15_mins}m (rem: {rem15_sec}s)")
print(f"  - Voca ratings: Again {again15_c} ({again15_pct}%), Hard {hard15_c}, Good {good15_c}, Easy {easy15_c}")
print(f"  - Reading deck: {read15_cnt} reviews, {read15_min:.1f}m, {read15_dist} cards")
print("=" * 60)
print("[2026-10-16 Recorded Successfully]")
print(f"  - Anki: {t16_cnt:,} reviews, {t16_sec:.2f}s ({round(t16_min, 2)}m / {int(t16_sec//60)}m {round(t16_sec%60, 2)}s, {min16_dt.strftime('%H:%M')}~{max16_dt.strftime('%H:%M')} KST)")
print(f"  - DB verified_minutes: {whole16_mins}m (rem: {rem16_sec}s)")
print(f"  - Voca ratings: Again {again16_c} ({again16_pct}%), Hard {hard16_c}, Good {good16_c}, Easy {easy16_c}")
print(f"  - Decks: {deck16_lines}")
print("=" * 60)
