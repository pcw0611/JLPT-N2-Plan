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
    },
    {
        "id": "READING-NEWS-0020",
        "kanji": "為になる",
        "kana": "ためになる",
        "meaning": "도움이 되다, 유익하다, 보탬이 되다 (품사: 관용구, N2 필수)",
        "sentences": (
            '<div class="example-ja"><ruby>先輩<rt>せんぱい</rt></ruby>の<ruby>助言<rt>じょげん</rt></ruby>は'
            '<span class="target-word"><ruby>為<rt>ため</rt></ruby>になる</span>ことばかりで、'
            '<ruby>大変<rt>たいへん</rt></ruby><ruby>勉強<rt>べんきょう</rt></ruby>になった。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 관용구] ためになる話(유익한 이야기/교훈이 되는 이야기), ためにならない(도움이 안 됨/백해무익함). 한자 표기: 為になる</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">선배의 조언은 유익하고 도움이 되는 것뿐이어서 대단히 공부가 되었다. (도움이 되는 이야기: ためになる話)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">為(위할 위, 훈: ため) + になる</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    나 자신이나 상대의 성장에 진정한 이익·보탬(為)이 됨 ➔ 도움이 되다\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【為になる】 ためになる</span>\n'
            '  <span class="mnemonic-parts">인생이나 지식에 교훈과 보탬이 되는 유익함을 뜻함</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "청해_어휘", "관용구", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0021",
        "kanji": "為替",
        "kana": "かわせ",
        "meaning": "환, 외환, 환율 (★초특급 숙자훈 특수 독음! 품사: 명사)",
        "sentences": (
            '<div class="example-ja"><ruby>円安<rt>えんやす</rt></ruby>が<ruby>急速<rt>きゅうそく</rt></ruby>に'
            '<ruby>進<rt>すす</rt></ruby>む<ruby>中<rt>なか</rt></ruby>、'
            '<ruby>政府<rt>せいふ</rt></ruby>による<span class="target-word"><ruby>為替<rt>かわせ</rt></ruby><ruby>介入<rt>かいにゅう</rt></ruby></span>への'
            '<ruby>警戒<rt>けいかい</rt></ruby><ruby>感<rt>かん</rt></ruby>が<ruby>高<rt>たか</rt></ruby>まっている。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [★특수 숙자훈: かわせ!] 為替相場(환율 시세), 外国為替(외국환/외환), 為替レート(환율), 為替介入(외환시장 개입)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">엔저가 급속히 진행되는 가운데 정부의 외환시장 개입에 대한 경계감이 고조되고 있다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">為(위할/할 위) + 替(바꿀 체) ➔ かわせ</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    현금 대신 어음이나 증서로 서로 교환(交わす かわす)하여 결제함 ➔ 환, 외환(かわせ)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【為替】 かわせ</span>\n'
            '  <span class="mnemonic-parts">★いかえ(X) ➔ かわせ(O)! 일본 경제 뉴스 1순위 독음</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "경제_금융", "특수독음", "JLPT_N2"]
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
