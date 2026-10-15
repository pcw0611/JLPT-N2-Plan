# -*- coding: utf-8 -*-
"""
Add '場当たり（場当たり的）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0085",
    "kanji": "場当たり（場当たり的）",
    "kana": "ばあたり（ばあたりてき）",
    "meaning": "1. (명사) 임기응변, 그때그때 둘러맞춤, 주먹구구 (계획성 없는 땜질) / 2. (형동: 場当たり的) 임기응변식의, 미봉책의 / 3. (연극) 무대 총연습(리허설)",
    "sentences": (
        '<div class="example-ja"><ruby>根本<rt>こんぽん</rt></ruby><ruby>的<rt>てき</rt></ruby>な'
        '<ruby>原因<rt>げんいん</rt></ruby>を<ruby>究明<rt>きゅうめい</rt></ruby>せず、'
        '<span class="target-word"><ruby>場当<rt>ばあ</rt></ruby>たり<ruby>的<rt>てき</rt></ruby>な'
        '<ruby>対応<rt>たいおう</rt></ruby></span>を<ruby>繰<rt>く</rt></ruby>り<ruby>返<rt>かえ</rt></ruby>していては、'
        '<ruby>問題<rt>もんだい</rt></ruby>は<ruby>解決<rt>かいけつ</rt></ruby>しない。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [신문 사설·비판 논설 독해 절대 1순위 ★★★] <b>場当たり的な対応(임기응변식 대응 / 땜질식 처방)</b>, <b>場当たり的な政策(주먹구구식 땜질 정책)</b>, <b>その場しのぎ(그 자리 모면하기/미봉책)</b> / [유의어] <b>一時しのぎ(いちじしのぎ, 임시변통)</b>, <b>付け焼き刃(つけやきば, 벼락치기/임시방편)</b>, 弥縫策(びほうさく, 미봉책) / [반의어] <b>抜本的(ばっぽんてき, 발본적/근본적인)</b> ➔ 抜本的な改革(근본적인 개혁)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">근본적인 원인을 규명하지 않고, 임기응변식 대응(場当たり的な対応, 땜질식 처방)만을 반복해서는 문제는 해결되지 않는다. (★비판 사설·논설 1순위 표현: \'場当たり的な対応/땜질식 대응\', 유의어 \'その場しのぎ\', 반의어 \'抜本的/근본적인\')</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">場 (마당/그 자리 장: ば) + 当たり (맞을 당: あたり)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    미리 계획을 세우지 않고 그 자리(場)에 부딪히는(当たり) 대로 둘러댐 ➔ 임기응변, 땜질, 주먹구구 (場当たり) / 형동: 場当たり的 (임기응변식의, 땜질식의)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【場当たり (ばあたり)】 임기응변 / 【場当たり的】 땜질식의</span>\n'
        '  <span class="mnemonic-parts">★훈독 구성: ば + あたり / 비판 논설 단골: 場当たり的な対応(땜질식 대응) vs 抜本的(근본적)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "사설_논설", "명사", "형용동사", "JLPT_N2", "JLPT_N1"]
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
