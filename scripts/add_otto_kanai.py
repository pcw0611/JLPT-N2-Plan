# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT 한끝 Voca::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"

def call_mcp(name, arguments={}):
    req = urllib.request.Request(
        'http://127.0.0.1:3141/',
        data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': {'name': name, 'arguments': arguments}}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith('data: '):
            return json.loads(line[6:])['result']
    return None

cards_to_add = [
    {
        "id": "READING-NEWS-0012",
        "kanji": "夫",
        "kana": "おっと",
        "meaning": "남편 (자신의 남편을 객관적/공식적으로 지칭, 품사: 명사)",
        "sentences": (
            '<div class="example-ja"><ruby>共働<rt>ともばたら</rt></ruby>きの<ruby>家庭<rt>かてい</rt></ruby>が'
            '<ruby>増<rt>ふ</rt></ruby>え、'
            '<span class="target-word"><ruby>夫<rt>おっと</rt></ruby></span>も'
            '<ruby>家事<rt>かじ</rt></ruby>や<ruby>育児<rt>いくじ</rt></ruby>を<ruby>分担<rt>ぶんたん</rt></ruby>することが'
            '<ruby>当<rt>あ</rt></ruby>たり<ruby>前<rt>まえ</rt></ruby>になりつつある。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [호칭 구별] 자신의 남편: 夫(おっと)・主人(しゅじん) ／ 상대 남편: ご主人(ごしゅじん)・旦那様(だんなさま). 짝이 되는 단어: 妻(つま)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">맞벌이 가정이 늘어나며 남편도 가사와 육아를 분담하는 것이 당연해지고 있다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">夫(사내/지아비 부, 훈: おっと)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    성인이 되어 상투를 튼 성인 남성 ➔ 지아비, 남편. 짝이 되는 단어: 妻(つま)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【夫】 지아비 부 (훈독: おっと)</span>\n'
            '  <span class="mnemonic-parts">자신의 남편을 객관적·공식적으로 지칭. (남의 남편에게 쓰지 않음!)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "가족_호칭", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0013",
        "kanji": "家内",
        "kana": "かない",
        "meaning": "아내, 집사람 (자신의 아내를 정중/겸양하게 지칭, 품사: 명사)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>家内<rt>かない</rt></ruby></span>と'
            '<ruby>相談<rt>そうだん</rt></ruby>した<ruby>上<rt>うえ</rt></ruby>で、'
            '<ruby>改<rt>あらた</rt></ruby>めてお<ruby>返事<rt>へんじ</rt></ruby>させていただきます。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [호칭 구별] 자신의 아내: 妻(つま)・家内(かない) ／ 상대 아내: 奥様(おくさま)・奥さん(おくさん). 남의 아내에게 家内 사용 절대 금지!</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">집사람(아내)과 상의한 후에 다시 답변드리겠습니다. (남의 아내에게는 奥様 사용)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">家(집 가) + 内(안 내)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    집 안(家内) 사람 ➔ 자신의 아내를 낮추어 부르는 겸양 표현 ("저희 집사람")\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【家内】 かない</span>\n'
            '  <span class="mnemonic-parts">자신의 아내를 정중히 부르는 표현. (남의 아내에겐 奥様/奥さん)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "가족_호칭", "JLPT_N2"]
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
    print(f"Added note for [{card['kanji']}]:", res.get('structuredContent', {}).get('message') or res.get('content'))

call_mcp('sync')
print("Anki sync triggered!")
