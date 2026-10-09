import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/n2_grammar_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total items: {len(data)}\n")

suspects = []

for idx, item in enumerate(data):
    qid = item.get('id')
    num = item.get('num')
    pat = item.get('pattern', '')
    target = item.get('sentence_ja_target', '')
    blank = item.get('sentence_ja_blank', '')
    ja = item.get('sentence_ja', '')
    ko = item.get('sentence_ko', '')
    target_ko = item.get('target_ko', '')
    
    parts = blank.split('（　　）')
    if len(parts) == 2:
        prefix, suffix = parts
        actual_blanked = ja[len(prefix):len(ja)-len(suffix)] if (ja.startswith(prefix) and ja.endswith(suffix)) else target
    else:
        actual_blanked = target

    # Strip symbols from pattern
    clean_pat = re.sub(r'[〜~・/／\(\)（）\s]', '', pat)
    
    # Check if actual_blanked starts with something that is clearly not part of the pattern
    # For example, kanji at the start of actual_blanked when pattern is hiragana!
    has_leading_kanji = bool(re.match(r'^[一-龥]+', actual_blanked)) and not bool(re.match(r'^[一-龥]+', clean_pat))
    
    # Or actual_blanked has kanji when pattern is e.g. 〜おきに, 〜にすぎない, 〜一方だ
    # Let's check length difference
    # If actual_blanked contains words outside pattern
    suspects.append({
        'idx': idx + 1,
        'id': qid,
        'pattern': pat,
        'clean_pat': clean_pat,
        'actual_blanked': actual_blanked,
        'ja': ja,
        'blank': blank,
        'ko': ko,
        'target_ko': target_ko,
        'leading_kanji': has_leading_kanji
    })

print(f"=== Items where blanked starts with Kanji but pattern does not ===")
kanji_swallowed = [s for s in suspects if s['leading_kanji']]
for s in kanji_swallowed:
    print(f"#{s['idx']:03d} [{s['id']}] Pat: {s['pattern']} | Blanked: '{s['actual_blanked']}'")
    print(f"     JA:    {s['ja']}")
    print(f"     Blank: {s['blank']}")
    print(f"     KO:    {s['ko']}")
    print()

print(f"\nTotal leading kanji swallowed: {len(kanji_swallowed)}")
