import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
print("Intervals for 2026-11-02:")
for r in cur.execute("SELECT * FROM study_intervals WHERE session_date = '2026-11-02'").fetchall():
    print(r)
print("Session for 2026-11-02:")
for r in cur.execute("SELECT * FROM study_sessions WHERE session_date = '2026-11-02'").fetchall():
    print(r)
con.close()
