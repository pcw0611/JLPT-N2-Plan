# -*- coding: utf-8 -*-
"""
Add '地道' and '及びません' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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

cards_to_add = [
    {
        "id": "READING-NEWS-0036",
        "kanji": "地道",
        "kana": "じみち",
        "meaning": "착실함, 건실함, 꾸준함, 요행을 바라지 않음 (품사: な형용사, 명사, N2 독해 초빈출)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>地道<rt>じみち</rt></ruby>な</span>'
            '<ruby>努力<rt>どりょく</rt></ruby>を<ruby>重<rt>かさ</rt></ruby>ねることが、'
            '<ruby>成功<rt>せいこう</rt></ruby>への<ruby>一番<rt>いちばん</rt></ruby>の'
            '<ruby>近道<rt>ちかみち</rt></ruby>だ。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 地道な努力(착실한/꾸준한 노력), 地道に働く(우직하게/착실하게 일하다), 地道な活動(꾸준한 활동) / 유의어: 着実(ちゃくじつ, 착실), こつこつ(꾸준히, 끊임없이) ↔ 派手(はで, 화려함/눈에 띔)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">착실한(꾸준한) 노력을 거듭하는 것이, 성공으로 가는 가장 빠른 지름길이다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">地 (땅 지) + 道 (길 도)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    땅(地)에 두 발을 굳건히 딛고 바른 길(道)을 한 걸음씩 묵묵히 걸어가다 ➔ 착실함, 건실함, 꾸준함\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【地道 (じみち)】 착실함 / 건실함 / 꾸준함</span>\n'
            '  <span class="mnemonic-parts">★독음 주의: 地(じ) + 道(みち)의 관용적 결합으로 \'じみち\'로 발음 (ちみち X) / 부사적 활용: 地道に (착실히, 묵묵히)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "형용동사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0037",
        "kanji": "及びません（及ぶ）",
        "kana": "およびません（およぶ）",
        "meaning": "1. (~할) 필요는 없습니다, ~하지 않으셔도 됩니다 (★문형: 〜には及びません) / 2. 미치지 못합니다 (도달 X)",
        "sentences": (
            '<div class="example-ja"><ruby>心配<rt>しんぱい</rt></ruby>なさるには'
            '<span class="target-word"><ruby>及<rt>およ</rt></ruby>びません</span>。'
            '<ruby>手術<rt>しゅじゅつ</rt></ruby>は<ruby>無事<rt>ぶじ</rt></ruby>に<ruby>成功<rt>せいこう</rt></ruby>しました。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 문형 & 연어] 〜には及びません / 〜に及ばない(~할 필요는 없다 = 〜する必要はない), 心配には及びません(걱정하실 필요 없습니다), わざわざ行くには及びません(굳이 갈 필요 없습니다) / [비교·도달] 足元にも及ばない(발끝에도 못 미치다), 被害が全国に及ぶ(피해가 전국에 미치다)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">걱정하실 필요는 없습니다. 수술은 무사히 성공했습니다. (★독해·청해 비즈니스 정중 경어 초빈출 표현: 〜には及びません = ~하실 필요 없습니다)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">及 (미칠 급)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    앞사람의 옷자락을 손을 뻗어 뒤에서 따라잡는 모습 ➔ 어떤 수준·범위에 닿다, 미치다\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【及ぶ (およぶ)】 미치다, 달하다 / 【〜に及ばない】 ~할 필요는 없다</span>\n'
            '  <span class="mnemonic-parts">★핵심 문형: 손을 뻗어 애쓸(及ぶ) 지경까지는 아니다 ➔ \'~할 필요는 없다\' (=〜する必要はない) / 공손형: 〜には及びません (~하실 필요는 없습니다)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "문법연계", "JLPT_N2"]
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
    msg = res.get('structuredContent', {}).get('message') or res.get('content')
    print(f"Added note for [{card['kanji']}]: {msg}")

call_mcp('sync')
print("Anki sync completed successfully!")
