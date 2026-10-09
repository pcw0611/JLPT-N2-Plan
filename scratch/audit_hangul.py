# -*- coding: utf-8 -*-
import re
from questions_data import QUESTIONS

hangul = re.compile(r'[\uac00-\ud7af\u1100-\u11ff\u3130-\u318f]')

found = []

for q in QUESTIONS:
    qid = q['id']
    for field in ['prompt_prefix', 'prompt_suffix', 'full_sentence']:
        val = q.get(field, '')
        if hangul.search(val):
            found.append((qid, field, val))
    for s in q.get('slots', []):
        ans = s.get('answer', '')
        if hangul.search(ans):
            found.append((qid, f"slot_{s['id']}", ans))
    for idx, b in enumerate(q.get('blocks', [])):
        if hangul.search(b):
            found.append((qid, f"block_{idx}", b))

print(f"Total Hangul defects found: {len(found)}")
for item in found:
    print(f"  [{item[0]}] {item[1]} -> '{item[2]}'")
