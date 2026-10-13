# -*- coding: utf-8 -*-
"""
Add '求め' (もとめ) to Anki deck: 'JLPT 한끝 Voca::14 독해・기사・모의고사 어휘'
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
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith('data: '):
            return json.loads(line[6:])['result']
    return None

new_card = {
    "id": "READING-NEWS-0022",
    "kanji": "求め",
    "kana": "もとめ",
    "meaning": "요구, 요청, 바람, 청구 (★동사 求める의 전성명사! 연어: 求めに応じる 요구에 응하다)",
    "sentences": (
        '<div class="example-ja"><ruby>市民<rt>しみん</rt></ruby>の'
        '<span class="target-word"><ruby>求<rt>もと</rt></ruby>め</span>に'
        '<ruby>応<rt>おう</rt></ruby>じて、<ruby>夜間<rt>やかん</rt></ruby>のバスの'
        '<ruby>運行<rt>うんこう</rt></ruby><ruby>本数<rt>ほんすう</rt></ruby>が<ruby>増<rt>ふ</rt></ruby>やされた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 관용구·연어] 求めに応じる(もとめに おうじる, 요구·요청에 응하다), 求めに応える(もとめに こたえる, 요구·기대에 부응하다), お求め(구입/구매, 例: お求めはこちら)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">시민들의 요구에 따라(응하여), 야간 버스 운행 편수가 늘어났다. (비즈니스/안내문: お求め＝구입)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">求(구할 구, 훈: もと・める)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    손이나 마음으로 무언가를 간절히 찾고 원함 ➔ 구함, 요구, 바람(もとめ)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【求め】 もとめ</span>\n'
        '  <span class="mnemonic-parts">동사 求める(구하다/바라다)의 명사형! ★『求めに応じる(요구에 응하다)』 독해 1순위 연어</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "비즈니스_안내문", "연어_표현", "JLPT_N2"]
}

fields = {
    "id": new_card["id"],
    "kanji": new_card["kanji"],
    "kana": new_card["kana"],
    "meaning": new_card["meaning"],
    "sentences": new_card["sentences"],
    "mp3": new_card["mp3"],
    "hanja_mnemonic": new_card["hanja_mnemonic"]
}

res = call_mcp('add_note', {
    'deck_name': DECK_NAME,
    'model_name': MODEL_NAME,
    'fields': fields,
    'tags': new_card["tags"],
    'allow_duplicate': True
})
print("Added note for [求め]:", res.get('structuredContent', {}).get('message') or res.get('content'))

call_mcp('sync')
print("Anki sync triggered successfully!")
