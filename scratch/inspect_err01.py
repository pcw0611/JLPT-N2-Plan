import sys, json

sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = 'const ALL_ERROR_QUESTIONS = '
start_idx = text.find(start_marker) + len(start_marker)
# Find matching closing bracket
# Let's count brackets
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

raw_json = text[start_idx:end_idx].strip()
questions = json.loads(raw_json)

q = [x for x in questions if x.get('id') == 'err-listen-01'][0]
print('id:', q['id'])
print('exam_src:', q['exam_src'])
print('q_num:', q['q_num'])
print('category_detail:', q['category_detail'])
print('choices:', q['choices'])
print('correct_num:', q['correct_num'])
print('correct_text:', q['correct_text'])
print('audio_file:', q['audio_file'])
print('explanation_html:')
print(q['explanation_html'])
