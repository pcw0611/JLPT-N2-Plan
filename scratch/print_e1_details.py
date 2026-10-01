import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    e1_html = f.read()

m1 = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', e1_html, re.DOTALL)
e1_questions = json.loads(m1.group(1))
e1_map = {q['id']: q for q in e1_questions}

e1_wrongs = [76, 80, 90, 94, 97, 99, 102, 106]
for qid in e1_wrongs:
    q = e1_map.get(qid)
    print(f"=== Exam 1 Q{qid} ({q.get('problemNo')}) ===")
    print("Prompt:", q.get('prompt'))
    print("Choices:", q.get('choices'))
    print("Answer:", q.get('answer'), "->", q.get('choices')[q.get('answer')] if q.get('answer') is not None and q.get('choices') else "None")
    print("Audio lines:")
    for l in q.get('audio', []):
        print("  ", l)
    print()
