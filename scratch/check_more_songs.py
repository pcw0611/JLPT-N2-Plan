import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
songs = json.loads(m.group(1))

for s in songs:
    if s['id'] in ['haruhikage', 'maigo', 'swim', 'aoiharu']:
        print(f"=== {s['title']} ({s['id']}) ===")
        for p in s['parts']:
            print(f" Part: {p['name']}")
            for l in p['lines'][:4]:
                print(f"  JA: {l['ja']}")
                print(f"  RO: {l['romaji']}")
                print(f"  CR: {l.get('charRomaji')}")
