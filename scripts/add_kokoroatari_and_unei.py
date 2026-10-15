# -*- coding: utf-8 -*-
"""
Add 'お心当たり（心当たり）' and '運営事務局（運営・事務局）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
        "id": "READING-NEWS-0083",
        "kanji": "お心当たり（心当たり）",
        "kana": "おこころあたり（こころあたり）",
        "meaning": "1. (상대방에 대해) 짚이는 곳, 짐작 가는 바, 기억나는 바 (명사/경어: お心当たり) / 2. 짚이는 데, 짐작 (명사: 心当たり)",
        "sentences": (
            '<div class="example-ja"><ruby>館内<rt>かんない</rt></ruby>にて'
            '<ruby>鍵<rt>かぎ</rt></ruby>のお<ruby>落<rt>と</rt></ruby>とし<ruby>物<rt>もの</rt></ruby>がございました。'
            '<span class="target-word">お<ruby>心当<rt>こころあ</rt></ruby>たりのある<ruby>方<rt>かた</rt></ruby></span>は、'
            '<ruby>受付<rt>うけつけ</rt></ruby>までお<ruby>越<rt>こ</rt></ruby>しください。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [청해·안내방송·비즈니스 절대 1순위 ★★★] <b>お心当たりのある方(짚이는 바가 있으신 분 / 해당자)</b>, <b>お心当たりはございませんか(짐작 가시는 바 없으신지요?)</b> / [기본형 관용구] <b>全く心当たりがない(전혀 짚이는 데가 없다)</b>, 心当たりを当たる / 探す(짚이는 곳을 수소문하다/찾아보다) / [유의 관용구] <b>身に覚えがない(みにおぼえがない, 자신이 한 기억/잘못이 없다)</b> ≒ 心当たりがない</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">관내에서 열쇠 분실물이 있었습니다. 짚이는 바가 있으신 분(お心当たりのある方)은 안내 데스크로 와 주시기 바랍니다. (★청해 안내방송 및 비즈니스 1순위 표현: \'お心当たりのある方/짐작 가는 바가 있으신 분\', 관용구 \'全く心当たりがない/전혀 짚이는 데가 없다\')</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">お + 心 (마음 심) + 当たり (닿을/맞을 당)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    마음(心)에 딱 짚여서 맞닿는(当たり: 当たる) 구석이나 짐작 ➔ 짚이는 데, 짐작(心当たり) / 경어: お心当たり\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【心当たり (こころあたり)】 짚이는 곳 / 【お心当たり】 (경어)</span>\n'
            '  <span class="mnemonic-parts">★훈독 구성: こころ + あたり / 청해 방송 단골: お心当たりのある方(짚이는 바가 있으신 분)</span>\n'
            '</div>'
        ),
        "tags": ["청해_어휘", "비즈니스_경어", "독해_어휘", "명사", "관용구", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0084",
        "kanji": "運営事務局（運営・事務局）",
        "kana": "うんえいじむきょく（うんえい・じむきょく）",
        "meaning": "운영 사무국 (행사, 대회, 단체, 웹사이트 등의 실무 및 운영을 총괄하는 본부 부서)",
        "sentences": (
            '<div class="example-ja">ご<ruby>不明<rt>ふめい</rt></ruby>な<ruby>点<rt>てん</rt></ruby>やご<ruby>質問<rt>しつもん</rt></ruby>がございましたら、'
            '<span class="target-word"><ruby>大会<rt>たいかい</rt></ruby><ruby>運営<rt>うんえい</rt></ruby><ruby>事務<rt>じむ</rt></ruby><ruby>局<rt>きょく</rt></ruby></span>まで'
            'お<ruby>問<rt>と</rt></ruby>い<ruby>合<rt>あ</rt></ruby>わせください。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [정보검색·공지문 독해 1순위 ★★★] <b>運営事務局にお問い合わせください(운영 사무국으로 문의해 주십시오)</b>, <b>大会運営事務局(대회 운영 사무국)</b>, 事務局長(사무국장) / [핵심 분해] <b>運営(うんえい, 운영)</b>: 組織・イベントを運営する(조직/이벤트를 운영하다) / <b>事務局(じむきょく, 사무국/집행본부)</b> / [주의 한자 음독] 局: 薬局(やっきょく), 郵便局(ゆうびんきょく)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">궁금한 점이나 질문이 있으시면 대회 운영 사무국(大会運営事務局)으로 문의해 주시기 바랍니다. (★독해 문제 9 정보검색 및 안내문 1순위: \'運営事務局にお問い合わせください/운영 사무국으로 문의 바랍니다\', 핵심어: 運営 うんえい / 事務局 じむきょく)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">運(운전할 운) + 営(경영할 영) + 事(일 사) + 務(힘쓸 무) + 局(판/부서 국)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    조직이나 행사를 굴려 경영하는(運営 うんえい) 실무를 맡아보는 부서(事務局 じむきょく) ➔ 운영 사무국\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【運営 (うんえい)】 운영 / 【事務局 (じむきょく)】 사무국</span>\n'
            '  <span class="mnemonic-parts">★음독: 運(うん) + 営(えい) / 事(じ) + 務(む) + 局(きょく) / 안내문/공지문 문의처 단골</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "비즈니스_어휘", "실용문_정보검색", "명사", "복합명사", "JLPT_N2"]
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
