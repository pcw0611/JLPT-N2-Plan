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
        "id": "READING-NEWS-0008",
        "kanji": "諸手",
        "kana": "もろて",
        "meaning": "두 손, 양손 (★초빈출 관용구: 諸手を挙げて 두 손을 들고, 전적으로/무조건 찬성·환영)",
        "sentences": (
            '<div class="example-ja"><ruby>新<rt>しん</rt></ruby><ruby>提案<rt>ていあん</rt></ruby>に'
            '<span class="target-word"><ruby>諸手<rt>もろて</rt></ruby>を<ruby>挙<rt>あ</rt></ruby>げて</span>'
            '<ruby>賛成<rt>さんせい</rt></ruby>するわけにはいかない。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 관용구] 諸手を挙げて(もろてをあげて): 두 손 들어 찬성/환영하다. 음독 しょて(X) ➔ 훈독 もろて(O)!</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">새 제안에 두 손 들어(전적으로) 찬성할 수만은 없다. (기사/사설 비판 지문 단골 표현)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">諸(양쪽/모두 제, 훈: もろ) + 手(손 수, て)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    양손(諸手)을 번쩍 들어 무조건적인 찬성이나 환영을 표함. ★특수 훈독 もろて 주의!\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【諸】 모두 제 (훈독: もろ)</span>\n'
            '  <span class="mnemonic-parts">양쪽, 둘 다, 온갖 (예: 諸刃 もろは - 양날의 검)</span>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【手】 손 수 (훈독: て)</span>\n'
            '  <span class="mnemonic-parts">손 (諸手: 양손, 두 손)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "관용구", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0009",
        "kanji": "連れ",
        "kana": "つれ",
        "meaning": "동행, 동반자, 일행; 함께 감 (품사: 명사)",
        "sentences": (
            '<div class="example-ja"><ruby>休日<rt>きゅうじつ</rt></ruby>の<ruby>公園<rt>こうえん</rt></ruby>は'
            '<span class="target-word"><ruby>家族<rt>かぞく</rt></ruby><ruby>連<rt>づ</rt></ruby>れ</span>や'
            '<ruby>子<rt>こ</rt></ruby><ruby>連<rt>づ</rt></ruby>れの<ruby>人<rt>ひと</rt></ruby>々で'
            '<ruby>賑<rt>にぎ</rt></ruby>わっている。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [접객/경어 빈출] お連れ様(おつれさま, 일행분), 連れ合い(つれあい, 배우자), 道連れ(길동무)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">휴일의 공원은 가족 동반이나 아이를 동반한 사람들로 붐비고 있다. (일행분이 다 오시는 대로 안내하겠습니다: お連れ様がお揃いになり次第)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">連(이을 련/연, 훈: つれる)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    수레(車)가 줄지어 가듯(辶) 함께 동행하여 가는 일행(連れ)이나 배우자\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【連】 이을 련 (훈독: つれる, つれ)</span>\n'
            '  <span class="mnemonic-parts">수레 차(車) + 쉬엄쉬엄 갈 착(辶): 줄지어 함께 감</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "모의고사_어휘", "JLPT_N2"]
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
    print(f"Added note for [{card['kanji']}]:", res.get('structuredContent') or res.get('content'))

print("Both cards added successfully!")
