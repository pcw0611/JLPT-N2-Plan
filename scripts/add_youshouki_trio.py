# -*- coding: utf-8 -*-
"""
Add '幼少期', '人見知り', '激しい' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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

cards = [
    {
        "id": "READING-NEWS-0080",
        "kanji": "幼少期（幼い）",
        "kana": "ようしょうき（おさない）",
        "meaning": "유년기, 어린 시절 (명사: 나이가 매우 어렸을 때의 시기 / 수필·인터뷰 독해 단골)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>幼少<rt>ようしょう</rt></ruby><ruby>期<rt>き</rt></ruby></span>は'
            '<ruby>人見知<rt>ひとみし</rt></ruby>りが<ruby>激<rt>はげ</rt></ruby>しく、'
            '<ruby>知<rt>し</rt></ruby>らない<ruby>人<rt>ひと</rt></ruby>の<ruby>前<rt>まえ</rt></ruby>ではうまく'
            '<ruby>話<rt>はな</rt></ruby>せなかった。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★ 자서전·수필 단골] <b>幼少期を過ごす(유년기를 보내다)</b>, <b>幼少期の思い出 / 体験(유년기의 추억/체험)</b>, 幼少期の記憶(유년기의 기억) / [유의어] 幼少時代(ようしょうじだい), 子供の頃(こどものころ) / [한자 幼의 훈독 형용사] <b>幼い(おさない, 어리다/미숙하다)</b> ➔ 幼い子ども(어린아이), 考えが幼い(생각이 어리숙하다) / 음독: 幼児(ようじ, 유아), 幼稚園(ようちえん)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">유년기(幼少期)에는 낯가림이 심해서, 모르는 사람 앞에서는 제대로 말을 하지 못했다. (★인물 수필·인터뷰 지문 1순위: 幼少期を過ごす/유년기를 보내다, 훈독 형용사 \'幼い おさない/어리다\')</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">幼 (어릴 유) + 少 (적을/젊을 소) + 期 (기약할 기)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    실(幺)처럼 작고 힘(力)이 약하며, 나이가 적은(少) 인생의 초기(期) ➔ 유년기(幼少期)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【幼少期 (ようしょうき)】 유년기</span>\n'
            '  <span class="mnemonic-parts">★음독: 幼(よう) + 少(しょう) + 期(き) ➔ ようしょうき / 훈독 형용사: 幼い(おさない, 어리다)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "인물_수필", "명사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0081",
        "kanji": "人見知り",
        "kana": "ひとみしり",
        "meaning": "낯가림, 낯을 가림 (명사 / する동사: 낯선 사람을 부끄러워하고 대하기 꺼림)",
        "sentences": (
            '<div class="example-ja"><ruby>彼<rt>かれ</rt></ruby>は<span class="target-word"><ruby>人見知<rt>ひとみし</rt></ruby>りをする</span>性格だが、'
            '<ruby>打<rt>う</rt></ruby>ち<ruby>解<rt>と</rt></ruby>けるととても<ruby>明<rt>あか</rt></ruby>るくよく<ruby>話<rt>はな</rt></ruby>す。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★ 청해·성격 묘사 단골] <b>人見知りをする(낯을 가리다)</b>, <b>人見知りが激しい(낯가림이 심하다)</b>, <b>人見知りを克服する(낯가림을 극복하다)</b>, 人見知りが直る(낯가림이 고쳐지다) / [짝꿍 동사] 打ち解ける(うちとける, 마음을 터놓고 친해지다 ➔ N2 빈출!) / 관련 표현: 内気(うちき, 내성적임), 照れ屋(てれや, 수줍음을 많이 타는 사람)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">그는 낯을 가리는(人見知りをする) 성격이지만, 마음을 터놓으면(打ち解けると) 매우 밝고 말을 잘한다. (★청해·성격 묘사 1순위: 人見知りをする/낯을 가리다, 人見知りが激しい/낯가림이 심하다, 打ち解ける/마음을 터놓다)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">人 (사람 인) + 見知り (보고 앎)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    사람(人)을 보고(見) 아는 사람인지 모르는 낯선 사람인지 따져서 부끄러워함 ➔ 낯가림(人見知り)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【人見知り (ひとみしり)】 낯가림</span>\n'
            '  <span class="mnemonic-parts">★훈독 구성: ひと + みしり / 초빈출 연어: 人見知りをする(낯을 가리다), 人見知りが激しい(낯가림이 심하다)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "청해_어휘", "성격_심리", "명사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0082",
        "kanji": "激しい",
        "kana": "はげしい",
        "meaning": "격렬하다, 심하다, 세차다 (い형용사: 세기·기세·감정·변화·경쟁 등이 맹렬하고 심함)",
        "sentences": (
            '<div class="example-ja"><ruby>市場<rt>しじょう</rt></ruby>での<ruby>競争<rt>きょうそう</rt></ruby>が<span class="target-word"><ruby>激<rt>はげ</rt></ruby>しくなる</span>につれて、'
            '<ruby>企業<rt>きぎょう</rt></ruby>には<ruby>迅速<rt>じんそく</rt></ruby>な<ruby>決断<rt>けつだん</rt></ruby>が<ruby>求<rt>もと</rt></ruby>められる。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★ N2 독해·문맥규정 1순위] <b>人見知りが激しい(낯가림이 심하다)</b>, <b>競争が激しい(경쟁이 치열하다)</b>, <b>雨・風が激しい(비바람이 거세다)</b>, 寒暖の差が激しい(일교차가 심하다), 感情の起伏が激しい(감정 기복이 심하다), 激しく変化する(격렬하게 변화하다) / [한자 激의 음독 げき] 激増(げきぞう, 격증), 激減(げきげん, 격감), 刺激(しげき, 자극), 感激(かんげき, 감격)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">시장에서의 경쟁이 치열해짐(激しくなる)에 따라, 기업에는 신속한 결단이 요구된다. (★시험 1순위 연어: 人見知りが激しい/낯가림이 심하다, 競争が激しい/경쟁이 치열하다, 寒暖の差が激しい/기온차가 심하다)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n  <div class="visual-scan-header">\n    <span class="visual-scan-badge">激 (격할 격)</span>\n  </div>\n  <div class="visual-scan-desc">\n    물(氵)길이 거센 바위에 세차게 부딪치며(敫) 하얗게 물보라를 일으키는 모습 ➔ 격렬하다, 심하다(激しい はげしい)\n  </div>\n</div>\n<div class="mnemonic-item">\n  <span class="mnemonic-char">【激しい (はげしい)】 격렬하다, 심하다, 세차다</span>\n  <span class="mnemonic-parts">★훈독: はげしい / 음독: げき(激増・激減・刺激・感激) / 연어: 競争が激しい(경쟁이 치열하다)</span>\n</div>'
        ),
        "tags": ["독해_어휘", "형용사", "상태_묘사", "JLPT_N2"]
    }
]

for card in cards:
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
