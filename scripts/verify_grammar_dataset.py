# -*- coding: utf-8 -*-
import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for x in items:
    num = x['num']
    pattern = x['pattern']
    ja = x['sentence_ja']
    blank = x['sentence_ja_blank']
    t_ja = x['sentence_ja_target']
    ko = x['sentence_ko']
    t_ko = x['target_ko']
    
    # Flags
    issues = []
    if t_ko not in ko:
        issues.append("T_KO_NOT_IN_KO")
    if len(t_ja) > 10:
        issues.append(f"LONG_T_JA({t_ja})")
    if '、' in t_ja:
        issues.append(f"COMMA_IN_T_JA({t_ja})")
    if blank.startswith('（　　）'):
        issues.append("STARTS_BLANK")
    if blank.endswith('（　　）。') or blank.endswith('（　　）'):
        # Some predicates end with the blank, which is fine if it's predicate grammar like 〜わけにはいかない
        pass

    if issues:
        print(f"[{num}] {pattern}")
        print(f"  JA   : {ja}")
        print(f"  BLANK: {blank}")
        print(f"  T_JA : {t_ja}")
        print(f"  KO   : {ko}")
        print(f"  T_KO : {t_ko}")
        print(f"  FLAG : {issues}")
        print("-" * 60)
