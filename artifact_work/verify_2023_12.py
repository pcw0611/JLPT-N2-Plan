import json

with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Exam ID:', data.get('examId'))
print('Total Items in JSON:', len(data.get('questions', [])))
print('Declared TotalItems:', data.get('totalItems'))

sections = {}
parts = {}
problem_nos = {}
errors = []

for idx, q in enumerate(data['questions']):
    qid = q.get('id')
    sec = q.get('sectionName', 'unknown')
    part = q.get('part', 'unknown')
    prob = q.get('problemNo', 'unknown')
    
    sections[sec] = sections.get(sec, 0) + 1
    parts[part] = parts.get(part, 0) + 1
    problem_nos[prob] = problem_nos.get(prob, 0) + 1
    
    # Check required fields
    for field in ['instruction', 'prompt', 'choices', 'answer', 'translation']:
        if field not in q or q[field] is None:
            errors.append(f"Q{qid}: missing {field}")
            
    choices = q.get('choices', [])
    ans = q.get('answer')
    if not isinstance(ans, int) or ans < 0 or ans >= len(choices):
        errors.append(f"Q{qid}: invalid answer index {ans} for choices len {len(choices)}")

with open('artifact_work/2023_12_analysis.txt', 'w', encoding='utf-8') as out:
    out.write(f"Exam: {data.get('title')}\n")
    out.write(f"Total: {len(data['questions'])}\n")
    out.write(f"Sections: {json.dumps(sections, ensure_ascii=False, indent=2)}\n")
    out.write(f"Parts: {json.dumps(parts, ensure_ascii=False, indent=2)}\n")
    out.write(f"ProblemNos: {json.dumps(problem_nos, ensure_ascii=False, indent=2)}\n")
    out.write(f"Errors count: {len(errors)}\n")
    for err in errors[:20]:
        out.write(f"  {err}\n")

print(f"Analysis saved. Total questions: {len(data['questions'])}, Errors: {len(errors)}")
