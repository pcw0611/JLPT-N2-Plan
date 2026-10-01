import json
import re
import sqlite3
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()

c.execute("SELECT id, test_date, title FROM tests ORDER BY test_date DESC")
tests = c.fetchall()
print("All tests in DB:")
for t in tests:
    print(f"  {t[0]} | {t[1]} | {t[2]}")

print("\n" + "="*60)
print("--- AUDITING EXAM 1 (2026-09-20) ---")
# Find test 1 id
t1_id = [t[0] for t in tests if '2026-09-20' in t[1]][0]
c.execute("""
    SELECT item_no, item_type_id, response_state, response_seconds, selected_text, correct_text, trap_hypothesis
    FROM question_attempts
    WHERE test_id = ? AND item_no >= 76
    ORDER BY item_no
""", (t1_id,))
t1_attempts = c.fetchall()
print(f"Exam 1 listening attempts ({len(t1_attempts)} total):")
t1_wrongs = [a for a in t1_attempts if a[2] != 'correct']
print(f"Wrong count: {len(t1_wrongs)}")
for a in t1_wrongs:
    print(f"  Item {a[0]} ({a[1]}): state={a[2]}, selected='{a[4]}', correct='{a[5]}'")

print("\n" + "="*60)
print("--- AUDITING EXAM 2 (2026-09-30) ---")
t2_id = [t[0] for t in tests if '2026-09-30' in t[1] or '202312' in t[0]][0]
c.execute("""
    SELECT item_no, item_type_id, response_state, response_seconds, selected_text, correct_text, trap_hypothesis
    FROM question_attempts
    WHERE test_id = ? AND item_no >= 73
    ORDER BY item_no
""", (t2_id,))
t2_attempts = c.fetchall()
print(f"Exam 2 listening attempts ({len(t2_attempts)} total):")
t2_wrongs = [a for a in t2_attempts if a[2] != 'correct']
print(f"Wrong count: {len(t2_wrongs)}")
for a in t2_wrongs:
    print(f"  Item {a[0]} ({a[1]}): state={a[2]}, selected='{a[4]}', correct='{a[5]}'")

