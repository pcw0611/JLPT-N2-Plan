# -*- coding: utf-8 -*-
import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for x in items:
    if x['num'] in ['082', '083', '084', '090', '091', '093', '094', '095', '096', '098', '099', '100', '102', '103', '105']:
        print(f"[{x['num']}] PATTERN: {x['pattern']}")
        print(f"   JA: {x['sentence_ja']}")
        print(f"   KO: {x['sentence_ko']}")
        print(f"   T_JA_OLD: {x['sentence_ja_target']}")
        print(f"   T_KO_OLD: {x['target_ko']}")
        print("-" * 50)
