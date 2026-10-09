import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total items: {len(items)}\n")

fixes = []

for x in items:
    num = x['num']
    qid = x['id']
    pat = x['pattern']
    ja = x['sentence_ja']
    t_ja = x.get('sentence_ja_target', '')
    blank = x.get('sentence_ja_blank', '')
    ko = x.get('sentence_ko', '')
    target_ko = x.get('target_ko', '')
    
    # Extract core pattern variants (remove 〜, ~, /)
    # e.g. "〜おきに" -> "おきに"
    # e.g. "〜かねない" -> "かねない"
    # e.g. "〜くせに" -> "くせに"
    # e.g. "〜にすぎない" -> "にすぎない"
    # e.g. "〜て以来" -> "て以来", "以来"
    # e.g. "〜たび（に）" -> "たびに", "たび"
    # e.g. "〜たとたん（に）" -> "とたんに", "たとたんに", "とたん"
    
    # We want to identify the EXACT substring in ja that corresponds to the grammar pattern itself,
    # NOT including the preceding noun, quantity, verb stem, adjective stem.
    
    print(f"[{num}] {pat} | Target: '{t_ja}'")
    print(f"     Sentence: {ja}")
    print(f"     Blank:    {blank}")
    print("-" * 50)
