import sys
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/namu_haruhikage.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all('table')
for tbl in tables:
    if '悴んだ心' in tbl.get_text():
        trs = tbl.find_all('tr')
        lyrics_td = trs[-1].find_all(['td', 'th'])[-1]
        text_lines = [l.strip() for l in lyrics_td.get_text(separator='\n').splitlines() if l.strip()]
        print(f"Total lines extracted with separator='\\n': {len(text_lines)}")
        for i, l in enumerate(text_lines[:25]):
            print(f"{i+1:2d}: {l}")
        break
