import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    exam = json.load(f)

q_map = {q['id']: q for q in exam['questions']}

e2_wrong_listening = [75, 76, 77, 78, 80, 82, 85, 86, 88, 89, 90, 91, 95, 97, 98, 99, 101]

for qid in e2_wrong_listening:
    q = q_map.get(qid, {})
    prob = q.get('problemNo', '')
    prompt = q.get('prompt', '')
    choices = q.get('choices', [])
    meaning = q.get('meaning', '')
    print(f"\n=== Exam 2 Q{qid} ({prob}) ===")
    print("Prompt:", prompt)
    print("Meaning snippet:", meaning[:200])
    if prob == '問題4':
        print("Choices (Spoken replies):", choices)

