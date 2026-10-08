import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('"id": "haruhikage"')
idx_next = text.find('"id": "utakotoba"')
snippet = text[idx:idx_next]
print("haruhikage snippet length:", len(snippet))
part_matches = re.findall(r'"name":\s*"([^"]+)"', snippet)
print("Part names:", part_matches)
ja_matches = re.findall(r'"ja":\s*"([^"]+)"', snippet)
print(f"Total ja lines in haruhikage: {len(ja_matches)}")
for l in ja_matches:
    print(" ", l)
