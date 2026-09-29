import re
import json

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    print(f'Total songs: {len(data)}')
    total_lines = sum(len(p['lines']) for s in data for p in s['parts'])
    print(f'Total lines: {total_lines}')
    for i, s in enumerate(data[:3]):
        print(f'Song {i+1}: {s["title"]} ({len(s["parts"])} parts)')
        for p in s['parts']:
            print(f'  Part {p["id"]}: {len(p["lines"])} lines')
            for l in p['lines'][:2]:
                print(f'    ja: {l["ja"]}')
                print(f'    ro: {l["romaji"]}')
                print(f'    cr: {l.get("charRomaji")}')
else:
    print('Could not find SONGS array')
