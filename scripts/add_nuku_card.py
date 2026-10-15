# -*- coding: utf-8 -*-
"""
Add '抜く（抜き・抜ける）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0066",
    "kanji": "抜く（抜き・抜ける）",
    "kana": "ぬく（ぬき・ぬける）",
    "meaning": "1. 뽑다, 빼다, 거르다, 앞지르다 (동사원형: 抜く) / 2. 빼기, 제외 (명사/접미사: 抜き) / 3. N2 문법 문형: 〜抜く(끝까지 ~해내다), 〜抜きで(제외하고)",
    "sentences": (
        '<div class="example-ja"><ruby>本番<rt>ほんばん</rt></ruby>では'
        '<ruby>緊張<rt>きんちょう</rt></ruby>せずに'
        '<span class="target-word"><ruby>肩<rt>かた</rt></ruby>の<ruby>力<rt>ちから</rt></ruby>を'
        '<ruby>抜<rt>ぬ</rt></ruby>き</span>、'
        '<ruby>最後<rt>さいご</rt></ruby>まで'
        '<span class="target-word"><ruby>走<rt>はし</rt></ruby>り<ruby>抜<rt>ぬ</rt></ruby>いた</span>。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [동사 抜く 초빈출 관용구 ★★★] <b>手を抜く(てをぬく, 적당히 얼렁뚱땅하다/요령 피우다 ➔ N2 초빈출!)</b>, <b>肩の力を抜く(어깨 힘을 빼다/긴장을 풀다)</b>, <b>息を抜く(숨을 돌리다/한숨 쉬다)</b>, 朝食を抜く(아침을 거르다), 前の車を抜く(앞 차를 추월하다) / [명사·접미사 抜き] <b>冗談抜きで(농담 빼고/진담으로)</b>, ワサビ抜き(와사비 빼고) / [★N2 핵심 문법 문형] <b>Vます형 + 抜く (끝까지 ~해내다)</b>: 生き抜く(살아남다), 勝ち抜く(끝까지 이겨내다), 悩み抜く(끝까지 고민하다) / <b>N + 抜きにしては (~을 빼놓고는/제외하고는)</b> / [자동사 짝꿍] <b>抜ける(ぬける, 빠지다/사라지다)</b>: 気が抜ける(맥이 풀리다/김빠지다), 力が抜ける</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">실전(본 시험)에서는 긴장하지 않고 어깨의 힘을 빼고(肩の力を抜き), 끝까지 완주했다(走り抜いた). (★시험 초빈출: 관용구 \'手を抜く(요령 피우다, 대충 얼렁뚱땅하다)\', 문법 문형 \'〜抜く(끝까지 ~해내다)\', \'〜抜きで(제외하고)\'는 필수 세트입니다!)</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">抜 (뽑을 발)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    손(扌)으로 단단히 박혀 있는 것의 무리(友) 사이에서 쑥 잡아당겨 빼내는 모습 ➔ 뽑다, 빼다(抜く・抜き)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【抜く (ぬく)】 뽑다, 빼다 / 【抜き】 빼기 / 【抜ける】 빠지다</span>\n'
        '  <span class="mnemonic-parts">★훈독: ぬく(抜く), ぬき(抜き), ぬける(抜ける) vs 음독: ばつ(抜群 ばつぐん, 選抜 せんばつ) / 관용구: 手を抜く(대충하다), 冗談抜き(농담 제쳐두고)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "동사", "명사", "문법연계", "관용구", "JLPT_N2"]
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
