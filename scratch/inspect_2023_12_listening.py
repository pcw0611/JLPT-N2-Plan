import json

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

listening_qs = [q for q in data['questions'] if q['id'] >= 73]
print("2023_12 listening count:", len(listening_qs))
if listening_qs:
    q = listening_qs[0]
    print("Q73 keys:", list(q.keys()))
    print("Q73 audio:", q.get('audio'))
