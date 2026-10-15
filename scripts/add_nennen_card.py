# -*- coding: utf-8 -*-
"""
Add '年々（ねんねん）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0079",
    "kanji": "年々",
    "kana": "ねんねん",
    "meaning": "해마다, 해를 거듭할수록 (부사: 해가 갈수록 정도나 수량이 점점 변화함을 나타냄 / 통계·독해 지문 1순위 부사)",
    "sentences": (
        '<div class="example-ja"><ruby>少子<rt>しょうし</rt></ruby><ruby>高齢<rt>こうれい</rt></ruby><ruby>化<rt>か</rt></ruby>が'
        '<ruby>進<rt>すす</rt></ruby>むにつれて、'
        '<ruby>労働<rt>ろうどう</rt></ruby><ruby>力<rt>りょく</rt></ruby><ruby>不足<rt>ぶそく</rt></ruby>が'
        '<span class="target-word"><ruby>年々<rt>ねんねん</rt></ruby></span>'
        '<ruby>深刻<rt>しんこく</rt></ruby><ruby>化<rt>か</rt></ruby>している。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★ 통계·독해 지문 1순위] <b>年々深刻化している(해마다 심각해지고 있다)</b>, <b>年々増加する / 減少する(해마다 증가/감소하다)</b>, 年々厳しさを増す(해마다 가혹함이 더해지다), 年々悪化する(해마다 악화되다) / [첩어(반복어) 부사 비교] <b>年々(ねんねん, 해마다 / 연도별 변화 추이)</b> vs <b>日々(ひび, 나날이/매일매일)</b> vs <b>月々(つきづき, 다달이/매월)</b> vs 徐々に(じょじょに, 서서히) vs 段々(だんだん, 점점)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">저출산 고령화가 진행됨에 따라, 노동력 부족이 해마다(年々) 심각해지고 있다. (★통계·도표·사회 독해 1순위 부사: \'年々増加する/증가하다\', \'年々減少する/감소하다\', \'年々深刻化する/심각해지다\')</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">年 (해 년) + 々 (반복 기호)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    한 해(年)가 가고 또 다음 해(々)가 오며 해를 거듭할수록 계속해서 변화함 ➔ 해마다(年々)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【年々 (ねんねん)】 해마다, 해를 거듭할수록</span>\n'
        '  <span class="mnemonic-parts">★음독 반복: ねん + ねん ➔ ねんねん (훈독 반복: としどし) / 짝꿍 동사: 増加する, 減少する, 深刻化する</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "통계_도표", "부사", "JLPT_N2"]
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
