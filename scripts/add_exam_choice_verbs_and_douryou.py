# -*- coding: utf-8 -*-
"""
Add 5 cards to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘':
1. 真似る (まねる) - 흉내 내다, 모방하다 (정답 まねて의 사전형)
2. 倣う (ならう) - 본뜨다, 전례를 따르다 (오답 ならって의 사전형)
3. 気取る (きどる) - 폼 잡다, ~인 체하다, 잘난 척하다 (오답 きどって의 사전형)
4. 従う (したがう) - 따르다, 순종하다, 준수하다 (오답 したがって의 사전형)
5. 同僚 (どうりょう) - 동료, 직장 동료
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
        "id": "READING-NEWS-0023",
        "kanji": "真似る",
        "kana": "まねる",
        "meaning": "흉내 내다, 모방하다, 본뜨다 (★보기 ① まねて의 사전형! 품사: 2그룹 타동사)",
        "sentences": (
            '<div class="example-ja"><ruby>先生<rt>せんせい</rt></ruby>の<ruby>発音<rt>はつおん</rt></ruby>をよく<ruby>聞<rt>き</rt></ruby>いて、'
            '<ruby>同<rt>おな</rt></ruby>じになるように<ruby>発音<rt>はつおん</rt></ruby>を'
            '<span class="target-word"><ruby>真似<rt>まね</rt></ruby>て</span>みましょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [관련 어휘·관용구] 発音を真似る(발음을 흉내 내다), 真似(まね, 흉내/짓거리), 人の真似をする(남의 흉내를 내다), 馬鹿な真似(바보 같은 짓)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">선생님의 발음을 잘 듣고, 똑같이 되도록 발음을 흉내 내어(따라 해) 봅시다. (명사: 真似 흉내, 짓)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">真(참 진) + 似(닮을 사, 훈: にる)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    진짜(真)처럼 똑같이 닮게(似) 하다 ➔ 흉내 내다, 모방하다(まねる)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【真似る】 まねる</span>\n'
            '  <span class="mnemonic-parts">소리나 행동을 흉내 내다! (본 시험 정답: 発音を真似る)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "유의어_구분", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0024",
        "kanji": "倣う",
        "kana": "ならう",
        "meaning": "본뜨다, (전례나 선례를) 따르다, 본받다 (★보기 ② ならって의 사전형! 품사: 1그룹 동사)",
        "sentences": (
            '<div class="example-ja"><ruby>前例<rt>ぜんれい</rt></ruby>に'
            '<span class="target-word"><ruby>倣<rt>なら</rt></ruby>って</span>、'
            '<ruby>新<rt>あたら</rt></ruby>しい<ruby>計画<rt>けいかく</rt></ruby>を'
            '<ruby>進<rt>すす</rt></ruby>めることにした。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 관용구·연어] 前例に倣う(전례를 따르다/본뜨다 ★시험 1순위!), 習慣に倣う(관습을 따르다), 右に倣え(우향우/남을 무작정 따라 함)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">전례를 본떠서(따라서), 새로운 계획을 추진하기로 했다. (cf. 習う: 배우다, 익히다)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">倣(본뜰 방, 훈: なら・う)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    사람(亻)이 본보기를 놓아두고(放) 그대로 본떠서 따름 ➔ 본뜨다, 전례를 따르다(ならう)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【倣う】 ならう</span>\n'
            '  <span class="mnemonic-parts">★『前例に倣う(전례를 따르다)』로 외우기! 真似る(단순 흉내)와 구분</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "유의어_구분", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0025",
        "kanji": "気取る",
        "kana": "きどる",
        "meaning": "폼 잡다, ~인 체하다, 잘난 척하다 (★보기 ③ きどって의 사전형! 품사: 1그룹 동사)",
        "sentences": (
            '<div class="example-ja"><ruby>彼<rt>かれ</rt></ruby>はいつも'
            '<span class="target-word"><ruby>気取<rt>きど</rt></ruby>った</span>'
            '<ruby>態度<rt>たいど</rt></ruby>をとるので、<ruby>周<rt>まわ</rt></ruby>りから<ruby>敬遠<rt>けいえん</rt></ruby>されている。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 표현] 気取った態度(폼 잡는 태도/거들먹거리는 태도), 気取らない人(꾸밈없는 소탈한 사람), 学者気取り(학자 행세), 気取る(잘난 척하다)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">그는 언제나 폼 잡는 태도를 취해서, 주변으로부터 경원시당하고 있다. (気取らない＝소탈하다)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">気(기운/마음 기) + 取(취할 취)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    마음이나 폼(気)을 거만하게 취함(取) ➔ 폼 잡다, ~인 체하다, 잘난 척하다(きどる)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【気取る】 きどる</span>\n'
            '  <span class="mnemonic-parts">★気取らない人(꾸밈없고 털털한 사람) / 学者気取り(학자인 체함)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "유의어_구분", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0026",
        "kanji": "従う",
        "kana": "したがう",
        "meaning": "따르다, 순종하다, 준수하다; (~에) 따르다 (★보기 ④ したがって의 사전형! 품사: 1그룹 자동사)",
        "sentences": (
            '<div class="example-ja"><ruby>会社<rt>かいしゃ</rt></ruby>の<ruby>規則<rt>きそく</rt></ruby>や'
            '<ruby>上司<rt>じょうし</rt></ruby>の<ruby>指示<rt>しじ</rt></ruby>に'
            '<span class="target-word"><ruby>従<rt>したが</rt></ruby>って</span><ruby>行動<rt>こうどう</rt></ruby>してください。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 指示に従う(지시에 따르다), 規則に従う(규칙을 따르다), 予定に従って(예정에 따라), 法律に従う(법률을 준수하다)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">회사의 규칙이나 상사의 지시에 따라 행동해 주십시오. (복종·준수하여 따름)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">従(따를 종, 훈: したが・う)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    길(彳)에서 앞서가는 사람의 발자국을 뒤따름 ➔ 복종하여 따르다, 준수하다(したがう)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【従う】 したがう</span>\n'
            '  <span class="mnemonic-parts">★사람의 지시나 법/규칙에 복종하여 따르는 것! (指示に従う)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "유의어_구분", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0027",
        "kanji": "同僚",
        "kana": "どうりょう",
        "meaning": "동료, 직장 동료 (품사: 명사, JLPT N2 필수)",
        "sentences": (
            '<div class="example-ja"><ruby>困<rt>こま</rt></ruby>ったときは、'
            '<ruby>会社<rt>かいしゃ</rt></ruby>の<span class="target-word"><ruby>同僚<rt>どうりょう</rt></ruby></span>に'
            '<ruby>相談<rt>そうだん</rt></ruby>するといいアドバイスがもらえる。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [연어 및 뉘앙스] 会社の同僚(직장 동료), 同僚と協力する(동료와 협력하다) ↔ 仲間(취미·모임의 친구/동료), 同期(입사 동기)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">곤란할 때는 회사 동료에게 상담하면 좋은 조언을 얻을 수 있다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">同(같을 동/どう) + 僚(동료 료/りょう)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    같은(同) 직무를 맡아 일하는 관원/동료(僚) ➔ 직장 동료(どうりょう)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【同僚】 どうりょう</span>\n'
            '  <span class="mnemonic-parts">★직장 동료는 무조건 同僚! (장음 どう + 장음 りょう 주의)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "비즈니스_직장", "JLPT_N2"]
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
