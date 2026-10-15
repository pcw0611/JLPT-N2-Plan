# -*- coding: utf-8 -*-
"""
Add '基礎（きそ）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0056",
    "kanji": "基礎",
    "kana": "きそ",
    "meaning": "기초, 토대, 바탕 (명사: 학문·기술·사물 등의 밑바탕이 되는 근본)",
    "sentences": (
        '<div class="example-ja"><ruby>何事<rt>なにごと</rt></ruby>も'
        '<ruby>焦<rt>あせ</rt></ruby>らずに'
        '<span class="target-word"><ruby>基礎<rt>きそ</rt></ruby>を'
        '<ruby>固<rt>かた</rt></ruby>める</span>ことが、'
        '<ruby>将来<rt>しょうらい</rt></ruby>の<ruby>大<rt>おお</rt></ruby>きな'
        '<ruby>成長<rt>せいちょう</rt></ruby>につながる。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] <b>基礎を固める(기초를 다지다)</b>, <b>基礎を築く(きそをきずく, 기초/토대를 쌓다·구축하다)</b>, 基礎知識(기초 지식), 基礎体力(기초 체력), 基礎から学ぶ(기초부터 배우다) / [유의어 비교] 基礎(きそ, 학문·건물의 밑바탕·토대) vs 基本(きほん, 규칙·원리·기본 룰) vs 土台(どだい, 물리적 토대 / 애초에·원래) / 한자 礎의 훈독: いしずえ(주춧돌/토대)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">무슨 일이든 조급해하지 않고 기초를 다지는 것(基礎を固める)이 장래의 큰 성장으로 이어진다. (★시험 단골 연어: 基礎を固める/기초를 다지다, 基礎を築く/기초를 쌓다)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">基 (터 기) + 礎 (주춧돌 초)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    집을 지을 터(基) 위에 튼튼한 돌(石)로 받쳐놓은 주춧돌(礎) ➔ 만물의 바탕, 기초(基礎)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【基礎 (きそ)】 기초 / 토대</span>\n'
        '  <span class="mnemonic-parts">★음독: 基(き: 基礎・基本・基準) + 礎(そ: 基礎) ➔ きそ / 훈독: 基く(もとづく, 근거하다), 礎(いしずえ, 주춧돌·토대)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "명사", "학습_개념", "JLPT_N2"]
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
