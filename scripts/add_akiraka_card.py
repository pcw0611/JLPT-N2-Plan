# -*- coding: utf-8 -*-
"""
Add '明らかになる (明らかになった)' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0032",
    "kanji": "明らかになる",
    "kana": "あきらかになる",
    "meaning": "밝혀지다, 드러나다, 규명되다 (★과거형: 明らかになった / 타동사: 明らかにする 밝히다)",
    "sentences": (
        '<div class="example-ja"><ruby>東<rt>ひがし</rt></ruby><ruby>鉄道<rt>てつどう</rt></ruby><ruby>竹山<rt>たけやま</rt></ruby><ruby>線<rt>せん</rt></ruby><ruby>内<rt>ない</rt></ruby>にある'
        '<ruby>二<rt>ふた</rt></ruby>つの<ruby>信号機<rt>しんごうき</rt></ruby>が<ruby>故障<rt>こしょう</rt></ruby>しており、'
        '<ruby>大事故<rt>だいじこ</rt></ruby>が<ruby>起<rt>お</rt></ruby>きかねない<ruby>危険<rt>きけん</rt></ruby>な<ruby>状態<rt>じょうたい</rt></ruby>が'
        '<ruby>続<rt>つづ</rt></ruby>いていたことが'
        '<span class="target-word"><ruby>明<rt>あき</rt></ruby>らかになった</span>。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 기사 패턴] 〜という事実が明らかになった(~라는 사실이 밝혀졌다), 原因が明らかになる(원인이 밝혀지다), 真相を明らかにする(진상을 밝히다/규명하다), 明らかな証拠(명백한 증거)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">동철도 다케야마선 내의 신호기 2대가 고장 나 있어, 대형 사고가 일어날 수도 있는 위험한 상태가 지속되고 있었던 것이 밝혀졌다. (자동: 〜が 明らかになる / 타동: 〜を 明らかにする)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">明(밝을 명, 훈: あきら・か) + になる</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    어둠 속에 가려져 있던 사실이 환하게 밝아짐 ➔ 밝혀지다, 드러나다(あきらかになる)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【明らかになる】 あきらかになる</span>\n'
        '  <span class="mnemonic-parts">★기사·뉴스 단골 결말: 〜ことが明らかになった(~한 사실이 밝혀졌다)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "모의고사_어휘", "관용구", "JLPT_N2"]
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
