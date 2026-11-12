# -*- coding: utf-8 -*-
"""
Record Anki study stats and reconcile study sessions for:
2026-11-11 (Final / 마감)
2026-11-12 (In-progress / 진행 중)
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
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_exec_20261112')
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
    ('2026-11-11', False), # is_today = False (마감)
    ('2026-11-12', True),  # is_today = True (진행 중)
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

    # 모의고사 어휘 decks (1회차, 2회차, 2023.07, 2021.12, 2026.07 등)
    cur_anki.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%모의고사%' AND d.name NOT LIKE '%독해%'
    ''', (s_ms, e_ms))
    mock_row = cur_anki.fetchone()
    mock_cnt = mock_row[0] or 0
    mock_sec = (mock_row[1] or 0) / 1000.0
    mock_min = mock_sec / 60.0
    mock_dist = mock_row[2] or 0

    # N1 Sampler deck (15 실생활・N1 고급어휘 맛보기)
    cur_anki.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%15 실생활%'
    ''', (s_ms, e_ms))
    samp_row = cur_anki.fetchone()
    samp_cnt = samp_row[0] or 0
    samp_sec = (samp_row[1] or 0) / 1000.0
    samp_min = samp_sec / 60.0
    samp_dist = samp_row[2] or 0

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

    # 1. study_intervals update
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

    # Calculate total duration for the day from ALL intervals (anki + exam)
    cur_db.execute('''
        SELECT sum(duration_seconds)
        FROM study_intervals
        WHERE session_date = ? AND status = 'completed'
    ''', (d_str,))
    day_total_sec = cur_db.fetchone()[0] or int(round(t_sec))
    whole_mins = int(day_total_sec // 60)
    rem_sec = round(day_total_sec % 60, 2)

    extra_parts = []
    if mock_cnt > 0:
        extra_parts.append(f"모의고사어휘 ➔ {mock_cnt}회({round(mock_min, 1)}분, {mock_dist}장)")
    if samp_cnt > 0:
        extra_parts.append(f"N1고급어휘맛보기 ➔ {samp_cnt}회({round(samp_min, 1)}분, {samp_dist}장)")
    if read_cnt > 0:
        extra_parts.append(f"독해어휘 ➔ {read_cnt}회({round(read_min, 1)}분, {read_dist}장)")
    if toeic_cnt > 0:
        extra_parts.append(f"TOEIC ➔ {toeic_cnt}회({round(toeic_min, 1)}분, {toeic_dist}장)")
    extra_str = f". {', '.join(extra_parts)}" if extra_parts else ""

    anki_summary_part = (
        f"1) ★Anki 회독 세션 {t_cnt:,}회 실측 ({int(t_sec//60)}분 {round(t_sec%60, 2)}초 / {t_sec:.2f}초, "
        f"{min_dt.strftime('%H:%M')}~{max_dt.strftime('%H:%M')} KST 완수, 고유 카드 {t_dist}장)★: "
        f"[시간 공통 반영: 총 {round(t_min, 1)}분] [정확도·반응 지표: 한끝 Voca 기준] {v_cnt:,}회({round(v_min, 1)}분, 고유 카드 {v_dist}장, 카드당 {v_sec_per_card}초) ➔ "
        f"Again {v_again:,} ({v_again_pct}%), Hard {v_hard} ({round(v_hard/v_cnt*100, 2) if v_cnt else 0}%), "
        f"Good {v_good} ({round(v_good/v_cnt*100, 2) if v_cnt else 0}%), Easy {v_easy} ({round(v_easy/v_cnt*100, 2) if v_cnt else 0}%){extra_str}. "
        f"주요 덱: {', '.join(deck_lines[:8])}. "
        f"잔여 큐: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장)."
    )

    if d_str == '2026-11-11':
        # Final / 마감 with exam details
        exam_summary_part = (
            f"2) [모의고사 반영 20261111] 2021년 12월 N2 개인 모의고사 58/101 (57.4%), "
            f"비공식 참고 99.5/180 (언어지식 36.5 · 독해 27.0 · 청해 36.0). "
            f"시험 147분 51초 (8,871초 · 필기 104분 28초 + 청해 43분 23초) + Anki {int(t_sec//60)}분 {round(t_sec%60, 2)}초 ({t_sec:.2f}초) = "
            f"당일 최종 완결 {whole_mins}분 {rem_sec}초 (정수 {whole_mins}분, 잔여 {rem_sec}초 보존). "
            f"오답 43문항 D+1/3/7 복습 큐 등록. 공식 척도점수·합격 확정 아님. {status_label}."
        )
        session_summary = (
            f"[{d_str}] 당일 최종 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 "
            f"(약 {whole_mins//60}시간 {whole_mins%60}분 / {round(day_total_sec/60.0, 2)}분, {status_label}). "
            f"{anki_summary_part}\n{exam_summary_part}"
        )
    elif d_str == '2026-11-12':
        session_summary = (
            f"[{d_str}] 당일 현재 누적 순수 학습시간 {whole_mins}분 {rem_sec}초 "
            f"(약 {whole_mins//60}시간 {whole_mins%60}분 / {round(day_total_sec/60.0, 2)}분, {status_label}). "
            f"{anki_summary_part} 잔여 {rem_sec}초 보존."
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
            'mockVocabReviews': mock_cnt,
            'mockVocabMinutes': round(mock_min, 2),
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

    print(f"Recorded {d_str} ({status_label}): {t_cnt} reviews, total day time {whole_mins}m {rem_sec}s (Anki {int(t_sec//60)}m {t_sec%60:.2f}s)")

con_db.commit()

# Assertions
assert con_db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert not con_db.execute('PRAGMA foreign_key_check').fetchall()

con_db.close()
con_anki.close()

print("Successfully recorded 2026-11-11 (마감) and 2026-11-12 (진행 중) in database!")
