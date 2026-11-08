# -*- coding: utf-8 -*-
import sqlite3

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
print('Tests >= 2026-11-01:')
print(cur.execute("SELECT * FROM tests WHERE test_date >= '2026-11-01'").fetchall())
print('Intervals (source != anki) >= 2026-11-01:')
print(cur.execute("SELECT * FROM study_intervals WHERE session_date >= '2026-11-01' AND source != 'anki'").fetchall())
con.close()
