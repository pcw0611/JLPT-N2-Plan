# -*- coding: utf-8 -*-
"""
Add '組み（組・組む）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0055",
    "kanji": "組み（組・組む）",
    "kana": "くみ（くむ）",
    "meaning": "1. 조, 반, 한 패, 세트, 짝 (명사/접미사: 組み・組) / 2. (일정·예산을) 짜다, 손잡다, 엮다 (동사원형: 組む) / 3. 독해 필수 복합어(取り組み·仕組み·枠組み)",
    "sentences": (
        '<div class="example-ja"><ruby>新<rt>しん</rt></ruby>しいプロジェクトに向けて'
        '<ruby>他社<rt>たしゃ</rt></ruby>と<span class="target-word"><ruby>手<rt>て</rt></ruby>を'
        '<ruby>組<rt>く</rt></ruby>み</span>、'
        '<ruby>綿密<rt>めんみつ</rt></ruby>なスケジュールを'
        '<span class="target-word"><ruby>組<rt>く</rt></ruby>んだ</span>。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [명사·접미사 組み/組] A組(A조), 勝ち組・負け組(승자/패자 집단), トランプ一組(카드 한 벌) / [★N2 독해 1순위 복합명사] <b>取り組み(とりくみ, 대처/노력)</b>, <b>仕組み(しくみ, 구조/원리/메커니즘)</b>, <b>枠組み(わくぐみ, 틀/프레임워크)</b>, <b>骨組み(ほねぐみ, 뼈대)</b> / [동사 組む 초빈출 연어] 手を組む(손을 잡다/제휴하다), スケジュール・予算を組む(일정/예산을 짜다), 腕を組む(팔짱을 끼다), 足を組む(다리를 꼬다) / 음독: 組織(そしき, 조직)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">새로운 프로젝트를 위해 타사와 손을 잡고(제휴하고), 면밀한 일정을 짰다. (★명사 \'組み(조, 세트, 짜임)\'와 함께 N2 독해 지문의 단골인 \'取り組み(대처, 노력)\', \'仕組み(구조, 장치)\', \'枠組み(틀, 체계)\'는 필수 세트입니다!)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">組 (짤 조)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    실(糸)을 또(且: 또 차/조) 엮고 또 엮어서 하나로 짜맞추는 모습 ➔ 짜다, 조직하다, 조(組・組み・組む)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【組み (くみ)】 조, 세트, 짜임 / 【組む (くむ)】 짜다, 제휴하다</span>\n'
        '  <span class="mnemonic-parts">★훈독: くみ(組み), くむ(組む) vs 음독: そ(組織 そしき, 組成 そせい) / N2 독해 핵심: 取り組み(대처), 仕組み(구조), 枠組み(틀)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "명사", "동사", "JLPT_N2"]
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
