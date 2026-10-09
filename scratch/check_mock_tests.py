import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

print('=== 2023.12 mock exam in tests ===')
for r in cur.execute('SELECT id, test_date, title, total_items, correct_items, notes FROM tests WHERE title LIKE "%2023%" OR title LIKE "%제2집%"').fetchall():
    print(r)

con.close()
