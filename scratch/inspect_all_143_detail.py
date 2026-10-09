import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total items: {len(items)}\n")

for i, x in enumerate(items):
    num = x['num']
    qid = x['id']
    pat = x['pattern']
    ja = x['sentence_ja']
    t_ja = x.get('sentence_ja_target', '')
    blank = x.get('sentence_ja_blank', '')
    ko = x.get('sentence_ko', '')
    
    # Let's inspect what is currently blanked
    parts = blank.split('（　　）')
    blanked = ja[len(parts[0]):len(ja)-len(parts[1])] if len(parts) == 2 and ja.startswith(parts[0]) and ja.endswith(parts[1]) else t_ja
    
    print(f"#{num} [{qid}] Pattern: {pat}")
    print(f"   Sentence JA: {ja}")
    print(f"   Target:      {t_ja}")
    print(f"   Blank:       {blank}")
    print(f"   Blanked:     {blanked}")
    print(f"   Sentence KO: {ko}")
    print()
