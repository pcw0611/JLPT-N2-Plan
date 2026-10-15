# -*- coding: utf-8 -*-
"""
Add '態度' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0048",
    "kanji": "態度",
    "kana": "たいど",
    "meaning": "태도, 자세, 몸가짐 (품사: 명사, N2 초빈출 필수 어휘)",
    "sentences": (
        '<div class="example-ja"><ruby>彼<rt>かれ</rt></ruby>の'
        '<span class="target-word"><ruby>態度<rt>たいど</rt></ruby></span>は'
        '<ruby>不誠実<rt>ふせいじつ</rt></ruby>だと、'
        '<ruby>周囲<rt>しゅうい</rt></ruby>から'
        '<ruby>批判<rt>ひはん</rt></ruby>を<ruby>浴<rt>あ</rt></ruby>びた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 態度をとる(태도를 취하다), 態度を改める(태도를 고치다), 曖昧な態度(애매한 태도), 強気な態度(강경한 태도), 真面目な態度(성실한 태도), 態度に出る(태도로 드러나다) / 관련어: 姿勢(しせい, 자세), 振る舞い(ふるまい, 행동거지)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">그의 태도는 불성실하다고, 주변으로부터 비판을 받았다(비판을 뒤집어썼다).</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">態 (모양/태도 태) + 度 (법도 도)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    능력(能)과 상황을 대하는 마음(心)의 모습(態)과, 행동의 척도와 기준(度) ➔ 態度(たいど: 태도, 몸가짐)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【態度 (たいど)】 태도 / 몸가짐</span>\n'
        '  <span class="mnemonic-parts">★음독: 態(たい, 状態・事態) + 度(ど, 程度・制度) ➔ たいど / 초빈출 연어: 曖昧な態度(애매한 태도), 態度を改める(태도를 고치다)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "명사", "인간_심리", "JLPT_N2"]
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
