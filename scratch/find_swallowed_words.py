# -*- coding: utf-8 -*-
import json, sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r"c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan")
DATASET_PATH = ROOT / "scripts" / "n2_grammar_dataset.json"

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Total items: {len(items)}")

for x in items:
    num = x['num']
    pat = x['pattern'] # e.g. 〜おきに
    tgt = x['sentence_ja_target'] # e.g. 二十分おきに
    blank = x['sentence_ja_blank']
    full_ja = x['sentence_ja']
    
    # Normalize pattern to find core keywords
    # remove 〜, split / or ,
    pat_alts = [p.replace('〜', '').strip() for p in re.split(r'[/／]', pat)]
    
    # Check if tgt contains words that precede the grammar pattern
    # For example, if pat is おきに, but tgt is 二十分おきに
    # If any alt is in tgt, check what is before that alt in tgt!
    matched_alt = None
    for alt in pat_alts:
        # e.g. alt could be "からいうと", "おきに", "あげく", etc.
        # Note some alts have 〜 inside like "〜ば〜ほど", "〜も〜ば〜も"
        clean_alt = alt.replace('〜', '')
        if clean_alt and clean_alt in tgt:
            matched_alt = clean_alt
            break
            
    prefix_swallowed = ""
    suffix_swallowed = ""
    if matched_alt:
        idx = tgt.find(matched_alt)
        prefix_swallowed = tgt[:idx]
        suffix_swallowed = tgt[idx + len(matched_alt):]
        
    print(f"[{num}] Pat: {pat:15s} | Tgt: {tgt:22s} | Match: {str(matched_alt):12s} | Pre: '{prefix_swallowed}' | Post: '{suffix_swallowed}'")
