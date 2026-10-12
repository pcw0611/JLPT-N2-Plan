import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/public/exams/n2-past-exam-202312-mock.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const (?:QUESTIONS|RAW_QUESTIONS|examData|questions)\s*=\s*(\[.*?\]);\s*\n', text, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    print(f"Total questions in 202312: {len(data)}")
    for q in data:
        qid = q.get('id')
        if qid in [48, 49, 50, 51, 52, 53, 54, 57, 58, 63, 64, 66, 67, 69]:
            keys = list(q.keys())
            print(f"ID {qid} ({q.get('problemNo')} {q.get('subtype')}): keys={keys}")
            for k in ['instruction', 'passage', 'passage_text', 'text', 'prompt', 'question_text', 'context']:
                if k in q and q[k]:
                    print(f"   {k}: {str(q[k])[:80].replace(chr(10), ' ')}")
