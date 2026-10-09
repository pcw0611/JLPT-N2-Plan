# -*- coding: utf-8 -*-
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for x in items:
    num = x['num']
    pat = x['pattern']
    tgt = x['sentence_ja_target']
    blank = x['sentence_ja_blank']
    full_ja = x['sentence_ja']
    
    # Clean pattern components
    alts = [p.replace('〜', '').strip() for p in re.split(r'[/／・]', pat)]
    
    # Check whether tgt matches an alt or if tgt has extra words before it
    has_exact = False
    for alt in alts:
        # e.g. alt = "からすると", tgt = "ことからすると"
        if tgt == alt:
            has_exact = True
            break
        # or alt with conjugation
        if tgt.startswith(alt) or alt.startswith(tgt):
            has_exact = True
            break
            
    if not has_exact:
        print(f"[{num:0>3}] PAT: {pat:25s} | TGT: {tgt:20s}")
        print(f"      JA : {full_ja}")
        print(f"      BLK: {blank}")
        print()
