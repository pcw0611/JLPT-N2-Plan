import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

print('=== all tests since Oct 1 ===')
for r in cur.execute('SELECT id, test_date, title, total_items, correct_items, elapsed_seconds FROM tests WHERE test_date >= "2026-10-01" ORDER BY test_date, id').fetchall():
    print(r)

con.close()
