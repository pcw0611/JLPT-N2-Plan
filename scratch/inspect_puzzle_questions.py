import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/public/exams/n2-grammar-puzzle.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const QUESTIONS\s*=\s*(\[.*?\]);', text, re.DOTALL)
questions = json.loads(m.group(1))

print(f"Total questions: {len(questions)}")
courses = {}
for q in questions:
    c_list = q.get('course', ['all'])
    if isinstance(c_list, str):
        c_list = [c_list]
    for c in c_list:
        courses[c] = courses.get(c, 0) + 1
print("Courses in puzzle:", courses)

for i, q in enumerate(questions):
    print(f"{i+1:2d}. [{q.get('id')}] {q.get('grammar_point')}: {q.get('meaning')}")
