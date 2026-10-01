import json
import re
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

q_map = {q['id']: q for q in questions}

print("Exam 1 Listening Questions (76~107):")
for qid in range(76, 108):
    q = q_map.get(qid, {})
    prob = q.get('problemNo', '')
    prompt = q.get('prompt', '')[:40]
    audio_dialogue = q.get('audio', [])
    print(f"Q{qid} ({prob}): prompt='{prompt}', audio lines={len(audio_dialogue)}")

