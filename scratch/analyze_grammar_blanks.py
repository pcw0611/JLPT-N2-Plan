import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total items in n2_grammar_dataset.json: {len(data)}")

mismatches = []
for item in data:
    pat = item.get('pattern', '').replace('〜', '').replace('~', '').strip()
    target = item.get('sentence_ja_target', '').strip()
    blank = item.get('sentence_ja_blank', '').strip()
    ja = item.get('sentence_ja', '').strip()
    
    # Check if target contains more than just the pattern
    # e.g. target is "二十分おきに" while pattern is "〜おきに" (pat is "おきに")
    if pat not in target:
        mismatches.append((item, "pattern_not_in_target"))
    elif len(target) > len(pat):
        mismatches.append((item, "target_has_extra_words"))

print(f"Items where target has extra words or mismatch: {len(mismatches)}")
print("\n=== Listing all cases where target has extra words ===")
for item, reason in mismatches:
    pat = item.get('pattern')
    target = item.get('sentence_ja_target')
    ja = item.get('sentence_ja')
    blank = item.get('sentence_ja_blank')
    print(f"[{item.get('id')}] Pattern: {pat} | Target: {target}")
    print(f"   JA:    {ja}")
    print(f"   Blank: {blank}")
    print(f"   KO:    {item.get('sentence_ko')}")
    print()
