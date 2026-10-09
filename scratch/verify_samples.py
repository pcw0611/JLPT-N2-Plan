# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)
for x in items:
    if x['num'] in ['008', '021', '054']:
        print(f"[{x['num']}] {x['pattern']} -> blank: {x['sentence_ja_blank']} | tgt: {x['sentence_ja_target']} | tko: {x['target_ko']}")
