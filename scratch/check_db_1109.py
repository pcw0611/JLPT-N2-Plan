import sqlite3

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
print('intervals 11/09:', cur.execute("SELECT * FROM study_intervals WHERE session_date = '2026-11-09'").fetchall())
print('exam_results 11/09:', cur.execute("SELECT * FROM exam_results WHERE date(taken_at) = '2026-11-09'").fetchall())
print('sessions 11/09:', cur.execute("SELECT * FROM study_sessions WHERE session_date = '2026-11-09'").fetchall())
con.close()
