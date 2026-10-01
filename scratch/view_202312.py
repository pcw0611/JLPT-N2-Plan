import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data['questions']:
    if q['id'] in [75, 76, 77]:
        print(f"=== Q{q['id']} ===")
        print("Prompt:", q.get('prompt'))
        print("Choices:", q.get('choices'))
        print("Translation:", q.get('translation'))
        print("Example / Script:", q.get('example'))
