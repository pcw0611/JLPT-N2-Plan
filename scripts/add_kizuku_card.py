# -*- coding: utf-8 -*-
"""
Add '築く（きずく）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0061",
    "kanji": "築く",
    "kana": "きずく",
    "meaning": "쌓다, 구축하다, 쌓아 올리다 (동사: 5단 타동사 / 성·건축물을 쌓다, 신뢰·관계·재산·지위·기초 등을 다지고 구축하다)",
    "sentences": (
        '<div class="example-ja"><ruby>互<rt>たが</rt></ruby>いに<ruby>本音<rt>ほんね</rt></ruby>で'
        '<ruby>語<rt>かた</rt></ruby>り<ruby>合<rt>あ</rt></ruby>うことで、'
        '<ruby>深<rt>ふか</rt></ruby>い<ruby>信頼<rt>しんらい</rt></ruby><ruby>関係<rt>かんけい</rt></ruby>を'
        '<span class="target-word"><ruby>築<rt>きず</rt></ruby>く</span>ことができた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★ N2 독해 지문 1순위] <b>信頼関係を築く(신뢰 관계를 구축하다/쌓다)</b>, <b>良好な関係を築く(양호한 관계를 쌓다)</b>, <b>財産・富を築く(재산/부를 쌓다)</b>, 地位を築く(지위를 다지다/구축하다), 基礎を築く(기초를 쌓다), 城を築く(성을 쌓다) / [한자 독음 구별] 훈독: きずく(築く) vs 음독: <b>ちく</b> (建築 けんちく, 新築 しんちく, 改築 かいちく, 築年数 ちくねんすう)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">서로 솔직한 속마음(本音)을 터놓고 이야기함으로써 깊은 신뢰 관계를 쌓을(築く) 수 있었다. (★시험 1순위 연어: 信頼関係を築く/신뢰관계를 쌓다, 財産を築く/재산을 쌓다, 地位を築く/지위를 구축하다)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">築 (쌓을 축)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    대나무(竹)와 흙을 다져 공이(筑)로 바닥을 치며 차곡차곡 쌓아 올리는 모습 ➔ 쌓다, 구축하다(築く)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【築く (きずく)】 쌓다, 구축하다</span>\n'
        '  <span class="mnemonic-parts">★훈독: きずく(築く) vs 음독: ちく(建築 けんちく, 新築 しんちく, 築年数 ちくねんすう)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "동사", "인간관계", "JLPT_N2"]
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
