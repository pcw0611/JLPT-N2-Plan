# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/public/exams/n2-grammar-speedrun.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('const ALL_PATTERNS = [')
idx2 = text.find('];\n\nclass SoundEngine', idx1)
patterns = json.loads(text[idx1 + len('const ALL_PATTERNS = '):idx2 + 1])
print(f"Total patterns in HTML: {len(patterns)}")

for p in patterns:
    if p['num'] in ['008', '021', '054']:
        print(f"[{p['num']}] {p['pattern']} -> blank: {p['sentence_ja_blank']} | tgt: {p['sentence_ja_target']} | tko: {p['target_ko']}")
