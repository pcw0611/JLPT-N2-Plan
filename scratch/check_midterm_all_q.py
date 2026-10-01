import json, re, sys, io
sys.stdout.reconfigure(encoding='utf-8')

with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', text, re.DOTALL)
qs = json.loads(m.group(1))
q_map = {q['id']: q for q in qs}

print("=== Q76 to Q82 in n2-midterm-mock-exam-20260920.html ===")
for qid in range(76, 83):
    q = q_map.get(qid, {})
    print(f"\nQ{qid}: {q.get('problemNo')} ({q.get('category', '')})")
    print("  Prompt:", q.get('prompt'))
    print("  Choices:", q.get('choices'))
    print("  Answer:", q.get('answer'))
    print("  Audio:", q.get('audio'))
