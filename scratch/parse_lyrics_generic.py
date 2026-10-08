import sys
import re
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def inspect_lyrics_in_html(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Look for table containing lyrics
    # Usually has columns for Japanese, Korean pronunciation, Korean translation
    tables = soup.find_all('table')
    print(f"\n=== Inspecting {html_path} (tables: {len(tables)}) ===")
    
    # Try finding tables with lyrics
    for idx, table in enumerate(tables):
        text = table.get_text()
        # Japanese hiragana/kanji keywords or typical line
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if len(lines) > 20 and any(kw in text for kw in ('가사', 'MyGO', 'ver', '作詞')):
            print(f"Table #{idx} matched! Total text lines: {len(lines)}")
            # Show first 15 lines
            for l in lines[:15]:
                print(f"  {l}")
            break
    else:
        # If no table matched, search text directly
        text = soup.get_text()
        print("Fallback fulltext length:", len(text))

inspect_lyrics_in_html("scratch/namu_haruhikage.html")
inspect_lyrics_in_html("scratch/namu_hitoshizuku.html")
inspect_lyrics_in_html("scratch/namu_hekitenbansou.html")
inspect_lyrics_in_html("scratch/namu_utakotoba.html")
