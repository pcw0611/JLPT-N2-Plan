# -*- coding: utf-8 -*-
"""
Add '真似る' (まねる) to Anki deck: 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0023",
    "kanji": "真似る",
    "kana": "まねる",
    "meaning": "흉내 내다, 모방하다, 본뜨다 (품사: 2그룹 타동사 / 명사형: 真似 흉내, 짓거리)",
    "sentences": (
        '<div class="example-ja"><ruby>子<rt>こ</rt></ruby>どもは<ruby>親<rt>おや</rt></ruby>の'
        '<ruby>言動<rt>げんどう</rt></ruby>を'
        '<span class="target-word"><ruby>真似<rt>まね</rt></ruby>る</span>ことで、'
        '<ruby>多<rt>おお</rt></ruby>くの<ruby>事<rt>こと</rt></ruby>を<ruby>学<rt>まな</rt></ruby>んでいく。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [관련 어휘·관용구] 真似(まね, 흉내/짓거리), 人の真似をする(남의 흉내를 내다), 馬鹿な真似はよせ(바보 같은 짓은 그만둬), 見習う(みならう, 본받다)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">아이는 부모의 언행을 흉내 내며 많은 것을 배워 간다. (명사: 真似 흉내, 짓)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">真(참 진) + 似(닮을 사, 훈: にる)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    진짜(真)처럼 똑같이 닮게(似) 하다 ➔ 흉내 내다, 모방하다(まねる)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【真似る】 まねる</span>\n'
        '  <span class="mnemonic-parts">★진짜처럼 닮게 흉내 냄! 명사: 真似(まね, 흉내 / バカな真似 바보 같은 짓)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "기초_필수동사", "JLPT_N2"]
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
print("Added note for [真似る]:", res.get('structuredContent', {}).get('message') or res.get('content'))

call_mcp('sync')
print("Anki sync triggered successfully!")
