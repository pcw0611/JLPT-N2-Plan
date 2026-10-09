import sys, json

sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = 'const ALL_ERROR_QUESTIONS = '
start_idx = text.find(start_marker) + len(start_marker)
end_idx = text.find(';\n\nlet currentQuestions = [];', start_idx)
if end_idx == -1:
    end_idx = text.find('];', start_idx) + 1

raw_json = text[start_idx:end_idx].strip()
questions = json.loads(raw_json)

listening_qs = [q for q in questions if q.get('is_listening') or q.get('section') == '聴解']
print(f'Total questions in pool: {len(questions)}')
print(f'Total listening questions: {len(listening_qs)}')

for idx, q in enumerate(listening_qs):
    print(f"{idx+1:2d}. id={q['id']:15s} | exam_src={q.get('exam_src')} | q_num={q.get('q_num')} | audio={q.get('audio_file')} | cat={q.get('category_detail')}")
