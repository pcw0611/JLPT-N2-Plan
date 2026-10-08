import sys
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/namu_haruhikage.html', 'r', encoding='utf-8') as f:
    text = f.read()

snippet = text[227000:250000]
soup = BeautifulSoup(snippet, 'html.parser')
lines = [l.strip() for l in soup.get_text().splitlines() if l.strip()]
print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines[:50]):
    print(f"{i+1:2d}: {l}")

with open('scratch/haruhikage_raw.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(lines))
