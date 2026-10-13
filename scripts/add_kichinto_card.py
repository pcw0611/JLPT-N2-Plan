# -*- coding: utf-8 -*-
"""
Add 'きちんと' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0033",
    "kanji": "きちんと",
    "kana": "きちんと",
    "meaning": "제대로, 똑바로, 깔끔하게, 빈틈없이 (규칙·약속·정리가 반듯한 모양, 품사: 부사 / と·する)",
    "sentences": (
        '<div class="example-ja"><ruby>約束<rt>やくそく</rt></ruby>の<ruby>時間<rt>じかん</rt></ruby>を'
        '<span class="target-word">きちんと</span><ruby>守<rt>まも</rt></ruby>り、'
        '<ruby>部屋<rt>へや</rt></ruby>を<span class="target-word">きちんと</span><ruby>片付<rt>かたづ</rt></ruby>けるのが'
        '<ruby>社会人<rt>しゃかいじん</rt></ruby>の<ruby>基本<rt>きほん</rt></ruby>だ。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] きちんと説明する(제대로 설명하다), きちんと片付ける(깔끔히 치우다), きちんと食べる(꼬박꼬박 챙겨먹다) ↔ ちゃんと(회화체), しっかり(야무지게/꽉), きっちり(수치/시간이 딱)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">약속 시간을 제대로 지키고, 방을 깔끔하게 치우는 것이 사회인의 기본이다. (반듯하고 흐트러짐 없는 모양)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">きちんと (부사)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    각진 상자처럼 흐트러짐 없이 단정하고 반듯한 모양 ➔ 제대로, 단정히, 깔끔히\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【きちんと】 제대로 / 깔끔히</span>\n'
        '  <span class="mnemonic-parts">★규칙·정리정돈이 반듯함! 회화체: ちゃんと / 야무지게: しっかり / 오차 없이 딱: きっちり</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기초_필수부사", "태도_정리", "JLPT_N2"]
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
msg = res.get('structuredContent', {}).get('message') or res.get('content')
print(f"Added note for [{new_card['kanji']}]: {msg}")

call_mcp('sync')
print("Anki sync completed successfully!")
