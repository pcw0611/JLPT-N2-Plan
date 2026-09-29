import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'"id":\s*"([^"]+)",\s*"title":\s*"([^"]+)"', content)
print(f"Total songs: {len(matches)}")
for m in matches:
    print(f"- {m[0]}: {m[1]}")
