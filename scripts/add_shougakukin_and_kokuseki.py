# -*- coding: utf-8 -*-
"""
Add '奨学金' and '国籍' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
        "id": "READING-NEWS-0063",
        "kanji": "奨学金",
        "kana": "しょうがくきん",
        "meaning": "장학금 (명사: 학생에게 지급되는 학비·생활비 보조금 / N2 청해·독해 대학생활 단골 어휘)",
        "sentences": (
            '<div class="example-ja"><ruby>成績<rt>せいせき</rt></ruby><ruby>優秀<rt>ゆうしゅう</rt></ruby>者として'
            '<span class="target-word"><ruby>奨学金<rt>しょうがくきん</rt></ruby>を</span>'
            '<ruby>受<rt>う</rt></ruby>けることができ、'
            '<ruby>学費<rt>がくひ</rt></ruby>の<ruby>負担<rt>ふたん</rt></ruby>が'
            '<ruby>軽<rt>かる</rt></ruby>くなった。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★ 대학·청년 생활 단골] <b>奨学金を受ける / 支給される(장학금을 받다/지급받다)</b>, <b>奨学金を申請する / 申し込む(장학금을 신청하다)</b>, <b>奨学金を返還する(장학금을 상환하다)</b> / [장학금 유형] 給付型(きゅうふがた, 무상 지급형) ↔ 貸与型(たいよがた, 대여·상환형) / [관련 필수어] 授業料免除(수업료 면제), <b>仕送り(しおくり, 본가에서 보내주는 생활비/용돈 송금 ➔ N2 초빈출!)</b> / 한자 奨의 음독: 奨励(しょうれい, 장려), 推奨(すいしょう, 추천/권장)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">성적 우수자로서 장학금(奨学金)을 받을 수 있게 되어, 학비 부담이 가벼워졌다. (★N2 청해·독해 대학생활 지문 1순위 어휘: 奨学金を申請する/신청하다, 奨学金を返還する/상환하다, 仕送り/송금)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">奨 (권장할 장) + 学 (배울 학) + 金 (쇠/돈 금)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    학업(学)에 힘쓰도록 북돋우고 장려(奨)하기 위해 지급하는 돈(金) ➔ 장학금(奨学金)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【奨学金 (しょうがくきん)】 장학금</span>\n'
            '  <span class="mnemonic-parts">★음독: 奨(しょう: 奨学金・奨励・推奨) + 学(がく) + 金(きん) ➔ しょうがくきん / 관련어: 奨学生(장학생), 仕送り(생활비 송금)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "청해_어휘", "학교_생활", "명사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0064",
        "kanji": "国籍",
        "kana": "こくせき",
        "meaning": "국적 (명사: 어떤 국가의 국민으로서의 신분·자격 / N2 문형 [〜を問わず] 1순위 연어)",
        "sentences": (
            '<div class="example-ja">この<ruby>企業<rt>きぎょう</rt></ruby>では'
            '<span class="target-word"><ruby>国籍<rt>こくせき</rt></ruby>を<ruby>問<rt>と</rt></ruby>わず</span>、'
            '<ruby>優秀<rt>ゆうしゅう</rt></ruby>な<ruby>人材<rt>じんざい</rt></ruby>を'
            '<ruby>積極<rt>せっきょく</rt></ruby><ruby>的<rt>てき</rt></ruby>に'
            '<ruby>採用<rt>さいよう</rt></ruby>している。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 문법 짝꿍 ★★★ N2 1순위] <b>国籍を問わず / 国籍にかかわらず(국적을 불문하고 / 국적에 상관없이)</b> / [초빈출 연어] 国籍を取得する(국적을 취득하다), 国籍を離脱する(국적을 이탈하다), 二重国籍(이중국적), 外国籍(외국 국적), 日本国籍(일본 국적) / [한자 籍(서적/호적 적) 관련 필수어] <b>戸籍(こせき, 호적)</b>, <b>在籍(ざいせき, 재적/소속되어 있음)</b>, 書籍(しょせき, 서적), 本籍(ほんせき, 본적)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">이 기업에서는 국적을 불문하고(国籍を問わず), 우수한 인재를 적극적으로 채용하고 있다. (★N2 핵심 문형 \'〜を問わず(불문하고)\', \'〜にかかわらず(상관없이)\'와 항상 짝꿍으로 출제되는 1순위 단어입니다!)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">国 (나라 국) + 籍 (문서/호적 적)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    특정 나라(国)의 장부(竹 + 耤 = 籍)에 정식 국민으로 등록되어 있는 신분 ➔ 국적(国籍)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【国籍 (こくせき)】 국적</span>\n'
            '  <span class="mnemonic-parts">★음독: 国(こく) + 籍(せき: 国籍・戸籍・在籍・書籍) ➔ こくせき / N2 문형 짝꿍: 国籍を問わず(국적을 불문하고)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "문법연계", "사회_국제", "명사", "JLPT_N2"]
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
