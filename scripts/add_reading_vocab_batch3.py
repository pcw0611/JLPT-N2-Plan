# -*- coding: utf-8 -*-
"""
Add '政府', '政策', '連日', '報じられている' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
        "id": "READING-NEWS-0038",
        "kanji": "政府",
        "kana": "せいふ",
        "meaning": "정부 (품사: 명사, N2 독해·신문기사 필수 기본 어휘)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>政府<rt>せいふ</rt></ruby></span>は'
            '<ruby>物価<rt>ぶっか</rt></ruby><ruby>高騰<rt>こうとう</rt></ruby>に<ruby>対<rt>たい</rt></ruby>する'
            '<ruby>緊急<rt>きんきゅう</rt></ruby><ruby>支援<rt>しえん</rt></ruby><ruby>策<rt>さく</rt></ruby>を<ruby>発表<rt>はっぴょう</rt></ruby>した。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 政府が発表する(정부가 발표하다), 政府の対応(정부의 대응), 日本政府(일본 정부) / 관련어: 行政(ぎょうせい, 행정), 内閣(ないかく, 내각)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">정부는 물가 급등에 대한 긴급 지원책을 발표했다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">政 (정사 정) + 府 (관청 부)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    나라의 정사(政)를 돌보고 집행하는 최고 관청(府) ➔ 정부(政府)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【政府 (せいふ)】 정부</span>\n'
            '  <span class="mnemonic-parts">★음독: 政(せい, 政治・政策) + 府(ふ, 幕府・京都府) ➔ せいふ</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "명사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0039",
        "kanji": "政策",
        "kana": "せいさく",
        "meaning": "정책 (품사: 명사, N2 독해·뉴스·사설 초빈출 어휘)",
        "sentences": (
            '<div class="example-ja"><ruby>少子化<rt>しょうしか</rt></ruby><ruby>対策<rt>たいさく</rt></ruby>として、'
            '<ruby>新<rt>あたら</rt></ruby>しい<ruby>子育<rt>こそだ</rt></ruby>て<ruby>支援<rt>しえん</rt></ruby>'
            '<span class="target-word"><ruby>政策<rt>せいさく</rt></ruby></span>が<ruby>打<rt>う</rt></ruby>ち<ruby>出<rt>だ</rt></ruby>された。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 政策を打ち出す(정책을 내놓다/제시하다), 政策を実施・推進する(정책을 실시/추진하다), 経済政策(경제정책), 外交政策(외교정책) / ★동음이의어 구별: 政策(せいさく, 정책) vs 製作・制作(せいさく, 제작/만듦)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">저출산 대책으로서, 새로운 육아 지원 정책이 제시되었다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">政 (정사 정) + 策 (꾀/계책 책)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    정사(政)를 바르게 다스리기 위해 세우는 계획과 계책(策) ➔ 정책(政策)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【政策 (せいさく)】 정책</span>\n'
            '  <span class="mnemonic-parts">★음독: 政(せい) + 策(さく, 対策・方策) ➔ せいさく / 주의: 制作・製作(せいさく, 예술작품/물건 제작)과 문맥 구별 필수!</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "명사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0040",
        "kanji": "連日",
        "kana": "れんじつ",
        "meaning": "연일, 매일 계속됨 (품사: 명사, 부사적 사용, N2 기사·독해 단골)",
        "sentences": (
            '<div class="example-ja"><ruby>猛暑<rt>もうしょ</rt></ruby>が<ruby>続<rt>つづ</rt></ruby>き、'
            '<span class="target-word"><ruby>連日<rt>れんじつ</rt></ruby></span>'
            '<ruby>熱中症<rt>ねっちゅうしょう</rt></ruby>への<ruby>警戒<rt>けいかい</rt></ruby>が<ruby>呼<rt>よ</rt></ruby>びかけられている。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 連日報じられる(연일 보도되다), 連日満員(연일 만원), 連日の猛暑(연일 계속되는 폭염) / 유의어: 日々(ひび, 나날), 毎日(まいにち) ↔ 連夜(れんや, 연야/매일 밤)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">혹서(무더위)가 계속되어, 연일 열사병에 대한 경계가 당부되고 있다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">連 (이을 련) + 日 (날 일)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    수레(車)가 줄지어 가듯(辶) 날(日)들이 줄줄이 잇달아 계속되다 ➔ 연일(連日)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【連日 (れんじつ)】 연일 / 매일 계속됨</span>\n'
            '  <span class="mnemonic-parts">★음독: 連(れん, 連続・連休) + 日(じつ, 休日・祝日・当日) ➔ れんじつ</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "명사", "부사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0041",
        "kanji": "報じられている（報じる）",
        "kana": "ほうじられている（ほうじる）",
        "meaning": "보도되고 있다, 전해지고 있다 (원형: 報じる / 품사: 2그룹 일단 타동사 수동형, N2 독해 뉴스·사설 최다 빈출)",
        "sentences": (
            '<div class="example-ja"><ruby>政府<rt>せいふ</rt></ruby>の<ruby>新<rt>あたら</rt></ruby>しい<ruby>政策<rt>せいさく</rt></ruby>について、'
            'メディアで<span class="target-word"><ruby>連日<rt>れんじつ</rt></ruby><ruby>大<rt>おお</rt></ruby>きく<ruby>報<rt>ほう</rt></ruby>じられている</span>。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 & 활용] 〜と報じられている(~라고 보도되고 있다), 大きく報じられる(대대적으로 보도되다), ニュースで報じる(뉴스에서 보도하다/알리다) / 유의어: 報道される(ほうどうされる, 보도되다), 伝えられる(つたえられる, 전해지다)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">정부의 새로운 정책에 대해, 언론(미디어)에서 연일 대대적으로 보도되고 있다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">報 (알릴 보)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    어떤 사실이나 중요한 소식을 사람들에게 널리 알리다 ➔ 보도하다(報じる)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【報じる (ほうじる)】 보도하다 / 알리다 (수동형: 報じられる)</span>\n'
            '  <span class="mnemonic-parts">★뉴스 독해 필수 구문: \'〜と報じられている\' ➔ \"~라고 보도되고 있다\" / 관련어: 報道(ほうどう, 보도), 報告(ほうこく, 보고)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "동사_활용", "JLPT_N2"]
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
