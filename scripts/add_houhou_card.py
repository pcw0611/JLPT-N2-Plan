# -*- coding: utf-8 -*-
"""
Add '方法（ほうほう）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0071",
    "kanji": "方法",
    "kana": "ほうほう",
    "meaning": "방법 (명사: 목적을 달성하기 위한 구체적 방식과 절차 / 유의어 비교: 方法 vs 手段)",
    "sentences": (
        '<div class="example-ja"><ruby>問題<rt>もんだい</rt></ruby>を'
        '<ruby>根本<rt>こんぽん</rt></ruby><ruby>的<rt>てき</rt></ruby>に<ruby>解決<rt>かいけつ</rt></ruby>するための'
        '<span class="target-word"><ruby>有効<rt>ゆうこう</rt></ruby>な<ruby>方法<rt>ほうほう</rt></ruby></span>を'
        '<ruby>模索<rt>もさく</rt></ruby>している。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★] <b>解決方法(해결 방법)</b>, <b>有効な方法(유효한 방법)</b>, 対処方法(대처 방법), <b>〜という方法をとる(~라는 방법을 취하다)</b>, 方法を見出す(방법을 찾아내다) / [유의어 뉘앙스 비교] <b>方法(ほうほう, 목적에 도달하는 구체적 절차·방식)</b> vs <b>手段(しゅだん, 목적을 위해 이용하는 도구·수단 ➔ 手段を選ばない: 수단을 가리지 않다)</b> / [한자 독음] 方(ほう) + 法(ほう: 方法・文法・法律) ➔ ほうほう</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">문제를 근본적으로 해결하기 위한 유효한 방법(有効な方法)을 모색하고 있다. (★시험 빈출: 有効な方法/유효한 방법, 〜という方法をとる/~라는 방법을 취하다 / 유의어 비교: 手段(수단) ➔ 手段を選ばない/수단을 가리지 않다)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n  <div class="visual-scan-header">\n    <span class="visual-scan-badge">方 (방향/방법 방) + 法 (법/도리 법)</span>\n  </div>\n  <div class="visual-scan-desc">\n    올바른 방향(方)을 향해 물(氵)이 자연스레 흘러가듯(去) 순리에 맞게 따르는 법칙(法) ➔ 방법(方法)\n  </div>\n</div>\n<div class="mnemonic-item">\n  <span class="mnemonic-char">【方法 (ほうほう)】 방법</span>\n  <span class="mnemonic-parts">★음독: 方(ほう) + 法(ほう: 方法・文法 ぶんぽう) ➔ ほうほう / 유의어: 手段(しゅだん: 手段を選ばない)</span>\n</div>'
    ),
    "tags": ["독해_어휘", "기초_어휘", "명사", "JLPT_N2"]
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
