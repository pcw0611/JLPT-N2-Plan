# -*- coding: utf-8 -*-
"""
Add 'なさる' and 'される' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith('data: '):
            return json.loads(line[6:])['result']
    return None

cards_to_add = [
    {
        "id": "READING-NEWS-0030",
        "kanji": "なさる",
        "kana": "なさる",
        "meaning": "하시다 (★'する'의 특별/고유 존경어! 공식 안내문·비즈니스 1순위)",
        "sentences": (
            '<div class="example-ja"><ruby>周辺<rt>しゅうへん</rt></ruby><ruby>住民<rt>じゅうみん</rt></ruby>の<ruby>方<rt>かた</rt></ruby>の<ruby>迷惑<rt>めいわく</rt></ruby>になりますので、'
            '<ruby>指定<rt>してい</rt></ruby>の<ruby>駐車場<rt>ちゅうしゃじょう</rt></ruby><ruby>以外<rt>いがい</rt></ruby>には'
            '<span class="target-word"><ruby>駐車<rt>ちゅうしゃ</rt></ruby>なさらないよう</span>、お<ruby>願<rt>ねが</rt></ruby>いいたします。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 경어 패턴] 〜なさらないよう(にお願いします)(~하지 않으시도록), どうなさいますか(어떻게 하시겠습니까?), お〜なさる(하시다), ます형: なさいます, 명령형: なさい</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">주변 주민분들께 폐가 되므로, 지정된 주차장 이외에는 주차하지 않으시도록 부탁드립니다. (비즈니스/공지문 1순위 고유 존경어)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">なさる (為さる, 할 위)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    상대방의 행동(する)을 가장 높여 부르는 고유 특별 존경어 ➔ 하시다(なさる)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【なさる】 하시다</span>\n'
            '  <span class="mnemonic-parts">★경의도: なさる(공식 공지/고객 최고급) > される(가벼운 일상 존경)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "경어_필수", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0031",
        "kanji": "される",
        "kana": "される",
        "meaning": "1) [존경] 하시다 (する의 조동사형 존경)  2) [수동/피동] 되다, 당하다 (품사: 2그룹 동사)",
        "sentences": (
            '<div class="example-ja"><ruby>社長<rt>しゃちょう</rt></ruby>は<ruby>来週<rt>らいしゅう</rt></ruby>アメリカへ'
            '<span class="target-word"><ruby>出張<rt>しゅっちょう</rt></ruby>される</span><ruby>予定<rt>よてい</rt></ruby>です。／ '
            '<ruby>不当<rt>ふとう</rt></ruby>な<ruby>扱<rt>あつか</rt></ruby>いを<span class="target-word">されて</span><ruby>抗議<rt>こうぎ</rt></ruby>した。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [주의] される는 일상 존경(\'하시다\')과 수동(\'당하다/되다\') 양쪽으로 쓰임. 격식 있는 공식 공지문에서는 수동 오인 방지 및 경의도를 위해 なさる를 우선함!</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">사장님은 다음 주에 미국으로 출장 가실 예정입니다. (존경) ／ 부당한 대우를 당해서 항의했다. (수동)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">される (する의 미연형 さ + れる)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    1) 존경: 하시다 (가벼운 회화체)  2) 수동(피동): 당하다, 되다 (비판되다/주차당하다)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【される】 하시다 / 당하다</span>\n'
            '  <span class="mnemonic-parts">★수동태의 의미를 함께 가지므로 공식 공지문 금지 표현에는 부적합!</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "경어_수동", "JLPT_N2"]
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
