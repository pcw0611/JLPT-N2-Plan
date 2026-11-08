import sqlite3
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
cur.execute('SELECT * FROM study_intervals WHERE session_date >= "2026-11-07"')
print('study_intervals:', cur.fetchall())
cur.execute('SELECT * FROM tests WHERE test_date >= "2026-11-07"')
print('tests:', cur.fetchall())
con.close()
