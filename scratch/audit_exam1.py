import json
import re
import sqlite3
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. DB attempts for Exam 1
conn = sqlite3.connect('database/jlpt_learning.db')
cursor = conn.cursor()

# Find Exam 1 test ID
cursor.execute("SELECT test_id, name, date FROM tests WHERE date LIKE '2026-09-20%' OR name LIKE '%2집%'")
rows = cursor.fetchall()
print("Tests matching Exam 1:", rows)

test_id = rows[0][0] if rows else 'official-vol2-full-mock-20260920'

cursor.execute("""
    SELECT question_id, section, problem_number, is_correct, selected_answer, answer_time_seconds
    FROM question_attempts
    WHERE test_id = ? AND section = 'listening'
""", (test_id,))
attempts = cursor.fetchall()
print(f"Total listening attempts in DB for {test_id}: {len(attempts)}")
wrong_attempts = [a for a in attempts if not a[3]]
print(f"Wrong listening attempts ({len(wrong_attempts)}):")
for a in wrong_attempts:
    print(f"  Q{a[0]} ({a[2]}): user_ans={a[4]}, time={a[5]}s")

# 2. Check quiz_sites/n2-midterm-mock-exam-20260920.html
with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', html, re.DOTALL)
if m:
    raw_q = json.loads(m.group(1))
    q_map = {q['id']: q for q in raw_q}
    print("\n--- Exam 1 Mock HTML questions for wrong items ---")
    for a in wrong_attempts:
        qid = a[0]
        q = q_map.get(qid)
        if q:
            print(f"\n[HTML Q{qid}] Problem: {q.get('problemNo')} / Type: {q.get('type')}")
            print(f"  Prompt: {q.get('prompt')}")
            print(f"  Choices: {q.get('choices')}")
            print(f"  Answer: {q.get('answer')}")
            print(f"  Audio lines: {q.get('audio')}")
        else:
            print(f"  Q{qid} NOT FOUND in HTML!")
