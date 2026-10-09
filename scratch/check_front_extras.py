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
    
    # For each alt, check if tgt contains alt, but has extra characters AT THE FRONT of alt!
    for alt in alts:
        # e.g. alt = "からすると", tgt = "ことからすると" -> extra at front: "こと"
        clean_alt = alt.replace('（', '').replace('）', '').replace('(', '').replace(')', '')
        # check if clean_alt in tgt
        if clean_alt in tgt:
            idx = tgt.find(clean_alt)
            if idx > 0:
                front = tgt[:idx]
                print(f"[{num:0>3}] FRONT EXTRA '{front}': PAT '{pat}' | TGT '{tgt}' | JA '{ja}'")
