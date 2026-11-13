# -*- coding: utf-8 -*-
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'database' / 'jlpt_learning.db'

con = sqlite3.connect(DB)
cur = con.cursor()

print("--- study_sessions ---")
cur.execute('''
    SELECT session_date, verified_minutes, has_untracked_activity, summary
    FROM study_sessions
    WHERE session_date >= '2026-11-10'
    ORDER BY session_date
''')
for r in cur.fetchall():
    print(f"Date: {r[0]} | Mins: {r[1]} | Untracked: {r[2]}")
    print(f"Summary: {r[3][:150]}...")
    print("-" * 40)

print("\n--- study_intervals ---")
cur.execute('''
    SELECT session_date, started_at, ended_at, duration_seconds, status, source, notes
    FROM study_intervals
    WHERE session_date >= '2026-11-10'
    ORDER BY session_date, id
''')
for r in cur.fetchall():
    print(r)

print("\n--- anki_daily_stats ---")
cur.execute('''
    SELECT snapshot_date, scope_label, source_filename, captured_at
    FROM anki_daily_stats
    WHERE snapshot_date >= '2026-11-10'
    ORDER BY snapshot_date
''')
for r in cur.fetchall():
    print(r)

con.close()
