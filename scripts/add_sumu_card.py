# -*- coding: utf-8 -*-
"""
Add '済む（済んでしまったこと）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0067",
    "kanji": "済む（済んでしまったこと・済ませる）",
    "kana": "すむ（すんでしまったこと・すませる）",
    "meaning": "1. 끝나다, 해결되다, 때워지다, 무사히 넘어가다 (동사원형: 済む) / 2. 이미 끝나 버린 일 (済んでしまったこと) / 3. N2 문법 문형: 〜ずに済む(~하지 않고 끝나다), 〜で済む(~로 해결되다)",
    "sentences": (
        '<div class="example-ja"><span class="target-word"><ruby>済<rt>す</rt></ruby>んでしまったこと</span>を'
        '<ruby>今<rt>いま</rt></ruby>さら<ruby>悔<rt>く</rt></ruby>やんでも'
        '<ruby>始<rt>はじ</rt></ruby>まらないから、'
        '<ruby>前<rt>まえ</rt></ruby>を<ruby>向<rt>む</rt></ruby>いて<ruby>進<rt>すす</rt></ruby>もう。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [사진 속 표현] <b>済んでしまったこと / 済んだこと</b>(이미 끝나 버린 일 / 지나간 일) / [★N2 필수 핵심 문법 문형] <b>〜ないで済む / 〜ずに済む (~하지 않고도 해결되다/넘어가다)</b>: 買わずに済んだ(사지 않고도 넘어갔다), 手術を受けずに済んだ(수술받지 않고 끝났다) / <b>〜で済む / 〜て済む (~로 해결되다/때워지다)</b>: 謝って済む問題ではない(사과해서 끝날 문제가 아니다), 弁償で済む(변상으로 해결되다), 軽傷で済む(가벼운 부상으로 그치다) / [타동사 짝꿍] <b>済ます / 済ませる(すませる, 끝내다/때우다)</b>: 朝食をパンで済ませる(아침을 빵으로 때우다) / 음독: 経済(けいざい, 경제), 救済(きゅうさい, 구제), 返済(へんさい, 변제/상환)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">이미 끝나 버린 일(済んでしまったこと)을 이제 와서 후회해 봐야 소용없으니, 앞을 향해 나아가자. (★N2 핵심 문법 문형: \'〜ずに済む(~하지 않고도 해결되다)\', \'〜で済む(~로 때워지다/끝나다)\'와 타동사 \'済ませる(때우다/끝내다)\'는 필수 세트입니다!)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n  <div class="visual-scan-header">\n    <span class="visual-scan-badge">済 (건널/끝날 제)</span>\n  </div>\n  <div class="visual-scan-desc">\n    물(氵)을 건너(斉: 가지런할 제) 무사히 맞은편 언덕에 도달하여 일이 끝난 모습 ➔ 끝나다, 해결되다(済む・済ます)\n  </div>\n</div>\n<div class="mnemonic-item">\n  <span class="mnemonic-char">【済む (すむ)】 끝나다, 해결되다 / 【済ませる】 끝내다, 때우다</span>\n  <span class="mnemonic-parts">★훈독: すむ(済む), すませる(済ませる) vs 음독: さい(経済・救済), せい(返済) / N2 문형: 〜ずに済む(~않고 해결되다), 〜で済む(~로 끝나다)</span>\n</div>'
    ),
    "tags": ["독해_어휘", "동사", "문법연계", "회화_청해", "JLPT_N2"]
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
