import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
songs = json.loads(m.group(1))

# Check for suspicious readings
SUSPICIOUS = {
    '人': (['nin', 'jin'], 'hito', ['人間', '八方美人', '何人', '恋人', '旅人', '他人', '大人']),
    '君': (['kun'], 'kimi', []),
    '声': (['sei'], 'koe', ['名無声', '歓声', '無声']),
    '空': (['kuu'], 'sora', ['空間', '青空']),
    '夜': (['ya'], 'yoru', ['今夜', '夜空', '深夜', '熱帯夜', '白夜']),
    '心': (['shin'], 'kokoro', ['核心', '関心', '感心', '信心', '決心']),
    '手': (['shu'], 'te', ['握手', '拍手', '歌手', '手話']),
    '目': (['moku'], 'me', ['盲目', '目的', '注目']),
    '音': (['on'], 'oto', ['音一会', '本音', '雑音', '発音']),
    '雨': (['u'], 'ame', ['雨天', '梅雨', '降雨']),
    '星': (['sei'], 'hoshi', ['迷星叫', '惑星', '衛星']),
    '月': (['getsu'], 'tsuki', ['年月', '一ヶ月', '満月']),
    '道': (['dou'], 'michi', ['歩道', '軌道', '道路']),
    '今': (['kon'], 'ima', ['今夜', '今回', '今日']),
    '何': (['ka'], 'nani', ['幾何']),
}

findings = []

for s in songs:
    for p in s['parts']:
        for l in p['lines']:
            ja = l['ja']
            cr = l.get('charRomaji', [])
            ro = l['romaji']
            for k, (bad_readings, good_reading, exceptions) in SUSPICIOUS.items():
                if k in ja:
                    # check if in exceptions
                    is_exc = any(exc in ja for exc in exceptions)
                    if is_exc:
                        continue
                    for i, ch in enumerate(ja):
                        if ch == k and i < len(cr):
                            r = cr[i]
                            if r in bad_readings:
                                findings.append((s['id'], ja, k, r, good_reading, ro))

print(f"Total suspicious findings: {len(findings)}")
for f in findings:
    print(f"[{f[0]}] {f[1]} -> '{f[2]}' read as '{f[3]}' (expected '{f[4]}') | ro: {f[5]}")
