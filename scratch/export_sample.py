import sqlite3
import json

conn = sqlite3.connect('database/jlpt_learning.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT * FROM tests WHERE id = 'official-vol2-full-mock-20260920';")
test_row = dict(cur.fetchone())
with open('scratch/prev_test.json', 'w', encoding='utf-8') as f:
    json.dump(test_row, f, ensure_ascii=False, indent=2)

cur.execute("SELECT * FROM question_attempts WHERE test_id = 'official-vol2-full-mock-20260920' LIMIT 5;")
attempts = [dict(r) for r in cur.fetchall()]
with open('scratch/prev_attempts.json', 'w', encoding='utf-8') as f:
    json.dump(attempts, f, ensure_ascii=False, indent=2)

print("Saved prev_test and prev_attempts to json")
