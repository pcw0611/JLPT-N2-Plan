import sqlite3
import json
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Tables:", tables)

with open('jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html', encoding='utf-8') as f:
    text = f.read()

import re
match = re.search(r'\{"id":\s*"err-listen-06".*?\}\s*,\s*\{"id":', text, re.DOTALL)
if match:
    item_str = match.group(0)[:-len(', {"id":')]
    item = json.loads(item_str)
    print("q_num:", item.get("q_num"))
    print("mondai_title:", item.get("mondai_title"))
    print("category_detail:", item.get("category_detail"))
    print("correct_num:", item.get("correct_num"))
    print("explanation preview:")
    exp = item.get("explanation_html", "")
    import re
    clean_exp = re.sub(r'<[^>]+>', ' ', exp)
    print(" ".join(clean_exp.split())[:600])







cur.execute("SELECT * FROM question_attempts WHERE test_id LIKE 'machigai-review-20261008%'")
for r in cur.fetchall():
    print("attempt:", r)




# 2. Check study_intervals on 2026-10-08
cur.execute("SELECT id, duration_seconds, notes FROM study_intervals WHERE session_date = '2026-10-08'")
print("\nStudy intervals on 2026-10-08:")
total_interval_sec = 0
for row in cur.fetchall():
    print(row)
    total_interval_sec += row[1] if row[1] else 0

print(f"\nTotal interval seconds: {total_interval_sec} ({total_interval_sec/60:.2f} mins)")

# 3. Check study_sessions for 2026-10-08
cur.execute("SELECT id, session_date, verified_minutes, summary FROM study_sessions WHERE session_date = '2026-10-08'")
print("\nStudy session for 2026-10-08:")
print(cur.fetchone())

con.close()
