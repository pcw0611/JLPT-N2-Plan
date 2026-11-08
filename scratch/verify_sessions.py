import sqlite3
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
for r in cur.execute('SELECT session_date, verified_minutes, summary FROM study_sessions WHERE session_date >= "2026-11-06" ORDER BY session_date'):
    print(r[0], r[1], r[2])
con.close()
