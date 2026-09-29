import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
songs = json.loads(m.group(1))

targets = [
    '交差点の真ん中急ぐ人に紛れて',
    '人の顔色を窺いながら流されるままに衣食住',
    '不器用で空回って傷つくことから逃げている',
    '言葉になんてしたところで戸惑う人の目が怖かった',
    '十分君はもう頑張ってる',
    '心臓の音響かせて',
    '僕と君なのに叫びたい想いが重なる',
    '幾重にも重なる想いの層を突き破り',
    '意地悪な人の空に',
    'ねえママ僕好きな人が出来たんだ',
    '大切な人を笑顔にするため',
    '前衛的シルエットダンス',
    'ビニール越しの空からこぼれ落ちる音響いて'
]

for s in songs:
    for p in s['parts']:
        for l in p['lines']:
            for t in targets:
                if t in l['ja']:
                    print(f"[{s['id']}] JA: {l['ja']}")
                    print(f"     RO: {l['romaji']}")
                    print(f"     CR: {l.get('charRomaji')}")
                    print("-" * 50)
