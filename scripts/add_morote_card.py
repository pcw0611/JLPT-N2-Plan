# -*- coding: utf-8 -*-
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
    "id": "READING-NEWS-0008",
    "kanji": "諸手",
    "kana": "もろて",
    "meaning": "두 손, 양손 (★초빈출 관용구: 諸手を挙げて 두 손을 들고, 전적으로/무조건 찬성·환영)",
    "sentences": (
        '<div class="example-ja"><ruby>新<rt>しん</rt></ruby><ruby>提案<rt>ていあん</rt></ruby>に'
        '<span class="target-word"><ruby>諸手<rt>もろて</rt></ruby>を<ruby>挙<rt>あ</rt></ruby>げて</span>'
        '<ruby>賛成<rt>さんせい</rt></ruby>するわけにはいかない。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 관용구] 諸手を挙げて(もろてをあげて): 두 손 들어 찬성/환영하다. 음독 しょて(X) ➔ 훈독 もろて(O)!</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">새 제안에 두 손 들어(전적으로) 찬성할 수만은 없다. (기사/사설 비판 지문 단골 표현)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">諸(양쪽/모두 제, 훈: もろ) + 手(손 수, て)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    양손(諸手)을 번쩍 들어 무조건적인 찬성이나 환영을 표함. ★특수 훈독 もろて 주의!\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【諸】 모두 제 (훈독: もろ)</span>\n'
        '  <span class="mnemonic-parts">양쪽, 둘 다, 온갖 (예: 諸刃 もろは - 양날의 검)</span>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【手】 손 수 (훈독: て)</span>\n'
        '  <span class="mnemonic-parts">손 (諸手: 양손, 두 손)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "관용구", "JLPT_N2"]
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
print("Added note for [諸手]:", res.get('structuredContent') or res.get('content'))

call_mcp('sync')
print("Anki sync triggered!")
