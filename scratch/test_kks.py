import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
import pykakasi

kks = pykakasi.kakasi()

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
if not m:
    print('Failed to find SONGS')
    sys.exit(1)

songs = json.loads(m.group(1))
print(f'Loaded {len(songs)} songs')

# Let's inspect line 1 and 2 of song 1
for line in songs[0]['parts'][0]['lines'][:5]:
    print('JA:    ', line['ja'])
    print('RO:    ', line['romaji'])
    print('OLD CR:', line.get('charRomaji'))
    # Kakasi breakdown
    conv = kks.convert(line['ja'])
    print('KKS:   ', [(c['orig'], c['hepburn']) for c in conv])
    print('-'*50)
