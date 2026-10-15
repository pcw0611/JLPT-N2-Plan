# -*- coding: utf-8 -*-
"""
Add '巻き込む（巻き込まれる）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0049",
    "kanji": "巻き込む（巻き込まれる）",
    "kana": "まきこむ（まきこまれる）",
    "meaning": "1. 휩쓸어 넣다, 말아 넣다, 끌어들이다 (원형: 巻き込む) / 2. (사건·사고 등에) 휘말리다, 말려들다 (★수동형: 巻き込まれる)",
    "sentences": (
        '<div class="example-ja"><ruby>予期<rt>よき</rt></ruby>せぬトラブルに'
        '<span class="target-word"><ruby>巻<rt>ま</rt></ruby>き<ruby>込<rt>こ</rt></ruby>まれて</span>、'
        '<ruby>計画<rt>け이かく</rt></ruby>が'
        '<ruby>大幅<rt>おおはば</rt></ruby>に<ruby>狂<rt>くる</rt></ruby>ってしまった。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 & 활용] 事件・事故に巻き込まれる(사건·사고에 휘말리다), 争い・トラブルに巻き込む(분쟁·트러블에 끌어들이다), 機械に巻き込まれる(기계에 말려들어가다) / 어원 복합동사: 巻く(まく, 말다/감다) + 込む(こむ, 안으로 넣다/들어가다)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">예기치 못한 트러블(문제)에 휘말려서, 계획이 대폭 어긋나 버렸다. (★독해·청해 수동형 빈출: 〜に巻き込まれる)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">巻 (말 권) + 込 (담을 입)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    회오리바람이나 종이를 둘둘 말듯(巻く), 안쪽 깊숙이 쏙 집어넣다(込む) ➔ 휩쓸어 넣다, 말아 넣다, 끌어들이다\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【巻き込む (まきこむ)】 끌어들이다, 말아 넣다</span>\n'
        '  <span class="mnemonic-parts">★독해 90% 이상은 수동형으로 출제: \'〜に巻き込まれる\' ➔ \"~에 휘말리다, 말려들다\" (사건/사고/분쟁/트러블)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "복합동사", "수동태", "JLPT_N2"]
}

# Fix small ruby typo if any
card["sentences"] = card["sentences"].replace('<ruby>計画<rt>け이かく</rt></ruby>', '<ruby>計画<rt>けいかく</rt></ruby>')

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
