# -*- coding: utf-8 -*-
"""Record updated Anki study stats and study session for 2026-09-14 (290.84 min / 2,507 reviews)."""

import sqlite3
import json
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r'c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan')
DB = ROOT / 'database' / 'jlpt_learning.db'
DATE = '2026-09-14'

# Inspect remaining cards from Anki collection
src = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_0914')
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

WHOLE_MINUTES = 290  # 290분 50.25초 (17,450.25초 / 4시간 50분 50.25초, 290.84분)

SUMMARY_PAYLOAD = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks',
    'scopeLabel': '전체 덱',
    'answeredCards': 2507,
    'studyMinutes': 290.84,
    'secondsPerCard': 6.96,
    'againCount': 1920,
    'againPct': 76.59,
    'learningReviews': 2097,
    'reviewsDone': 410,
    'ratings': {
        'again': 1920,
        'hard': 80,
        'good': 124,
        'easy': 383
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'studyDay': '2026-09-14',
    'ankiResourceStudyDayRaw': '2026-09-14',
    'sourceNote': 'Anki revlog 2026-09-14 실측치 (총 2,507회, 290분 50.25초 / 4시간 50분 50초 / 290.84분). 옵션 A 9일차 완수: N2 신규 66장 100% 완수(394->328, 누적 72.0%), N3 신규 20장(59->39, 누적 92.4%), N2 문법 001-150 예문 복습 36회(5분 42초, 31장 복습), N2 보완 덱 12개 체계 구축 및 신규 카드 학습 개시, 당일 총 105개 신규 카드 노출.',
    'inventory': {
        'n3_unseen': 39,
        'n2_unseen': 328,
        'n2_new_today': 66,
        'n3_new_today': 20,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 36,
        'grammar_unseen': 0,
        'new_cards_exposed_today': 105
    }
}

SESSION_SUMMARY = (
    '[2026-09-14] Anki 단어·문법 세션 2,507회(290분 50초, 4시간 50분 50초 / 290.84분). '
    '옵션 A 9일차 완수: N2 신규 66장 100% 달성(394->328, 누적 72.0%), N3 신규 20장 100% 달성(59->39, 누적 92.4%) + '
    'N2 문법 001-150 예문 복습 36회(5분 42초, 고유 31장), N2 12개 보완 덱 체계 구축 및 신규 서브덱 학습 개시, 당일 신규 노출 총 105장. '
    '잔여 50.25초 보존.'
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
            ('전체 덱', json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), 'Anki revlog snapshot 2026-09-14', DATE)
        )
    else:
        con.execute(
            'INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at, updated_at) '
            'VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)',
            (DATE, '전체 덱', json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), 'Anki revlog snapshot 2026-09-14')
        )

    assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert not con.execute('PRAGMA foreign_key_check').fetchall()

print('Successfully updated 2026-09-14 stats (290.84 min, 2507 reviews) to DB!')
cur = con.cursor()
cur.execute('SELECT * FROM study_sessions WHERE session_date=?', (DATE,))
print('study_sessions:', cur.fetchall())
con.close()
