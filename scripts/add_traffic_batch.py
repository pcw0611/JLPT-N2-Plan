# -*- coding: utf-8 -*-
"""
Add '巻き込む（巻き込まれる）' and '事故渋滞' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
        "id": "READING-NEWS-0049",
        "kanji": "巻き込む（巻き込まれる）",
        "kana": "まきこむ（まきこまれる）",
        "meaning": "1. 휩쓸어 넣다, 말아 넣다, 끌어들이다 (원형: 巻き込む) / 2. (사건·사고 등에) 휘말리다, 말려들다 (★수동형: 巻き込まれる)",
        "sentences": (
            '<div class="example-ja"><ruby>高速<rt>こうそく</rt></ruby><ruby>道路<rt>どうろ</rt></ruby>で'
            '<ruby>事故<rt>じこ</rt></ruby><ruby>渋滞<rt>じゅうたい</rt></ruby>に'
            '<span class="target-word"><ruby>巻<rt>ま</rt></ruby>き<ruby>込<rt>こ</rt></ruby>まれて</span>、'
            '<ruby>約束<rt>やくそく</rt></ruby>の<ruby>時間<rt>じかん</rt></ruby>に'
            '<ruby>遅<rt>おく</rt></ruby>れてしまった。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 & 활용] 事故渋滞に巻き込まれる(사고 정체에 휘말리다/갇히다), トラブル・事件に巻き込まれる(트러블/사건에 휘말리다), 争いに巻き込む(분쟁에 끌어들이다) / 복합동사 어원: 巻く(まく, 말다) + 込む(こむ, 안으로 넣다)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">고속도로에서 사고 정체(교통 체증)에 휘말려서, 약속 시간에 늦고 말았다. (★동사 원형: 巻き込む / 시험 출제는 90% 이상 수동형 巻き込まれる!)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">巻 (말 권) + 込 (담을 입)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    회오리바람이나 종이를 둘둘 말듯(巻く), 안쪽 깊숙이 쏙 집어넣다(込む) ➔ 휩쓸어 넣다, 끌어들이다 / 수동형: 휩쓸려 들어가다, 휘말리다(巻き込まれる)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【巻き込む (まきこむ)】 동사 원형: 끌어들이다 / 수동: 휘말리다</span>\n'
            '  <span class="mnemonic-parts">★원형은 \'巻き込む(1그룹 5단 타동사)\'이며, 시험 지문에서는 \'〜に巻き込まれる(수동형: ~에 휘말리다)\'로 최다 출제!</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "복합동사", "수동태", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0050",
        "kanji": "事故渋滞（渋滞）",
        "kana": "じこじゅうたい（じゅうたい）",
        "meaning": "사고 정체, 사고로 인한 교통 체증 (핵심 어휘: 渋滞 じゅうたい: 정체, 밀림)",
        "sentences": (
            '<div class="example-ja"><ruby>トンネル<rt></rt></ruby><ruby>内<rt>ない</rt></ruby>の'
            '<span class="target-word"><ruby>事故<rt>じこ</rt></ruby><ruby>渋滞<rt>じゅうたい</rt></ruby></span>のため、'
            '<ruby>車<rt>くるま</rt></ruby>が<ruby>一<rt>いっ</rt></ruby><ruby>歩<rt>ぽ</rt></ruby>も'
            '<ruby>動<rt>うご</rt></ruby>かない。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 事故渋滞にはまる/巻き込まれる(사고 정체에 갇히다/휘말리다), 渋滞が発生する(정체가 발생하다), 渋滞を避ける(정체를 피하다), 渋滞が緩和する(정체가 완화되다) / 핵심 어휘: 渋滞(じゅうたい, 정체/교통체증) / 유의어: 混雑(こんざつ, 혼잡)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">터널 안의 사고 정체(교통 체증) 때문에, 차가 한 걸음도 움직이지 않는다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">事故 (じこ) + 渋滞 (じゅうたい)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    事故(사고) + 물(氵)이 떫고 거칠어(渋) 흐르지 못하고 막혀 머무르다(滞) ➔ 사고로 차들이 막혀 꼼짝 못 하는 정체(事故渋滞)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【渋滞 (じゅうたい)】 교통 정체 / 체증</span>\n'
            '  <span class="mnemonic-parts">★음독 주의: 渋(じゅう, 渋滞) + 滞(たい, 滞在・停滞) ➔ じゅうたい / 훈독: 渋い(しぶい, 떫다/차분한 멋이 있다)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "교통_어휘", "명사", "JLPT_N2"]
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
