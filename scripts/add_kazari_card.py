# -*- coding: utf-8 -*-
"""
Add '飾り（飾る）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0054",
    "kanji": "飾り（飾る）",
    "kana": "かざり（かざる）",
    "meaning": "1. 장식, 장식물, 겉치레 (명사: 飾り) / 2. 장식하다, 꾸미다 (동사원형: 飾る)",
    "sentences": (
        '<div class="example-ja"><ruby>部屋<rt>へや</rt></ruby>を'
        '<ruby>季節<rt>きせつ</rt></ruby>の<ruby>花<rt>はな</rt></ruby>の'
        '<span class="target-word"><ruby>飾<rt>かざ</rt></ruby>り</span>で'
        '<ruby>彩<rt>いろど</rt></ruby>り、<ruby>気分<rt>きぶん</rt></ruby>を'
        '<ruby>明<rt>あか</rt></ruby>るくした。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어·관용구] <b>飾る(かざる, 꾸미다/장식하다)</b>: 部屋を花で飾る(꽃으로 방을 꾸미다), 言葉を飾る(말을 겉치레로 꾸미다), <b>有終の美を飾る(ゆうしゅうのびをかざる, 유종의 미를 거두다 ➔ N2/N1 관용구 초빈출!)</b> / <b>飾り(かざり, 장식)</b>: クリスマスツリーの飾り(트리 장식), 飾り気がない(꾸밈이 없다/소탈하다), ただの飾り(단지 겉치레 장식품일 뿐) / 음독: 装飾(そうしょく, 장식), 修飾(しゅうしょく, 수식)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">방을 계절 꽃 장식(飾り)으로 물들여, 기분을 밝게 만들었다. (★동사원형은 \'飾る かざる\'이며 관용구 \'有終の美を飾る: 유종의 미를 거두다\'도 시험 단골입니다!)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">飾 (꾸밀 식)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    음식(食)과 옷감·수건(巾)을 정성껏 보기 좋게 차려 놓은 모습 ➔ 꾸미다, 장식하다(飾る・飾り)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【飾り (かざり)】 장식 / 【飾る (かざる)】 장식하다</span>\n'
        '  <span class="mnemonic-parts">★훈독: かざり(飾り), かざる(飾る) vs 음독: しょく(装飾 そうしょく, 修飾 しゅうしょく)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "명사", "동사", "JLPT_N2"]
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
