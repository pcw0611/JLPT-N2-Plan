import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('quiz_sites/n2-past-exam-202312-mock.html', 'r', encoding='utf-8') as f:
    e2_html = f.read()

m2 = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', e2_html, re.DOTALL)
e2_questions = json.loads(m2.group(1))
e2_map = {q['id']: q for q in e2_questions}

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    e2_json = json.load(f)
e2_json_map = {q['id']: q for q in e2_json.get('questions', [])}

e2_wrongs = [75, 76, 77, 78, 80, 82, 85, 86, 88, 89, 90, 91, 95, 97, 98, 99, 101]

for qid in e2_wrongs:
    q_html = e2_map.get(qid, {})
    q_json = e2_json_map.get(qid, {})
    print(f"=== Exam 2 Q{qid} ({q_html.get('problemNo')}) ===")
    print("Prompt HTML:", q_html.get('prompt'))
    print("Choices HTML:", q_html.get('choices'))
    ans_idx = q_html.get('answer')
    ans_text = q_html.get('choices')[ans_idx] if ans_idx is not None and q_html.get('choices') else None
    print(f"Answer HTML: index {ans_idx} -> '{ans_text}'")
    print("Audio HTML:", q_html.get('audio'))
    print("Audio JSON:", q_json.get('audio'))
    print("Script in JSON (audio_script):", q_json.get('audio_script'))
    print("Meaning in JSON:", q_json.get('meaning'))
    print()
