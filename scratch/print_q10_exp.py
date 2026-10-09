import sys, json

sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = 'const ALL_ERROR_QUESTIONS = '
start_idx = text.find(start_marker) + len(start_marker)

bracket_depth = 0
in_string = False
escape = False
quote_char = None
end_idx = -1

for i in range(start_idx, len(text)):
    c = text[i]
    if in_string:
        if escape:
            escape = False
        elif c == '\\':
            escape = True
        elif c == quote_char:
            in_string = False
    else:
        if c in ('"', "'"):
            in_string = True
            quote_char = c
        elif c == '[':
            bracket_depth += 1
        elif c == ']':
            bracket_depth -= 1
            if bracket_depth == 0:
                end_idx = i + 1
                break

questions = json.loads(text[start_idx:end_idx].strip())
q10 = [q for q in questions if q.get('id') == 'err-listen-10'][0]
print("explanation_html:")
print(q10['explanation_html'])
