import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
songs = json.loads(m.group(1))

from test_all_989_lines import align_line_to_romaji

sample_indices = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

for idx in sample_indices:
    s = songs[idx]
    print(f"=== Song {idx+1}: {s['title']} ({s['id']}) ===")
    for p in s['parts']:
        print(f"  Part: {p['name']}")
        for line in p['lines'][:3]:
            ja = line['ja']
            ro = line['romaji']
            cr = align_line_to_romaji(ja, ro)
            print(f"    JA: {ja}")
            print(f"    RO: {ro}")
            print(f"    CR: {cr}")
            # Show zip of ja and cr
            pairs = [f"{ch}({c})" for ch, c in zip(ja, cr)]
            print(f"    PAIRS: {' '.join(pairs)}")
            print()
