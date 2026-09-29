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

# Check every word in every line against pykakasi
discrepancies = []

for s in songs:
    for p in s['parts']:
        for l in p['lines']:
            ja = l['ja']
            ro = l['romaji']
            cr = l.get('charRomaji', [])

            # Check individual tokens
            tokens = kks.convert(ja)
            for t in tokens:
                orig = t['orig']
                hira = jaconv.kata2hira(t['hira'])
                hep = t['hepburn'].lower()
                
                # If orig is 人 and not part of compound
                if orig == '人' and ro:
                    # find where 人 is in ja
                    idx = ja.find('人')
                    if idx != -1 and idx < len(cr):
                        if cr[idx] in ['nin', 'jin']:
                            discrepancies.append((s['id'], ja, orig, cr[idx], 'hito', ro))

                # Check 君
                if orig == '君' and ro:
                    idx = ja.find('君')
                    if idx != -1 and idx < len(cr):
                        if cr[idx] == 'kun':
                            discrepancies.append((s['id'], ja, orig, cr[idx], 'kimi', ro))

                # Check 重なる
                if '重な' in ja and 'omonar' in ro:
                    discrepancies.append((s['id'], ja, '重なる', 'omonaru', 'kasanaru', ro))

                # Check 響く
                if '響' in ja and ('kyou' in ro or 'onkyou' in ro):
                    discrepancies.append((s['id'], ja, '響', 'kyou', 'hibi', ro))

                # Check 窺
                if '窺' in ja and 'kii' in ro:
                    discrepancies.append((s['id'], ja, '窺', 'kii', 'ukagai', ro))

                # Check 空回
                if '空回' in ja and 'kuukai' in ro:
                    discrepancies.append((s['id'], ja, '空回', 'kuukai', 'karamawa', ro))

                # Check 前衛
                if '前衛' in ja and 'zenmamoru' in ro:
                    discrepancies.append((s['id'], ja, '前衛', 'zenmamoru', 'zen\'ei', ro))

print(f"Total discrepancies: {len(discrepancies)}")
for d in discrepancies:
    print(f"[{d[0]}] {d[1]} | {d[2]}: {d[3]} -> {d[4]}")
