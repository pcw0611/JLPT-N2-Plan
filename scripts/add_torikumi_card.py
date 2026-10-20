# -*- coding: utf-8 -*-
"""
Add '取り組み（取り組む）' (READING-NEWS-0086) to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
and make it immediately due for today's review.
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
    "id": "READING-NEWS-0086",
    "kanji": "取り組み（取り組む）",
    "kana": "とりくみ（とりくむ）",
    "meaning": "1. (명사) 대처, 노력, 실천 방안, 추진 (과제나 문제를 해결하기 위해 진지하게 맞붙어 힘쓰는 구체적 활동) / 2. (동사: 取り組む) [조사: 〜に取り組む] ~에 몰두하다, 진지하게 달라붙다, 힘쓰다 / 3. (스모·시합 용어) 맞붙음, 대진표, 시합",
    "sentences": (
        '<div class="example-ja"><ruby>地球<rt>ちきゅう</rt></ruby><ruby>温暖化<rt>おんだんか</rt></ruby>を'
        '<ruby>防<rt>ふせ</rt></ruby>ぐため、<ruby>企業<rt>きぎょう</rt></ruby>や<ruby>自治体<rt>じちたい</rt></ruby>による'
        '<ruby>脱炭素<rt>だつたんそ</rt></ruby>への<span class="target-word"><ruby>取<rt>と</rt></ruby>り<ruby>組<rt>く</rt></ruby>み</span>が'
        '<ruby>加速<rt>かそく</rt></ruby>している。<br>'
        '<span style="color:#6b7280;font-size:13px">※ [신문 기사·사설·독해 초빈출 1순위 ★★★] <b>〜への取り組み(~에 대한 대처/노력)</b>, <b>取り組みを強化する(대응·노력을 강화하다)</b>, <b>取り組みを進める(추진해 나가다)</b>, <b>積極的な取り組み(적극적인 대처)</b> / [동사 짝꿍 ★필수 조사] <b>〜に取り組む (~에 진지하게 달라붙다/몰두하다)</b>: 課題に取り組む(과제에 달라붙다), 問題の解決に取り組む(문제 해결에 힘쓰다) / [유의어 비교] <b>対策(たいさく, 대책/수단)</b>, <b>対応(たいおう, 응대/대처)</b>, <b>試み(こころみ, 시도)</b> / [스모 용어] <b>本日の取組(ほんじつのとりくみ, 오늘의 대진/시합)</b></span></div>'
        '<div class="example-ko"><span class="translation-label">해석</span>'
        '<span class="translation-text">지구 온난화를 막기 위해, 기업과 지자체에 의한 탈탄소 대처(取り組み, 실천 노력)가 가속화되고 있다. (★신문 기사·사설 단골 1순위 명사 \'〜への取り組み\', 동사 \'〜に取り組む(~에 진지하게 매달리다)\')</span></div>'
    ),
    "mp3": "",
    "hanja_mnemonic": (
        '<div class="visual-scan-item">\n'
        '  <div class="visual-scan-header">\n'
        '    <span class="visual-scan-badge">取 (가질/잡을 취: と・る) + 組 (짤/맞붙을 조: く・む)</span>\n'
        '  </div>\n'
        '  <div class="visual-scan-desc">\n'
        '    상대방의 샅바나 옷깃을 쥐고(取) 정면으로 맞붙는(組) 스모 동작에서 유래 ➔ 과제나 난제에 정면으로 맞서 힘을 쏟는 일 ➔ 대처, 노력, 추진 방안(取り組み) / 동사: 取り組む(~에 매달리다, 몰두하다)\n'
        '  </div>\n'
        '</div>\n'
        '<div class="mnemonic-item">\n'
        '  <span class="mnemonic-char">【取り組み (とりくみ)】 대처, 노력 / 【取り組む】 몰두하다, 힘쓰다</span>\n'
        '  <span class="mnemonic-parts">★조사 결합: 〜への取り組み(명사) vs 〜に取り組む(동사) / 기사 단골: 取り組みを強化する(노력을 강화하다)</span>\n'
        '</div>'
    ),
    "tags": ["독해_어휘", "기사_어휘", "모의고사_어휘", "명사", "동사", "JLPT_N2"]
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

# 1. Add Note
res = call_mcp('add_note', {
    'deck_name': DECK_NAME,
    'model_name': MODEL_NAME,
    'fields': fields,
    'tags': card["tags"],
    'allow_duplicate': True
})
print("add_note response:", res)

# Retrieve note ID from response
nid = None
if 'structuredContent' in res and 'noteId' in res['structuredContent']:
    nid = res['structuredContent']['noteId']
elif 'content' in res:
    try:
        text_data = json.loads(res['content'][0]['text'])
        nid = text_data.get('noteId') or text_data.get('note_id')
    except Exception:
        pass

if not nid:
    # Find note by id field
    find_res = call_mcp('find_notes', {'query': f'deck:"{DECK_NAME}" id:"{card["id"]}"'})
    note_ids = find_res.get('structuredContent', {}).get('noteIds', [])
    if note_ids:
        nid = note_ids[0]

print(f"Created Note ID: {nid}")

if nid:
    info_res = call_mcp('notes_info', {'notes': [nid]})
    cards = info_res['structuredContent']['notes'][0]['cards']
    print(f"Associated Card IDs: {cards}")
    # Make card due today for immediate review
    due_res = call_mcp('card_set_due_date', {
        'card_ids': cards,
        'days': '0!'
    })
    print(f"Set card due today response: {due_res}")

call_mcp('sync')
print("Anki sync completed successfully!")
