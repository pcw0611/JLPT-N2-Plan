# -*- coding: utf-8 -*-
"""
Record Anki study stats for 2026-10-15 (and reconcile 2026-10-14 final stats) in database/jlpt_learning.db.

2026-10-14 (Reconciled Final):
- Anki: 635 reviews, 7,541.78s (125m 41.78s / 125.70m), 377 distinct cards (07:48 ~ 22:30 KST)
- Online Quizzes: 3 sessions, 17,348s (289m 8s), 150/165 correct (90.9%)
- Total learning time: 24,889.78s = 414m 49.78s (approx 6h 54m 50s / 414.83m, verified_minutes = 414m, rem: 49.78s)

2026-10-15:
- Anki: 485 reviews, 6,374.29s (106m 14.29s / 106.24m / ~1h 46m 14s), 271 distinct cards (10:07 ~ 16:36 KST)
- All 485 reviews in JLPT 한끝 Voca decks
- Ratings: Again 214 (44.12%), Hard 6 (1.24%), Good 7 (1.44%), Easy 258 (53.20%)
- Types: Review 271, Relearn 214
- Queue: new 366, learning 28, review 3048 (total 3442)
- Total learning time: 6,374.29s = 106m 14.29s (verified_minutes = 106m, rem: 14.29s, in progress)
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
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1015_record')
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
# 1. Reconcile 2026-10-14 Final
# ==========================================
d14_str = '2026-10-14'
s14_dt = datetime(2026, 10, 14, 4, 0, 0, tzinfo=KST)
e14_dt = s14_dt + timedelta(days=1)
s14_ms = int(s14_dt.timestamp() * 1000)
e14_ms = int(e14_dt.timestamp() * 1000)

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s14_ms, e14_ms))
t14_cnt, t14_tms, t14_dist, min14_id, max14_id = cur_anki.fetchone()
t14_sec = (t14_tms or 0) / 1000.0
t14_min = t14_sec / 60.0
min14_dt = datetime.fromtimestamp(min14_id / 1000.0, tz=KST)
max14_dt = datetime.fromtimestamp(max14_id / 1000.0, tz=KST)

# Ratings 10-14 (Voca only for accuracy metric)
cur_anki.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
''', (s14_ms, e14_ms))
voca14_cnt, voca14_tms, voca14_dist = cur_anki.fetchone()
voca14_sec = (voca14_tms or 0) / 1000.0
voca14_min = voca14_sec / 60.0
voca14_sec_per_card = round(voca14_sec / voca14_cnt, 2) if voca14_cnt else 0

cur_anki.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s14_ms, e14_ms))
r14_voca = dict(cur_anki.fetchall())
again14_c = r14_voca.get(1, 0)
hard14_c = r14_voca.get(2, 0)
good14_c = r14_voca.get(3, 0)
easy14_c = r14_voca.get(4, 0)
again14_pct = round((again14_c / voca14_cnt * 100), 2) if voca14_cnt else 0.0

# 10-14 Decks breakdown
cur_anki.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s14_ms, e14_ms))
deck14_breakdown = []
deck14_lines = []
for did, d_cnt, d_dist, d_tms in cur_anki.fetchall():
    d_sec = (d_tms or 0) / 1000.0
    d_m = round(d_sec / 60.0, 1)
    d_name = deck_names.get(did, f"Deck {did}")
    deck14_breakdown.append({
        'deckId': did,
        'deckName': d_name,
        'reviews': d_cnt,
        'distinctCards': d_dist,
        'studyMinutes': d_m,
        'seconds': round(d_sec, 1)
    })
    deck14_lines.append(f"{d_name} {d_cnt:,}회({d_m}분)")

# Update 10-14 Anki interval
anki14_note = (
    f"[2026-10-14 Anki 회독 세션] {int(t14_sec//60)}분 {round(t14_sec%60, 2)}초 "
    f"(한끝 Voca 및 N2 독해어휘 회독: 총 {t14_cnt:,}회 실측, "
    f"고유 카드 {t14_dist}장, {min14_dt.strftime('%H:%M')}~{max14_dt.strftime('%H:%M')} KST)"
)
cur_db.execute('''
    UPDATE study_intervals
    SET started_at = ?,
        ended_at = ?,
        duration_seconds = ?,
        notes = ?
    WHERE session_date = '2026-10-14' AND source = 'anki'
''', (
    min14_dt.strftime('%Y-%m-%d %H:%M:%S'),
    max14_dt.strftime('%Y-%m-%d %H:%M:%S'),
    int(round(t14_sec)),
    anki14_note
))

# Sum 10-14 intervals
cur_db.execute('SELECT source, duration_seconds, notes FROM study_intervals WHERE session_date = ?', (d14_str,))
int14 = cur_db.fetchall()
q14_sec = sum(dur for src, dur, note in int14 if src != 'anki')
total14_sec = t14_sec + q14_sec
whole14_mins = int(total14_sec // 60)
rem14_sec = round(total14_sec % 60, 2)

q14_summaries = []
for src, dur, note in int14:
    if src != 'anki':
        m = dur // 60
        s = dur % 60
        t_str = f"{m}분 {s}초" if m > 0 else f"{s}초"
        q14_summaries.append(f"{note.split(']')[0].replace('[', '')}: {t_str}")

q14_part_str = f" 2) ★실전 훈련 {len(q14_summaries)}세션 실측 ({q14_sec//60}분 {q14_sec%60}초 / {q14_sec}초, 150/165 정답)★: " + ", ".join(q14_summaries) + "."

session14_summary = (
    f"[{d14_str}] 당일 최종 누적 순수 학습시간 {whole14_mins}분 {rem14_sec}초 (약 {whole14_mins//60}시간 {whole14_mins%60}분 / {round(total14_sec/60.0, 2)}분, 마감). "
    f"1) ★Anki 회독 세션 {t14_cnt:,}회 실측 ({int(t14_sec//60)}분 {round(t14_sec%60, 2)}초 / {t14_sec:.2f}초, {min14_dt.strftime('%H:%M')}~{max14_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t14_dist}장)★: "
    f"[시간 공통 반영: 총 {round(t14_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {voca14_cnt:,}회({round(voca14_min, 1)}분, 고유 카드 {voca14_dist}장, 카드당 {voca14_sec_per_card}초) ➔ "
    f"Again {again14_c:,} ({again14_pct}%), Hard {hard14_c} ({round(hard14_c/voca14_cnt*100, 2)}%), "
    f"Good {good14_c} ({round(good14_c/voca14_cnt*100, 2)}%), Easy {easy14_c} ({round(easy14_c/voca14_cnt*100, 2)}%). "
    f"신규 단어장 암기 ➔ 독해어휘·변화문형 150회(36.4분, 48장 집중 회독). "
    f"주요 덱: {', '.join(deck14_lines[:6])}. "
    f"{q14_part_str} "
    f"잔여 {rem14_sec}초 보존."
)

cur_db.execute('''
    UPDATE study_sessions
    SET verified_minutes = ?,
        summary = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE session_date = '2026-10-14'
''', (whole14_mins, session14_summary))

payload14 = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks_time_voca_ratings',
    'scopeLabel': '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)',
    'answeredCards': voca14_cnt,
    'totalAnsweredCardsAllDecks': t14_cnt,
    'studyMinutes': round(t14_min, 2),
    'secondsPerCard': voca14_sec_per_card,
    'againCount': again14_c,
    'againPct': again14_pct,
    'learningReviews': 150,
    'reviewsDone': 485,
    'ratings': {
        'again': again14_c,
        'hard': hard14_c,
        'good': good14_c,
        'easy': easy14_c
    },
    'allDecksStats': {
        'totalReviews': t14_cnt,
        'totalStudyMinutes': round(t14_min, 2),
        'distinctCards': t14_dist,
        'readingAndChangeDecksReviews': 150,
        'readingAndChangeDecksMinutes': 36.4
    },
    'cardsRemaining': {
        'new': 366,
        'learning': 28,
        'review': 3048
    },
    'decks': deck14_breakdown,
    'studyDay': d14_str,
    'ankiResourceStudyDayRaw': d14_str,
    'sourceNote': f"Anki revlog 2026-10-14 실측치 (시간 공통: {t14_cnt:,}회 {round(t14_min, 2)}분 / 정확도: 한끝 Voca {voca14_cnt:,}회 {again14_pct}% Again).",
    'inventory': {
        'n3_unseen': 0,
        'n2_unseen': 0,
        'n2_new_today': 0,
        'n3_new_today': 0,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 0,
        'grammar_unseen': 0,
        'new_cards_exposed_today': 48
    }
}

cur_db.execute('''
    UPDATE anki_daily_stats
    SET scope_label = ?,
        payload_json = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE snapshot_date = '2026-10-14'
''', ('전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)', json.dumps(payload14, ensure_ascii=False)))


# ==========================================
# 2. Record 2026-10-15 (Today)
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
t15_sec_per_card = round(t15_sec / t15_cnt, 2) if t15_cnt else 0

# Ratings
cur_anki.execute('''
    SELECT ease, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY ease
''', (s15_ms, e15_ms))
r15 = dict(cur_anki.fetchall())
again15_c = r15.get(1, 0)
hard15_c = r15.get(2, 0)
good15_c = r15.get(3, 0)
easy15_c = r15.get(4, 0)
again15_pct = round((again15_c / t15_cnt * 100), 2) if t15_cnt else 0.0

# Types
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s15_ms, e15_ms))
type15_map = dict(cur_anki.fetchall())
learn15_revs = type15_map.get(0, 0) + type15_map.get(2, 0) # 214 relearn
revs15_done = type15_map.get(1, 0) + type15_map.get(3, 0)  # 271 review

# Decks
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

# 1. study_intervals for 2026-10-15
cur_db.execute('SELECT id FROM study_intervals WHERE session_date = ? AND source = "anki"', (d15_str,))
existing15_anki = cur_db.fetchone()
anki15_note = (
    f"[2026-10-15 Anki 회독 세션] {int(t15_sec//60)}분 {round(t15_sec%60, 2)}초 "
    f"(한끝 Voca 전범위 집중 회독: 총 {t15_cnt:,}회 실측, "
    f"고유 카드 {t15_dist}장, {min15_dt.strftime('%H:%M')}~{max15_dt.strftime('%H:%M')} KST)"
)

if existing15_anki:
    cur_db.execute('''
        UPDATE study_intervals
        SET started_at = ?,
            ended_at = ?,
            duration_seconds = ?,
            notes = ?
        WHERE id = ?
    ''', (
        min15_dt.strftime('%Y-%m-%d %H:%M:%S'),
        max15_dt.strftime('%Y-%m-%d %H:%M:%S'),
        int(round(t15_sec)),
        anki15_note,
        existing15_anki[0]
    ))
else:
    cur_db.execute('''
        INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
        VALUES (?, ?, ?, ?, 'completed', 'anki', ?)
    ''', (
        d15_str,
        min15_dt.strftime('%Y-%m-%d %H:%M:%S'),
        max15_dt.strftime('%Y-%m-%d %H:%M:%S'),
        int(round(t15_sec)),
        anki15_note
    ))

# 2. Sum all intervals for 2026-10-15
cur_db.execute('SELECT source, duration_seconds, notes FROM study_intervals WHERE session_date = ?', (d15_str,))
int15 = cur_db.fetchall()
q15_sec = sum(dur for src, dur, note in int15 if src != 'anki')
total15_sec = t15_sec + q15_sec
whole15_mins = int(total15_sec // 60)
rem15_sec = round(total15_sec % 60, 2)

session15_summary = (
    f"[{d15_str}] 당일 현재 누적 순수 학습시간 {whole15_mins}분 {rem15_sec}초 (약 {whole15_mins//60}시간 {whole15_mins%60}분 / {round(total15_sec/60.0, 2)}분, 진행 중). "
    f"1) ★Anki 집중 회독 세션 {t15_cnt:,}회 실측 ({int(t15_sec//60)}분 {round(t15_sec%60, 2)}초 / {t15_sec:.2f}초, {min15_dt.strftime('%H:%M')}~{max15_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t15_dist}장, 카드당 {t15_sec_per_card}초)★: "
    f"[전체 덱 실측: {round(t15_min, 1)}분, 전량 한끝 Voca 덱] "
    f"주요 덱: {', '.join(deck15_lines[:6])}. "
    f"학습 반응: Again {again15_c:,} ({again15_pct}%), Hard {hard15_c} ({round(hard15_c/t15_cnt*100, 2)}%), "
    f"Good {good15_c} ({round(good15_c/t15_cnt*100, 2)}%), Easy {easy15_c} ({round(easy15_c/t15_cnt*100, 2)}%). "
    f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장). "
    f"잔여 {rem15_sec}초 보존."
)

cur_db.execute('''
    INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
    VALUES (?, ?, 0, ?)
    ON CONFLICT(session_date) DO UPDATE SET
        verified_minutes = excluded.verified_minutes,
        summary = excluded.summary,
        updated_at = CURRENT_TIMESTAMP
''', (d15_str, whole15_mins, session15_summary))

payload15 = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks_time_voca_ratings',
    'scopeLabel': '전체 덱 (시간 공통 / 한끝 Voca 전량)',
    'answeredCards': t15_cnt,
    'totalAnsweredCardsAllDecks': t15_cnt,
    'studyMinutes': round(t15_min, 2),
    'secondsPerCard': t15_sec_per_card,
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
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'decks': deck15_breakdown,
    'studyDay': d15_str,
    'ankiResourceStudyDayRaw': d15_str,
    'sourceNote': f"Anki revlog 2026-10-15 실측치 (전체 덱: {t15_cnt:,}회 {round(t15_min, 2)}분 / 정확도: 한끝 Voca 전량 {again15_pct}% Again).",
    'inventory': {
        'n3_unseen': 0,
        'n2_unseen': 0,
        'n2_new_today': 0,
        'n3_new_today': 0,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 0,
        'grammar_unseen': 0,
        'new_cards_exposed_today': 0
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
''', (d15_str, '전체 덱 (시간 공통 / 한끝 Voca 전량)', json.dumps(payload15, ensure_ascii=False), f'Anki revlog snapshot {d15_str}'))

con_db.commit()

# Assertions
assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
con_anki.close()

print("=" * 60)
print("[2026-10-14 Reconciled Final]")
print(f"  - Anki: {t14_cnt:,} reviews, {t14_sec:.2f}s ({round(t14_min, 1)}m), {t14_dist} distinct cards")
print(f"  - Quizzes: {len(q14_summaries)} sessions, {q14_sec}s ({q14_sec//60}m {q14_sec%60}s)")
print(f"  - Total: {whole14_mins}m {rem14_sec}s (DB verified_minutes={whole14_mins})")
print("-" * 60)
print("[2026-10-15 Recorded Successfully]")
print(f"  - Anki: {t15_cnt:,} reviews, {t15_sec:.2f}s ({round(t15_min, 2)}m / {int(t15_sec//60)}m {round(t15_sec%60, 2)}s, {min15_dt.strftime('%H:%M')}~{max15_dt.strftime('%H:%M')} KST)")
print(f"  - DB verified_minutes: {whole15_mins}m (rem: {rem15_sec}s)")
print(f"  - Ratings: Again {again15_c} ({again15_pct}%), Hard {hard15_c}, Good {good15_c}, Easy {easy15_c}")
print(f"  - Decks: {deck15_lines}")
print("=" * 60)
