# -*- coding: utf-8 -*-
"""
Add '秘密（ひみつ）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0057",
    "kanji": "秘密",
    "kana": "ひみつ",
    "meaning": "비밀 (명사 / な형용사: 남에게 알리지 않고 숨김, 기밀)",
    "sentences": (
        '<div class="example-ja"><ruby>信頼<rt>しんらい</rt></ruby>できる<ruby>親友<rt>しんゆう</rt></ruby>にだけ、'
        '<ruby>長年<rt>ながねん</rt></ruby><ruby>心<rt>こころ</rt></ruby>に<ruby>秘<rt>ひ</rt></ruby>めていた'
        '<span class="target-word"><ruby>秘密<rt>ひみつ</rt></ruby>を</span>'
        '<ruby>打<rt>う</rt></ruby>ち<ruby>明<rt>あ</rt></ruby>けた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어·동사 짝꿍 ★★★] <b>秘密を守る(비밀을 지키다)</b>, <b>秘密を漏らす(ひみつをもらす, 비밀을 누설하다)</b> ↔ <b>秘密が漏れる(비밀이 새다)</b>, <b>秘密を打ち明ける(털어놓다/고백하다)</b>, 秘密裏に(ひみつりに, 비밀리에), 秘密厳守(비밀 엄수) / [청해·회화 유의어] <b>内緒(ないしょ, 비밀/귀띔)</b> ➔ 内緒にする(비밀로 하다) / [공식 기밀] 機密(きみつ) / 동사: 秘める(ひめる, 마음에 간직하다/품다)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">신뢰할 수 있는 절친에게만 오랜 세월 마음에 품고 있던 비밀(秘密)을 털어놓았다(打ち明けた). (★시험 단골 짝꿍 동사: 秘密を漏らす/누설하다, 秘密を打ち明ける/털어놓다, 秘密を守る/지키다)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">秘 (숨길 비) + 密 (빽빽할 밀)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    벼(禾) 이삭 뒤에 반드시(必) 꼭꼭 숨겨(秘), 틈새 없이 빽빽하게(密) 감추어 둔 것 ➔ 비밀(秘密)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【秘密 (ひみつ)】 비밀</span>\n'
        '  <span class="mnemonic-parts">★음독: 秘(ひ: 秘密・秘訣・秘書) + 密(みつ: 秘密・精密・親密) ➔ ひみつ / 훈독: 秘める(ひめる, 간직하다/숨기다), 密か(ひそか, 남몰래/은밀히)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "명사", "청해_어휘", "JLPT_N2"]
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
