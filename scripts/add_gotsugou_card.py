# -*- coding: utf-8 -*-
"""
Add 'ご都合（都合）' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
    "id": "READING-NEWS-0068",
    "kanji": "ご都合（都合）",
    "kana": "ごつごう（つごう）",
    "meaning": "1. (상대방의) 형편, 사정, 일정 (명사/경어: ご都合) / 2. 형편, 사정, 융통 (명사: 都合) / 3. 시간을 내다, 융통하다 (都合をつける)",
    "sentences": (
        '<div class="example-ja"><ruby>来週<rt>らいしゅう</rt></ruby>の'
        '<ruby>打<rt>う</rt></ruby>ち<ruby>合<rt>あ</rt></ruby>わせについて、'
        '<span class="target-word">ご<ruby>都合<rt>つごう</rt></ruby>のよろしい</span>'
        '<ruby>日時<rt>にちじ</rt></ruby>をいくつかお'
        '<ruby>知<rt>し</rt></ruby>らせいただけますでしょうか。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [청해·비즈니스 경어 초빈출 1위 ★★★] <b>ご都合はいかがでしょうか(일정/형편이 어떠신지요?)</b>, <b>ご都合のよろしい日時(편하신 일시)</b> / [N2 필수 관용구 ★★★] <b>都合をつける(つごうをつける, 어떻게든 시간을 내다 / 일정을 맞추다 / 돈을 융통하다)</b> / [독해·공지문 단골] <b>都合により(사정상 / 사정에 의해)</b> ➔ 本日は都合により臨時休業いたします(금일은 사정상 임시 휴업합니다) / [기본 표현] 都合がいい(일정이 맞다/형편이 좋다) ↔ 都合が悪い(일정이 안 맞다) / 한자 都의 특이 음독: と(都会 とかい) vs つ(都合 つごう)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">다음 주 미팅(회의)에 대해, 편하신 일시(ご都合のよろしい日時)를 몇 개 알려주실 수 있으신지요? (★N2 청해 및 비즈니스 일정 조율 1순위: \'ご都合はいかがでしょうか\', N2 빈출 관용구 \'都合をつける: 시간을 내다/융통하다\')</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">ご + 都 (도읍 도) + 合 (합할 합)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    수도(都)의 사람과 자원이 딱 들어맞게(合) 돌아가듯, 개인의 상황과 일정이 딱 맞아떨어지는 형편 ➔ 사정, 형편(都合) / 존경: ご都合\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【都合 (つごう)】 사정, 형편 / 【ご都合】 (상대방의) 형편</span>\n'
        '  <span class="mnemonic-parts">★발음 특이음독: 都(つ) + 合(ごう) ➔ つごう / 관용구: 都合をつける(시간을 내다), 都合により(사정상)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "청해_어휘", "비즈니스_경어", "명사", "관용구", "JLPT_N2"]
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
