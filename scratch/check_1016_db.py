import sqlite3

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
cur.execute("SELECT session_date, verified_minutes, summary FROM study_sessions WHERE session_date = '2026-10-16'")
print('study_sessions:', cur.fetchall())
cur.execute("SELECT source, duration_seconds, notes FROM study_intervals WHERE session_date = '2026-10-16'")
for r in cur.fetchall():
    print('interval:', r)
