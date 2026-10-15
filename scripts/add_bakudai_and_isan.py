# -*- coding: utf-8 -*-
"""
Add '莫大' and '遺産' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
        "id": "READING-NEWS-0069",
        "kanji": "莫大",
        "kana": "ばくだい",
        "meaning": "막대함 (な형용사 / 명사: 수량·금액·비용·손해 등이 엄청나게 크고 많음)",
        "sentences": (
            '<div class="example-ja"><ruby>新<rt>しん</rt></ruby>しい<ruby>技術<rt>ぎじゅつ</rt></ruby>の<ruby>開発<rt>かいはつ</rt></ruby>には、'
            '<span class="target-word"><ruby>莫大<rt>ばくだい</rt></ruby>な<ruby>費用<rt>ひよう</rt></ruby></span>と'
            '<ruby>年月<rt>ねんげつ</rt></ruby>が<ruby>掛<rt>か</rt></ruby>かる。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★] <b>莫大な遺産(막대한 유산)</b>, <b>莫大な費用 / 莫大なコスト(막대한 비용)</b>, <b>莫大な損害 / 被害(막대한 손해/피해)</b>, 莫大な借金(막대한 빚), 莫大な時間(막대한 시간) / [유의어 뉘앙스 비교] <b>莫大(ばくだい, 금액·비용·손해의 막대함)</b> vs <b>膨大(ぼうだい, 데이터·자료·지식 등의 방대함 ➔ 膨大なデータ)</b> vs 多額(たがく, 많은 금액) vs 巨大(きょだい, 물리적 크기)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">새로운 기술 개발에는 막대한 비용(莫大な費用)과 세월이 걸린다. (★초빈출 세트: 莫大な遺産/막대한 유산, 莫大な費用/막대한 비용, 莫大な損害/막대한 손해 ➔ 자료·데이터가 많은 것은 \'膨大 ぼうだい\')</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">莫 (없을/클 막) + 大 (큰 대)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    해(日)가 풀숲(艹, 大)에 가려 끝없이 넓고 아득하듯, 견줄 것 없이 엄청나게 큼 ➔ 막대함(莫大)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【莫大 (ばくだい)】 막대함</span>\n'
            '  <span class="mnemonic-parts">★음독: 莫(ばく: 莫大・漠然 ばくぜん) + 大(だい) ➔ ばくだい / 연어: 莫大な遺産(막대한 유산), 莫大な費用(막대한 비용)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "형용동사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0070",
        "kanji": "遺産",
        "kana": "いさん",
        "meaning": "유산 (명사: 1. 사망자가 남긴 재산 / 2. 인류와 사회가 물려받은 문화·자연적 가치)",
        "sentences": (
            '<div class="example-ja"><ruby>親<rt>おや</rt></ruby>が<ruby>残<rt>のこ</rt></ruby>した'
            '<span class="target-word"><ruby>莫大<rt>ばくだい</rt></ruby>な<ruby>遺産<rt>いさん</rt></ruby></span>を'
            '<ruby>巡<rt>めぐ</rt></ruby>り、<ruby>親族<rt>しんぞく</rt></ruby>の<ruby>間<rt>あいだ</rt></ruby>で'
            '<ruby>争<rt>あらそ</rt></ruby>いが<ruby>起<rt>お</rt></ruby>きた。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어·문형 연계 ★★★] <b>莫大な遺産(막대한 유산)</b>, <b>遺産を相続する(유산을 상속하다 ➔ 相続 そうぞく 빈출!)</b>, <b>遺産を巡る争い(유산을 둘러싼 다툼 ➔ 〜を巡る 문형 단골!)</b>, 遺産を残す(유산을 남기다) / [문화·역사 연어] <b>世界遺産(せかいいさん, 세계유산)</b>, 文化遺産(문화유산), 負の遺産(마이너스/부정적 유산) / [한자 遺의 음독] い(遺産・遺跡 いせき・遺族・遺憾 いかん) / 특이음독: 遺言(ゆいごん, 유언)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">부모가 남긴 막대한 유산(莫大な遺産)을 둘러싸고(巡り), 친족들 사이에서 다툼이 일어났다. (★N2 핵심 연어 & 문형: 莫大な遺産/막대한 유산, 遺産を相続する/상속하다, 遺産を巡る争い/유산을 둘러싼 다툼, 世界遺産/세계유산)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">遺 (남길 유) + 産 (재산/낳을 산)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    세상을 떠나며 귀한 재물(貴)을 길(辶) 뒤에 남겨(遺) 후대에 물려주는 재산(産) ➔ 유산(遺産)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【遺産 (いさん)】 유산</span>\n'
            '  <span class="mnemonic-parts">★음독: 遺(い: 遺産・遺跡・遺憾・遺族) + 産(さん: 財産・生産・破産) ➔ いさん / 예외음독: 遺言(ゆいごん)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "사회_문화", "명사", "JLPT_N2"]
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
