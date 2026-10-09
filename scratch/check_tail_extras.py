# -*- coding: utf-8 -*-
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for x in items:
    num = x['num']
    pat = x['pattern']
    tgt = x['sentence_ja_target']
    ja = x['sentence_ja']
    
    # Clean pattern
    alts = [p.replace('〜', '').strip() for p in re.split(r'[/／・]', pat)]
    
    # Check if tgt ends with extra characters not in alt
    # E.g. alt = "たばかり", tgt = "ばかりなのに" -> trailing "なのに"
    # E.g. alt = "からすると", tgt = "ことからすると"
    for alt in alts:
        clean_alt = alt.replace('（', '').replace('）', '').replace('(', '').replace(')', '')
        if clean_alt in tgt:
            idx = tgt.find(clean_alt)
            tail = tgt[idx + len(clean_alt):]
            if tail:
                print(f"[{num:0>3}] TAIL EXTRA '{tail}': PAT '{pat}' | TGT '{tgt}' | JA '{ja}'")
