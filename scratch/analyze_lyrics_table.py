import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/haruhikage_raw.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

# Let's see how lines are structured
# A typical pattern:
# Japanese line (contains kanji/hiragana/katakana)
# Korean reading (pure hangul with optional spaces and dashes/dots)
# Korean translation (hangul with punctuation/meaning)
# Let's inspect raw text tokens
tokens = [t.strip() for t in raw.split('　') if t.strip()]
print(f"Tokens split by fullwidth space: {len(tokens)}")

# Or let's inspect the actual HTML table cells!
with open('scratch/namu_haruhikage.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the lyrics table in HTML
idx = html.find('3. 가사')
idx_table = html.find('<table', idx)
idx_table_end = html.find('</table>', idx_table)
table_html = html[idx_table:idx_table_end+8]

from bs4 import BeautifulSoup
soup = BeautifulSoup(table_html, 'html.parser')
rows = soup.find_all('tr')
print(f"Total tr rows in lyrics table: {len(rows)}")

for i, tr in enumerate(rows[:10]):
    tds = tr.find_all(['td', 'th'])
    td_texts = [td.get_text().strip() for td in tds]
    print(f"Row {i}: {td_texts}")
