import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's test fetching one song: 迷星叫
url = 'https://namu.wiki/w/%E8%BF%B7%E6%98%9F%E5%8F%AB'
req = urllib.request.Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        print(f"Fetched {len(html)} bytes")
        # Check if lyrics table is in the html
        if '交差点' in html:
            print("Found 交差点 in HTML!")
        else:
            print("Lyrics text not found in raw HTML")
except Exception as e:
    print(f"Error: {e}")
