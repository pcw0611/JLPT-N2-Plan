import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("--- Searching in 2023_12.json ---")
for q in data['questions']:
    if q.get('sectionName') == '聴解':
        full_text = f"{q.get('prompt', '')} {q.get('meaning', '')} {q.get('translation', '')} {q.get('example', '')}"
        if 'ラジオ' in full_text or '라디오' in full_text:
            print(f"Q{q['id']} ({q.get('problemNo')}): {q.get('prompt')}")
            print(f"Meaning snippet: {q.get('meaning', '')[:300]}")
            print("="*50)

print("\n--- Searching in VTT subtitle ---")
with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    vtt = f.read()

lines = vtt.split('\n')
for i, line in enumerate(lines):
    if 'ラジオ' in line:
        start = max(0, i-5)
        end = min(len(lines), i+15)
        print(f"VTT around line {i}:")
        for j in range(start, end):
            print(f"  {lines[j]}")
        print("="*50)
