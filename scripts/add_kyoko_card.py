# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT 한끝 Voca::14 독해・기사・모의고사 어휘"
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
    "id": "READING-NEWS-0015",
    "kanji": "強固",
    "kana": "きょうこ",
    "meaning": "견고함, 굳건함, 강고함 (품사: な형용사 / 명사, N1급 사설 어휘)",
    "sentences": (
        '<div class="example-ja"><ruby>両国<rt>りょうこく</rt></ruby>は'
        '<ruby>長年<rt>ながねん</rt></ruby>にわたり、'
        '<span class="target-word"><ruby>強固<rt>きょうこ</rt></ruby></span>な'
        '<ruby>信頼<rt>しんらい</rt></ruby><ruby>関係<rt>かんけい</rt></ruby>を'
        '<ruby>築<rt>きず</rt></ruby>き<ruby>上<rt>あ</rt></ruby>げてきた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 콜로케이션] 強固な基盤(견고한 기반), 強固な意志(굳건한 의지), 強固な団結(굳건한 단결), 強固な協力体制(견고한 협력 체제)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">양국은 오랜 세월에 걸쳐 견고한 신뢰 관계를 쌓아 올렸다. (조직의 견고한 단결과 굳건한 의지)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">強(강할 강/きょう) + 固(굳을 고/こ)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    힘이 세고(強) 단단하게 굳어(固) 결코 흔들리지 않음 ➔ 견고함, 굳건함\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【強固】 きょうこ</span>\n'
        '  <span class="mnemonic-parts">조직·신뢰·의지·기반이 굳건함을 나타내는 N1 사설/기사 빈출어</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "N1급_어휘", "콜로케이션", "JLPT_N2"]
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
print("Added note for [強固]:", res.get('structuredContent', {}).get('message') or res.get('content'))

call_mcp('sync')
print("Anki sync triggered!")
