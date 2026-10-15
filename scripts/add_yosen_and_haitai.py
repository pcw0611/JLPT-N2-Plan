# -*- coding: utf-8 -*-
"""
Add '予選' and '敗退' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
        "id": "READING-NEWS-0059",
        "kanji": "予選",
        "kana": "よせん",
        "meaning": "예선 (명사 / する동사: 본선·결승 진출자를 가리기 위한 경기나 심사)",
        "sentences": (
            '<div class="example-ja"><ruby>全国<rt>ぜんこく</rt></ruby><ruby>大会<rt>たいかい</rt></ruby>への'
            '<ruby>出場<rt>しゅつじょう</rt></ruby>を<ruby>目指<rt>めざ</rt></ruby>し、'
            '<ruby>厳<rt>きび</rt></ruby>しい<span class="target-word"><ruby>予選<rt>よせん</rt></ruby>を</span>'
            '<ruby>突<rt>とっ</rt></ruby><ruby>破<rt>ぱ</rt></ruby>した。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] <b>予選を突破する / 予選を通過する(예선을 돌파/통과하다)</b>, <b>予選敗退(よせんはいたい, 예선 탈락)</b>, <b>予選落ち(よせんおち, 예선 탈락)</b> / 대조어·관련어: 本選(ほんせん, 본선), 決勝(けっしょう, 결승), 準決勝(じゅんけっしょう, 준결승), 一回戦(いっかいせん, 1회전)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">전국대회 출전을 목표로 치열한 예선(予選)을 돌파했다. (★연어: 予選を突破する/통과하다, 予選敗退/예선 탈락)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">予 (미리 예) + 選 (가릴 선)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    본선에 앞서 미리(予) 대표 선수를 가려 뽑는(選) 경기 ➔ 예선(予選)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【予選 (よせん)】 예선</span>\n'
            '  <span class="mnemonic-parts">★음독: 予(よ: 予定・予測・予防) + 選(せん: 選手・選択・当選) ➔ よせん / 훈독: 選ぶ(えらぶ, 고르다/선택하다)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "스포츠_대회", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0060",
        "kanji": "敗退",
        "kana": "はいたい",
        "meaning": "패퇴, 패배하여 탈락함 (명사 / する동사: 시합·경기·경쟁에서 져서 물러남)",
        "sentences": (
            '<div class="example-ja"><ruby>強豪<rt>きょうごう</rt></ruby><ruby>相手<rt>あいて</rt></ruby>に'
            '<ruby>善戦<rt>ぜんせん</rt></ruby>したものの、'
            '<ruby>惜<rt>お</rt></ruby>しくも<ruby>一回戦<rt>いっかいせん</rt></ruby>で'
            '<span class="target-word"><ruby>敗退<rt>はいたい</rt></ruby>した</span>。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★] <b>予選敗退(よせんはいたい, 예선 탈락)</b>, <b>初戦敗退(しょせんはいたい, 첫 경기 탈락)</b>, 一回戦で敗退する(1회전에서 패퇴하다), 惜しくも敗退する(아쉽게도 패배하여 탈락하다) / 대조어: <b>勝ち進む(かちすすむ, 승리해 다음 라운드로 진출하다)</b> / 유의어: 敗北(はいぼく, 패배) / 동사: 敗れる(やぶれる, 패하다/지다), 退く(しりぞく, 물러나다)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">강호를 상대로 선전했으나, 아쉽게도 1회전에서 패퇴(탈락)했다. (★뉴스·스포츠 기사 단골: 予選敗退/예선 탈락, 初戦敗退/첫 경기 탈락, 勝ち進む/승리해 진출하다)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">敗 (패할 패) + 退 (물러날 퇴)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    시합에서 패하여(敗) 쓸쓸히 경기장 밖으로 물러나는(退) 모습 ➔ 패퇴, 탈락(敗退)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【敗退 (はいたい)】 패퇴 / 탈락</span>\n'
            '  <span class="mnemonic-parts">★음독: 敗(はい: 失敗・勝敗・敗北) + 退(たい: 引退・退職・辞退) ➔ はいたい / 훈독: 敗れる(やぶれる, 패하다), 退く(しりぞく, 물러나다)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "스포츠_대회", "JLPT_N2"]
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
