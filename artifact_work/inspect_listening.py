import json

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

listening_qs = [q for q in data['questions'] if q.get('section') == 2 or q.get('part') == '聴解']
print(f"Total listening questions: {len(listening_qs)}")

sample_l = listening_qs[0]
print("Sample Q keys:", list(sample_l.keys()))
print("Sample Q:", json.dumps({
    'id': sample_l.get('id'),
    'problemNo': sample_l.get('problemNo'),
    'prompt': sample_l.get('prompt'),
    'choices': sample_l.get('choices'),
    'script': sample_l.get('script'),
    'audioText': sample_l.get('audioText'),
    'speakers': sample_l.get('speakers')
}, ensure_ascii=False, indent=2))
