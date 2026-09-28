import json

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

listening_qs = [q for q in data['questions'] if q.get('section') == 2 or q.get('part') == '聴解']

with open('artifact_work/listening_sample.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total listening: {len(listening_qs)}\n")
    for q in listening_qs[:5]:
        f.write(f"ID: {q.get('id')}, Problem: {q.get('problemNo')}, Subtype: {q.get('subtype')}\n")
        f.write(f"Prompt: {q.get('prompt')}\n")
        f.write(f"Choices: {q.get('choices')}\n")
        f.write(f"Audio/Script info: {q.get('audio')}\n")
        f.write(f"Translation: {q.get('translation')}\n")
        f.write("-" * 50 + "\n")
print("Done")
