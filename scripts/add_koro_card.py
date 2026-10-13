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
    "id": "READING-NEWS-0017",
    "kanji": "頃",
    "kana": "ころ／ごろ",
    "meaning": "때, 시기, 시절; ~무렵, ~경 (품사: 명사 / 접미사, N2 빈출)",
    "sentences": (
        '<div class="example-ja"><ruby>京都<rt>きょうと</rt></ruby>の<ruby>紅葉<rt>もみじ</rt></ruby>は、'
        '<ruby>来週<rt>らいしゅう</rt></ruby><span class="target-word"><ruby>見頃<rt>みごろ</rt></ruby></span>を'
        '<ruby>迎<rt>むか</rt></ruby>える<ruby>見込<rt>みこ</rt></ruby>みです。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 복합어] 見頃(みごろ, 보기 딱 좋을 때/절정기), 食べ頃(たべごろ, 제철/먹기 좋은 때), 日頃(ひごろ, 평소), 近頃(ちかごろ, 요즈음), 3時ごろ(3시경)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">교토의 단풍은 다음 주에 절정(보기 가장 좋은 때)을 맞이할 전망입니다. (어린 시절: 子どもの頃)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">頃(이랑/잠깐 경, 훈: ころ/ごろ)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    머리를 잠깐 기울이는 순간이나 알맞은 시기 ➔ 때, 시절, ~무렵\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【頃】 ころ／ごろ</span>\n'
        '  <span class="mnemonic-parts">단독: 때/시절(ころ), 접미사: ~무렵/경(ごろ, 3時ごろ)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "시간_표현", "복합어", "JLPT_N2"]
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
print("Added note for [頃]:", res.get('structuredContent', {}).get('message') or res.get('content'))

call_mcp('sync')
print("Anki sync triggered!")
