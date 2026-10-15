# -*- coding: utf-8 -*-
"""
Add '両親（りょうしん）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0052",
    "kanji": "両親",
    "kana": "りょうしん",
    "meaning": "부모, 양친 (명사: 아버지와 어머니 두 분 모두)",
    "sentences": (
        '<div class="example-ja"><ruby>進学<rt>しんがく</rt></ruby>について'
        '<span class="target-word"><ruby>両親<rt>りょうしん</rt></ruby>に</span>'
        '<ruby>相談<rt>そうだん</rt></ruby>し、'
        '<ruby>理解<rt>りかい</rt></ruby>を<ruby>得<rt>え</rt></ruby>ることができた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 両親に相談する(부모님께 상의하다), 両親の期待に応える(부모님의 기대에 부응하다), 両親健在(부모님 두 분 다 생존해 계심) / 관련어: 親(おや, 부모), 父親(ちちおや), 母親(ははおや), 祖父母(そふぼ, 조부모)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">진학에 대해 부모님(양친)께 상의하여, 이해를 얻을 수 있었다.</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">両 (두 량) + 親 (친할 친)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    둘(両) 다 나에게 가장 가깝고 친한(親) 분들 ➔ 부모, 양친(両親)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【両親 (りょうしん)】 부모, 양친</span>\n'
        '  <span class="mnemonic-parts">★음독: 両(りょう: 両方・両替) + 親(しん: 親切・親戚・親友) ➔ りょうしん / 훈독: 親(おや: 親・親指・父親・母親)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "명사", "인간관계_가족", "JLPT_N2"]
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
