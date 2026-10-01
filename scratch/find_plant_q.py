import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data['questions']:
    text = q.get('instruction', '') + q.get('prompt', '') + json.dumps(q.get('choices', []))
    if '植物を育てるとき' in text:
        print(f"Question ID: {q['id']}, Problem: {q.get('problemNo')}, Part: {q.get('part')}")
        print(f"Category: {q.get('category')}")
        print(f"Prompt: {q.get('prompt')}")
        print(f"Choices: {q.get('choices')}")
        print(f"Ans: {q.get('answer')}")
