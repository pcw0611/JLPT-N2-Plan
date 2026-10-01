import sqlite3
import json
import sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()

c.execute("SELECT item_no, item_type_id FROM question_attempts WHERE test_id='official-vol2-full-mock-20260920' ORDER BY item_no")
rows = c.fetchall()
print(f"Total attempts recorded for official-vol2: {len(rows)}")

counts = Counter(r[1] for r in rows)
for k, v in sorted(counts.items()):
    print(f"  {k}: {v}문항")
