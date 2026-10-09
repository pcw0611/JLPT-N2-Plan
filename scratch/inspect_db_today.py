import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

print('=== study_sessions ===')
for r in cur.execute('SELECT * FROM study_sessions WHERE session_date = ?', ('2026-10-09',)).fetchall():
    print(r)

print('\n=== study_intervals ===')
for r in cur.execute('SELECT * FROM study_intervals WHERE session_date = ?', ('2026-10-09',)).fetchall():
    print(r)

print('\n=== tests ===')
for r in cur.execute('SELECT id, test_date, test_type, title, score, total_score, duration_seconds FROM tests WHERE test_date = ?', ('2026-10-09',)).fetchall():
    print(r)

con.close()
