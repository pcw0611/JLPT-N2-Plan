# -*- coding: utf-8 -*-
"""
Add '山積み（山積）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0053",
    "kanji": "山積み（山積）",
    "kana": "やまづみ（さんせき）",
    "meaning": "산더미처럼 쌓임, 산적 (명사: 문제·과제·일·물건 등이 산더미처럼 많이 쌓여 있는 상태)",
    "sentences": (
        '<div class="example-ja"><ruby>新<rt>しん</rt></ruby>プロジェクトの<ruby>立<rt>た</rt></ruby>ち<ruby>上<rt>あ</rt></ruby>げに<ruby>伴<rt>ともな</rt></ruby>い、'
        '<ruby>解決<rt>かいけつ</rt></ruby>すべき<ruby>課題<rt>かだい</rt></ruby>が'
        '<span class="target-word"><ruby>山積<rt>やまづ</rt></ruby>み</span>になっている。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 課題が山積みだ(과제가 산더미다), 問題が山積みだ(문제가 산더미처럼 쌓여 있다), 仕事が山積み(일이 산더미) / 동의어(한자 음독): <b>山積（さんせき）する</b> (산적하다) ➔ 독해 패러프레이징 1순위! / 동사: 積む(つむ, 쌓다), 積もる(つもる, 쌓이다)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">새 프로젝트 시작에 따라 해결해야 할 과제가 산더미처럼 쌓여(山積み) 있다. (★음독 형태인 \'山積(さんせき)する: 산적하다\'와 완벽히 같은 뜻으로 독해 지문 단골 바꿔쓰기 표현입니다!)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">山 (뫼 산) + 積 (쌓을 적)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    산(山)처럼 벼(禾)와 재물(貝)을 높이 쌓아(積) 올린 모습 ➔ 산더미처럼 쌓임(山積み)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【山積み (やまづみ)】 산더미처럼 쌓임 / 【山積 (さんせき)】 산적</span>\n'
        '  <span class="mnemonic-parts">★훈독: やまづみ(山積み) vs 음독: さんせき(山積) / 관련 동사: 積む(つむ, 싣다/쌓다), 積もる(つもる, 눈·먼지 등이 쌓이다)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "명사", "비유_상태", "JLPT_N2"]
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
