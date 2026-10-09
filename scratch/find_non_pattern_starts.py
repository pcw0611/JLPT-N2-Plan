# -*- coding: utf-8 -*-
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('scratch/pat_vs_tgt.txt', 'w', encoding='utf-8') as out:
    for x in items:
        num = x['num']
        pat = x['pattern']
        tgt = x['sentence_ja_target']
        alts = [p.replace('〜', '').strip() for p in re.split(r'[/／・]', pat)]
        # Check if tgt does NOT start with any pattern alt
        starts_with_alt = False
        for a in alts:
            clean_a = a.replace('（', '').replace('）', '').replace('(', '').replace(')', '')
            # first 2 chars of alt
            if tgt.startswith(clean_a[:2]):
                starts_with_alt = True
                break
        if not starts_with_alt:
            out.write(f"[{num:0>3}] PAT: {pat}\n")
            out.write(f"      TGT: {tgt}\n")
            out.write(f"      JA : {x['sentence_ja']}\n")
            out.write(f"      BLK: {x['sentence_ja_blank']}\n\n")

print("Done writing scratch/pat_vs_tgt.txt")
