import sqlite3

conn = sqlite3.connect('database/jlpt_learning.db')
cur = conn.cursor()

cur.execute("SELECT id, test_date, title, source_class, total_items, correct_items, elapsed_seconds FROM tests ORDER BY test_date DESC;")
for row in cur.fetchall():
    print(row)
