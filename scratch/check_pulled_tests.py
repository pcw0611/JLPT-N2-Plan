import sqlite3

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
cur.execute("SELECT id, test_date, title, total_items, correct_items, elapsed_seconds, notes FROM tests WHERE id LIKE 'online-sub-%'")
for r in cur.fetchall():
    print(r)
