# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('database/past_exams/2023_12.json', encoding='utf-8'))
print(f"Total questions: {len(data['questions'])}")

for q in data['questions']:
    ans = q.get('answer')
    choices = q.get('choices', [])
    qid = q.get('id')
    if not (0 <= ans < len(choices)):
        print(f"ERROR: Q{qid} answer index {ans} out of bounds")
    
    # Check 問題8
    if q.get('problemNo') == '問題8':
        conn = q.get('connection', '')
        meaning = q.get('meaning', '')
        print(f"Q{qid}: ans_idx={ans} (Choice {ans+1}: '{choices[ans]}') | meaning: {meaning} | conn: {conn}")

