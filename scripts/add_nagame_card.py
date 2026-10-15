# -*- coding: utf-8 -*-
"""
Add '眺め（眺める）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0045",
    "kanji": "眺め（眺める）",
    "kana": "ながめ（ながめる）",
    "meaning": "1. 전망, 경치 (명사: 眺め) / 2. 바라보다, 내다보다 (동사: 眺める) (N2 초빈출)",
    "sentences": (
        '<div class="example-ja"><ruby>部屋<rt>へや</rt></ruby>の<ruby>窓<rt>まど</rt></ruby>からの'
        '<span class="target-word"><ruby>眺<rt>なが</rt></ruby>め</span>が<ruby>素晴<rt>すば</rt></ruby>らしく、'
        'しばらく<ruby>海<rt>うみ</rt></ruby>を'
        '<span class="target-word"><ruby>眺<rt>なが</rt></ruby>めていた</span>。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 眺めがいい/素晴らしい(전망/경치가 좋다/훌륭하다), 窓からの眺め(창밖 전망), 景色を眺める(경치를 바라보다), ぼんやり眺める(멍하니 바라보다) / 유의어: 景色(けしき, 경치), 風景(ふうけい, 풍경), 見渡す(みわたす, 멀리 내다보다)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">방 창문으로 내다보는 전망(경치)이 훌륭해서, 한동안 바다를 바라보고 있었다.</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">眺 (바라볼 조)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    目(눈 목) + 兆(조짐/갈라질 조) ➔ 눈(目)을 크게 뜨고 멀리 멀리(兆) 펼쳐진 풍경을 바라보다 ➔ 바라볼 조(眺)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【眺め (ながめ)】 전망, 경치 / 【眺める (ながめる)】 바라보다</span>\n'
        '  <span class="mnemonic-parts">★연상 공식: 눈으로 멀리 내다보는 \'전망\'(명사 眺め) ➔ 바라보다(동사 眺める) / 음독: 眺望(ちょうぼう, 조망)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "명사", "동사", "JLPT_N2"]
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
