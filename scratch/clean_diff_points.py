# -*- coding: utf-8 -*-
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect all ~[Japanese][Korean] patterns in public file
p = Path('jlpt-calendar-site/public/exams/n2-grammar-speedrun.html')
text = p.read_text(encoding='utf-8')

idx1 = text.find('const ALL_PATTERNS = [')
idx2 = text.find('];\n\nclass SoundEngine', idx1)
data = json.loads(text[idx1 + len('const ALL_PATTERNS = '):idx2 + 1])

# Replace diff_point patterns where Japanese grammar has attached Korean particle:
# e.g., "〜末に도" -> "〜末に 도"
# "〜きる는" -> "〜きる 는"
# "〜ばかりだ와" -> "〜ばかりだ 와"

replacements_count = 0
for item in data:
    dp = item.get('diff_point', '')
    if not dp: continue
    
    # Match 〜[Japanese][Korean]
    def repl(m):
        ja = m.group(1)
        ko = m.group(2)
        return f"{ja} {ko}"
    
    # Japanese chars followed immediately by Korean chars
    # Japanese: \u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFFー
    # Korean: \uac00-\ud7a3
    new_dp = re.sub(r'([〜~][\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFFー]+)([\uac00-\ud7a3])', repl, dp)
    if new_dp != dp:
        print(f"[{item['num']}] Old: {dp}")
        print(f"      New: {new_dp}")
        item['diff_point'] = new_dp
        replacements_count += 1

print(f"\nTotal diff_points cleaned: {replacements_count}")
