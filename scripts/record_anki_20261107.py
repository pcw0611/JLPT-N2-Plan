# -*- coding: utf-8 -*-
"""
Record Anki study stats and reconcile study sessions for:
2026-11-05 (Final / 마감)
2026-11-06 (Final / 마감)
2026-11-07 (In-progress / 진행 중)
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
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_exec_20261107')
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

days = [
    ('2026-11-05', False), # is_today = False (마감)
    ('2026-11-06', False), # is_today = False (마감)
    ('2026-11-07', True),  # is_today = True (진행 중)
]

for d_str, is_today in days:
    status_label = "진행 중" if is_today else "마감"
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
    t_cnt, t_tms, t_dist, min_id, max_id = cur_anki.fetchone()
    if not t_cnt:
        continue

    t_sec = (t_tms or 0) / 1000.0
    t_min = t_sec / 60.0
    min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST)
    max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST)

    # 한끝 Voca only
    cur_anki.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    ''', (s_ms, e_ms))
    v_cnt, v_tms, v_dist = cur_anki.fetchone()
    v_cnt = v_cnt or 0
    v_sec = (v_tms or 0) / 1000.0
    v_min = v_sec / 60.0
    v_sec_per_card = round(v_sec / v_cnt, 2) if v_cnt else 0

    cur_anki.execute('''
        SELECT r.ease, count(*)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
        GROUP BY r.ease
    ''', (s_ms, e_ms))
    r_voca = dict(cur_anki.fetchall())
    v_again = r_voca.get(1, 0)
    v_hard = r_voca.get(2, 0)
    v_good = r_voca.get(3, 0)
    v_easy = r_voca.get(4, 0)
    v_again_pct = round((v_again / v_cnt * 100), 2) if v_cnt else 0.0

    # Reading deck
    cur_anki.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
    ''', (s_ms, e_ms))
    read_row = cur_anki.fetchone()
    read_cnt = read_row[0] or 0
    read_sec = (read_row[1] or 0) / 1000.0
    read_min = read_sec / 60.0
    read_dist = read_row[2] or 0

    # TOEIC decks
    cur_anki.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%TOEIC%'
    ''', (s_ms, e_ms))
    toeic_row = cur_anki.fetchone()
    toeic_cnt = toeic_row[0] or 0
    toeic_sec = (toeic_row[1] or 0) / 1000.0
    toeic_min = toeic_sec / 60.0
    toeic_dist = toeic_row[2] or 0

    # Types overall
    cur_anki.execute('''
        SELECT type, count(*)
        FROM revlog
        WHERE id >= ? AND id < ?
        GROUP BY type
    ''', (s_ms, e_ms))
    type_map = dict(cur_anki.fetchall())
    learn_revs = type_map.get(0, 0)
    revs_done = type_map.get(1, 0)
    relearn_revs = type_map.get(2, 0)

    # First time cards exposed
    cur_anki.execute('''
        SELECT count(distinct r.cid)
        FROM revlog r
        WHERE r.id >= ? AND r.id < ?
          AND r.cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
    ''', (s_ms, e_ms, s_ms))
    first_cards = cur_anki.fetchone()[0] or 0

    # Decks breakdown
    cur_anki.execute('''
        SELECT c.did, count(*), count(distinct c.id), sum(r.time)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        WHERE r.id >= ? AND r.id < ?
        GROUP BY c.did
        ORDER BY sum(r.time) DESC
    ''', (s_ms, e_ms))
    deck_breakdown = []
    deck_lines = []
    for did, d_cnt, d_dist, d_tms in cur_anki.fetchall():
        d_sec = (d_tms or 0) / 1000.0
        d_m = round(d_sec / 60.0, 1)
        d_name = deck_names.get(did, f"Deck {did}")
        deck_breakdown.append({
            'deckId': did,
            'deckName': d_name,
            'reviews': d_cnt,
            'distinctCards': d_dist,
            'studyMinutes': d_m,
            'seconds': round(d_sec, 1)
        })
        deck_lines.append(f"{d_name} {d_cnt:,}회({d_m}분)")

    # 1. study_intervals
    anki_note = (
        f"[{d_str} Anki 회독 세션] {int(t_sec//60)}분 {round(t_sec%60, 2)}초 "
        f"(총 {t_cnt:,}회 실측, 고유 카드 {t_dist}장, {min_dt.strftime('%H:%M')}~{max_dt.strftime('%H:%M')} KST)"
    )
    cur_db.execute('DELETE FROM study_intervals WHERE session_date = ? AND source = "anki"', (d_str,))
    cur_db.execute('''
        INSERT INTO study_intervals (session_date, started_at, ended_at, duration_seconds, status, source, notes)
        VALUES (?, ?, ?, ?, 'completed', 'anki', ?)
    ''', (
        d_str,
        min_dt.strftime('%Y-%m-%d %H:%M:%S'),
        max_dt.strftime('%Y-%m-%d %H:%M:%S'),
        int(round(t_sec)),
        anki_note
    ))

    whole_mins = int(t_sec // 60)
    rem_sec = round(t_sec % 60, 2)

    extra_parts = []
    if read_cnt > 0:
        extra_parts.append(f"독해어휘 ➔ {read_cnt}회({round(read_min, 1)}분, {read_dist}장)")
    if toeic_cnt > 0:
        extra_parts.append(f"TOEIC ➔ {toeic_cnt}회({round(toeic_min, 1)}분, {toeic_dist}장)")
    extra_str = f". {', '.join(extra_parts)}" if extra_parts else ""

    session_summary = (
        f"[{d_str}] 당일 {'현재' if is_today else '최종'} 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 "
        f"(약 {whole_mins//60}시간 {whole_mins%60}분 / {round(t_sec/60.0, 2)}분, {status_label}). "
        f"1) ★Anki 회독 세션 {t_cnt:,}회 실측 ({int(t_sec//60)}분 {round(t_sec%60, 2)}초 / {t_sec:.2f}초, "
        f"{min_dt.strftime('%H:%M')}~{max_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t_dist}장)★: "
        f"[시간 공통 반영: 총 {round(t_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {v_cnt:,}회({round(v_min, 1)}분, 고유 카드 {v_dist}장, 카드당 {v_sec_per_card}초) ➔ "
        f"Again {v_again:,} ({v_again_pct}%), Hard {v_hard} ({round(v_hard/v_cnt*100, 2) if v_cnt else 0}%), "
        f"Good {v_good} ({round(v_good/v_cnt*100, 2) if v_cnt else 0}%), Easy {v_easy} ({round(v_easy/v_cnt*100, 2) if v_cnt else 0}%){extra_str}. "
        f"주요 덱: {', '.join(deck_lines[:6])}. "
        f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장). "
        f"잔여 {rem_sec}초 보존."
    )

    cur_db.execute('''
        INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary)
        VALUES (?, ?, 0, ?)
        ON CONFLICT(session_date) DO UPDATE SET
            verified_minutes = excluded.verified_minutes,
            summary = excluded.summary,
            updated_at = CURRENT_TIMESTAMP
    ''', (d_str, whole_mins, session_summary))

    payload = {
        'schema': 'daily_summary_v1',
        'scope': 'all_decks_time_voca_ratings',
        'scopeLabel': '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)',
        'answeredCards': v_cnt if v_cnt > 0 else t_cnt,
        'totalAnsweredCardsAllDecks': t_cnt,
        'studyMinutes': round(t_min, 2),
        'secondsPerCard': v_sec_per_card if v_cnt > 0 else round(t_sec / t_cnt, 2),
        'againCount': v_again,
        'againPct': v_again_pct,
        'learningReviews': learn_revs,
        'reviewsDone': revs_done,
        'ratings': {
            'again': v_again,
            'hard': v_hard,
            'good': v_good,
            'easy': v_easy
        },
        'allDecksStats': {
            'totalReviews': t_cnt,
            'totalStudyMinutes': round(t_min, 2),
            'distinctCards': t_dist,
            'readingVocabReviews': read_cnt,
            'readingVocabMinutes': round(read_min, 2),
            'toeicReviews': toeic_cnt,
            'toeicMinutes': round(toeic_min, 2)
        },
        'cardsRemaining': {
            'new': new_rem,
            'learning': learn_rem,
            'review': rev_rem
        },
        'decks': deck_breakdown,
        'studyDay': d_str,
        'ankiResourceStudyDayRaw': d_str,
        'sourceNote': f"Anki revlog {d_str} 실측치 (전체 덱: {t_cnt:,}회 {round(t_min, 2)}분 / 한끝 Voca: {v_cnt:,}회 {v_again_pct}% Again).",
        'inventory': {
            'n3_unseen': 0,
            'n2_unseen': 0,
            'n2_new_today': 0,
            'n3_new_today': 0,
            'grammar_new_today': 0,
            'grammar_reviewed_today': 0,
            'grammar_unseen': 0,
            'new_cards_exposed_today': first_cards
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
    ''', (d_str, '전체 덱 (시간 공통 / 정확도: 한끝 Voca 기준)', json.dumps(payload, ensure_ascii=False), f'Anki revlog snapshot {d_str}'))

    print(f"Recorded {d_str} ({status_label}): {t_cnt} reviews, {whole_mins}m {rem_sec}s")

con_db.commit()

# Assertions
assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
con_anki.close()

print(f"Successfully recorded 2026-11-05 (마감), 2026-11-06 (마감), 2026-11-07 (진행 중) in database!")
