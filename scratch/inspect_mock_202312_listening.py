import json
import re

with open('quiz_sites/n2-past-exam-202312-mock.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', text, re.DOTALL)
if m:
    questions = json.loads(m.group(1))
    listening_qs = [q for q in questions if q.get('id') >= 73]
    print(f"Total listening questions in mock html: {len(listening_qs)}")
    for q in listening_qs:
        qid = q['id']
        prob = q.get('problemNo', '')
        prompt = q.get('prompt', '').replace('\n', ' ')
        choices = q.get('choices', [])
        print(f"Q{qid} ({prob}): prompt='{prompt[:50]}'")
        print(f"    choices: {choices}")
        if 'audio' in q:
            print(f"    audio: {q.get('audio')}")
        print()
else:
    print("Could not find RAW_QUESTIONS")
