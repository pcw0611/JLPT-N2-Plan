import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for idx, q in enumerate(d['questions'][72:], start=73):
    print(f"{idx}: Q{q['id']} - {q.get('problemNo')} {q.get('part')} - {q.get('prompt')[:40]}")
