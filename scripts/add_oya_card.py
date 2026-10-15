# -*- coding: utf-8 -*-
"""
Add '親（おや）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0062",
    "kanji": "親",
    "kana": "おや",
    "meaning": "부모, 어버이 (명사 / 비유: 모회사·주최자 / N2 초빈출 관용구: 親の脛をかじる)",
    "sentences": (
        '<div class="example-ja"><ruby>大学<rt>だいがく</rt></ruby><ruby>卒業<rt>そつぎょう</rt></ruby>を'
        '<ruby>機<rt>き</rt></ruby>に<span class="target-word"><ruby>親元<rt>おやもと</rt></ruby>を</span>'
        '<ruby>離<rt>はな</rt></ruby>れ、<ruby>自立<rt>じりつ</rt></ruby>した'
        '<ruby>生活<rt>せいかつ</rt></ruby>を<ruby>始<rt>はじ</rt></ruby>めた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 관용구 ★★★ N2 단골] <b>親の脛をかじる(おやのすねをかじる, 부모 등골을 빼먹다 / 성인이 되어서도 부모에게 얹혀살며 기생하다)</b> / [초빈출 복합어·연어] <b>親元を離れる(부모 곁을 떠나 자립하다)</b>, <b>親孝行(おやこうこう, 효도)</b> ↔ <b>親不孝(おやふこう, 불효)</b>, 親譲り(おやゆずり, 부모에게 물려받음), 親馬鹿(おやばか, 자식 바보), 親会社(おやがいしゃ, 모회사), 親指(おやゆび, 엄지) / [파생 훈독] 親しい(したしい, 친하다), 親しむ(したしむ, 친해지다) / [음독 しん] 両親(りょうしん), 親密(しんみつ), 親戚(しんせき)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">대학교 졸업을 계기로 부모 곁을 떠나(親元を離れ), 자립한 생활을 시작했다. (★N2 시험 초빈출 관용구: \'親の脛をかじる(부모 등골을 빼먹다, 부모에게 얹혀살다)\'는 필수 암기 표현입니다!)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">親 (친할 친 / 어버이 친)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    나무(木) 위에 올라서서(立) 멀리 나간 자식이 무사히 돌아오는지 늘 바라보고(見) 계시는 분 ➔ 어버이, 부모(親 おや)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【親 (おや)】 부모, 어버이</span>\n'
        '  <span class="mnemonic-parts">★훈독: おや(親・親元・親指), したしい(親しい), したしむ(親しむ) / 음독: しん(両親・親切・親友・親戚・親密)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "명사", "인간관계_가족", "관용구", "JLPT_N2"]
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
