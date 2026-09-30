import sqlite3
import json

conn = sqlite3.connect('database/jlpt_learning.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT * FROM tests WHERE id = 'official-vol2-full-mock-20260920';")
row = dict(cur.fetchone())
for k, v in row.items():
    print(f"{k}: {v}")

cur.execute("SELECT count(*) as cnt FROM question_attempts WHERE test_id = 'official-vol2-full-mock-20260920';")
print("Attempts count:", cur.fetchone()['cnt'])

cur.execute("SELECT * FROM question_attempts WHERE test_id = 'official-vol2-full-mock-20260920' LIMIT 2;")
for r in cur.fetchall():
    print(dict(r))
