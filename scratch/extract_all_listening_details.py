import json
import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. EXAM 1
print("="*60)
print("EXAM 1 (from quiz_sites/n2-midterm-mock-exam-20260920.html)")
with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    e1_html = f.read()

m1 = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', e1_html, re.DOTALL)
e1_questions = json.loads(m1.group(1))
e1_map = {q['id']: q for q in e1_questions}

e1_wrongs = [76, 80, 90, 94, 97, 99, 102, 106]
for qid in e1_wrongs:
    q = e1_map.get(qid)
    print(f"\n[E1 Q{qid}] Problem: {q.get('problemNo')} ({q.get('type')})")
    print(f"  Prompt: {q.get('prompt')}")
    print(f"  Choices: {q.get('choices')}")
    print(f"  Answer: {q.get('answer')}")
    print(f"  Audio dialogue lines ({len(q.get('audio', []))}):")
    for line in q.get('audio', []):
        print(f"    {line}")

# 2. EXAM 2
print("\n" + "="*60)
print("EXAM 2 (from quiz_sites/n2-past-exam-202312-mock.html and 2023_12.json)")
with open('quiz_sites/n2-past-exam-202312-mock.html', 'r', encoding='utf-8') as f:
    e2_html = f.read()

m2 = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', e2_html, re.DOTALL)
e2_questions = json.loads(m2.group(1))
e2_map = {q['id']: q for q in e2_questions}

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    e2_json = json.load(f)
e2_json_map = {q['id']: q for q in e2_json.get('questions', [])}

e2_wrongs = [75, 76, 77, 78, 80, 82, 85, 86, 88, 89, 90, 91, 95, 97, 98, 99, 101]
for qid in e2_wrongs:
    q_html = e2_map.get(qid, {})
    q_json = e2_json_map.get(qid, {})
    print(f"\n[E2 Q{qid}] Problem: {q_html.get('problemNo')}")
    print(f"  Prompt (HTML): {q_html.get('prompt')}")
    print(f"  Prompt (JSON): {q_json.get('prompt')}")
    print(f"  Choices (HTML): {q_html.get('choices')}")
    print(f"  Choices (JSON): {q_json.get('choices')}")
    print(f"  Answer (HTML): {q_html.get('answer')}")
    print(f"  Audio in HTML: {q_html.get('audio')}")
    print(f"  Script/Meaning in JSON: {q_json.get('meaning', '')[:200]}")
