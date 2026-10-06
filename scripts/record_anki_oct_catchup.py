# -*- coding: utf-8 -*-
"""Record Anki study stats and study sessions for 2026-10-01 through 2026-10-06."""

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

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_catchup')
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

dates = [
    '2026-10-01',
    '2026-10-02',
    '2026-10-03',
    '2026-10-04',
    '2026-10-05',
    '2026-10-06'
]

results = {}

for d_str in dates:
    y, m, d = map(int, d_str.split('-'))
    s_dt = datetime(y, m, d, 4, 0, 0, tzinfo=KST)
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
    total_time_ms = total_time_ms or 0
    sec = total_time_ms / 1000.0
    anki_mins = sec / 60.0
    sec_per_card = round(sec / cnt, 2) if cnt > 0 else 0

    min_dt_str = datetime.fromtimestamp(min_id/1000, tz=KST).strftime('%H:%M') if min_id else ''
    max_dt_str = datetime.fromtimestamp(max_id/1000, tz=KST).strftime('%H:%M') if max_id else ''

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
    deck_lines = []
    for did, d_count, d_dist, d_tms in cur_anki.fetchall():
        dname = deck_names.get(did, f'did:{did}')
        d_sec = d_tms / 1000.0
        d_mins = round(d_sec / 60.0, 1)
        deck_breakdown.append({
            'name': dname,
            'reviews': d_count,
            'cards': d_dist,
            'minutes': d_mins,
            'seconds': round(d_sec, 1)
        })
        deck_lines.append(f"{dname}: {d_count:,}회({d_dist}장, {d_mins}분)")

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

    whole_mins = int(sec // 60)
    rem_sec = round(sec % 60, 2)

    deck_summary_str = ", ".join(deck_lines[:5])
    if len(deck_lines) > 5:
        deck_summary_str += f" 외 {len(deck_lines)-5}개 덱"

    is_today = (d_str == '2026-10-06')
    prefix = "당일 현재 누적 순수 학습시간" if is_today else "총 순수 학습시간"
    status_suffix = " (04:00~06:09 KST 현재 진행 중)" if is_today else ""

    session_summary = (
        f"[{d_str}] {prefix} {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(anki_mins, 2)}분{status_suffix}). "
        f"★Anki 집중 세션 {cnt:,}회 실측 ({min_dt_str}~{max_dt_str} 완수, 고유 카드 {distinct_cards}장, 카드당 평균 {sec_per_card}초)★: "
        f"1) 주요 덱 회독: {deck_summary_str}. "
        f"2) 학습 반응: Again {again_c:,} ({again_pct}%), Hard {hard_c} ({round(hard_c/cnt*100, 2) if cnt else 0}%), "
        f"Good {good_c} ({round(good_c/cnt*100, 2) if cnt else 0}%), Easy {easy_c} ({round(easy_c/cnt*100, 2) if cnt else 0}%). "
        f"3) 컬렉션 재학습 큐 {learn_rem}장 타이트 소화 관리 중. 잔여 {rem_sec}초 보존."
    )

    source_note = (
        f"Anki revlog {d_str} 실측치 (총 {cnt:,}회, {whole_mins}분 {rem_sec}초 / {round(anki_mins, 2)}분{status_suffix}). "
        f"고유 카드 {distinct_cards}장 회독 (카드당 평균 {sec_per_card}초). "
        f"주요 덱: {deck_summary_str}. "
        f"재학습 큐 {learn_rem}장 타이트 소화 관리 중."
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

    results[d_str] = {
        'cnt': cnt,
        'whole_mins': whole_mins,
        'rem_sec': rem_sec,
        'anki_mins': anki_mins,
        'sec_per_card': sec_per_card,
        'distinct_cards': distinct_cards,
        'min_dt_str': min_dt_str,
        'max_dt_str': max_dt_str,
        'again_c': again_c,
        'again_pct': again_pct,
        'hard_c': hard_c,
        'good_c': good_c,
        'easy_c': easy_c,
        'learn_rem': learn_rem,
        'deck_breakdown': deck_breakdown,
        'session_summary': session_summary,
        'summary_payload': summary_payload
    }

con_anki.close()

# Update Database
con_db = sqlite3.connect(DB)
with con_db:
    cur_db = con_db.cursor()
    for d_str, data in results.items():
        # Update study_sessions
        cur_db.execute('''
            INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
            VALUES (?, ?, 0, ?)
            ON CONFLICT(session_date) DO UPDATE SET
                verified_minutes = excluded.verified_minutes,
                summary = excluded.summary,
                updated_at = CURRENT_TIMESTAMP
        ''', (d_str, data['whole_mins'], data['session_summary']))

        # Update anki_daily_stats
        cur_db.execute('''
            INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(snapshot_date) DO UPDATE SET
                scope_label = excluded.scope_label,
                payload_json = excluded.payload_json,
                source_filename = excluded.source_filename,
                captured_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
        ''', (d_str, '전체 덱', json.dumps(data['summary_payload'], ensure_ascii=False), f'Anki revlog snapshot {d_str}'))

        print(f"[{d_str}] DB Updated: {data['cnt']:,} reviews, {data['whole_mins']}m {data['rem_sec']}s ({round(data['anki_mins'], 2)}m)")

    assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
print("All dates 2026-10-01 to 2026-10-06 successfully updated in database!")
