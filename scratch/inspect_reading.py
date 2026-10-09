import json, sys
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan\jlpt-calendar-site\public\exams\n2-mock-error-review-pool.html'
content = open(html_path, 'r', encoding='utf-8').read()

idx1 = content.find('const ALL_ERROR_QUESTIONS = [')
idx2 = content.find('];\n  </script>', idx1)
if idx2 == -1: idx2 = content.find('];\r\n  </script>', idx1)

data = json.loads(content[idx1 + len('const ALL_ERROR_QUESTIONS = '):idx2 + 1])

reading_items = [q for q in data if '読解' in q.get('section', '')]
print(f"Total reading items: {len(reading_items)}")

for q in reading_items:
    print(f"\n==========================================")
    print(f"ID: {q['id']} | Num: {q['q_num']} | Mondai: {q['mondai_title']}")
    print(f"question_text: {q['question_text']}")
    print(f"instruction: {q['instruction'][:80]}...")
    print(f"passage length: {len(q.get('passage_text', ''))}")
    print(f"choices: {q['choices'][:2]}...")
