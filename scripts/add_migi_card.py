# -*- coding: utf-8 -*-
"""
Add '右に出る（右に出る者はいない）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0044",
    "kanji": "右に出る（右に出る者はいない）",
    "kana": "みぎにでる（みぎにでるものはいない）",
    "meaning": "~보다 낫다, 능가하다 (★99% 부정형: 右に出る者はいない ~를 능가할 사람이 없다, 따라올 자가 없다)",
    "sentences": (
        '<div class="example-ja"><ruby>彼<rt>かれ</rt></ruby>の'
        '<ruby>料理<rt>りょうり</rt></ruby>の<ruby>腕<rt>うで</rt></ruby>に'
        '<span class="target-word"><ruby>右<rt>みぎ</rt></ruby>に<ruby>出<rt>で</rt></ruby>る<ruby>者<rt>もの</rt></ruby>はいない</span>。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 관용구 패턴] 〜の右に出る者はない／いない (~를 능가할 자는 없다, 그 분야에서 최고다) / 유의어: 〜に敵(かな)う者はいない(~를 당해낼 자는 없다), 足元にも及ばない(발끝에도 못 미친다) ↔ 左遷(させん: 낮은 자리로 좌천되다)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">그의 요리 솜씨를 능가할 자는 없다 (요리 실력에서 그 사람을 따라올 사람이 없다).</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">右に出る (오른쪽에 나오다 ➔ 능가하다)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    동양 고대 관습상 오른쪽(右) 자리가 왼쪽보다 더 높은 상석(上席)! ➔ 어떤 사람의 오른쪽(더 윗자리)에 나설 수 있는 사람이 없다 ➔ 그 사람을 능가할 자가 없다!\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【右に出る者はいない】 능가하는 자가 없다 (최고다)</span>\n'
        '  <span class="mnemonic-parts">★무조건 부정형과 호응: 거의 항상 \'〜の右に出る者はいない\' 형태로 출제되어 \"~에서는 그 사람을 따라올 자가 없다/독보적이다\"라는 뜻으로 쓰임</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "관용구", "JLPT_N2"]
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
