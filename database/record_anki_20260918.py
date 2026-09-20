# -*- coding: utf-8 -*-
"""Record Anki study stats and study session for 2026-09-18 (400.67 min / 4,288 reviews)."""

import sqlite3
import json
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r'c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan')
DB = ROOT / 'database' / 'jlpt_learning.db'
DATE = '2026-09-18'

# Inspect remaining cards from Anki collection
src = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_0918')
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

WHOLE_MINUTES = 400  # 400분 40.04초 (24,040.04초 / 6시간 40분 40초 / 400.67분)

SUMMARY_PAYLOAD = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks',
    'scopeLabel': '전체 덱',
    'answeredCards': 4288,
    'studyMinutes': 400.67,
    'secondsPerCard': 5.61,
    'againCount': 3627,
    'againPct': 84.58,
    'learningReviews': 3838,  # 971 learn + 2867 relearn
    'reviewsDone': 450,
    'ratings': {
        'again': 3627,
        'hard': 70,
        'good': 79,
        'easy': 512
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'studyDay': '2026-09-18',
    'ankiResourceStudyDayRaw': '2026-09-18',
    'sourceNote': (
        'Anki revlog 2026-09-18 실측치 (총 4,288회, 400분 40.04초 / 6시간 40분 40초 / 400.67분). '
        '★역대 최고 회독량 경신 (4,288회, 고유 카드 653장)★. '
        'N2 신규 66장 완수(1040~1105번, 진도율 94.5% 돌파, 누적 1,105/1,169장). '
        '사용자 전략적 판단: 최난도 잔여 36단어는 뇌 인지 부하 관리 및 익일 단어와 혼합 회독 시 암기 효율 극대화를 위해 의도적 익일 이월. '
        'N2 집중 회독 3,531회, N3 복습 592회, N4 45회, N5 41회, 의상 39회, N2 문법 예문 28회, 의성/의태어 12회. '
        '잔여 재학습 큐 43장(N2 33, N3 3 등) 익일 복습 큐로 정상 이월.'
    ),
    'inventory': {
        'n3_unseen': 0,
        'n2_unseen': 64,
        'n2_new_today': 66,
        'n3_new_today': 0,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 28,
        'grammar_unseen': 0,
        'new_cards_exposed_today': 66
    }
}

SESSION_SUMMARY = (
    '[2026-09-18] 총 순수 학습시간 400분 40.04초 (6시간 40분 40초 / 400.67분). '
    '★Anki 4,288회 역대 최고 회독 돌파(고유 카드 653장)★: '
    '1) N2 단어장 신규 66장 100% 소화 및 집중 3,531회 회독 (누적 진도율 94.5%, 1,105/1,169장). '
    '2) 최난도 잔여 36단어는 뇌 피로도 및 암기 효율 극대화를 위해 익일 단어와 혼합 학습 전략으로 의도적 배분. '
    '3) N3 단어 592회 복습 유지, N4 45회, N5 41회, 의상 39회, N2 문법 001-150 예문 28회, 의성·의태어 12회 완수. '
    '잔여 40.04초 보존.'
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
            ('전체 덱', json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), 'Anki revlog snapshot 2026-09-18', DATE)
        )
    else:
        con.execute(
            'INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at, updated_at) '
            'VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)',
            (DATE, '전체 덱', json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), 'Anki revlog snapshot 2026-09-18')
        )

    assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert not con.execute('PRAGMA foreign_key_check').fetchall()

print('Successfully updated 2026-09-18 stats (400.67 min, 4288 reviews) to DB!')
cur = con.cursor()
cur.execute('SELECT * FROM study_sessions WHERE session_date=?', (DATE,))
print('study_sessions:', cur.fetchall())
con.close()
