import sqlite3
import json

conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()
c.execute('SELECT id, test_date, title, source_class, total_items, correct_items, unknown_items, unanswered_items, elapsed_seconds FROM tests ORDER BY test_date DESC LIMIT 20')
for row in c.fetchall():
    print(row)
