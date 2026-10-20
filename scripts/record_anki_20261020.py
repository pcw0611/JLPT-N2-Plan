# -*- coding: utf-8 -*-
"""
Record Anki study stats and reconcile study sessions for:
- 2026-10-19 (Reconciled full day: 564 reviews, 8,034.58s = 133m 54.58s, closed/final)
- 2026-10-20 (Today in-progress: 436 reviews, 3,847.46s = 64m 7.46s)
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

# 1. Backup DB first
backup_db = ROOT / 'database' / f'jlpt_learning_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
shutil.copy2(DB, backup_db)
print(f"[DB Backup created]: {backup_db.name}")

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1020_exec')
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

# =========================================================================
# 1. Reconcile 2026-10-19 Final (마감 확정)
# =========================================================================
d19_str = '2026-10-19'
s19_dt = datetime(2026, 10, 19, 4, 0, 0, tzinfo=KST)
e19_dt = s19_dt + timedelta(days=1)
s19_ms = int(s19_dt.timestamp() * 1000)
e19_ms = int(e19_dt.timestamp() * 1000)

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s19_ms, e19_ms))
t19_cnt, t19_tms, t19_dist, min19_id, max19_id = cur_anki.fetchone()
t19_sec = (t19_tms or 0) / 1000.0
t19_min = t19_sec / 60.0
min19_dt = datetime.fromtimestamp(min19_id / 1000.0, tz=KST)
max19_dt = datetime.fromtimestamp(max19_id / 1000.0, tz=KST)

# Voca only
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
''', (s19_ms, e19_ms))
voca19_cnt, voca19_tms, voca19_dist = cur_anki.fetchone()
voca19_cnt = voca19_cnt or 0
voca19_sec = (voca19_tms or 0) / 1000.0
voca19_min = voca19_sec / 60.0
voca19_sec_per_card = round(voca19_sec / voca19_cnt, 2) if voca19_cnt else 0

cur_anki.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s19_ms, e19_ms))
r19_voca = dict(cur_anki.fetchall())
again19_c = r19_voca.get(1, 0)
hard19_c = r19_voca.get(2, 0)
good19_c = r19_voca.get(3, 0)
easy19_c = r19_voca.get(4, 0)
again19_pct = round((again19_c / voca19_cnt * 100), 2) if voca19_cnt else 0.0

# Reading deck stats
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
''', (s19_ms, e19_ms))
read19_row = cur_anki.fetchone()
read19_cnt = read19_row[0] or 0
read19_sec = (read19_row[1] or 0) / 1000.0
read19_min = read19_sec / 60.0
read19_dist = read19_row[2] or 0

# Types (overall)
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s19_ms, e19_ms))
type19_map = dict(cur_anki.fetchall())
learn19_revs = type19_map.get(0, 0)
revs19_done = type19_map.get(1, 0)
relearn19_revs = type19_map.get(2, 0)

# First time cards exposed
cur_anki.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    WHERE r.id >= ? AND r.id < ?
      AND r.cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
''', (s19_ms, e19_ms, s19_ms))
first19_cards = cur_anki.fetchone()[0] or 0

# Decks breakdown
cur_anki.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s19_ms, e19_ms))
deck19_breakdown = []
deck19_lines = []
for did, d_cnt, d_dist, d_tms in cur_anki.fetchall():
    d_sec = (d_tms or 0) / 1000.0
    d_m = round(d_sec / 60.0, 1)
    d_name = deck_names.get(did, f"Deck {did}")
    deck19_breakdown.append({
        'deckId': did,
        'deckName': d_name,
        'reviews': d_cnt,
        'distinctCards': d_dist,
        'studyMinutes': d_m,
        'seconds': round(d_sec, 1)
    })
    deck19_lines.append(f"{d_name} {d_cnt:,}회({d_m}분)")

# 1. study_intervals for 2026-10-19
anki19_note = (
    f"[2026-10-19 Anki 회독 세션] {int(t19_sec//60)}분 {round(t19_sec%60, 2)}초 "
    f"(한끝 Voca 및 N2 독해어휘 회독: 총 {t19_cnt:,}회 실측, "
    f"고유 카드 {t19_dist}장, {min19_dt.strftime('%H:%M')}~{max19_dt.strftime('%H:%M')} KST)"
)
cur_db.execute('DELETE FROM study_intervals WHERE session_date = ? AND source = "anki"', (d19_str,))
cur_db.execute('''
    INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
    VALUES (?, ?, ?, ?, 'completed', 'anki', ?)
''', (
    d19_str,
    min19_dt.strftime('%Y-%m-%d %H:%M:%S'),
    max19_dt.strftime('%Y-%m-%d %H:%M:%S'),
    int(round(t19_sec)),
    anki19_note
))

whole19_mins = int(t19_sec // 60)
rem19_sec = round(t19_sec % 60, 2)

session19_summary = (
    f"[{d19_str}] 당일 최종 누적 순수 학습시간 {whole19_mins}분 {rem19_sec}초 (약 {whole19_mins//60}시간 {whole19_mins%60}분 / {round(t19_sec/60.0, 2)}분, 마감). "
    f"1) ★Anki 회독 세션 {t19_cnt:,}회 실측 ({int(t19_sec//60)}분 {round(t19_sec%60, 2)}초 / {t19_sec:.2f}초, {min19_dt.strftime('%H:%M')}~{max19_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t19_dist}장)★: "
    f"[시간 공통 반영: 총 {round(t19_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {voca19_cnt:,}회({round(voca19_min, 1)}분, 고유 카드 {voca19_dist}장, 카드당 {voca19_sec_per_card}초) ➔ "
    f"Again {again19_c:,} ({again19_pct}%), Hard {hard19_c} ({round(hard19_c/voca19_cnt*100, 2)}%), "
    f"Good {good19_c} ({round(good19_c/voca19_cnt*100, 2)}%), Easy {easy19_c} ({round(easy19_c/voca19_cnt*100, 2)}%). "
    f"독해어휘 ➔ {read19_cnt}회({round(read19_min, 1)}분, {read19_dist}장). "
    f"주요 덱: {', '.join(deck19_lines[:6])}. "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장). "
    f"잔여 {rem19_sec}초 보존."
)

cur_db.execute('''
    INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
    VALUES (?, ?, 0, ?)
    ON CONFLICT(session_date) DO UPDATE SET
        verified_minutes = excluded.verified_minutes,
        summary = excluded.summary,
        updated_at = CURRENT_TIMESTAMP
''', (d19_str, whole19_mins, session19_summary))

payload19 = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks_time_voca_ratings',
    'scopeLabel': '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)',
    'answeredCards': voca19_cnt,
    'totalAnsweredCardsAllDecks': t19_cnt,
    'studyMinutes': round(t19_min, 2),
    'secondsPerCard': voca19_sec_per_card,
    'againCount': again19_c,
    'againPct': again19_pct,
    'learningReviews': learn19_revs,
    'reviewsDone': revs19_done,
    'ratings': {
        'again': again19_c,
        'hard': hard19_c,
        'good': good19_c,
        'easy': easy19_c
    },
    'allDecksStats': {
        'totalReviews': t19_cnt,
        'totalStudyMinutes': round(t19_min, 2),
        'distinctCards': t19_dist,
        'readingVocabReviews': read19_cnt,
        'readingVocabMinutes': round(read19_min, 2),
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'decks': deck19_breakdown,
    'studyDay': d19_str,
    'ankiResourceStudyDayRaw': d19_str,
    'sourceNote': f"Anki revlog 2026-10-19 실측치 (시간 공통: {t19_cnt:,}회 {round(t19_min, 2)}분 / 정확도: 한끝 Voca {voca19_cnt:,}회 {again19_pct}% Again).",
    'inventory': {
        'n3_unseen': 0,
        'n2_unseen': 0,
        'n2_new_today': 0,
        'n3_new_today': 0,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 0,
        'grammar_unseen': 0,
        'new_cards_exposed_today': first19_cards
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
''', (d19_str, '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)', json.dumps(payload19, ensure_ascii=False), f'Anki revlog snapshot {d19_str}'))


# =========================================================================
# 2. Record 2026-10-20 In-Progress (당일 진행 중)
# =========================================================================
d20_str = '2026-10-20'
s20_dt = datetime(2026, 10, 20, 4, 0, 0, tzinfo=KST)
e20_dt = s20_dt + timedelta(days=1)
s20_ms = int(s20_dt.timestamp() * 1000)
e20_ms = int(e20_dt.timestamp() * 1000)

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s20_ms, e20_ms))
t20_cnt, t20_tms, t20_dist, min20_id, max20_id = cur_anki.fetchone()
t20_cnt = t20_cnt or 0
t20_sec = (t20_tms or 0) / 1000.0
t20_min = t20_sec / 60.0
min20_dt = datetime.fromtimestamp(min20_id / 1000.0, tz=KST) if min20_id else s20_dt
max20_dt = datetime.fromtimestamp(max20_id / 1000.0, tz=KST) if max20_id else s20_dt

# Voca only
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
''', (s20_ms, e20_ms))
voca20_cnt, voca20_tms, voca20_dist = cur_anki.fetchone()
voca20_cnt = voca20_cnt or 0
voca20_sec = (voca20_tms or 0) / 1000.0
voca20_min = voca20_sec / 60.0
voca20_sec_per_card = round(voca20_sec / voca20_cnt, 2) if voca20_cnt else 0

cur_anki.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s20_ms, e20_ms))
r20_voca = dict(cur_anki.fetchall())
again20_c = r20_voca.get(1, 0)
hard20_c = r20_voca.get(2, 0)
good20_c = r20_voca.get(3, 0)
easy20_c = r20_voca.get(4, 0)
again20_pct = round((again20_c / voca20_cnt * 100), 2) if voca20_cnt else 0.0

# Reading deck stats
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
''', (s20_ms, e20_ms))
read20_row = cur_anki.fetchone()
read20_cnt = read20_row[0] or 0
read20_sec = (read20_row[1] or 0) / 1000.0
read20_min = read20_sec / 60.0
read20_dist = read20_row[2] or 0

# Types (overall)
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s20_ms, e20_ms))
type20_map = dict(cur_anki.fetchall())
learn20_revs = type20_map.get(0, 0)
revs20_done = type20_map.get(1, 0)
relearn20_revs = type20_map.get(2, 0)

# First time cards exposed
cur_anki.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    WHERE r.id >= ? AND r.id < ?
      AND r.cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
''', (s20_ms, e20_ms, s20_ms))
first20_cards = cur_anki.fetchone()[0] or 0

# Decks breakdown
cur_anki.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s20_ms, e20_ms))
deck20_breakdown = []
deck20_lines = []
for did, d_cnt, d_dist, d_tms in cur_anki.fetchall():
    d_sec = (d_tms or 0) / 1000.0
    d_m = round(d_sec / 60.0, 1)
    d_name = deck_names.get(did, f"Deck {did}")
    deck20_breakdown.append({
        'deckId': did,
        'deckName': d_name,
        'reviews': d_cnt,
        'distinctCards': d_dist,
        'studyMinutes': d_m,
        'seconds': round(d_sec, 1)
    })
    deck20_lines.append(f"{d_name} {d_cnt:,}회({d_m}분)")

# 1. study_intervals for 2026-10-20
anki20_note = (
    f"[2026-10-20 Anki 회독 세션] {int(t20_sec//60)}분 {round(t20_sec%60, 2)}초 "
    f"(한끝 Voca 전량 집중 회독: 총 {t20_cnt:,}회 실측, "
    f"고유 카드 {t20_dist}장, {min20_dt.strftime('%H:%M')}~{max20_dt.strftime('%H:%M')} KST)"
)
cur_db.execute('DELETE FROM study_intervals WHERE session_date = ? AND source = "anki"', (d20_str,))
cur_db.execute('''
    INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
    VALUES (?, ?, ?, ?, 'completed', 'anki', ?)
''', (
    d20_str,
    min20_dt.strftime('%Y-%m-%d %H:%M:%S'),
    max20_dt.strftime('%Y-%m-%d %H:%M:%S'),
    int(round(t20_sec)),
    anki20_note
))

whole20_mins = int(t20_sec // 60)
rem20_sec = round(t20_sec % 60, 2)

session20_summary = (
    f"[{d20_str}] 당일 현재 누적 순수 학습시간 {whole20_mins}분 {rem20_sec}초 (약 {whole20_mins//60}시간 {whole20_mins%60}분 / {round(t20_sec/60.0, 2)}분, 진행 중). "
    f"1) ★Anki 회독 세션 {t20_cnt:,}회 실측 ({int(t20_sec//60)}분 {round(t20_sec%60, 2)}초 / {t20_sec:.2f}초, {min20_dt.strftime('%H:%M')}~{max20_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t20_dist}장)★: "
    f"[시간 공통 반영: 총 {round(t20_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {voca20_cnt:,}회({round(voca20_min, 1)}분, 고유 카드 {voca20_dist}장, 카드당 {voca20_sec_per_card}초) ➔ "
    f"Again {again20_c:,} ({again20_pct}%), Hard {hard20_c} ({round(hard20_c/voca20_cnt*100, 2)}%), "
    f"Good {good20_c} ({round(good20_c/voca20_cnt*100, 2)}%), Easy {easy20_c} ({round(easy20_c/voca20_cnt*100, 2)}%). "
    f"주요 덱: {', '.join(deck20_lines[:6])}. "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장). "
    f"잔여 {rem20_sec}초 보존."
)

cur_db.execute('''
    INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
    VALUES (?, ?, 0, ?)
    ON CONFLICT(session_date) DO UPDATE SET
        verified_minutes = excluded.verified_minutes,
        summary = excluded.summary,
        updated_at = CURRENT_TIMESTAMP
''', (d20_str, whole20_mins, session20_summary))

payload20 = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks_time_voca_ratings',
    'scopeLabel': '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)',
    'answeredCards': voca20_cnt,
    'totalAnsweredCardsAllDecks': t20_cnt,
    'studyMinutes': round(t20_min, 2),
    'secondsPerCard': voca20_sec_per_card,
    'againCount': again20_c,
    'againPct': again20_pct,
    'learningReviews': learn20_revs,
    'reviewsDone': revs20_done,
    'ratings': {
        'again': again20_c,
        'hard': hard20_c,
        'good': good20_c,
        'easy': easy20_c
    },
    'allDecksStats': {
        'totalReviews': t20_cnt,
        'totalStudyMinutes': round(t20_min, 2),
        'distinctCards': t20_dist,
        'readingVocabReviews': read20_cnt,
        'readingVocabMinutes': round(read20_min, 2),
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'decks': deck20_breakdown,
    'studyDay': d20_str,
    'ankiResourceStudyDayRaw': d20_str,
    'sourceNote': f"Anki revlog 2026-10-20 실측치 (시간 공통: {t20_cnt:,}회 {round(t20_min, 2)}분 / 정확도: 한끝 Voca {voca20_cnt:,}회 {again20_pct}% Again).",
    'inventory': {
        'n3_unseen': 0,
        'n2_unseen': 0,
        'n2_new_today': 0,
        'n3_new_today': 0,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 0,
        'grammar_unseen': 0,
        'new_cards_exposed_today': first20_cards
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
''', (d20_str, '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)', json.dumps(payload20, ensure_ascii=False), f'Anki revlog snapshot {d20_str}'))

con_db.commit()

# Assertions
assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
con_anki.close()

print("=" * 60)
print("[2026-10-19 Reconciled Final Successfully]")
print(f"  - Anki: {t19_cnt:,} reviews, {t19_sec:.2f}s ({round(t19_min, 2)}m / {int(t19_sec//60)}m {round(t19_sec%60, 2)}s, {min19_dt.strftime('%H:%M')}~{max19_dt.strftime('%H:%M')} KST)")
print(f"  - DB verified_minutes: {whole19_mins}m (rem: {rem19_sec}s)")
print(f"  - Voca ratings: Again {again19_c} ({again19_pct}%), Hard {hard19_c}, Good {good19_c}, Easy {easy19_c}")
print(f"  - Reading vocab: {read19_cnt} reviews, {round(read19_min, 2)}m")
print(f"  - Decks: {deck19_lines}")
print("=" * 60)
print("[2026-10-20 Recorded Today In-Progress Successfully]")
print(f"  - Anki: {t20_cnt:,} reviews, {t20_sec:.2f}s ({round(t20_min, 2)}m / {int(t20_sec//60)}m {round(t20_sec%60, 2)}s, {min20_dt.strftime('%H:%M')}~{max20_dt.strftime('%H:%M')} KST)")
print(f"  - DB verified_minutes: {whole20_mins}m (rem: {rem20_sec}s)")
print(f"  - Voca ratings: Again {again20_c} ({again20_pct}%), Hard {hard20_c}, Good {good20_c}, Easy {easy20_c}")
print(f"  - Decks: {deck20_lines}")
print("=" * 60)
