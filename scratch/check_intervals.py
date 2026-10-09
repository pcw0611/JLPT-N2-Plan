import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

cur.execute("SELECT id, duration_seconds, notes FROM study_intervals WHERE session_date = '2026-10-08'")
rows = cur.fetchall()
print("All study intervals on 2026-10-08:")
for r in rows:
    print(r)

con.close()
