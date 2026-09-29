import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
import pykakasi
import jaconv

kks = pykakasi.kakasi()

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
songs = json.loads(m.group(1))

# Let's inspect all lines where kakasi kunyomi/lyrics reading differs from line['romaji']
diffs = []

for s in songs:
    for p in s['parts']:
        for l in p['lines']:
            ja = l['ja']
            ro = l['romaji']
            cr = l.get('charRomaji', [])
            
            # Specific known words check
            # 1. 人に, 人の, 人を, 人が -> hito
            for pattern, correct in [
                (r'急ぐ人に', 'isoguhitoni'),
                (r'人の顔色', 'hitonokaoiro'),
                (r'窺いながら', 'ukagainagara'),
                (r'戸惑う人の', 'tomodauhitono'),
                (r'君はもう', 'kimihamou'),
                (r'音響かせて', 'otohibikasete'),
                (r'君なのに', 'kiminanoni'),
                (r'排気音が', 'haikionga'),
                (r'人の空に', 'hitonosorani'),
                (r'好きな人が', 'sukinahitoga'),
                (r'大切な人を', 'taisetsunahitowo'),
                (r'空からこぼれ落ちる音響いて', 'sorakarakoboreochiruotohibiite'),
                (r'空回って', 'karamawatte'),
                (r'前衛的', 'zen\'eiteki'),
            ]:
                if re.search(pattern, ja):
                    diffs.append((s['id'], ja, pattern, correct, ro))

print(f"Known phonetic mismatches found: {len(diffs)}")
for d in diffs:
    print(f"[{d[0]}] {d[1]} | Pattern: {d[2]} -> Should have: {d[3]} | Current: {d[4]}")
