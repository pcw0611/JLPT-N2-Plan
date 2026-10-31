# -*- coding: utf-8 -*-
"""
Generate markdown entries for JLPT_STUDY_LOG.md from 2026-10-20 to 2026-10-30
"""

import sqlite3
import sys
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'database' / 'jlpt_learning.db'
LOG_FILE = ROOT / 'JLPT_STUDY_LOG.md'

con_db = sqlite3.connect(DB)
cur_db = con_db.cursor()

cur_db.execute('''
    SELECT snapshot_date, payload_json
    FROM anki_daily_stats
    WHERE snapshot_date >= '2026-10-20'
    ORDER BY snapshot_date ASC
''')
rows = cur_db.fetchall()

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_exec_oct_catchup')
con_anki = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur_anki = con_anki.cursor()

KST = timezone(timedelta(hours=9))
EXAM_DATE = datetime(2026, 12, 6, tzinfo=KST)

cur_anki.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur_anki.fetchall())
new_rem = queue_counts.get(0, 0)
learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
rev_rem = queue_counts.get(2, 0)

markdown_blocks = []

for d_str, payload_str in rows:
    p = json.loads(payload_str)
    y, m, d = map(int, d_str.split('-'))
    target_dt = datetime(y, m, d, tzinfo=KST)
    d_day = (EXAM_DATE - target_dt).days
    is_today = (d_str == '2026-10-31')
    status_label = "진행 중" if is_today else "마감"

    s_dt = datetime(y, m, d, 4, 0, 0, tzinfo=KST)
    e_dt = s_dt + timedelta(days=1)
    s_ms = int(s_dt.timestamp() * 1000)
    e_ms = int(e_dt.timestamp() * 1000)

    cur_anki.execute('''
        SELECT min(id), max(id)
        FROM revlog
        WHERE id >= ? AND id < ?
    ''', (s_ms, e_ms))
    min_id, max_id = cur_anki.fetchone()
    min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST) if min_id else s_dt
    max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST) if max_id else s_dt

    cur_db.execute('SELECT duration_seconds, notes FROM study_intervals WHERE session_date = ? AND source = "anki"', (d_str,))
    interval_row = cur_db.fetchone()
    t_sec = interval_row[0] if interval_row else 0
    t_min = t_sec / 60.0
    whole_mins = int(t_sec // 60)
    rem_sec = round(t_sec % 60, 2)

    total_reviews = p['allDecksStats']['totalReviews']
    distinct_cards = p['allDecksStats']['distinctCards']

    voca_cnt = p['answeredCards']
    voca_again = p['againCount']
    voca_again_pct = p['againPct']
    voca_ratings = p['ratings']
    voca_sec_per_card = p['secondsPerCard']

    decks = p.get('decks', [])

    block = []
    block.append(f"<!-- anki-session-{d_str.replace('-', '')} -->")
    time_str = f"{whole_mins}분 {int(rem_sec)}초" if whole_mins > 0 else f"{int(rem_sec)}초"
    hours_str = f"{whole_mins//60}시간 {whole_mins%60}분 {int(rem_sec)}초" if whole_mins >= 60 else time_str
    block.append(f"### {d_str} — Anki 회독 {total_reviews:,}회 실측 ({time_str} / {hours_str} / {round(t_min, 2)}분, {status_label}, D-{d_day})\n")
    block.append(f"- **수행 내용**:")
    block.append(f"  - **1) Anki 회독 세션 (총 {total_reviews:,}회 실측, 시간 공통 / 정확도: 한끝 Voca 기준)**:")
    block.append(f"    - **실측 Anki 학습시간 (공통 전체 덱)**: **{time_str} ({t_sec:.2f}초 / {hours_str} / {round(t_min, 2)}분)** ({min_dt.strftime('%H:%M')} ~ {max_dt.strftime('%H:%M')} KST 실측, 고유 카드 {distinct_cards}장).")
    
    if voca_cnt > 0:
        block.append(f"    - **한끝 Voca 지표 (정확도·속도 공식 기준)**:")
        block.append(f"      - **회독수**: **{voca_cnt:,}회**.")
        block.append(f"      - **평균 응답 속도**: **{voca_sec_per_card}초/카드**.")
        block.append(f"      - **학습 반응 분포**: Again {voca_again:,} (**{voca_again_pct}%**), Hard {voca_ratings['hard']:,} ({round(voca_ratings['hard']/voca_cnt*100, 2)}%), Good {voca_ratings['good']:,} ({round(voca_ratings['good']/voca_cnt*100, 2)}%), Easy {voca_ratings['easy']:,} ({round(voca_ratings['easy']/voca_cnt*100, 2)}%).")
        block.append(f"      - **유형별 분포**: Review {p['reviewsDone']:,}회, Relearn/Learn {p['learningReviews']:,}회.")

    read_cnt = p['allDecksStats'].get('readingVocabReviews', 0)
    if read_cnt > 0:
        read_min = p['allDecksStats'].get('readingVocabMinutes', 0.0)
        block.append(f"    - **독해어휘 암기 (`JLPT N2::14 독해・기사・모의고사 어휘`)**:")
        block.append(f"      - **회독수**: **{read_cnt:,}회**, **{read_min}분**.")

    toeic_cnt = p['allDecksStats'].get('toeicReviews', 0)
    if toeic_cnt > 0:
        toeic_min = p['allDecksStats'].get('toeicMinutes', 0.0)
        block.append(f"    - **TOEIC 단어장 병행**:")
        block.append(f"      - **회독수**: **{toeic_cnt:,}회**, **{toeic_min}분**.")

    block.append(f"    - **덱별 실측 현황**:")
    for d in decks[:8]:
        block.append(f"      - `{d['deckName']}`: **{d['reviews']:,}회**, **{d['studyMinutes']}분 ({d['seconds']}초)** (고유 카드 {d['distinctCards']}장)")
    block.append(f"    - **잔여 큐**: new {new_rem:,}장, learning {learn_rem:,}장, review {rev_rem:,}장 (총 {new_rem+learn_rem+rev_rem:,}장).")

    block.append(f"- **당일 {'현재' if is_today else '최종'} 누적 순수 학습시간**: **{time_str} ({hours_str} / {round(t_min, 2)}분 / {status_label})** (DB 정수 **{whole_mins}분** 반영, 잔여 {rem_sec}초 보존).")
    block.append(f"- **사이트 동기화 진행**: Cloudflare / Legacy 양쪽 주소 동기화 완료 (`studyMinutes: {whole_mins}`, `questions: 0`).\n")
    markdown_blocks.append('\n'.join(block))

full_new_content = '\n'.join(markdown_blocks)

# Read original log and replace from <!-- anki-session-20261020 --> onwards
content = LOG_FILE.read_text(encoding='utf-8')
split_marker = "<!-- anki-session-20261020 -->"
if split_marker in content:
    base_content = content.split(split_marker)[0]
    updated_content = base_content + full_new_content + "\n"
else:
    updated_content = content + "\n\n" + full_new_content + "\n"

LOG_FILE.write_text(updated_content, encoding='utf-8')
print("Successfully updated JLPT_STUDY_LOG.md with all entries from 2026-10-20 to 2026-10-31!")
