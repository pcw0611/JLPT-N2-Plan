import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', html, re.DOTALL)
qs = json.loads(m.group(1))

print(f"Total questions: {len(qs)}")
for q in qs:
    qid = q['id']
    if 76 <= qid <= 85:
        p = q.get('prompt', '').replace('\n', ' ')
        choices = q.get('choices', [])
        ans = q.get('correctAnswer')
        print(f"Q{qid} [{q.get('problemNo')}]: {p}")
        print(f"   Choices: {choices}")
        print(f"   Ans: {ans}")
