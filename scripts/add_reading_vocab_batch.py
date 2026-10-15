# -*- coding: utf-8 -*-
"""
Add '試す（試した）' and '組み立てる' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
        "id": "READING-NEWS-0034",
        "kanji": "試す（試した）",
        "kana": "ためす（ためした）",
        "meaning": "시험삼아 해보다, 시도하다, 시험하다 (★과거형: 試した / 품사: 1그룹 5단 타동사, N2 필수)",
        "sentences": (
            '<div class="example-ja"><ruby>新<rt>あたら</rt></ruby>しい<ruby>方法<rt>ほうほう</rt></ruby>を'
            '<span class="target-word"><ruby>試<rt>ため</rt></ruby>した</span>ところ、'
            '<ruby>作業<rt>さぎょう</rt></ruby><ruby>効率<rt>こうりつ</rt></ruby>が<ruby>大幅<rt>おおはば</rt></ruby>に<ruby>向上<rt>こうじょう</rt></ruby>した。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 方法を試す(방법을 시험해보다), 実力・腕を試す(실력을 시험하다), 味を試す(맛을 보다) / 유의어: 試みる(こころみる, 문어체·의지적 시도)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">새로운 방법을 시도해 보았더니(시험삼아 해보았더니), 작업 효율이 대폭 향상되었다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">試 (시험할 시)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    言(말씀 언) + 式(법 식/규칙) ➔ 정해진 격식과 말로 실력을 평가해 보다 ➔ 試 (시험할 시)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【試す (ためす)】 시험삼아 해보다 / 시도하다</span>\n'
            '  <span class="mnemonic-parts">★훈독: ためす (시험하다/시도하다), こころみる (시도하다) / 음독: 試合(しあい), 試験(しけん)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "동사_활용", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0035",
        "kanji": "組み立てる",
        "kana": "くみたてる",
        "meaning": "조립하다, 구성하다, 짜 맞추다 (품사: 2그룹 일단 타동사, 복합동사, N2 필수)",
        "sentences": (
            '<div class="example-ja"><ruby>説明書<rt>せつめいしょ</rt></ruby>を<ruby>見<rt>み</rt></ruby>ながら、'
            '<ruby>自分<rt>じぶん</rt></ruby>で<ruby>家具<rt>かぐ</rt></ruby>を<span class="target-word"><ruby>組<rt>く</rt></ruby>み<ruby>立<rt>た</rt></ruby>てた</span>。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어] 家具・機械を組み立てる(가구·기계를 조립하다), 計画・理論を組み立てる(계획·이론을 구성하다) ↔ 分解する(분해하다), 解体する(해체하다) / 명사형: 組み立て(조립), 組み立て式(조립식)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">설명서를 보면서 스스로 가구를 조립했다. (부품을 짜 맞추어 세우다 / 논리·계획을 구성하다)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">組 (짤 조) + 立 (설 립)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    糸(실)를 짜듯(組) 부품들을 엮어서 똑바로 세우다(立) ➔ 조립하다, 구성하다\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【組み立てる (くみたてる)】 조립하다 / 구성하다</span>\n'
            '  <span class="mnemonic-parts">★조립식: 組み立て式(くみたてしき) / 반대말: 分解する(ぶんかいする, 분해하다)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "모의고사_어휘", "복합동사", "JLPT_N2"]
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
