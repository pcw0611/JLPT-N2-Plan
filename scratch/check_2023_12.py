import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total questions: {len(data['questions'])}")

flagged = [8, 40, 41, 42, 43, 44, 45, 46, 47]
for q in data['questions']:
    if q['id'] in flagged:
        print("="*60)
        print(f"ID: {q['id']}, ProblemNo: {q.get('problemNo')}, Part: {q.get('part')}, Ans: {q.get('answer')}")
        print(f"Prompt: {q.get('prompt')}")
        for i, c in enumerate(q.get('choices', [])):
            print(f"  {i+1}: {c}")
        print(f"Explanation trap/meaning: {q.get('meaning', '')} | {q.get('trap', '')}")
