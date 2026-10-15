# -*- coding: utf-8 -*-
"""
Add '親切（しんせつ）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0065",
    "kanji": "親切",
    "kana": "しんせつ",
    "meaning": "친절 (명사 / な형용사: 친절하다, 다정하다 / N2 독해 단골: 親切の押し売り)",
    "sentences": (
        '<div class="example-ja"><ruby>見知<rt>みし</rt></ruby>らぬ<ruby>土地<rt>とち</rt></ruby>で'
        '<ruby>道<rt>みち</rt></ruby>に<ruby>迷<rt>まよ</rt></ruby>った<ruby>際<rt>さい</rt></ruby>、'
        '<ruby>地元<rt>じもと</rt></ruby>の<ruby>人<rt>ひと</rt></ruby>がとても'
        '<span class="target-word"><ruby>親切<rt>しんせつ</rt></ruby>に</span>'
        '<ruby>案内<rt>あんない</rt></ruby>してくれた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 표현·비즈니스 경어] <b>ご親切にありがとうございます(친절에 진심으로 감사드립니다)</b>, <b>親切丁寧(しんせつていねい, 친절하고 정중함)</b>, 親切心(しんせつしん, 친절한 마음씨) ↔ 不親切(ふしんせつ, 불친절) / [★N2 독해 지문 단골 테마] <b>親切の押し売り(しんせつのおしうり, 원치 않는 친절의 강요/오지랖)</b> ≒ 余計なお世話(쓸데없는 참견) / [한자 切의 음독] 切(せつ: 親切・適切・切実) ↔ 訓: 切る(きる, 자르다)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">낯선 땅에서 길을 잃었을 때, 현지 주민이 매우 친절하게(親切に) 안내해 주었다. (★N2 독해 단골 비판 주제인 \'親切の押し売り(친절의 강요/오지랖)\'과 비즈니스 표현 \'ご親切にありがとうございます\'는 필수입니다!)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n  <div class="visual-scan-header">\n    <span class="visual-scan-badge">親 (친할 친) + 切 (간절할/끊을 절)</span>\n  </div>\n  <div class="visual-scan-desc">\n    내 몸에 직접 닿을(切: 迫る/간절할 절) 만큼 가깝고 친근하게(親) 남을 배려하는 마음 ➔ 친절(親切)\n  </div>\n</div>\n<div class="mnemonic-item">\n  <span class="mnemonic-char">【親切 (しんせつ)】 친절</span>\n  <span class="mnemonic-parts">★음독: 親(しん: 親切・親友・両親) + 切(せつ: 親切・適切・切実) ➔ しんせつ / N2 독해 테마: 親切の押し売り(친절 강요/오지랖)</span>\n</div>'
    ),
    "tags": ["독해_어휘", "명사", "형용동사", "인간관계", "JLPT_N2"]
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
