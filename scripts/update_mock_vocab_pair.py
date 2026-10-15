# -*- coding: utf-8 -*-
"""
Update both '済んでしまったこと' and '決して言う' in Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
and set them both immediately due today for instant review.
"""
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
SUMU_NOTE_ID = 1791968752995
KESSHITE_NOTE_ID = 1791970014828

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

# 1. Update 済んでしまったこと
sumu_fields = {
    "kanji": "済んでしまったこと（済む・済ませる）",
    "kana": "すんでしまったこと（すむ・すませる）",
    "meaning": "1. 이미 끝나 버린 일 (済んでしまったこと) / 2. 끝나다, 해결되다, 때워지다, 무사히 넘어가다 (동사원형: 済む) / 3. [★N2 필수 핵심 문법 문형] 〜ずに済む(~하지 않고 끝나다), 〜で済む(~로 해결되다)",
    "sentences": (
        '<div class="example-ja"><span class="target-word"><ruby>済<rt>す</rt></ruby>んでしまったこと</span>を'
        '<ruby>今<rt>いま</rt></ruby>さら<ruby>悔<rt>く</rt></ruby>やんでも'
        '<ruby>始<rt>はじ</rt></ruby>まらないから、'
        '<ruby>前<rt>まえ</rt></ruby>を<ruby>向<rt>む</rt></ruby>いて<ruby>進<rt>すす</rt></ruby>もう。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [사진 속 출제 문맥 ★★★] <b>済んでしまったこと / 済んだこと</b>(이미 끝나 버린 일 / 지나간 일) / [★N2 필수 핵심 문법 문형] <b>〜ないで済む / 〜ずに済む (~하지 않고도 해결되다/넘어가다)</b>: 買わずに済んだ(사지 않고도 넘어갔다), 手術を受けずに済んだ(수술받지 않고 끝났다) / <b>〜で済む / 〜て済む (~로 해결되다/때워지다)</b>: 謝って済む問題ではない(사과해서 끝날 문제가 아니다), 弁償で済む(변상으로 해결되다), 軽傷で済む(가벼운 부상으로 그치다) / [타동사 짝꿍] <b>済ます / 済ませる(すませる, 끝내다/때우다)</b>: 朝食をパンで済ませる(아침을 빵으로 때우다) / 음독: 経済(けいざい, 경제), 救済(きゅうさい, 구제), 返済(へんさい, 변제/상환)</span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">이미 끝나 버린 일(済んでしまったこと)을 이제 와서 후회해 봐야 소용없으니, 앞을 향해 나아가자. (★N2 핵심 문법 문형: \'〜ずに済む(~하지 않고도 해결되다)\', \'〜で済む(~로 때워지다/끝나다)\'와 타동사 \'済ませる(때우다/끝내다)\'는 필수 세트입니다!)</span></div>'
    ),
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">済 (건널/끝날 제)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    물(氵)을 건너(斉: 가지런할 제) 무사히 맞은편 언덕에 도달하여 일이 끝난 모습 ➔ 끝나다, 해결되다(済む・済ます)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【済む (すむ)】 끝나다, 해결되다 / 【済ませる】 끝내다, 때우다</span>\n'
        '  <span class="mnemonic-parts">★훈독: すむ(済む), すませる(済ませる) vs 음독: さい(経済・救済), せい(返済) / N2 문형: 〜ずに済む(~않고 해결되다), 〜で済む(~로 끝나다)</span>\n'
        '</div>'
    )
}

res1 = call_mcp('update_note_fields', {'id': SUMU_NOTE_ID, 'fields': sumu_fields})
print(f"[1] 済んでしまったこと updated: {res1.get('structuredContent', {}).get('message', 'ok')}")

# 2. Update 決して言う
kesshite_fields = {
    "kanji": "決して言う（決して〜ない・決して〜ものではない）",
    "kana": "けっしていう（けっして〜ない・けっして〜ものではない）",
    "meaning": "1. 결코 말하다 (부정 호응: 결코 말하지 않다 / 결코 말해서는 안 된다: 決して言うものではない) / 2. 決して: 결코, 절대로 (부사: 뒤에 강한 부정 표현 〜ない, 〜まい, 〜ものではない 수반) / 3. [★N2 필수 도리 문법] 〜ものではない (~하는 것이 아니다 / ~해서는 안 된다)",
    "sentences": (
        '<div class="example-ja"><ruby>人<rt>ひと</rt></ruby>の<ruby>悪口<rt>わるくち</rt></ruby>や<ruby>陰口<rt>かげぐち</rt></ruby>は、'
        '<span class="target-word"><ruby>決<rt>けっ</rt></ruby>して<ruby>言<rt>い</rt></ruby>うものではない</span>。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [사진 속 출제 문맥 ★★★] <b>人の悪口や陰口は、決して言う（ものではない）。</b>(남의 욕이나 뒷담화는 결코 말하는 것이 아니다 / 해서는 안 된다) / [★N2 필수 핵심 문법 문형] <b>V사전형 ＋ ものではない (~해서는 안 된다 / ~하는 것이 아니다: 도덕적 훈계·상식)</b> / [부사 決して의 필수 부정 호응] <b>決して〜ない (결코 ~않다)</b>, <b>決して〜まい (결코 ~하지 않겠다)</b>, 決してあきらめない(결코 포기하지 않는다), 決して言うまい(결코 말하지 않겠다) / [부정 호응 부사 3총사 구별] <b>決して (결코 - 강한 의지/단언)</b> vs <b>めったに〜ない (좀처럼 ~않다 - 빈도)</b> vs <b>ちっとも・少しも〜ない (조금도 ~않다 - 정도)</b></span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">남의 욕(悪口)이나 뒷담화(陰口)는, 결코 말하는 것이 아니다(해서는 안 된다: 決して言うものではない)。<br>★N2 시험 단골 3종 세트: ① 부사 「決して(결코)」의 부정 호응, ② 연어 「悪口や陰口を言う(욕이나 험담을 하다)」, ③ 문법 「〜ものではない(도리: ~해서는 안 된다)」의 결합형입니다!</span></div>'
    ),
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">決 (결단할 결) + 言 (말씀 언)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    마음을 단단히 결단(決)하고 맹세하듯 단호하게 말함(言) ➔ 결코 말하지 않겠다(決して言うまい), 결코 말해서는 안 된다(決して言うものではない)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【決して言う (けっしていう)】 결코 말하다 ➔ 뒤에 반드시 부정 호응!</span>\n'
        '  <span class="mnemonic-parts">★발음: けっして(촉음화) + いう / 호응 문형: 決して言うものではない(~해서는 안 된다), 決して言うまい(~하지 않겠다), 決して言わない</span>\n'
        '</div>'
    )
}

res2 = call_mcp('update_note_fields', {'id': KESSHITE_NOTE_ID, 'fields': kesshite_fields})
print(f"[2] 決して言う updated: {res2.get('structuredContent', {}).get('message', 'ok')}")

# 3. Set both cards immediately due today
res_due = call_mcp('card_set_due_date', {
    'card_ids': [SUMU_NOTE_ID, KESSHITE_NOTE_ID],
    'days': '0!'
})
print(f"[3] Rescheduled both cards to due now: {res_due.get('structuredContent', {}).get('message', 'ok')}")

# 4. Sync Anki
call_mcp('sync')
print("[4] Anki sync completed successfully!")
