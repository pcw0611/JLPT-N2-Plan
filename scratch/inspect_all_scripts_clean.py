# -*- coding: utf-8 -*-
"""Inspect the exact script text in each of the 25 cards."""
import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_25_listening_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

for i, c in enumerate(cards):
    pos = c['back'].find('대본')
    end_pos = c['back'].find('<!-- User Mistake', pos)
    if end_pos == -1:
        end_pos = c['back'].find('<!-- Connection', pos)
    if end_pos == -1:
        end_pos = pos + 1500
    snippet = c['back'][pos:end_pos]
    clean = re.sub(r'<[^>]+>', ' ', snippet)
    clean = ' '.join(clean.split())
    exam = c['exam']
    qid = c['qid']
    print(f"CARD {i+1:2d} ({exam} Q{qid:03d}): len={len(clean)} chars")
    print(f"   {clean[:140]}...")
    print()
