import sqlite3
import json
import sys, io

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()

# Get Exam 1 attempts
c.execute("SELECT id FROM tests WHERE test_date LIKE '2026-09-20%'")
t1_id = c.fetchone()[0]

c.execute("SELECT id FROM tests WHERE test_date LIKE '2026-09-30%'")
t2_id = c.fetchone()[0]

e1_items = [76, 80, 90, 94, 97, 99, 102, 106]
e2_items = [75, 76, 77, 78, 80, 82, 85, 86, 88, 89, 90, 91, 95, 97, 98, 99, 101]

db_data = {}

for item in e1_items:
    c.execute("""
        SELECT item_no, item_type_id, response_state, response_seconds, selected_text, correct_text, trap_hypothesis
        FROM question_attempts
        WHERE test_id = ? AND item_no = ?
    """, (t1_id, item))
    row = c.fetchone()
    db_data[('1회_공식제2집', item)] = {
        'item_no': row[0],
        'type': row[1],
        'state': row[2],
        'seconds': row[3],
        'selected': row[4],
        'correct': row[5],
        'trap': row[6]
    }

for item in e2_items:
    c.execute("""
        SELECT item_no, item_type_id, response_state, response_seconds, selected_text, correct_text, trap_hypothesis
        FROM question_attempts
        WHERE test_id = ? AND item_no = ?
    """, (t2_id, item))
    row = c.fetchone()
    db_data[('2회_202312', item)] = {
        'item_no': row[0],
        'type': row[1],
        'state': row[2],
        'seconds': row[3],
        'selected': row[4],
        'correct': row[5],
        'trap': row[6]
    }

print(f"Dumped {len(db_data)} DB rows successfully!")
with open('scratch/db_listening_25.json', 'w', encoding='utf-8') as f:
    json.dump({f"{k[0]}_Q{k[1]}": v for k, v in db_data.items()}, f, ensure_ascii=False, indent=2)
print("Saved to scratch/db_listening_25.json")
