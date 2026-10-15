# -*- coding: utf-8 -*-
"""
Add '悪口', '陰口', '決して' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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

cards = [
    {
        "id": "READING-NEWS-0075",
        "kanji": "悪口",
        "kana": "わるくち（わるぐち）",
        "meaning": "욕, 험담, 악담 (명사: 남의 결점이나 안 좋은 점을 헐뜯는 말)",
        "sentences": (
            '<div class="example-ja"><ruby>人<rt>ひと</rt></ruby>の<span class="target-word"><ruby>悪口<rt>わるくち</rt></ruby>を</span><ruby>言<rt>い</rt></ruby>うのではなく、'
            '<ruby>互<rt>たが</rt></ruby>いの<ruby>長所<rt>ちょうしょ</rt></ruby>を<ruby>認<rt>みと</rt></ruby>め<ruby>合<rt>あ</rt></ruby>うことが<ruby>大切<rt>たいせつ</rt></ruby>だ。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★] <b>悪口を言う(욕을 하다/험담하다)</b>, <b>悪口をたたく(험담을 늘어놓다)</b> / [짝꿍 세트] <b>悪口や陰口(욕이나 뒷담화)</b> / [사자성어] 悪口雑言(あっこうぞうごん, 온갖 악담과 욕설) / 대조어: 褒め言葉(ほめことば, 칭찬의 말)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span><span class="translation-text">남의 욕(험담)을 하는 것이 아니라, 서로의 장점을 인정해 주는 것이 중요하다. (★짝꿍 표현: 悪口を言う/험담하다, 悪口や陰口/욕이나 뒷담화)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n  <div class="visual-scan-header">\n    <span class="visual-scan-badge">悪 (악할 악) + 口 (입 구)</span>\n  </div>\n  <div class="visual-scan-desc">\n    입(口)으로 남을 해치는 악(悪)한 말을 내뱉는 것 ➔ 욕, 험담(悪口 わるくち)\n  </div>\n</div>\n<div class="mnemonic-item">\n  <span class="mnemonic-char">【悪口 (わるくち / わるぐち)】 욕, 험담</span>\n  <span class="mnemonic-parts">★훈독: わるくち / 음독 사자성어: 悪口雑言(あっこうぞうごん) / 짝꿍: 陰口(かげぐち)</span>\n</div>'
        ),
        "tags": ["독해_어휘", "인간관계", "명사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0076",
        "kanji": "陰口",
        "kana": "かげぐち",
        "meaning": "뒷담화, 뒤에서 하는 험담 (명사: 본인이 없는 그늘/뒤에서 몰래 헐뜯는 말)",
        "sentences": (
            '<div class="example-ja"><ruby>本人<rt>ほんにん</rt></ruby>のいないところで<span class="target-word"><ruby>陰口<rt>かげぐち</rt></ruby>をたたく</span>のは、'
            '<ruby>卑怯<rt>ひきょう</rt></ruby>な<ruby>行為<rt>こうい</rt></ruby>だ。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 관용구 ★★★ N2 단골] <b>陰口をたたく(かげぐちをたたく, 뒷담화를 까다 / 뒤에서 헐뜯다)</b>, 陰口を言う(뒷담화를 하다), 陰口を言われる(뒤에서 욕을 먹다) / [대조 표현] <b>面と向かって言う(めんとむかっていう, 면전에서 대놓고 말하다)</b> ↔ 陰口をたたく(뒤에서 뒷담화를 까다)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span><span class="translation-text">본인이 없는 곳에서 뒷담화를 까는 것(陰口をたたく)은 비겁한 행위이다. (★N2 시험 1순위 관용구: \'陰口をたたく(뒷담화를 까다/뒤에서 험담하다)\'와 대조 표현 \'面と向かって言う(대놓고 말하다)\'는 필수 암기!)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n  <div class="visual-scan-header">\n    <span class="visual-scan-badge">陰 (그늘 음) + 口 (입 구)</span>\n  </div>\n  <div class="visual-scan-desc">\n    당사자 모르게 그늘(陰 かげ)에 숨어서 입(口)으로 험담을 늘어놓는 모습 ➔ 뒷담화(陰口 かげぐち)\n  </div>\n</div>\n<div class="mnemonic-item">\n  <span class="mnemonic-char">【陰口 (かげぐち)】 뒷담화</span>\n  <span class="mnemonic-parts">★훈독: かげ(陰) + ぐち(口) ➔ かげぐち / 초빈출 관용구: 陰口をたたく(뒷담화를 까다)</span>\n</div>'
        ),
        "tags": ["독해_어휘", "인간관계", "명사", "관용구", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0077",
        "kanji": "決して",
        "kana": "けっして",
        "meaning": "결코, 절대로 (부사: 뒤에 부정 표현을 수반하여 강한 결심이나 부정 명제를 나타냄: 決して〜ない / 〜まい)",
        "sentences": (
            '<div class="example-ja"><ruby>今回<rt>こんかい</rt></ruby>の<ruby>失敗<rt>しっぱい</rt></ruby>の<ruby>悔<rt>くや</rt></ruby>しさは、'
            '<span class="target-word"><ruby>決<rt>けっ</rt></ruby>して</span><ruby>忘<rt>わす</rt></ruby>れない。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 호응 문형 ★★★ N2 필수 부사] <b>決して〜ない (결코 ~하지 않다)</b>, <b>決して〜まい (결코 ~하지 않겠다 / 결코 ~하지 않을 것이다)</b>, 決してあきらめない(결코 포기하지 않는다), 決して〜わけではない(결코 ~인 것은 아니다) / [부정 호응 부사 비교] <b>決して(결코 - 강한 의지/단언)</b> vs <b>めったに〜ない(좀처럼 ~않다 - 빈도)</b> vs <b>ちっとも・少しも〜ない(조금도 ~않다 - 정도)</b></span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span><span class="translation-text">이번 실패의 분함(분한 마음)은 결코(決して) 잊지 않겠다. (★문법 호응 필수 짝꿍: \'決して〜ない(결코 ~않다)\', \'決して〜まい(결코 ~하지 않겠다)\')</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n  <div class="visual-scan-header">\n    <span class="visual-scan-badge">決 (결단할 결) + して</span>\n  </div>\n  <div class="visual-scan-desc">\n    마음을 단단히 결단(決)하고 맹세하듯 단호하게 말함 ➔ 결코, 절대로(決して)\n  </div>\n</div>\n<div class="mnemonic-item">\n  <span class="mnemonic-char">【決して (けっして)】 결코, 절대로</span>\n  <span class="mnemonic-parts">★발음 촉음화: けつ + して ➔ けっして / 호응 문형: 決して〜ない(결코 ~않다), 決して〜まい</span>\n</div>'
        ),
        "tags": ["독해_어휘", "문법연계", "부사", "JLPT_N2"]
    }
]

for card in cards:
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
