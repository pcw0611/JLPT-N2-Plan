# -*- coding: utf-8 -*-
import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print('Tables:', tables)

for t in ['study_sessions', 'study_intervals', 'tests', 'test_items', 'item_attempts']:
    if t in tables:
        cur.execute(f"PRAGMA table_info({t})")
        cols = [f"{c[1]} ({c[2]})" for c in cur.fetchall()]
        print(f"\n[{t}]:", ", ".join(cols))
