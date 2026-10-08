import sys
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/namu_haruhikage.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find heading containing '가사'
lyrics_heading = None
for h in soup.find_all(['h2', 'h3', 'h4', 'div']):
    if '가사' in h.get_text() and any(tag in h.name for tag in ('h2', 'h3')):
        lyrics_heading = h
        print(f"Found heading: {h.name} -> {h.get_text().strip()}")
        break

# Look at parent or sibling tables
tables = soup.find_all('table')
for idx, tbl in enumerate(tables):
    txt = tbl.get_text()
    if '悴んだ心' in txt:
        print(f"FOUND LYRICS TABLE at index {idx}!")
        trs = tbl.find_all('tr')
        print(f"Total trs: {len(trs)}")
        for r_idx, tr in enumerate(trs):
            print(f"--- TR {r_idx} ---")
            for td in tr.find_all(['td', 'th']):
                # Print clean lines of this td
                lines = [l.strip() for l in td.get_text().splitlines() if l.strip()]
                print(f"  TD (len={len(lines)}): {lines[:6]}")
        break
