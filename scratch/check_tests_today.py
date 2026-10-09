import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

print('=== tests today ===')
for r in cur.execute('SELECT id, title, total_items, correct_items, notes FROM tests WHERE test_date = "2026-10-09"').fetchall():
    print(r)

con.close()
