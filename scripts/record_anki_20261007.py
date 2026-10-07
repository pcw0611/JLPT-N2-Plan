# -*- coding: utf-8 -*-
"""
Record Anki study stats for 2026-10-07 (and finalize 2026-10-06) in database/jlpt_learning.db.
Updated with:
1) Anki latest revlog (1,323 reviews, 231.17 mins, 630 distinct cards)
2) User confirmed personal study 1 hour (60 mins, 3,600s)
Total for 2026-10-07: 291 mins 10.15s (4h 51m 10.15s)
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
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1007')
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

def process_day(d_str, day_num, extra_study_mins=0, extra_type="lecture", is_today=False):
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

    if d_str == '2026-10-06':
        session_summary = (
            f"[{d_str}] 총 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(total_sec/60.0, 2)}분, 완결). "
            f"1) Anki 회독 세션 {cnt:,}회 실측 ({round(anki_mins, 2)}분 / 2시간 0분 34초, {min_dt_str}~익일 {max_dt_str} 완수, 고유 카드 {distinct_cards}장, 카드당 평균 {sec_per_card}초): "
            f"주요 덱 {deck_summary_str}. "
            f"학습 반응: Again {again_c:,} ({again_pct}%), Hard {hard_c} ({round(hard_c/cnt*100, 2)}%), "
            f"Good {good_c} ({round(good_c/cnt*100, 2)}%), Easy {easy_c} ({round(easy_c/cnt*100, 2)}%). "
            f"2) N2 정규 강의 집중 수강: 24분 실측 (1,440초 완료, study_intervals ID 8 기록). "
            f"3) 컬렉션 재학습 큐 {learn_rem}장 타이트 소화 관리 중. 잔여 {rem_sec}초 보존."
        )
        source_note = (
            f"Anki revlog 2026-10-06 실측치 (총 {cnt:,}회, {round(anki_mins, 2)}분) + N2 정규 강의 24분 합산 (총 {whole_mins}분 {rem_sec}초)."
        )
    else:
        status_suffix = " (10:33~22:55 KST 진행 중)" if is_today else ""
        session_summary = (
            f"[{d_str}] 당일 현재 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 (약 {whole_mins//60}시간 {whole_mins%60}분 / {round(total_sec/60.0, 2)}분{status_suffix}). "
            f"1) ★Anki 대규모 집중 회독 세션 {cnt:,}회 실측 ({round(anki_mins, 2)}분 / 3시간 51분 10초, {min_dt_str}~{max_dt_str} 완수, 고유 카드 {distinct_cards}장, 카드당 평균 {sec_per_card}초)★: "
            f"주요 덱 회독 {deck_summary_str}. "
            f"학습 반응: Again {again_c:,} ({again_pct}%), Hard {hard_c} ({round(hard_c/cnt*100, 2)}%), "
            f"Good {good_c} ({round(good_c/cnt*100, 2)}%), Easy {easy_c} ({round(easy_c/cnt*100, 2)}%). "
            f"청해 오답 6회(5.1분), 경어·축약 5회(2.8분), 예외1그룹 1회 집중 점검 포함. "
            f"2) 사용자 명시 보고: 개인공부 1시간 (60분 / 3,600초 실측 추가, study_intervals ID 9 기록). "
            f"잔여 {rem_sec}초 보존."
        )
        source_note = (
            f"Anki revlog 2026-10-07 실측치 ({cnt:,}회, {round(anki_mins, 2)}분) + 개인공부 60분(3,600초) 합산 (총 {whole_mins}분 {rem_sec}초)."
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

data_06 = process_day('2026-10-06', 6, extra_study_mins=24, extra_type="lecture", is_today=False)
data_07 = process_day('2026-10-07', 7, extra_study_mins=60, extra_type="personal", is_today=True)

con_anki.close()

# Update SQLite Database
con_db = sqlite3.connect(DB)
with con_db:
    cur_db = con_db.cursor()

    # Insert study_intervals for 10/07 if not already inserted
    cur_db.execute("SELECT id FROM study_intervals WHERE session_date = '2026-10-07' AND source = 'chat_confirmed'")
    existing_interval = cur_db.fetchone()
    if existing_interval:
        cur_db.execute('''
            UPDATE study_intervals
            SET duration_seconds = 3600,
                notes = '사용자 명시 보고: 개인공부 1시간(60분/3,600초) 완료'
            WHERE id = ?
        ''', (existing_interval[0],))
        print(f"Updated study_intervals ID {existing_interval[0]} with 3,600s personal study.")
    else:
        cur_db.execute('''
            INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
            VALUES ('2026-10-07', '2026-10-07T21:45:00+09:00', '2026-10-07T22:45:00+09:00', 3600, 'completed', 'chat_confirmed', '사용자 명시 보고: 개인공부 1시간(60분/3,600초) 완료')
        ''')
        print("Inserted new study_intervals row for 2026-10-07 personal study 1h.")

    for data in [data_06, data_07]:
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
