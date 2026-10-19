# -*- coding: utf-8 -*-
"""
Record Anki study stats and reconcile study sessions for:
- 2026-10-16 (Reconciled full day: 603 reviews, 8,243.70s + 2 tests 2,677s = 182m 0.70s)
- 2026-10-17 (570 reviews, 3,277.12s = 54m 37.12s)
- 2026-10-18 (605 reviews, 5,538.46s = 92m 18.46s)
- 2026-10-19 (537 reviews, 7,584.32s = 126m 24.32s, in progress)
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

# Backup DB first
backup_db = ROOT / 'database' / f'jlpt_learning_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
shutil.copy2(DB, backup_db)
print(f"[DB Backup created]: {backup_db.name}")

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_catchup_1019')
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
# 1. Reconcile 2026-10-16 Final
# =========================================================================
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

# Voca only
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

# Update 10-16 study_intervals
anki16_note = (
    f"[2026-10-16 Anki 회독 세션] {int(t16_sec//60)}분 {round(t16_sec%60, 2)}초 "
    f"(한끝 Voca 및 N2 독해어휘 회독: 총 {t16_cnt:,}회 실측, "
    f"고유 카드 {t16_dist}장, {min16_dt.strftime('%H:%M')}~{max16_dt.strftime('%H:%M')} KST)"
)
cur_db.execute('''
    UPDATE study_intervals
    SET started_at = ?,
        ended_at = ?,
        duration_seconds = ?,
        notes = ?
    WHERE session_date = '2026-10-16' AND source = 'anki'
''', (
    min16_dt.strftime('%Y-%m-%d %H:%M:%S'),
    max16_dt.strftime('%Y-%m-%d %H:%M:%S'),
    int(round(t16_sec)),
    anki16_note
))

# Sum 10-16 intervals
cur_db.execute('SELECT source, duration_seconds, notes FROM study_intervals WHERE session_date = ?', (d16_str,))
int16 = cur_db.fetchall()
q16_sec = sum(dur for src, dur, note in int16 if src != 'anki')
total16_sec = t16_sec + q16_sec
whole16_mins = int(total16_sec // 60)
rem16_sec = round(total16_sec % 60, 2)

q16_summaries = []
for src, dur, note in int16:
    if src != 'anki':
        m = dur // 60
        s = dur % 60
        t_str = f"{m}분 {s}초" if m > 0 else f"{s}초"
        q16_summaries.append(f"{note.split(']')[0].replace('[', '')}: {t_str}")

cur_db.execute('SELECT count(*), sum(total_items), sum(correct_items) FROM tests WHERE test_date = ?', (d16_str,))
q16_test_cnt, q16_tot_items, q16_cor_items = cur_db.fetchone()
acc16_pct = round(q16_cor_items / q16_tot_items * 100, 1) if q16_tot_items else 0
q16_part_str = f" 2) ★실전 훈련 {len(q16_summaries)}세션 실측 ({q16_sec//60}분 {q16_sec%60}초 / {q16_sec}초, {q16_cor_items}/{q16_tot_items} 정답, {acc16_pct}%)★: " + ", ".join(q16_summaries) + "."

session16_summary = (
    f"[{d16_str}] 당일 최종 누적 순수 학습시간 {whole16_mins}분 {rem16_sec}초 (약 {whole16_mins//60}시간 {whole16_mins%60}분 / {round(total16_sec/60.0, 2)}분, 마감). "
    f"1) ★Anki 회독 세션 {t16_cnt:,}회 실측 ({int(t16_sec//60)}분 {round(t16_sec%60, 2)}초 / {t16_sec:.2f}초, {min16_dt.strftime('%H:%M')}~{max16_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t16_dist}장)★: "
    f"[시간 공통 반영: 총 {round(t16_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {voca16_cnt:,}회({round(voca16_min, 1)}분, 고유 카드 {voca16_dist}장, 카드당 {voca16_sec_per_card}초) ➔ "
    f"Again {again16_c:,} ({again16_pct}%), Hard {hard16_c} ({round(hard16_c/voca16_cnt*100, 2)}%), "
    f"Good {good16_c} ({round(good16_c/voca16_cnt*100, 2)}%), Easy {easy16_c} ({round(easy16_c/voca16_cnt*100, 2)}%). "
    f"독해어휘 ➔ {read16_cnt}회({round(read16_min, 1)}분, {read16_dist}장). "
    f"주요 덱: {', '.join(deck16_lines[:6])}. "
    f"{q16_part_str} "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장). "
    f"잔여 {rem16_sec}초 보존."
)

cur_db.execute('''
    UPDATE study_sessions
    SET verified_minutes = ?,
        summary = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE session_date = '2026-10-16'
''', (whole16_mins, session16_summary))

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
    UPDATE anki_daily_stats
    SET scope_label = ?,
        payload_json = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE snapshot_date = '2026-10-16'
''', ('전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)', json.dumps(payload16, ensure_ascii=False)))


# =========================================================================
# 2. Record 2026-10-17 Final
# =========================================================================
d17_str = '2026-10-17'
s17_dt = datetime(2026, 10, 17, 4, 0, 0, tzinfo=KST)
e17_dt = s17_dt + timedelta(days=1)
s17_ms = int(s17_dt.timestamp() * 1000)
e17_ms = int(e17_dt.timestamp() * 1000)

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s17_ms, e17_ms))
t17_cnt, t17_tms, t17_dist, min17_id, max17_id = cur_anki.fetchone()
t17_sec = (t17_tms or 0) / 1000.0
t17_min = t17_sec / 60.0
min17_dt = datetime.fromtimestamp(min17_id / 1000.0, tz=KST)
max17_dt = datetime.fromtimestamp(max17_id / 1000.0, tz=KST)

# Voca only
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
''', (s17_ms, e17_ms))
voca17_cnt, voca17_tms, voca17_dist = cur_anki.fetchone()
voca17_cnt = voca17_cnt or 0
voca17_sec = (voca17_tms or 0) / 1000.0
voca17_min = voca17_sec / 60.0
voca17_sec_per_card = round(voca17_sec / voca17_cnt, 2) if voca17_cnt else 0

cur_anki.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s17_ms, e17_ms))
r17_voca = dict(cur_anki.fetchall())
again17_c = r17_voca.get(1, 0)
hard17_c = r17_voca.get(2, 0)
good17_c = r17_voca.get(3, 0)
easy17_c = r17_voca.get(4, 0)
again17_pct = round((again17_c / voca17_cnt * 100), 2) if voca17_cnt else 0.0

# Reading deck stats
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
''', (s17_ms, e17_ms))
read17_row = cur_anki.fetchone()
read17_cnt = read17_row[0] or 0
read17_sec = (read17_row[1] or 0) / 1000.0
read17_min = read17_sec / 60.0
read17_dist = read17_row[2] or 0

# Types (overall)
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s17_ms, e17_ms))
type17_map = dict(cur_anki.fetchall())
learn17_revs = type17_map.get(0, 0)
revs17_done = type17_map.get(1, 0)
relearn17_revs = type17_map.get(2, 0)

# First time cards exposed
cur_anki.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    WHERE r.id >= ? AND r.id < ?
      AND r.cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
''', (s17_ms, e17_ms, s17_ms))
first17_cards = cur_anki.fetchone()[0] or 0

# Decks breakdown
cur_anki.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s17_ms, e17_ms))
deck17_breakdown = []
deck17_lines = []
for did, d_cnt, d_dist, d_tms in cur_anki.fetchall():
    d_sec = (d_tms or 0) / 1000.0
    d_m = round(d_sec / 60.0, 1)
    d_name = deck_names.get(did, f"Deck {did}")
    deck17_breakdown.append({
        'deckId': did,
        'deckName': d_name,
        'reviews': d_cnt,
        'distinctCards': d_dist,
        'studyMinutes': d_m,
        'seconds': round(d_sec, 1)
    })
    deck17_lines.append(f"{d_name} {d_cnt:,}회({d_m}분)")

# 1. study_intervals for 2026-10-17
anki17_note = (
    f"[2026-10-17 Anki 회독 세션] {int(t17_sec//60)}분 {round(t17_sec%60, 2)}초 "
    f"(한끝 Voca 전량 집중 회독: 총 {t17_cnt:,}회 실측, "
    f"고유 카드 {t17_dist}장, {min17_dt.strftime('%H:%M')}~{max17_dt.strftime('%H:%M')} KST)"
)
cur_db.execute('DELETE FROM study_intervals WHERE session_date = ? AND source = "anki"', (d17_str,))
cur_db.execute('''
    INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
    VALUES (?, ?, ?, ?, 'completed', 'anki', ?)
''', (
    d17_str,
    min17_dt.strftime('%Y-%m-%d %H:%M:%S'),
    max17_dt.strftime('%Y-%m-%d %H:%M:%S'),
    int(round(t17_sec)),
    anki17_note
))

whole17_mins = int(t17_sec // 60)
rem17_sec = round(t17_sec % 60, 2)

session17_summary = (
    f"[{d17_str}] 당일 최종 누적 순수 학습시간 {whole17_mins}분 {rem17_sec}초 (약 {whole17_mins//60}시간 {whole17_mins%60}분 / {round(t17_sec/60.0, 2)}분, 마감). "
    f"1) ★Anki 회독 세션 {t17_cnt:,}회 실측 ({int(t17_sec//60)}분 {round(t17_sec%60, 2)}초 / {t17_sec:.2f}초, {min17_dt.strftime('%H:%M')}~{max17_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t17_dist}장)★: "
    f"[시간 공통 반영: 총 {round(t17_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {voca17_cnt:,}회({round(voca17_min, 1)}분, 고유 카드 {voca17_dist}장, 카드당 {voca17_sec_per_card}초) ➔ "
    f"Again {again17_c:,} ({again17_pct}%), Hard {hard17_c} ({round(hard17_c/voca17_cnt*100, 2)}%), "
    f"Good {good17_c} ({round(good17_c/voca17_cnt*100, 2)}%), Easy {easy17_c} ({round(easy17_c/voca17_cnt*100, 2)}%). "
    f"주요 덱: {', '.join(deck17_lines[:6])}. "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장). "
    f"잔여 {rem17_sec}초 보존."
)

cur_db.execute('''
    INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
    VALUES (?, ?, 0, ?)
    ON CONFLICT(session_date) DO UPDATE SET
        verified_minutes = excluded.verified_minutes,
        summary = excluded.summary,
        updated_at = CURRENT_TIMESTAMP
''', (d17_str, whole17_mins, session17_summary))

payload17 = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks_time_voca_ratings',
    'scopeLabel': '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)',
    'answeredCards': voca17_cnt,
    'totalAnsweredCardsAllDecks': t17_cnt,
    'studyMinutes': round(t17_min, 2),
    'secondsPerCard': voca17_sec_per_card,
    'againCount': again17_c,
    'againPct': again17_pct,
    'learningReviews': learn17_revs,
    'reviewsDone': revs17_done,
    'ratings': {
        'again': again17_c,
        'hard': hard17_c,
        'good': good17_c,
        'easy': easy17_c
    },
    'allDecksStats': {
        'totalReviews': t17_cnt,
        'totalStudyMinutes': round(t17_min, 2),
        'distinctCards': t17_dist,
        'readingVocabReviews': read17_cnt,
        'readingVocabMinutes': round(read17_min, 2),
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'decks': deck17_breakdown,
    'studyDay': d17_str,
    'ankiResourceStudyDayRaw': d17_str,
    'sourceNote': f"Anki revlog 2026-10-17 실측치 (시간 공통: {t17_cnt:,}회 {round(t17_min, 2)}분 / 정확도: 한끝 Voca {voca17_cnt:,}회 {again17_pct}% Again).",
    'inventory': {
        'n3_unseen': 0,
        'n2_unseen': 0,
        'n2_new_today': 0,
        'n3_new_today': 0,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 0,
        'grammar_unseen': 0,
        'new_cards_exposed_today': first17_cards
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
''', (d17_str, '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)', json.dumps(payload17, ensure_ascii=False), f'Anki revlog snapshot {d17_str}'))


# =========================================================================
# 3. Record 2026-10-18 Final
# =========================================================================
d18_str = '2026-10-18'
s18_dt = datetime(2026, 10, 18, 4, 0, 0, tzinfo=KST)
e18_dt = s18_dt + timedelta(days=1)
s18_ms = int(s18_dt.timestamp() * 1000)
e18_ms = int(e18_dt.timestamp() * 1000)

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s18_ms, e18_ms))
t18_cnt, t18_tms, t18_dist, min18_id, max18_id = cur_anki.fetchone()
t18_sec = (t18_tms or 0) / 1000.0
t18_min = t18_sec / 60.0
min18_dt = datetime.fromtimestamp(min18_id / 1000.0, tz=KST)
max18_dt = datetime.fromtimestamp(max18_id / 1000.0, tz=KST)

# Voca only
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
''', (s18_ms, e18_ms))
voca18_cnt, voca18_tms, voca18_dist = cur_anki.fetchone()
voca18_cnt = voca18_cnt or 0
voca18_sec = (voca18_tms or 0) / 1000.0
voca18_min = voca18_sec / 60.0
voca18_sec_per_card = round(voca18_sec / voca18_cnt, 2) if voca18_cnt else 0

cur_anki.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s18_ms, e18_ms))
r18_voca = dict(cur_anki.fetchall())
again18_c = r18_voca.get(1, 0)
hard18_c = r18_voca.get(2, 0)
good18_c = r18_voca.get(3, 0)
easy18_c = r18_voca.get(4, 0)
again18_pct = round((again18_c / voca18_cnt * 100), 2) if voca18_cnt else 0.0

# Reading deck stats
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
''', (s18_ms, e18_ms))
read18_row = cur_anki.fetchone()
read18_cnt = read18_row[0] or 0
read18_sec = (read18_row[1] or 0) / 1000.0
read18_min = read18_sec / 60.0
read18_dist = read18_row[2] or 0

# Types (overall)
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s18_ms, e18_ms))
type18_map = dict(cur_anki.fetchall())
learn18_revs = type18_map.get(0, 0)
revs18_done = type18_map.get(1, 0)
relearn18_revs = type18_map.get(2, 0)

# First time cards exposed
cur_anki.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    WHERE r.id >= ? AND r.id < ?
      AND r.cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
''', (s18_ms, e18_ms, s18_ms))
first18_cards = cur_anki.fetchone()[0] or 0

# Decks breakdown
cur_anki.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s18_ms, e18_ms))
deck18_breakdown = []
deck18_lines = []
for did, d_cnt, d_dist, d_tms in cur_anki.fetchall():
    d_sec = (d_tms or 0) / 1000.0
    d_m = round(d_sec / 60.0, 1)
    d_name = deck_names.get(did, f"Deck {did}")
    deck18_breakdown.append({
        'deckId': did,
        'deckName': d_name,
        'reviews': d_cnt,
        'distinctCards': d_dist,
        'studyMinutes': d_m,
        'seconds': round(d_sec, 1)
    })
    deck18_lines.append(f"{d_name} {d_cnt:,}회({d_m}분)")

# 1. study_intervals for 2026-10-18
anki18_note = (
    f"[2026-10-18 Anki 회독 세션] {int(t18_sec//60)}분 {round(t18_sec%60, 2)}초 "
    f"(한끝 Voca 전량 집중 회독: 총 {t18_cnt:,}회 실측, "
    f"고유 카드 {t18_dist}장, {min18_dt.strftime('%H:%M')}~{max18_dt.strftime('%H:%M')} KST)"
)
cur_db.execute('DELETE FROM study_intervals WHERE session_date = ? AND source = "anki"', (d18_str,))
cur_db.execute('''
    INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
    VALUES (?, ?, ?, ?, 'completed', 'anki', ?)
''', (
    d18_str,
    min18_dt.strftime('%Y-%m-%d %H:%M:%S'),
    max18_dt.strftime('%Y-%m-%d %H:%M:%S'),
    int(round(t18_sec)),
    anki18_note
))

whole18_mins = int(t18_sec // 60)
rem18_sec = round(t18_sec % 60, 2)

session18_summary = (
    f"[{d18_str}] 당일 최종 누적 순수 학습시간 {whole18_mins}분 {rem18_sec}초 (약 {whole18_mins//60}시간 {whole18_mins%60}분 / {round(t18_sec/60.0, 2)}분, 마감). "
    f"1) ★Anki 회독 세션 {t18_cnt:,}회 실측 ({int(t18_sec//60)}분 {round(t18_sec%60, 2)}초 / {t18_sec:.2f}초, {min18_dt.strftime('%H:%M')}~{max18_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t18_dist}장)★: "
    f"[시간 공통 반영: 총 {round(t18_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {voca18_cnt:,}회({round(voca18_min, 1)}분, 고유 카드 {voca18_dist}장, 카드당 {voca18_sec_per_card}초) ➔ "
    f"Again {again18_c:,} ({again18_pct}%), Hard {hard18_c} ({round(hard18_c/voca18_cnt*100, 2)}%), "
    f"Good {good18_c} ({round(good18_c/voca18_cnt*100, 2)}%), Easy {easy18_c} ({round(easy18_c/voca18_cnt*100, 2)}%). "
    f"주요 덱: {', '.join(deck18_lines[:6])}. "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장). "
    f"잔여 {rem18_sec}초 보존."
)

cur_db.execute('''
    INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
    VALUES (?, ?, 0, ?)
    ON CONFLICT(session_date) DO UPDATE SET
        verified_minutes = excluded.verified_minutes,
        summary = excluded.summary,
        updated_at = CURRENT_TIMESTAMP
''', (d18_str, whole18_mins, session18_summary))

payload18 = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks_time_voca_ratings',
    'scopeLabel': '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)',
    'answeredCards': voca18_cnt,
    'totalAnsweredCardsAllDecks': t18_cnt,
    'studyMinutes': round(t18_min, 2),
    'secondsPerCard': voca18_sec_per_card,
    'againCount': again18_c,
    'againPct': again18_pct,
    'learningReviews': learn18_revs,
    'reviewsDone': revs18_done,
    'ratings': {
        'again': again18_c,
        'hard': hard18_c,
        'good': good18_c,
        'easy': easy18_c
    },
    'allDecksStats': {
        'totalReviews': t18_cnt,
        'totalStudyMinutes': round(t18_min, 2),
        'distinctCards': t18_dist,
        'readingVocabReviews': read18_cnt,
        'readingVocabMinutes': round(read18_min, 2),
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'decks': deck18_breakdown,
    'studyDay': d18_str,
    'ankiResourceStudyDayRaw': d18_str,
    'sourceNote': f"Anki revlog 2026-10-18 실측치 (시간 공통: {t18_cnt:,}회 {round(t18_min, 2)}분 / 정확도: 한끝 Voca {voca18_cnt:,}회 {again18_pct}% Again).",
    'inventory': {
        'n3_unseen': 0,
        'n2_unseen': 0,
        'n2_new_today': 0,
        'n3_new_today': 0,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 0,
        'grammar_unseen': 0,
        'new_cards_exposed_today': first18_cards
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
''', (d18_str, '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)', json.dumps(payload18, ensure_ascii=False), f'Anki revlog snapshot {d18_str}'))


# =========================================================================
# 4. Record 2026-10-19 In-Progress
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
    f"(한끝 Voca 전량 집중 회독: 총 {t19_cnt:,}회 실측, "
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
    f"[{d19_str}] 당일 현재 누적 순수 학습시간 {whole19_mins}분 {rem19_sec}초 (약 {whole19_mins//60}시간 {whole19_mins%60}분 / {round(t19_sec/60.0, 2)}분, 진행 중). "
    f"1) ★Anki 회독 세션 {t19_cnt:,}회 실측 ({int(t19_sec//60)}분 {round(t19_sec%60, 2)}초 / {t19_sec:.2f}초, {min19_dt.strftime('%H:%M')}~{max19_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t19_dist}장)★: "
    f"[시간 공통 반영: 총 {round(t19_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {voca19_cnt:,}회({round(voca19_min, 1)}분, 고유 카드 {voca19_dist}장, 카드당 {voca19_sec_per_card}초) ➔ "
    f"Again {again19_c:,} ({again19_pct}%), Hard {hard19_c} ({round(hard19_c/voca19_cnt*100, 2)}%), "
    f"Good {good19_c} ({round(good19_c/voca19_cnt*100, 2)}%), Easy {easy19_c} ({round(easy19_c/voca19_cnt*100, 2)}%). "
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

con_db.commit()

# Assertions
assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
con_anki.close()

print("=" * 60)
print("[2026-10-16 Reconciled Successfully]")
print(f"  - Anki: {t16_cnt:,} reviews, {t16_sec:.2f}s ({round(t16_min, 2)}m / {int(t16_sec//60)}m {round(t16_sec%60, 2)}s, {min16_dt.strftime('%H:%M')}~{max16_dt.strftime('%H:%M')} KST)")
print(f"  - Combined with quizzes ({q16_sec}s): {total16_sec:.2f}s -> verified_minutes = {whole16_mins}m (rem: {rem16_sec}s)")
print(f"  - Voca ratings: Again {again16_c} ({again16_pct}%), Hard {hard16_c}, Good {good16_c}, Easy {easy16_c}")
print(f"  - Decks: {deck16_lines}")
print("=" * 60)
print("[2026-10-17 Recorded Successfully]")
print(f"  - Anki: {t17_cnt:,} reviews, {t17_sec:.2f}s ({round(t17_min, 2)}m / {int(t17_sec//60)}m {round(t17_sec%60, 2)}s, {min17_dt.strftime('%H:%M')}~{max17_dt.strftime('%H:%M')} KST)")
print(f"  - DB verified_minutes: {whole17_mins}m (rem: {rem17_sec}s)")
print(f"  - Voca ratings: Again {again17_c} ({again17_pct}%), Hard {hard17_c}, Good {good17_c}, Easy {easy17_c}")
print(f"  - Decks: {deck17_lines}")
print("=" * 60)
print("[2026-10-18 Recorded Successfully]")
print(f"  - Anki: {t18_cnt:,} reviews, {t18_sec:.2f}s ({round(t18_min, 2)}m / {int(t18_sec//60)}m {round(t18_sec%60, 2)}s, {min18_dt.strftime('%H:%M')}~{max18_dt.strftime('%H:%M')} KST)")
print(f"  - DB verified_minutes: {whole18_mins}m (rem: {rem18_sec}s)")
print(f"  - Voca ratings: Again {again18_c} ({again18_pct}%), Hard {hard18_c}, Good {good18_c}, Easy {easy18_c}")
print(f"  - Decks: {deck18_lines}")
print("=" * 60)
print("[2026-10-19 Recorded Successfully]")
print(f"  - Anki: {t19_cnt:,} reviews, {t19_sec:.2f}s ({round(t19_min, 2)}m / {int(t19_sec//60)}m {round(t19_sec%60, 2)}s, {min19_dt.strftime('%H:%M')}~{max19_dt.strftime('%H:%M')} KST)")
print(f"  - DB verified_minutes: {whole19_mins}m (rem: {rem19_sec}s)")
print(f"  - Voca ratings: Again {again19_c} ({again19_pct}%), Hard {hard19_c}, Good {good19_c}, Easy {easy19_c}")
print(f"  - Decks: {deck19_lines}")
print("=" * 60)
