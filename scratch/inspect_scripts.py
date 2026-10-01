import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))
q_map = {q['id']: q for q in questions}

for qid in [76, 80, 90, 94, 97, 99, 102, 106]:
    q = q_map.get(qid, {})
    lines = q.get('audio', [])
    print(f"\n=== Exam 1 Q{qid} ({len(lines)} lines) ===")
    for line in lines:
        spk = "女" if line.get("speaker") == 1 else ("男" if line.get("speaker") == 2 else str(line.get("speaker")))
        print(f"  {spk}: {line.get('text')}")

