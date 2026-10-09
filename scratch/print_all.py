# -*- coding: utf-8 -*-
import json, sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(r"c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan")
DATASET_PATH = ROOT / "scripts" / "n2_grammar_dataset.json"

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    items = json.load(f)

for x in items:
    num = x['num']
    pat = x['pattern']
    tgt = x['sentence_ja_target']
    blank = x['sentence_ja_blank']
    full_ja = x['sentence_ja']
    
    # print all items so we can examine every single one
    print(f"[{num:0>3}] PAT: {pat}")
    print(f"      JA : {full_ja}")
    print(f"      TGT: {tgt}")
    print(f"      BLK: {blank}")
    print(f"      KO : {x['sentence_ko']}")
    print(f"      TKO: {x['target_ko']}")
    print("-" * 80)
