import sqlite3

conn = sqlite3.connect('database/jlpt_learning.db')
cur = conn.cursor()
cur.execute('SELECT * FROM study_sessions WHERE session_date = "2026-09-30";')
print("Session 2026-09-30:", cur.fetchall())

cur.execute('SELECT * FROM study_intervals WHERE session_date = "2026-09-30";')
print("Intervals 2026-09-30:")
for r in cur.fetchall():
    print(r)
