import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

seen = set()
for l in lines[2840:2980]:
    txt = re.sub(r'<[^>]+>', '', l).strip()
    if txt and not txt.startswith(('00:', 'WEBVTT')) and txt not in seen:
        seen.add(txt)
        print(txt)
