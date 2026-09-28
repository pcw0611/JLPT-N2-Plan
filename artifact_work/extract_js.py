import re

with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);\s*\n\s*(.*)', html, re.DOTALL)
if m:
    print("Found RAW_QUESTIONS. Length of json string:", len(m.group(1)))
    rest = m.group(2)
    print("Next 500 characters after RAW_QUESTIONS:\n", rest[:500])
    with open('artifact_work/mock_js_tail.js', 'w', encoding='utf-8') as out:
        out.write(rest)
    print("Saved mock_js_tail.js")
else:
    print("Not found")
