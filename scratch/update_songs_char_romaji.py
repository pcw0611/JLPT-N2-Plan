import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Match preamble before SONGS
m_pre = re.search(r'^(.*?export const SONGS:\s*Song\[\]\s*=\s*)', text, re.DOTALL)
if not m_pre:
    print("Could not find SONGS preamble")
    sys.exit(1)

preamble = m_pre.group(1)

m_json = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
if not m_json:
    print("Could not extract SONGS array")
    sys.exit(1)

songs = json.loads(m_json.group(1))
print(f"Loaded {len(songs)} songs from songs.ts")

from test_all_989_lines import align_line_to_romaji

total_lines = 0
updated_lines = 0

for s in songs:
    for p in s['parts']:
        for line in p['lines']:
            total_lines += 1
            ja = line['ja']
            ro = line['romaji']
            cr = align_line_to_romaji(ja, ro)
            assert len(cr) == len(ja), f"Length mismatch: {ja} vs {cr}"
            assert "".join(cr) == ro, f"Content mismatch: {ro} vs {''.join(cr)}"
            line['charRomaji'] = cr
            updated_lines += 1

print(f"Verified and updated all {updated_lines}/{total_lines} lines!")

# Write updated file
new_songs_ts = preamble + json.dumps(songs, ensure_ascii=False, indent=2) + ";\n"

with open('jlpt-calendar-site/app/typing/songs.ts', 'w', encoding='utf-8') as f:
    f.write(new_songs_ts)

print("Successfully written updated songs.ts!")
