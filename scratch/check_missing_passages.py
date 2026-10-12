# -*- coding: utf-8 -*-
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load midterm 20260920
with open('jlpt-calendar-site/public/exams/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    text_mid = f.read()

m_mid = re.search(r'const (?:QUESTIONS|RAW_QUESTIONS|examData|questions)\s*=\s*(\[.*?\]);\s*\n', text_mid, re.DOTALL)
if not m_mid:
    # search for array of objects with id: 54
    m_mid = re.search(r'const QUESTIONS\s*=\s*(\[.*?\]);', text_mid, re.DOTALL)
mid_questions = {q['id']: q for q in json.loads(m_mid.group(1))} if m_mid else {}
print("Loaded midterm questions:", len(mid_questions))

# 2. Load past 202312
with open('jlpt-calendar-site/public/exams/n2-past-exam-202312-mock.html', 'r', encoding='utf-8') as f:
    text_past = f.read()

m_past = re.search(r'const (?:QUESTIONS|RAW_QUESTIONS|examData|questions)\s*=\s*(\[.*?\]);\s*\n', text_past, re.DOTALL)
past_questions = {q['id']: q for q in json.loads(m_past.group(1))} if m_past else {}
print("Loaded past 202312 questions:", len(past_questions))

# Check err-lang questions from n2-mock-error-review-pool.html
with open('jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html', 'r', encoding='utf-8') as f:
    text_pool = f.read()

m_pool = re.search(r'const ALL_ERROR_QUESTIONS = (\[.*?\]);\s*\n', text_pool)
pool_questions = json.loads(m_pool.group(1))
print("Loaded pool questions:", len(pool_questions))

# Check which ones need passage
for q in pool_questions:
    qid = q['id']
    qnum_int = int(q['q_num'].replace('Q', ''))
    exam_src = q['exam_src']
    
    if len(q.get('passage_text', '')) == 0 and ('問題9' in q.get('mondai_title', '') or '読解' in q.get('section', '')):
        print(f"\nTarget: {qid} ({q['q_num']}) from {exam_src}")
        if '第2集' in exam_src:
            orig = mid_questions.get(qnum_int)
        else:
            orig = past_questions.get(qnum_int)
            
        if orig:
            print("  Found orig:", orig.get('id'), orig.get('problemNo'), orig.get('subtype'))
            print("  orig prompt:", orig.get('prompt'))
            instr = orig.get('instruction', '')
            print("  orig instruction len:", len(instr), "snippet:", instr[:120].replace('\n', ' '))
        else:
            print("  NOT FOUND in orig!")
