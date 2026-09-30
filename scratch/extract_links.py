import urllib.request
import re

url = 'https://nihongoph.com/jlpt-n2-12-2023/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
        for l in links:
            if any(k in l.lower() for k in ['drive', 'mega', 'mediafire', '.mp3', 'audio', 'download', 'choukai', 'listening', 'youtube']):
                print(l)
except Exception as e:
    print("Error:", e)
