# -*- coding: utf-8 -*-
"""
Add '怠る' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0043",
    "kanji": "怠る",
    "kana": "おこたる",
    "meaning": "게을리하다, 소홀히 하다, 방심하다 (품사: 1그룹 5단 타동사/자동사, N2 초빈출)",
    "sentences": (
        '<div class="example-ja"><ruby>日頃<rt>ひごろ</rt></ruby>の'
        '<ruby>安全<rt>あんぜん</rt></ruby><ruby>確認<rt>かくにん</rt></ruby>を'
        '<span class="target-word"><ruby>怠<rt>おこた</rt></ruby>った</span>ため、'
        '<ruby>大<rt>おお</rt></ruby>きな<ruby>事故<rt>じこ</rt></ruby>につながってしまった。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 努力を怠る(노력을 게을리하다), 注意を怠る(주의를 소홀히 하다/방심하다), 準備・点検を怠る(준비/점검을 게을리하다), 警戒を怠らない(경계를 늦추지 않다) / ★[N2 초강력 구별 함정] 怠る(おこたる: 의무·주의·노력을 소홀히 하다/방심하다, 1그룹) vs 怠ける(なまける: 일·공부를 하기 싫어 땡땡이치다/빈둥거리다, 2그룹)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">평소의 안전 확인을 소홀히 했기(게을리했기) 때문에, 큰 사고로 이어지고 말았다.</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">怠 (게으를 태)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    마음(心)이 풀어져 받침대(台) 위에 널브러져 게으름을 피우다 ➔ 게으를 태(怠)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【怠る (おこたる)】 소홀히 하다 / 게을리하다 / 방심하다</span>\n'
        '  <span class="mnemonic-parts">★오쿠리가나 구별: 怠る(おこたる, 소홀히 하다) vs 怠ける(なまける, 빈둥거리다/땡땡이치다) / 음독: 怠慢(たいまん, 태만)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "동사", "동사_구별", "JLPT_N2"]
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
