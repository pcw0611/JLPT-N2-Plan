import json, re, sys, pypdf
sys.stdout.reconfigure(encoding='utf-8')

# 1. 9/20 Quiz site
with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);\s*\n', html, re.DOTALL)
if not m: m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', html, re.DOTALL)
qs = json.loads(m.group(1))

print('=== [9/20 퀴즈 사이트에 들어있던 청해 문항] ===')
for q in qs:
    qid = q['id']
    if qid in [76, 77, 78, 81, 82]:
        p = q.get('prompt', '').replace('\n', ' ')
        print(f"ID {qid} ({q.get('problemNo')}) : {p}")
        print(f"   선택지: {q.get('choices')}")

# 2. Official Workbook Script
reader = pypdf.PdfReader('references/official_vol2_listening/N2_listening_script.pdf')
full_text = '\n'.join([p.extract_text() for p in reader.pages])

print('\n=== [공식 문제집 제2집 원본 스크립트 대문항별 1, 2번] ===')
# Let's inspect Problem 1
m1 = re.search(r'問題 1(.*?)問題 2', full_text, re.DOTALL)
if m1:
    txt = m1.group(1)
    parts = re.split(r'(\d+番|例)', txt)
    for i in range(1, len(parts), 2):
        label = parts[i]
        body = parts[i+1]
        first_few = [l.strip() for l in body.split('\n') if len(l.strip()) > 3][:3]
        print(f"問題 1 - {label}: {' '.join(first_few)}")

m2 = re.search(r'問題 2(.*?)問題 3', full_text, re.DOTALL)
if m2:
    txt = m2.group(1)
    parts = re.split(r'(\d+番|例)', txt)
    for i in range(1, len(parts), 2):
        label = parts[i]
        body = parts[i+1]
        first_few = [l.strip() for l in body.split('\n') if len(l.strip()) > 3][:3]
        print(f"問題 2 - {label}: {' '.join(first_few)}")
