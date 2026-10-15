# -*- coding: utf-8 -*-
"""
Add '創設（そうせつ）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
"""
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"

def call_mcp(name, arguments={}):
    req = urllib.request.Request(
        'http://127.0.0.1:3141/',
        data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': name, 'arguments': arguments}}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith('data: '):
            return json.loads(line[6:])['result']
    return None

card = {
    "id": "READING-NEWS-0074",
    "kanji": "創設",
    "kana": "そうせつ",
    "meaning": "창설, 신설 (명사 / する동사: 제도·기금·상·기관 등을 새로 만들어 세움)",
    "sentences": (
        '<div class="example-ja"><ruby>若手<rt>わかて</rt></ruby><ruby>研究<rt>けんきゅう</rt></ruby>者を'
        '<ruby>支援<rt>しえん</rt></ruby>するため、'
        '<ruby>新<rt>あら</rt></ruby>たな<ruby>奨学金<rt>しょうがくきん</rt></ruby><ruby>制度<rt>せいど</rt></ruby>が'
        '<span class="target-word"><ruby>創設<rt>そうせつ</rt></ruby>された</span>。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★ 뉴스·독해 단골] <b>制度を創設する(제도를 창설/신설하다)</b>, <b>基金を創設する(기금을 창설하다)</b>, 賞を創設する(상을 제정하다), 組織を創設する(조직을 창설하다) / [유의어 비교] <b>創設(そうせつ, 제도·기금·상의 첫 창설)</b> vs <b>設立(せつりつ, 회사·학교 등 법인 설립)</b> vs 新設(しんせつ, 부서·학과 등의 신설) / [한자 設의 훈독 동사 ★★★] <b>設ける(もうける, 마련하다/설치하다)</b> ➔ 基準を設ける(기준을 마련하다)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">젊은 연구자들을 지원하기 위해, 새로운 장학금 제도가 창설되었다(創設された). (★신문기사·독해 1순위: 制度を創設する/제도를 신설·창설하다, 基金を創設する/기금을 창설하다 / 한자 設의 훈독 동사 \'設ける(もうける: 마련하다)\'도 시험 필수!)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n  <div class="visual-scan-header">\n    <span class="visual-scan-badge">創 (비롯할 창) + 設 (베풀 설)</span>\n  </div>\n  <div class="visual-scan-desc">\n    처음으로 칼(刂)을 대어 새로운 것을 만들어내고(創), 말씀(言)과 행동(殳)으로 틀을 베풀어 세움(設) ➔ 창설(創設)\n  </div>\n</div>\n<div class="mnemonic-item">\n  <span class="mnemonic-char">【創設 (そうせつ)】 창설</span>\n  <span class="mnemonic-parts">★음독: 創(そう: 創設・創造・創作) + 設(せつ: 創設・設立・設置) ➔ そうせつ / 훈독 동사: 設ける(もうける, 마련하다/설치하다)</span>\n</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "사회_제도", "명사", "JLPT_N2"]
}

fields = {
    "id": card["id"],
    "kanji": card["kanji"],
    "kana": card["kana"],
    "meaning": card["meaning"],
    "sentences": card["sentences"],
    "mp3": card["mp3"],
    "hanja_mnemonic": card["hanja_mnemonic"]
}

res = call_mcp('add_note', {
    'deck_name': DECK_NAME,
    'model_name': MODEL_NAME,
    'fields': fields,
    'tags': card["tags"],
    'allow_duplicate': True
})
msg = res.get('structuredContent', {}).get('message') or res.get('content')
print(f"Added note for [{card['kanji']}]: {msg}")

call_mcp('sync')
print("Anki sync completed successfully!")
