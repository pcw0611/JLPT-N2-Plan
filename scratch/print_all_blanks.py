import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total items: {len(data)}\n")

issues = []
for idx, item in enumerate(data):
    qid = item.get('id')
    num = item.get('num')
    pat = item.get('pattern', '')
    target = item.get('sentence_ja_target', '')
    blank = item.get('sentence_ja_blank', '')
    ja = item.get('sentence_ja', '')
    ko = item.get('sentence_ko', '')
    target_ko = item.get('target_ko', '')
    
    # Check if target contains words outside pattern
    # Clean pattern: remove 〜, ~, ・, /, () etc.
    # We want to see what is blanked out in sentence_ja_blank compared to sentence_ja
    parts = blank.split('（　　）')
    if len(parts) == 2:
        prefix, suffix = parts
        # What was replaced by （　　）?
        # In ja, finding what's between prefix and suffix
        if ja.startswith(prefix) and ja.endswith(suffix):
            actual_blanked = ja[len(prefix):len(ja)-len(suffix)]
        else:
            actual_blanked = target
    else:
        actual_blanked = target

    issues.append({
        'idx': idx + 1,
        'id': qid,
        'num': num,
        'pattern': pat,
        'target': target,
        'actual_blanked': actual_blanked,
        'ja': ja,
        'blank': blank,
        'ko': ko,
        'target_ko': target_ko
    })

for it in issues:
    print(f"#{it['idx']:03d} [{it['id']}] Pattern: {it['pattern']}")
    print(f"     JA:     {it['ja']}")
    print(f"     Blank:  {it['blank']}")
    print(f"     Blanked:{it['actual_blanked']} | Target: {it['target']}")
    print(f"     KO:     {it['ko']} (Target: {it['target_ko']})")
    print("-" * 60)
