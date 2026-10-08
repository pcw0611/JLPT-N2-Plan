import sys
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_extract_triplets(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    for tbl in soup.find_all('table'):
        text = tbl.get_text()
        # Find table with lyrics markers
        trs = tbl.find_all('tr')
        if len(trs) >= 2:
            lyrics_td = trs[-1].find_all(['td', 'th'])[-1]
            lines = [l.strip() for l in lyrics_td.get_text(separator='\n').splitlines() if l.strip()]
            if len(lines) >= 30:
                print(f"\n[{html_file}] Found {len(lines)} lines! Triplet count: {len(lines)//3}")
                for i in range(min(4, len(lines)//3)):
                    print(f"  {lines[i*3]}")
                    print(f"    ({lines[i*3+1]})")
                    print(f"    => {lines[i*3+2]}")
                break

test_extract_triplets("scratch/namu_hitoshizuku.html")
test_extract_triplets("scratch/namu_hekitenbansou.html")
test_extract_triplets("scratch/namu_utakotoba.html")
