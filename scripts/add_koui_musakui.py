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

cards_to_add = [
    {
        "id": "READING-NEWS-0018",
        "kanji": "行為",
        "kana": "こうい",
        "meaning": "행위, 짓, 행동 (의식적·법적·도덕적 의도를 띤 행동, 품사: 명사)",
        "sentences": (
            '<div class="example-ja"><ruby>他者<rt>たしゃ</rt></ruby>に<ruby>迷惑<rt>めいわく</rt></ruby>をかける'
            '<span class="target-word"><ruby>行為<rt>こうい</rt></ruby></span>は'
            '<ruby>厳<rt>きび</rt></ruby>しく<ruby>慎<rt>つつし</rt></ruby>まなければならない。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [빈출 복합어] 迷惑行為(민폐 행위), 不正行為(부정행위), 違法行為(위법 행위), 行為に及ぶ(행위에 이르다/저지르다)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">타인에게 폐를 끼치는 행위는 엄격히 삼가야 한다. (부정행위, 악질적인 행위)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">行(행할 행/こう) + 為(할 위/い)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    의도나 목적을 가지고 실제로 행하는(行) 일(為) ➔ 행위\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【行為】 こうい</span>\n'
            '  <span class="mnemonic-parts">단순 움직임(行動)을 넘어 법적·도덕적 책임이 따르는 \'행위\'</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "법률_사회", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0019",
        "kanji": "無作為",
        "kana": "むさくい",
        "meaning": "무작위, 랜덤; 작위적이지 않음 (품사: 명사 / な형용사, N1급)",
        "sentences": (
            '<div class="example-ja"><ruby>世論<rt>せろん</rt></ruby><ruby>調査<rt>ちょうさ</rt></ruby>では、'
            '<ruby>全国<rt>ぜんこく</rt></ruby>から<span class="target-word"><ruby>無作為<rt>むさくい</rt></ruby></span>に'
            '<ruby>選<rt>えら</rt></ruby>ばれた<ruby>千人<rt>せんにん</rt></ruby>を<ruby>対象<rt>たいしょう</rt></ruby>に'
            '<ruby>意見<rt>いけん</rt></ruby>を<ruby>聞<rt>き</rt></ruby>いた。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [독해/통계 초빈출] 無作為抽出(무작위 추출/랜덤 샘플링), 無作為に選ぶ(무작위로 뽑다). 반대어: 作為的(さくいてき, 작위적임)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">여론조사에서는 전국에서 무작위(랜덤)로 선택된 1,000명을 대상으로 의견을 물었다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">無(없을 무) + 作為(지을 작 + 할 위 / さくい)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    인위적인 손길이나 의도(作為)가 개입되지 않음 ➔ 무작위(無作為), 랜덤\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【作為】 さくい</span>\n'
            '  <span class="mnemonic-parts">일부러 꾸며 만듦 (作為的: 작위적)</span>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【無作為】 むさくい</span>\n'
            '  <span class="mnemonic-parts">의도적인 조작 없음 ➔ 무작위 추출(無作為抽出)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "통계_논설", "N1급_어휘", "JLPT_N2"]
    }
]

for card in cards_to_add:
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
    print(f"Added note for [{card['kanji']}]:", res.get('structuredContent', {}).get('message') or res.get('content'))

call_mcp('sync')
print("Anki sync triggered!")
