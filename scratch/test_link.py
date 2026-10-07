# -*- coding: utf-8 -*-
"""Test card builder for both audio-only and paper cards."""
import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_25_listening_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

with open('scratch/translations_25.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

print(f"Loaded {len(cards)} cards and {len(translations)} translations.")

# Test building a sample of cards:
# 1) Card 1 (1회 Q76, 問題1 課題理解 - Paper)
# 2) Card 3 (1회 Q90, 問題3 概要理解 - Audio only)
# 3) Card 4 (1회 Q94, 問題4 即時応答 - Audio only)
# 4) Card 9 (2회 Q75, 問題1 課題理解 - Paper)
# 5) Card 15 (2회 Q85, 問題3 概要理解 - Audio only)
# 6) Card 18 (2회 Q89, 問題4 即時応答 - Audio only)

for idx in [0, 2, 3, 8, 14, 17]:
    c = cards[idx]
    trans_key = f"{c['exam']}_{c['qid']}"
    t_list = translations.get(trans_key, [])
    print(f"Card {idx+1}: {trans_key} has {len(t_list)} translation lines.")
