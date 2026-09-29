import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
import pykakasi

kks = pykakasi.kakasi()

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
songs = json.loads(m.group(1))

max_token_len = 0
long_tokens = []
total_tokens = 0

for s in songs:
    for p in s['parts']:
        for line in p['lines']:
            ja = line['ja']
            conv = kks.convert(ja)
            for c in conv:
                total_tokens += 1
                orig = c['orig']
                if len(orig) > max_token_len:
                    max_token_len = len(orig)
                if len(orig) > 4:
                    long_tokens.append((orig, c['hepburn'], ja))

print(f'Total tokens: {total_tokens}')
print(f'Max token length: {max_token_len}')
print(f'Tokens with len > 4: {len(long_tokens)}')
for t in long_tokens[:10]:
    print('  ', t[0], '->', t[1], 'in', t[2])
