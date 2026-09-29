import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
songs = json.loads(m.group(1))

# Check for 'nin' when ja has '人' (except e.g. '何人' or compounds)
hito_issues = []
for s in songs:
    for p in s['parts']:
        for l in p['lines']:
            ja = l['ja']
            cr = l.get('charRomaji', [])
            for i, ch in enumerate(ja):
                if ch == '人' and i < len(cr):
                    r = cr[i]
                    if r in ['nin', 'jin']:
                        # Check context
                        prev_ch = ja[i-1] if i > 0 else ''
                        next_ch = ja[i+1] if i + 1 < len(ja) else ''
                        hito_issues.append((s['id'], ja, f"prev={prev_ch}, next={next_ch}, r={r}", l['romaji']))

print(f"Found {len(hito_issues)} cases of 人 read as nin/jin:")
for item in hito_issues:
    print(f"[{item[0]}] {item[1]} -> {item[2]}")
