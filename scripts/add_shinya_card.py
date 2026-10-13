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
    "id": "READING-NEWS-0016",
    "kanji": "深夜",
    "kana": "しんや",
    "meaning": "심야, 한밤중, 늦은 밤 (품사: 명사, N2 빈출)",
    "sentences": (
        '<div class="example-ja"><ruby>作業<rt>さぎょう</rt></ruby>は'
        '<span class="target-word"><ruby>深夜<rt>しんや</rt></ruby></span>にまで'
        '<ruby>及<rt>およ</rt></ruby>び、'
        'スタッフ<ruby>全員<rt>ぜんいん</rt></ruby>が<ruby>疲労<rt>ひろう</rt></ruby><ruby>困憊<rt>こんぱい</rt></ruby>していた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [빈출 복합어/표현] 深夜勤務(심야 근무), 深夜営業(심야 영업), 深夜に及ぶ(심야에 이르다/지속되다). 회화체: 真夜中(まよなか)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">작업은 심야(한밤중)에까지 이르렀고, 스태프 전원이 피로에 지쳐 있었다. (심야에 큰 소리로 떠들지 마십시오)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">深(깊을 심/しん) + 夜(밤 야/や)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    밤(夜)이 깊어짐(深) ➔ 심야, 한밤중\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【深夜】 しんや</span>\n'
        '  <span class="mnemonic-parts">깊은 밤(보통 23시~04시경). 신문/뉴스 공적 표현 (회화체: 真夜中)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "청해_어휘", "시간_표현", "JLPT_N2"]
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
print("Added note for [深夜]:", res.get('structuredContent', {}).get('message') or res.get('content'))

call_mcp('sync')
print("Anki sync triggered!")
