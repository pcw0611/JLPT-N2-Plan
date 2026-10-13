# -*- coding: utf-8 -*-
"""
Add '腫れる' and '上達' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
        "id": "READING-NEWS-0028",
        "kanji": "腫れる",
        "kana": "はれる",
        "meaning": "붓다, 부어오르다 (품사: 2그룹 자동사 / 타동사: 腫らす はらす 부풀리다)",
        "sentences": (
            '<div class="example-ja"><ruby>一晩<rt>ひとばん</rt></ruby><ruby>中<rt>じゅう</rt></ruby><ruby>泣<rt>な</rt></ruby>いたせいで、'
            '<ruby>翌朝<rt>よくあさ</rt></ruby><ruby>目<rt>め</rt></ruby>が'
            '<span class="target-word"><ruby>腫<rt>は</rt></ruby>れて</span>しまった。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [★はれる 구분 필수!] 腫れる(눈·상처가 붓다), 晴れる(날씨·기분이 개다), 目を腫らす(눈을 퉁퉁 붓게 하다), 足が腫れる(발이 붓다)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">밤새도록 운 탓에, 다음 날 아침 눈이 부어 버렸다. (晴れる＝날씨가 개다와 구분!)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">腫(종기 종, 훈: は・れる)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    몸(月=육달월)에 무거운(重) 혹이 생겨 퉁퉁 부어오름 ➔ 붓다, 부어오르다(はれる)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【腫れる】 はれる</span>\n'
            '  <span class="mnemonic-parts">★晴れる(날씨가 개다) vs 腫れる(몸이 붓다) 한자 구분 빈출</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "신체_건강", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0029",
        "kanji": "上達",
        "kana": "じょうたつ",
        "meaning": "(기술·어학·실력 등이) 향상됨, 능숙해짐, 늚 (품사: 명사 / する동사, N2 필수)",
        "sentences": (
            '<div class="example-ja"><ruby>毎日<rt>まいにち</rt></ruby>コツコツ<ruby>練習<rt>れんしゅう</rt></ruby>したおかげで、'
            '<ruby>日本語<rt>にほんご</rt></ruby>の<ruby>会話<rt>かいわ</rt></ruby>がだいぶ'
            '<span class="target-word"><ruby>上達<rt>じょうたつ</rt></ruby>した</span>。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 上達が早い/遅い(습득/발전이 빠르다/느리다), 腕前が上達する(솜씨가 늘다) ↔ 向上(수준 향상), 進歩(과학·문명의 진보)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">매일 꾸준히 연습한 덕분에, 일본어 회화 실력이 꽤 늘었다. (개인의 기량·실력이 늚)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">上(위 상/じょう) + 達(달할 달/たつ)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    더 높은(上) 수준에 도달함(達) ➔ 실력·기량이 늘다, 능숙해지다(じょうたつ)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【上達】 じょうたつ</span>\n'
            '  <span class="mnemonic-parts">★개인의 솜씨나 외국어 실력이 느는 것은 무조건 上達!</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "기량_향상", "JLPT_N2"]
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
