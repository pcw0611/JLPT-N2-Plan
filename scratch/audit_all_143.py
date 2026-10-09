# -*- coding: utf-8 -*-
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r"c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan")
DATASET_PATH = ROOT / "scripts" / "n2_grammar_dataset.json"

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Total items: {len(items)}")
print("-" * 120)
for x in items:
    num = x['num']
    pat = x['pattern']
    clean_pat = pat.replace('〜', '').split('／')[0].strip()
    tgt = x['sentence_ja_target']
    blank = x['sentence_ja_blank']
    full_ja = x['sentence_ja']
    full_ko = x['sentence_ko']
    tgt_ko = x['target_ko']
    
    # flag items where tgt has extra chars beyond the grammatical pattern
    print(f"[{num}] PATTERN: {pat} | MEANING: {x['meaning']}")
    print(f"      JA FULL : {full_ja}")
    print(f"      JA TGT  : {tgt}")
    print(f"      JA BLANK: {blank}")
    print(f"      KO FULL : {full_ko}")
    print(f"      KO TGT  : {tgt_ko}")
    print("-" * 120)
