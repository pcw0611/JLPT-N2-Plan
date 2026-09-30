import json

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

listening_qs = data['questions'][72:]
print(f"Total listening questions: {len(listening_qs)}")

for idx, q in enumerate(listening_qs):
    print(f"[{idx+1}] ID:{q['id']} Part:{q.get('part')} Prob:{q.get('problemNo')} Ans:{q.get('answer')}")
    print(f"  Prompt: {q.get('prompt')}")
    print(f"  Choices: {q.get('choices')}")
    first_audio = q.get('audio', [{}])[0].get('text', '') if q.get('audio') else ''
    print(f"  First audio: {first_audio[:40]}")
