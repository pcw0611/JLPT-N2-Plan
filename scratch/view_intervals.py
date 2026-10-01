import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()
c.execute('SELECT id, session_date, started_at, ended_at, duration_seconds, source, notes FROM study_intervals WHERE session_date >= ?', ('2026-09-28',))
for r in c.fetchall():
    print(r)
