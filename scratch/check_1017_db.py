import sqlite3

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

cur.execute("SELECT * FROM tests WHERE test_date = '2026-10-17'")
print('Tests 10-17:', cur.fetchall())

cur.execute("SELECT * FROM study_intervals WHERE session_date = '2026-10-17'")
print('Intervals 10-17:', cur.fetchall())

cur.execute("SELECT * FROM study_sessions WHERE session_date = '2026-10-17'")
print('Sessions 10-17:', cur.fetchall())

cur.execute("SELECT * FROM anki_daily_stats WHERE snapshot_date >= '2026-10-15'")
for r in cur.fetchall():
    print('anki_daily_stats:', r[0], r[1], r[2], r[3], r[4])
