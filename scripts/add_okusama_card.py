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
    "id": "READING-NEWS-0014",
    "kanji": "奥様",
    "kana": "おくさま",
    "meaning": "사모님, 부인, 댁의 아내분 (상대방의 아내를 높여 부르는 존경 표현, 품사: 명사)",
    "sentences": (
        '<div class="example-ja"><span class="target-word"><ruby>奥様<rt>おくさま</rt></ruby></span>にも'
        'よろしくお<ruby>伝<rt>つた</rt></ruby>えください。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [존경 vs 겸양 구별 필수!] 상대방 아내: 奥様(おくさま)・奥さん(おくさん) ／ 자신의 아내: 妻(つま)・家内(かない). 자신의 아내에게 奥様 사용 절대 금지!</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">사모님(부인)께도 안부 전해 주십시오. (부장님, 사모님 몸조리 잘하시길 바랍니다: 部長、奥様どうぞお大事に)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">奥(깊을 옥/안채) + 様(님 양)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    저택의 깊숙한 안채(奥)에 계시는 안주인을 극진히 높이던 전통 ➔ 사모님\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【奥様】 おくさま</span>\n'
        '  <span class="mnemonic-parts">상대방의 아내를 높여 부르는 대표 존경어. (친근한 표현: 奥さん)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "경어_존경", "가족_호칭", "JLPT_N2"]
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
print("Added note for [奥様]:", res.get('structuredContent', {}).get('message') or res.get('content'))

call_mcp('sync')
print("Anki sync triggered!")
