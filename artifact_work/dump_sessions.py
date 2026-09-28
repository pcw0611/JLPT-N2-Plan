import sqlite3

conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()
c.execute("SELECT session_date, verified_minutes, has_untracked_activity, summary FROM study_sessions ORDER BY session_date DESC LIMIT 15")
rows = c.fetchall()
for row in rows:
    print(f"Date: {row[0]}, Min: {row[1]}, Untracked: {row[2]}")
    if row[3]:
        print(f"  Summary: {row[3][:100]}...")
