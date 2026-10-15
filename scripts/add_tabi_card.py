# -*- coding: utf-8 -*-
"""
Add '一人旅（旅・旅程）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0051",
    "kanji": "一人旅（旅・旅程）",
    "kana": "ひとりたび（たび・りょてい）",
    "meaning": "1. 나홀로 여행, 혼자 떠나는 여행 (一人旅) / 2. 여행, 여정 (명사: 旅 たび / 旅程 りょてい)",
    "sentences": (
        '<div class="example-ja"><ruby>気<rt>き</rt></ruby>ままな'
        '<span class="target-word"><ruby>一人旅<rt>ひとりたび</rt></ruby></span>に'
        '<ruby>出<rt>で</rt></ruby>て、'
        '<ruby>知<rt>し</rt></ruby>らない<ruby>町<rt>まち</rt></ruby>をのんびり'
        '<ruby>歩<rt>ある</rt></ruby>いた。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 一人旅に出る(나홀로 여행을 떠나다), 旅に出る(여행/여정을 떠나다), 旅の思い出(여행의 추억), 旅程を組む(여정/일정을 짜다) / 훈독: 旅(たび, 여행/여정) ↔ 음독: 旅程(りょてい, 여정), 旅行(りょこう, 여행), 旅館(りょかん, 료칸)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">마음 내키는 대로 나홀로 여행(혼자 여행)을 떠나, 낯선 마을을 느긋하게 걸었다. (★단독 한자 旅는 훈독 \'たび\'로 여행/여정을 뜻하며, 앞 글자가 \'人\'이면 시험 단골 \'一人旅 ひとりたび\'입니다!)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">旅 (나그네 려)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    깃발(方)을 앞세우고 무리 지어 먼 길을 떠나던 사람들의 모습 ➔ 나그네, 여행(旅)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【旅 (たび)】 여행, 여정 / 【一人旅 (ひとりたび)】 나홀로 여행</span>\n'
        '  <span class="mnemonic-parts">★독음 구별: 훈독 \'たび\'(一人旅・船旅) vs 음독 \'りょ\'(旅行・旅程・旅館) / \'여정\'의 한자어는 旅程(りょてい)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "명사", "문화_생활", "JLPT_N2"]
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
