"""Record updated Anki study stats and study session for 2026-09-12 including grammar review."""

import sqlite3
import json
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r'c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan')
DB = ROOT / 'database' / 'jlpt_learning.db'
DATE = '2026-09-12'

# Inspect remaining cards from Anki collection
src = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_0912')
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

WHOLE_MINUTES = 271  # 271분 36.33초 (16,296.33초 / 4시간 31분 36.33초)

SUMMARY_PAYLOAD = {
    'schema': 'daily_summary_v1',
    'scope': 'all_decks',
    'scopeLabel': '전체 덱',
    'answeredCards': 2667,
    'studyMinutes': 271.61,
    'secondsPerCard': 6.11,
    'againCount': 2100,
    'againPct': 78.74,
    'learningReviews': 2291,
    'reviewsDone': 376,
    'ratings': {
        'again': 2100,
        'hard': 142,
        'good': 88,
        'easy': 337
    },
    'cardsRemaining': {
        'new': new_rem,
        'learning': learn_rem,
        'review': rev_rem
    },
    'studyDay': '2026-09-12',
    'ankiResourceStudyDayRaw': '2026-09-12',
    'sourceNote': 'Anki revlog 2026-09-12 실측치 (총 2,667회, 271분 36.33초 / 4시간 31분 36초). 옵션 A 7일차 완수: N2 신규 66장 100% 완수(526->460, 누적 60.7%), N3 신규 20장(99->79, 누적 84.6%), N2 문법 001-150 예문 복습(59회 7분 6초, 정답률 100%), 당일 잔여 학습 큐 0장 전량 클리어.',
    'inventory': {
        'n3_unseen': 79,
        'n2_unseen': 460,
        'n2_new_today': 66,
        'n3_new_today': 20,
        'grammar_new_today': 0,
        'grammar_reviewed_today': 59,
        'grammar_unseen': 0,
        'new_cards_exposed_today': 86
    }
}

SESSION_SUMMARY = (
    '[2026-09-12] Anki 단어·문법 세션 2,667회(271분 36초, 4시간 31분 36초). '
    '옵션 A 7일차 완수: N2 신규 66장 100% 달성(526->460, 누적 60.7%), N3 신규 20장 100% 달성(99->79, 누적 84.6%) + '
    'N2 문법 001-150 예문 복습 59회(7분 6초, 59장 복습 완수, 유지율 100%), 당일 잔여 학습 큐 0장 전량 클리어 완수. '
    '잔여 36.33초 보존.'
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
            ('전체 덱', json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), 'Anki revlog snapshot 2026-09-12 (grammar update)', DATE)
        )
    else:
        con.execute(
            'INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at, updated_at) '
            'VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)',
            (DATE, '전체 덱', json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), 'Anki revlog snapshot 2026-09-12 (grammar update)')
        )

    assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert not con.execute('PRAGMA foreign_key_check').fetchall()

print('Successfully recorded updated 2026-09-12 stats to DB!')
cur = con.cursor()
cur.execute('SELECT * FROM study_sessions WHERE session_date=?', (DATE,))
print('study_sessions:', cur.fetchall())
cur.execute('SELECT snapshot_date, scope_label FROM anki_daily_stats WHERE snapshot_date=?', (DATE,))
print('anki_daily_stats:', cur.fetchall())
con.close()
