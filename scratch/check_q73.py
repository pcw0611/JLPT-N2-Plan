import json

data = json.load(open('database/past_exams/2023_12.json', encoding='utf-8'))
q = data['questions'][72]
print("ID:", q.get('id'))
print("choices:", q.get('choices'))
print("prompt:", q.get('prompt'))
print("translation:", q.get('translation'))
print("audio lines:")
for a in q.get('audio', []):
    print(" ", a)
