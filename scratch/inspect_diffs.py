# -*- coding: utf-8 -*-
"""Inspect the 7 items with count differences to perfectly align them."""
import sys, json

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/normalized_dialogues.json', 'r', encoding='utf-8') as f:
    norms = json.load(f)

with open('scratch/translations_25.json', 'r', encoding='utf-8') as f:
    trans = json.load(f)

for k in ['1회_102', '1회_106', '2회_76', '2회_77', '2회_78', '2회_82', '2회_101']:
    print(f"==================== {k} ====================")
    n_items = norms[k]
    t_items = trans[k]
    print(f"Norm items ({len(n_items)}):")
    for idx, ni in enumerate(n_items):
        print(f"  [{idx}] ({ni['speaker']}) {ni['japanese'][:60]}")
    print(f"\nTrans items ({len(t_items)}):")
    for idx, ti in enumerate(t_items):
        txt = ti[1] if isinstance(ti, (list, tuple)) else ti
        print(f"  [{idx}] {txt[:60]}")
    print()
