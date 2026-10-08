import sys
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/namu_mayoiuta.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

text = soup.get_text()
idx = text.find('交差点の真ん中')
if idx != -1:
    print('FOUND LYRICS! Length of snippet:')
    snippet = text[idx:idx+4000]
    with open('scratch/mayoiuta_raw_lyrics.txt', 'w', encoding='utf-8') as out:
        out.write(snippet)
    print("Saved to scratch/mayoiuta_raw_lyrics.txt")
else:
    print('Not found')
