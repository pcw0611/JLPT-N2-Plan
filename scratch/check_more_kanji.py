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

# Check for other common song words
words_to_check = [
    ('今日', ['konnichi'], 'kyou'),
    ('明日', ['myounichi'], 'ashita'),
    ('昨日', ['sakujitsu'], 'kinou'),
    ('風', ['fuu'], 'kaze'),
    ('道', ['dou'], 'michi'),
    ('空', ['kuu'], 'sora'),
    ('海', ['kai'], 'umi'),
    ('雨', ['u'], 'ame'),
    ('光', ['kou'], 'hikari'),
    ('影', ['ei'], 'kage'),
    ('音', ['on'], 'oto'),
    ('声', ['sei'], 'koe'),
    ('涙', ['rui'], 'namida'),
    ('夢', ['mu'], 'yume'),
    ('朝', ['chou'], 'asa'),
    ('夜', ['ya'], 'yoru'),
    ('花', ['ka'], 'hana'),
    ('星', ['sei'], 'hoshi'),
    ('歌', ['ka'], 'uta'),
]

more_findings = []

for s in songs:
    for p in s['parts']:
        for l in p['lines']:
            ja = l['ja']
            ro = l['romaji']
            cr = l.get('charRomaji', [])
            for kanji, bad_list, good_val in words_to_check:
                if kanji in ja:
                    idx = ja.find(kanji)
                    if idx < len(cr):
                        val = cr[idx]
                        if any(b in val for b in bad_list):
                            # Ignore compounds like 今日中 or 音声
                            more_findings.append((s['id'], ja, kanji, val, good_val, ro))

print(f"More findings: {len(more_findings)}")
for f in more_findings:
    print(f"[{f[0]}] {f[1]} | {f[2]}={f[3]} (expected {f[4]}) | {f[5]}")
