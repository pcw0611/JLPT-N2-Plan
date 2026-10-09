import sys, json, re

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
listening_qs = [q for q in questions if q.get('is_listening') or q.get('section') == '聴解']

for idx in range(0, 16):
    q = listening_qs[idx]
    exp = q.get('explanation_html', '')
    dialogue_lines = re.findall(r'<b[^>]*>([^<]+)</b>\s*([^<]+)', exp)
    print(f"\n==================================================")
    print(f"[{idx+1:02d}] {q['id']} | {q['exam_src']} | {q['q_num']} | audio: {q['audio_file']}")
    print(f"Category: {q['category_detail']}")
    print(f"Choices: {q['choices']}")
    print(f"Correct: {q['correct_num']} - {q['correct_text']}")
    print("Script extracted from explanation:")
    for spk, line in dialogue_lines[:4]:
        print(f"  {spk}: {line[:70]}...")
