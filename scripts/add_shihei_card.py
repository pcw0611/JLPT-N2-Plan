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
    "id": "READING-NEWS-0010",
    "kanji": "紙幣",
    "kana": "しへい",
    "meaning": "지폐, 종이돈 (품사: 명사)",
    "sentences": (
        '<div class="example-ja"><ruby>偽造<rt>ぎぞう</rt></ruby><ruby>防止<rt>ぼうし</rt></ruby>の'
        '<ruby>最新<rt>さいしん</rt></ruby><ruby>技術<rt>ぎじゅつ</rt></ruby>を<ruby>導入<rt>どうにゅう</rt></ruby>した'
        '<ruby>新<rt>しん</rt></ruby><span class="target-word"><ruby>紙幣<rt>しへい</rt></ruby></span>が'
        '<ruby>発行<rt>はっこう</rt></ruby>された。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [관련어] 硬貨(こうか, 동전/주화), お札(おさつ, 지폐의 회화체), 偽造紙幣(ぎぞうしへい, 위조지폐)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">위조 방지 최신 기술을 도입한 신지폐가 발행되었다. (일본 경제/사회 기사 최빈출 소재)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">紙(종이 지) + 幣(화폐/비단 폐)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    종이(紙)로 만들어 통용되는 화폐(幣) ➔ 지폐(紙幣)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【紙】 종이 지 (음: し)</span>\n'
        '  <span class="mnemonic-parts">실(糸)을 곱게 펴서 얇게 만든 종이</span>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【幣】 화폐 폐 (음: へい)</span>\n'
        '  <span class="mnemonic-parts">비단(巾)처럼 귀한 가치를 지닌 예물과 화폐</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "경제_사회", "JLPT_N2"]
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
print("Added note for [紙幣]:", res.get('structuredContent') or res.get('content'))
