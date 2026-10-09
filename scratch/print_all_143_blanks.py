import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total items: {len(items)}\n")

for x in items:
    num = x['num']
    pat = x['pattern']
    ja = x['sentence_ja']
    blank = x['sentence_ja_blank']
    t_ja = x.get('sentence_ja_target', '')
    
    parts = blank.split('（　　）')
    if len(parts) == 2:
        prefix, suffix = parts
        blanked = ja[len(prefix):len(ja)-len(suffix)]
    else:
        blanked = "ERROR"
        
    print(f"#{num} [{pat}]")
    print(f"   JA:      {ja}")
    print(f"   Blank:   {blank}")
    print(f"   Blanked: '{blanked}' (Target: '{t_ja}')")
    print()
