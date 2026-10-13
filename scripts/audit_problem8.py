# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('database/past_exams/2023_12.json', encoding='utf-8'))
for q in data.get('questions', []):
    if q.get('problemNo') == '問題8':
        qid = q.get('id')
        prompt = q.get('prompt')
        choices = q.get('choices')
        ans_idx = q.get('answer')
        chosen_choice = choices[ans_idx] if 0 <= ans_idx < len(choices) else 'INVALID'
        conn = q.get('connection')
        meaning = q.get('meaning')
        print(f"Q{qid}:")
        print(f"  prompt: {prompt}")
        print(f"  choices: {choices}")
        print(f"  answer index: {ans_idx} -> Choice {ans_idx+1}: {chosen_choice}")
        print(f"  connection: {conn}")
        print(f"  meaning: {meaning}")
        print("-" * 50)
