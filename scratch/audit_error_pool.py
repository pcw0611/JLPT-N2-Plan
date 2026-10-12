# -*- coding: utf-8 -*-
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const ALL_ERROR_QUESTIONS = (\[.*?\]);\s*\n', text)
questions = json.loads(m.group(1))

print(f"Total error pool questions: {len(questions)}")
suspicious = []

for idx, q in enumerate(questions):
    qid = q.get('id')
    qnum = q.get('q_num')
    section = q.get('section')
    m_title = q.get('mondai_title', '')
    is_lis = q.get('is_listening', False)
    passage = q.get('passage_text', '')
    qtext = q.get('question_text', '')
    choices = q.get('choices', [])

    issues = []

    # Check reading / passage
    if any(k in m_title for k in ['文章の文法', '読解', '情報検索', '統合理解', '短文', '中文', '長文']):
        if not passage or len(passage.strip()) == 0:
            issues.append(f"MISSING PASSAGE (title={m_title})")

    # Check question text
    if not qtext or len(qtext.strip()) == 0:
        issues.append("EMPTY QUESTION TEXT")
    elif qtext.strip() in ['問題9 (文章の文法)', '問題', '']:
        issues.append(f"GENERIC QUESTION TEXT ('{qtext}')")

    # Check choices
    if not choices or len(choices) < 2:
        issues.append(f"INVALID CHOICES (count={len(choices)})")

    # Check listening audio
    if is_lis:
        audio = q.get('audio_file', '')
        if not audio:
            issues.append("MISSING AUDIO FILE")

    if issues:
        suspicious.append((idx + 1, qid, qnum, section, m_title, issues))

print(f"\nFound {len(suspicious)} suspicious questions:")
for item in suspicious:
    print(f"#{item[0]} [{item[1]} / {item[2]}] Section: {item[3]} | Title: {item[4]}")
    for iss in item[5]:
        print(f"    -> {iss}")
