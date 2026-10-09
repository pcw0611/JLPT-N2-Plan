# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for x in items:
    num = x['num']
    pat = x['pattern']
    tgt = x['sentence_ja_target']
    
    # Check if 'こと' in tgt but NOT in pat
    if 'こと' in tgt and 'こと' not in pat:
        print(f"[{num:0>3}] 'こと' in tgt but not pat: PAT '{pat}' | TGT '{tgt}' | JA '{x['sentence_ja']}'")
    
    # Check if 'の' in tgt but NOT in pat
    # (exclude normal particles like もの, のだ, わりに)
    if 'の' in tgt and 'の' not in pat and not any(k in pat for k in ['もの', 'のだ', 'ので', 'のに', 'わけ']):
        print(f"[{num:0>3}] 'の' in tgt but not pat: PAT '{pat}' | TGT '{tgt}' | JA '{x['sentence_ja']}'")
