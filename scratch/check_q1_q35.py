import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data['questions'][:35]:
    correct_choice = q['choices'][q['answer']] if 0 <= q['answer'] < len(q['choices']) else 'INVALID'
    print(f"Q{q['id']} ({q.get('problemNo')}): ans_idx={q['answer']} (Option {q['answer']+1}) -> '{correct_choice}' | prompt: {q['prompt'][:40]}")
