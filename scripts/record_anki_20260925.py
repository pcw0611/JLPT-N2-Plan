# -*- coding: utf-8 -*-
"""Record Anki study stats and study session for 2026-09-25."""

import sqlite3
import json
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'database' / 'jlpt_learning.db'
DATE = '2026-09-25'

# 1. Inspect Anki collection
ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_0925')
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
s_dt = datetime(2026, 9, 25, 4, 0, 0, tzinfo=KST)
e_dt = datetime(2026, 9, 26, 4, 0, 0, tzinfo=KST)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s_ms, e_ms))
cnt, total_time_ms, distinct_cards = cur_anki.fetchone()
cnt = cnt or 0
total_time_ms = total_time_ms or 0
sec = total_time_ms / 1000.0
anki_mins = sec / 60.0
sec_per_card = round(sec / cnt, 2) if cnt > 0 else 0

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
again_pct = round((again_c / cnt) * 100, 2) if cnt > 0 else 0

# Review types
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s_ms, e_ms))
type_map = dict(cur_anki.fetchall())
learn_revs = type_map.get(0, 0) + type_map.get(2, 0)
revs_done = type_map.get(1, 0)

# Deck breakdown
cur_anki.execute('''
    SELECT c.did, count(*), count(distinct r.cid), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s_ms, e_ms))
deck_breakdown = []
for did, d_count, d_dist, d_tms in cur_anki.fetchall():
    dname = deck_names.get(did, f'did:{did}')
    d_sec = d_tms / 1000.0
    deck_breakdown.append({
        'name': dname,
        'reviews': d_count,
        'cards': d_dist,
        'minutes': round(d_sec / 60.0, 1),
        'seconds': round(d_sec, 1)
    })

# Check grammar reviewed today
cur_anki.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ? AND c.did IN (
        SELECT id FROM decks WHERE name LIKE '%문법%' OR name LIKE '%01%'
    )
''', (s_ms, e_ms))
grammar_reviewed_today = cur_anki.fetchone()[0] or 0

con_anki.close()

# Whole minutes & remainder seconds
whole_mins = int(sec // 60)
rem_sec = round(sec % 60, 2)

SUMMARY_PAYLOAD = {
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
    'studyDay': DATE,
    'ankiResourceStudyDayRaw': DATE,
    'sourceNote': (
        f'Anki revlog {DATE} 실측치 (총 {cnt:,}회, {whole_mins}분 {rem_sec}초 / {round(anki_mins, 2)}분). '
        f'고유 카드 {distinct_cards}장 회독 (카드당 평균 {sec_per_card}초). '
        f'N2 집중 회독 516회(149장, 94.1분 / 1시간 34분 8초, 1,169장 전량 1차 완독 회독 유지). '
        f'N3 79회(33장, 10.7분), N2 문법 001-150 예문 복습 37회(32장, 10.0분), N5 8회(8장, 1.3분), '
        f'공통 의성어/의태어 2회(1장, 0.1분), N4 2회(2장, 0.1분), 공통 의상 1회(1장, 0.1분).'
    ),
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

SESSION_SUMMARY = (
    f"[{DATE}] 총 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(anki_mins, 2)}분). "
    f"Anki 단어·문법 세션 {cnt:,}회 실측 (고유 카드 {distinct_cards}장, 카드당 평균 {sec_per_card}초): "
    f"1) JLPT 한끝 Voca 4-N2 고밀도 회독 516회(149장, 94.1분 / 1시간 34분 8초, 1,169장 1차 완독 전량 회독 유지). "
    f"2) N3 79회(33장, 10.7분), N2 문법 001-150 예문 복습 37회(32장, 10.0분), N5 8회(8장, 1.3분), "
    f"공통 의성어·의태어 2회(1장, 0.1분), N4 2회(2장, 0.1분), 공통 의상 1회(1장, 0.1분) 복습 유지. "
    f"3) 학습 반응: Again {again_c:,} ({again_pct}%), Hard {hard_c} ({round(hard_c/cnt*100, 2)}%), Good {good_c} ({round(good_c/cnt*100, 2)}%), Easy {easy_c} ({round(easy_c/cnt*100, 2)}%). "
    f"잔여 {rem_sec}초 보존."
)

con_db = sqlite3.connect(DB)
with con_db:
    # 1. Update or Insert study_sessions
    cur_db = con_db.cursor()
    cur_db.execute('''
        INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
        VALUES (?, ?, 0, ?)
        ON CONFLICT(session_date) DO UPDATE SET
            verified_minutes = excluded.verified_minutes,
            summary = excluded.summary,
            updated_at = CURRENT_TIMESTAMP
    ''', (DATE, whole_mins, SESSION_SUMMARY))

    # 2. Update or Insert anki_daily_stats
    cur_db.execute('''
        INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(snapshot_date) DO UPDATE SET
            scope_label = excluded.scope_label,
            payload_json = excluded.payload_json,
            source_filename = excluded.source_filename,
            captured_at = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
    ''', (DATE, '전체 덱', json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), f'Anki revlog snapshot {DATE}'))

    assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
print(f"Successfully recorded Anki stats for {DATE}: {cnt:,} reviews, {whole_mins}m {rem_sec}s ({round(anki_mins, 2)}m)")
