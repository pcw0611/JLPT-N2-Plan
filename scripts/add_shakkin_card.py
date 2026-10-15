# -*- coding: utf-8 -*-
"""
Add '借金' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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

card = {
    "id": "READING-NEWS-0042",
    "kanji": "借金",
    "kana": "しゃっきん",
    "meaning": "빚, 차금, 빌린 돈 (품사: 명사, 스루동사 借金する: 빚을 지다, N2 필수)",
    "sentences": (
        '<div class="example-ja"><ruby>友人<rt>ゆうじん</rt></ruby>からの'
        '<span class="target-word"><ruby>借金<rt>しゃっきん</rt></ruby></span>を、'
        '<ruby>計画<rt>けいかく</rt></ruby><ruby>的<rt>てき</rt></ruby>に'
        '<ruby>返済<rt>へんさい</rt></ruby>した。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 借金を返す/返済する(빚을 갚다/상환하다), 借金を抱える(빚을 떠안다), 借金がかさむ(빚이 불어나다), 多額の借金(거액의 빚) / 유의어: 負債(ふさい, 부채), ローン(대출) / 파생어: 借金取り(しゃっきんとり, 빚쟁이/빚독촉자)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">친구로부터 빌린 빚(돈)을 계획적으로 변제(상환)했다.</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">借 (빌릴 차) + 金 (쇠/돈 금)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    사람(亻)이 옛(昔)부터 서로 빌려 쓰던(借) 돈(金) ➔ 借金(しゃっきん: 빚, 빌린 돈)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【借金 (しゃっきん)】 빚 / 차금</span>\n'
        '  <span class="mnemonic-parts">★발음 촉음화 주의: 借(しゃく) + 金(きん) ➔ しゃっきん (しゃくきん X) / 동사: 借りる (かりる, 빌리다) ↔ 貸す (かす, 빌려주다)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "명사", "경제_생활", "JLPT_N2"]
}

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
