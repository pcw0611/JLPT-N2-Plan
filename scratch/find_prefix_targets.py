import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total items: {len(items)}\n")

candidates = []

for x in items:
    num = x['num']
    qid = x['id']
    pat = x['pattern']
    ja = x['sentence_ja']
    t_ja = x.get('sentence_ja_target', '')
    blank = x.get('sentence_ja_blank', '')
    ko = x.get('sentence_ko', '')
    target_ko = x.get('target_ko', '')
    
    # Clean pattern variants
    # Remove ~ / 〜
    raw_pat = pat.replace('〜', '').replace('~', '').strip()
    # Split by / or ／ or ・
    variants = re.split(r'[／/・]', raw_pat)
    variants = [v.strip() for v in variants if v.strip()]
    
    # For each variant, remove parentheses or optional parts: e.g. "たび（に）" -> "たびに", "たび"
    expanded_vars = []
    for v in variants:
        # e.g. "（は）", "(は)"
        expanded_vars.append(v)
        v_no_paren = re.sub(r'[\(（][^\)）]+[\)）]', '', v).strip()
        if v_no_paren and v_no_paren not in expanded_vars:
            expanded_vars.append(v_no_paren)
        v_full = v.replace('（', '').replace('）', '').replace('(', '').replace(')', '').strip()
        if v_full and v_full not in expanded_vars:
            expanded_vars.append(v_full)
            
    # Check if any variant is a substring of t_ja
    # And if t_ja is longer than the variant, what is the prefix?
    matching_var = None
    prefix_in_target = None
    for ev in sorted(expanded_vars, key=len, reverse=True):
        if ev in t_ja:
            idx = t_ja.find(ev)
            if idx > 0:
                matching_var = ev
                prefix_in_target = t_ja[:idx]
                break
            elif idx == 0 and len(t_ja) > len(ev):
                # Maybe suffix?
                pass
                
    if prefix_in_target:
        candidates.append({
            'num': num,
            'id': qid,
            'pattern': pat,
            'target': t_ja,
            'matching_var': matching_var,
            'prefix_in_target': prefix_in_target,
            'ja': ja,
            'blank': blank,
            'ko': ko
        })

print(f"Found {len(candidates)} items where target has a prefix that should stay in sentence:")
for c in candidates:
    print(f"[{c['num']}] {c['pattern']}")
    print(f"   JA:        {c['ja']}")
    print(f"   Target:    '{c['target']}' (Prefix: '{c['prefix_in_target']}', Core: '{c['matching_var']}')")
    print(f"   Cur Blank: {c['blank']}")
    # New proposed blank:
    # replace target with prefix + "（　　）"
    new_blank = c['ja'].replace(c['target'], c['prefix_in_target'] + "（　　）", 1)
    print(f"   New Blank: {new_blank}")
    print()
