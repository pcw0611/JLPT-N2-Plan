# -*- coding: utf-8 -*-
"""
Add 'サボる' and '上司' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
        "id": "READING-NEWS-0046",
        "kanji": "サボる",
        "kana": "さぼる",
        "meaning": "(일·공부 등을) 땡땡이치다, 농땡이 피우다, 게으름 피우다 (품사: 1그룹 5단 타동사/자동사, N2 필수)",
        "sentences": (
            '<div class="example-ja"><ruby>仕事<rt>しごと</rt></ruby>を'
            '<span class="target-word">サボって</span>'
            '<ruby>喫茶店<rt>きっさてん</rt></ruby>で<ruby>休<rt>やす</rt></ruby>んでいたところを、'
            '<ruby>偶然<rt>ぐうぜん</rt></ruby><ruby>上司<rt>じょうし</rt></ruby>に<ruby>見<rt>み</rt></ruby>つかってしまった。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 仕事をサボる(일을 땡땡이치다/농땡이 부리다), 学校・授業をサボる(학교/수업을 빼먹다), 練習をサボる(연습을 게을리하다) / 어원: 프랑스어 sabotage(사보타주: 노동쟁의/고의적 태업) + 일본어 동사 활용 어미 \'る\' / 유의어: 怠ける(なまける, 빈둥거리다), 怠る(おこたる, 소홀히 하다)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">일을 땡땡이치고 카페에서 쉬고 있던 것을, 우연히 상사에게 들키고 말았다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">サボる (외래어 어원 + 동사 연상)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    프랑스어 sabotage(사보타주: 고의적 태업)의 앞 글자 \'サボ\'에 1그룹 동사 어미 \'る\'를 결합! ➔ 일을 게을리하거나 땡땡이치다\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【サボる (さぼる)】 땡땡이치다 / 농땡이 부리다</span>\n'
            '  <span class="mnemonic-parts">★1그룹 5단 동사 활용: サボる ➔ サボった(땡땡이쳤다), サボっている(농땡이 피우고 있다), サボらないで(땡땡이치지 마)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "동사", "일상_어휘", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0047",
        "kanji": "上司",
        "kana": "じょうし",
        "meaning": "상사, 직속상관 (품사: 명사, N2 독해·청해 비즈니스 최다 빈출)",
        "sentences": (
            '<div class="example-ja"><ruby>新<rt>あたら</rt></ruby>しいプロジェクトの'
            '<ruby>進捗<rt>しんちょく</rt></ruby><ruby>状況<rt>じょうきょう</rt></ruby>について、'
            '<span class="target-word"><ruby>上司<rt>じょうし</rt></ruby>に</span>'
            '<ruby>報告<rt>ほうこく</rt></ruby>した。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 上司に報告・相談する(상사에게 보고/상의하다), 上司の指示に従う(상사의 지시에 따르다), 直属の上司(직속상사) / ★반의어: 部下(ぶか, 부하 직원) / 관련어: 同僚(どうりょう, 동료), 先輩(せんぱい), 後輩(こうはい)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">새로운 프로젝트의 진척 상황에 대해, 상사에게 보고했다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">上 (위 상) + 司 (맡을 사)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    나보다 위(上)에서 조직의 업무를 주관하고 맡아보는(司) 사람 ➔ 상사(上司)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【上司 (じょうし)】 상사 / 직속상관</span>\n'
            '  <span class="mnemonic-parts">★음독: 上(じょう, 上位・上級) + 司(し, 司会・司法) ➔ じょうし / ★반의어 세트 필수: 上司(じょうし) ↔ 部下(ぶか)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "비즈니스_어휘", "명사", "JLPT_N2"]
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
