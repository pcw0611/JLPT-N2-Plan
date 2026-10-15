# -*- coding: utf-8 -*-
"""
Add '引責辞任（いんせきじにん）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0078",
    "kanji": "引責辞任（引責・辞任）",
    "kana": "いんせきじにん（いんせき・じにん）",
    "meaning": "인책 사임 (명사 / する동사: 실패나 불상사·실적 부진 등의 책임을 지고 스스로 자리나 직책에서 물러남)",
    "sentences": (
        '<div class="example-ja"><ruby>相次<rt>あいつ</rt></ruby>ぐ<ruby>不祥事<rt>ふしょうじ</rt></ruby>の'
        '<ruby>責任<rt>せきにん</rt></ruby>を<ruby>取<rt>と</rt></ruby>り、'
        '<ruby>社長<rt>しゃちょう</rt></ruby>が'
        '<span class="target-word"><ruby>引責<rt>いんせき</rt></ruby><ruby>辞任<rt>じにん</rt></ruby>に</span>'
        '<ruby>追<rt>お</rt></ruby>い<ruby>込<rt>こ</rt></ruby>まれた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [신문·뉴스 초빈출 연어 ★★★] <b>引責辞任する(책임을 지고 사임하다)</b>, <b>引責辞任に追い込まれる(인책 사임으로 내몰리다 ➔ 追い込む 빈출!)</b>, 業績不振で引責辞任する(실적 부진으로 인책 사임하다) / [핵심 한자어 분해] <b>引責(いんせき, 책임을 떠안음)</b> ➔ 責任を引き受ける / <b>辞任(じにん, 직책을 그만둠)</b> ↔ <b>就任(しゅうにん, 취임)</b> / [유사어 비교] 辞任(じにん, 임원·장관 등 직책에서 물러남) vs 辞職(じしょく, 직업·회사 자체를 그만둠) vs 辞退(じたい, 후보나 상을 사양하고 물러남)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">잇따른 불상사(不祥事)의 책임을 지고, 사장이 인책 사임(引責辞任)으로 내몰렸다. (★시사·뉴스 기사 1순위: 引責(책임을 떠안음) + 辞任(사임) ➔ \'引責辞任に追い込まれる(인책 사임으로 내몰리다)\', 辞任 ↔ 就任(취임))</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n  <div class="visual-scan-header">\n    <span class="visual-scan-badge">引 (끌 인) + 責 (책임 책) + 辞 (말씀/사양할 사) + 任 (맡길 임)</span>\n  </div>\n  <div class="visual-scan-desc">\n    내 몸으로 책임(責)을 끌어안고(引), 맡았던(任) 직책을 스스로 사양하여(辞) 물러남 ➔ 인책 사임(引責辞任)\n  </div>\n</div>\n<div class="mnemonic-item">\n  <span class="mnemonic-char">【引責辞任 (いんせきじにん)】 인책 사임</span>\n  <span class="mnemonic-parts">★음독: 引(いん) + 責(せき) + 辞(じ: 辞任・辞職・辞退) + 任(にん: 辞任・就任・責任) / 대조어: 就任(しゅうにん, 취임)</span>\n</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "시사_정치_경제", "명사", "JLPT_N2"]
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
