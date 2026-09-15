# -*- coding: utf-8 -*-
"""Record Anki study stats and study session for 2026-09-15 (463.30 min / 4,562 reviews)."""

import sqlite3
import json
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r'c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan')
DB = ROOT / 'database' / 'jlpt_learning.db'
DATE = '2026-09-15'

# Inspect remaining cards from Anki collection
src = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_0915')
dst.mkdir(exist_ok=True)
shutil.copy2(src / 'collection.anki2', dst / 'collection.anki2')
if (src / 'collection.anki2-wal').exists():
    shutil.copy2(src / 'collection.anki2-wal', dst / 'collection.anki2-wal')

con_anki = sqlite3.connect(dst / 'collection.anki2')
cur_anki = con_anki.cursor()

cur_anki.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur_anki.fetchall())
print('Queue counts:', queue_counts)

new_rem = queue_counts.get(0, 0)
learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
rev_rem = queue_counts.get(2, 0)
con_anki.close()

WHOLE_MINUTES = 463  # 463분 17.96초 (27,797.96초 / 7시간 43분 17.96초, 463.30분)

SUMMARY_PAYLOAD = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks',
    'scopeLabel': '전체 덱',
    'answeredCards': 4562,
    'studyMinutes': 463.30,
    'secondsPerCard': 6.09,
    'againCount': 3927,
    'againPct': 86.08,
    'learningReviews': 4092,
    'reviewsDone': 470,
    'ratings': {
        'again': 3927,
        'hard': 87,
        'good': 101,
        'easy': 447
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'studyDay': '2026-09-15',
    'ankiResourceStudyDayRaw': '2026-09-15',
    'sourceNote': 'Anki revlog 2026-09-15 실측치 (총 4,562회, 463분 17.96초 / 7시간 43분 18초 / 463.30분). 옵션 A 10일차 완수: N2 신규 66장 100% 완수(328->262, 누적 77.59%), N3 신규 20장(39->19, 누적 96.29%), N2 문법 001-150 예문 복습 34회(6분 22초, 34장 복습), 당일 총 86개 신규 카드 노출.',
    'inventory': {
        'n3_unseen': 19,
        'n2_unseen': 262,
        'n2_new_today': 66,
        'n3_new_today': 20,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 34,
        'grammar_unseen': 0,
        'new_cards_exposed_today': 86
    }
}

SESSION_SUMMARY = (
    '[2026-09-15] Anki 단어·문법 세션 4,562회(463분 18초, 7시간 43분 18초 / 463.30분, 역대 일일 최다 리뷰 및 최장 순수 학습시간 기록!). '
    '옵션 A 10일차 완수: N2 신규 66장 100% 달성(328->262, 누적 77.59%), N3 신규 20장 100% 달성(39->19, 누적 96.29%, 1차 완독 D-1) + '
    'N2 문법 001-150 예문 복습 34회(6분 22초, 고유 34장), 당일 신규 노출 총 86장. '
    '잔여 17.96초 보존.'
)

con = sqlite3.connect(DB)
with con:
    # 1. Update or Insert study_sessions
    row = con.execute('SELECT verified_minutes, summary FROM study_sessions WHERE session_date=?', (DATE,)).fetchone()
    if row is None:
        con.execute(
            'INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary, updated_at) '
            'VALUES (?, ?, 0, ?, CURRENT_TIMESTAMP)',
            (DATE, WHOLE_MINUTES, SESSION_SUMMARY)
        )
    else:
        con.execute(
            'UPDATE study_sessions SET verified_minutes=?, summary=?, updated_at=CURRENT_TIMESTAMP WHERE session_date=?',
            (WHOLE_MINUTES, SESSION_SUMMARY, DATE)
        )

    # 2. Update or Insert anki_daily_stats
    anki_row = con.execute('SELECT snapshot_date FROM anki_daily_stats WHERE snapshot_date=?', (DATE,)).fetchone()
    if anki_row:
        con.execute(
            'UPDATE anki_daily_stats SET scope_label=?, payload_json=?, source_filename=?, updated_at=CURRENT_TIMESTAMP WHERE snapshot_date=?',
            ('전체 덱', json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), 'Anki revlog snapshot 2026-09-15', DATE)
        )
    else:
        con.execute(
            'INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at, updated_at) '
            'VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)',
            (DATE, '전체 덱', json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), 'Anki revlog snapshot 2026-09-15')
        )

    assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert not con.execute('PRAGMA foreign_key_check').fetchall()

print('Successfully updated 2026-09-15 stats (463.30 min, 4562 reviews) to DB!')
cur = con.cursor()
cur.execute('SELECT * FROM study_sessions WHERE session_date=?', (DATE,))
print('study_sessions:', cur.fetchall())
con.close()
