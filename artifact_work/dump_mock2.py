import sqlite3
import json

conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()
c.execute("SELECT notes FROM tests WHERE id='official-vol2-full-mock-20260920'")
row = c.fetchone()
if row and row[0]:
    with open('artifact_work/mock2_notes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(json.loads(row[0]), indent=2, ensure_ascii=False))
    print("Saved mock2_notes.json")
else:
    print("No notes found")
