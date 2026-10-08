# -*- coding: utf-8 -*-
"""
Record Anki study stats for 2026-10-08 (and finalize 2026-10-07) in database/jlpt_learning.db.
Updated with:
1) 2026-10-07 finalized with night reviews: 1,371 reviews (245.10m) + personal study 60m = 305m 5.79s (5h 5m 5.79s)
2) 2026-10-08 live: 559 reviews (84.40m / 1h 24m 24.2s), 303 distinct cards (07:11 ~ 14:29 ongoing)
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
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1008')
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

def process_day(d_str, day_num, extra_study_mins=0, extra_type="personal", is_today=False):
    s_dt = datetime(2026, 10, day_num, 4, 0, 0, tzinfo=KST)
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
            SELECT id FROM decks WHERE name LIKE '%문법%' OR name LIKE '%01%'
        )
    ''', (s_ms, e_ms))
    grammar_reviewed_today = cur_anki.fetchone()[0] or 0

    extra_sec = extra_study_mins * 60
    total_sec = anki_sec + extra_sec
    whole_mins = int(total_sec // 60)
    rem_sec = round(total_sec % 60, 2)

    deck_summary_str = ", ".join(deck_lines[:5])
    if len(deck_lines) > 5:
        deck_summary_str += f" 외 {len(deck_lines)-5}개 덱"

    if d_str == '2026-10-07':
        session_summary = (
            f"[{d_str}] 총 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(total_sec/60.0, 2)}분, 완결). "
            f"1) ★Anki 심야 포함 대규모 회독 세션 {cnt:,}회 실측 ({round(anki_mins, 2)}분 / 4시간 5분 6초, {min_dt_str}~익일 {max_dt_str} 완수, 고유 카드 {distinct_cards}장, 카드당 평균 {sec_per_card}초)★: "
            f"주요 덱 {deck_summary_str}. "
            f"학습 반응: Again {again_c:,} ({again_pct}%), Hard {hard_c} ({round(hard_c/cnt*100, 2)}%), "
            f"Good {good_c} ({round(good_c/cnt*100, 2)}%), Easy {easy_c} ({round(easy_c/cnt*100, 2)}%). "
            f"N2 문법 001-150 예문 48회(13.9분), 청해 오답 6회(5.1분) 집중 회독 포함. "
            f"2) 사용자 명시 보고: 개인공부 1시간 (60분 / 3,600초 실측, study_intervals ID 9 기록). "
            f"잔여 {rem_sec}초 보존."
        )
        source_note = (
            f"Anki revlog 2026-10-07 완결 실측치 (총 {cnt:,}회, {round(anki_mins, 2)}분) + 개인공부 60분 합산 (총 {whole_mins}분 {rem_sec}초)."
        )
    else:
        status_suffix = f" ({min_dt_str}~{max_dt_str} KST 진행 중)" if is_today else ""
        session_summary = (
            f"[{d_str}] 당일 현재 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(total_sec/60.0, 2)}분{status_suffix}). "
            f"1) ★Anki 회독 세션 {cnt:,}회 실측 ({round(anki_mins, 2)}분 / 1시간 24분 24초, {min_dt_str}~{max_dt_str} 진행 중, 고유 카드 {distinct_cards}장, 카드당 평균 {sec_per_card}초)★: "
            f"주요 덱 {deck_summary_str}. "
            f"학습 반응: Again {again_c:,} ({again_pct}%), Hard {hard_c} ({round(hard_c/cnt*100, 2)}%), "
            f"Good {good_c} ({round(good_c/cnt*100, 2)}%), Easy {easy_c} ({round(easy_c/cnt*100, 2)}%). "
            f"잔여 {rem_sec}초 보존."
        )
        source_note = (
            f"Anki revlog 2026-10-08 실측치 ({cnt:,}회, {round(anki_mins, 2)}분, 총 {whole_mins}분 {rem_sec}초)."
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

    return {
        'd_str': d_str,
        'cnt': cnt,
        'distinct_cards': distinct_cards,
        'anki_mins': anki_mins,
        'anki_sec': anki_sec,
        'extra_study_mins': extra_study_mins,
        'whole_mins': whole_mins,
        'rem_sec': rem_sec,
        'total_sec': total_sec,
        'sec_per_card': sec_per_card,
        'session_summary': session_summary,
        'summary_payload': summary_payload,
        'deck_breakdown': deck_breakdown,
        'deck_lines': deck_lines,
        'rating_map': rating_map,
        'min_dt_str': min_dt_str,
        'max_dt_str': max_dt_str
    }

data_07 = process_day('2026-10-07', 7, extra_study_mins=60, extra_type="personal", is_today=False)
data_08 = process_day('2026-10-08', 8, extra_study_mins=0, extra_type="", is_today=True)

con_anki.close()

# Update SQLite Database
con_db = sqlite3.connect(DB)
with con_db:
    cur_db = con_db.cursor()

    for data in [data_07, data_08]:
        d_str = data['d_str']
        # 1. Update or insert study_sessions
        cur_db.execute('''
            INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
            VALUES (?, ?, 0, ?)
            ON CONFLICT(session_date) DO UPDATE SET
                verified_minutes = excluded.verified_minutes,
                summary = excluded.summary,
                updated_at = CURRENT_TIMESTAMP
        ''', (d_str, data['whole_mins'], data['session_summary']))

        # 2. Update anki_daily_stats
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

        print(f"[{d_str}] DB Updated: {data['cnt']:,} reviews, {data['whole_mins']}m {data['rem_sec']}s ({round(data['total_sec']/60.0, 2)}m)")

    assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
print("\nDatabase update completed successfully!")
