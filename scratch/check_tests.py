import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
for r in cur.execute("SELECT id, test_date, title, total_items, correct_items, elapsed_seconds FROM tests WHERE test_date >= '2026-11-08'").fetchall():
    print(r)
con.close()
