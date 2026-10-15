# -*- coding: utf-8 -*-
"""
Add '方法', '予算', '提案' to Anki deck 'JLPT N2::14 독해・기사・모의고사 어휘'
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
        "id": "READING-NEWS-0071",
        "kanji": "方法",
        "kana": "ほうほう",
        "meaning": "방법 (명사: 목적을 달성하기 위한 구체적 방식과 절차 / 유의어 비교: 方法 vs 手段)",
        "sentences": (
            '<div class="example-ja"><ruby>問題<rt>もんだい</rt></ruby>を'
            '<ruby>根本<rt>こんぽん</rt></ruby><ruby>的<rt>てき</rt></ruby>に<ruby>解決<rt>かいけつ</rt></ruby>するための'
            '<span class="target-word"><ruby>有効<rt>ゆうこう</rt></ruby>な<ruby>方法<rt>ほうほう</rt></ruby></span>を'
            '<ruby>模索<rt>もさく</rt></ruby>している。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★] <b>解決方法(해결 방법)</b>, <b>有効な方法(유효한 방법)</b>, 対処方法(대처 방법), <b>〜という方法をとる(~라는 방법을 취하다)</b>, 方法を見出す(방법을 찾아내다) / [유의어 뉘앙스 비교] <b>方法(ほうほう, 목적에 도달하는 구체적 절차·방식)</b> vs <b>手段(しゅだん, 목적을 위해 이용하는 도구·수단 ➔ 手段を選ばない: 수단을 가리지 않다)</b> / [한자 독음] 方(ほう) + 法(ほう: 方法・文法・法律) ➔ ほうほう</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">문제를 근본적으로 해결하기 위한 유효한 방법(有効な方法)을 모색하고 있다. (★시험 빈출: 有効な方法/유효한 방법, 〜という方法をとる/~라는 방법을 취하다 / 유의어 비교: 手段(수단) ➔ 手段を選ばない/수단을 가리지 않다)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">方 (모/방법 방) + 法 (법/도리 법)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    올바른 방향(方)을 향해 물(氵)이 흘러가듯(去) 순리에 맞게 따르는 법칙(法) ➔ 방법(方法)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【方法 (ほうほう)】 방법</span>\n'
            '  <span class="mnemonic-parts">★음독: 方(ほう) + 法(ほう: 方法・文法 ぶんぽう) ➔ ほうほう / 유의어: 手段(しゅだん)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기초_어휘", "명사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0072",
        "kanji": "予算",
        "kana": "よさん",
        "meaning": "예산 (명사: 미리 필요한 비용을 계산함, 또는 그 비용 / 초빈출 연어: 予算を組む, 予算を削る)",
        "sentences": (
            '<div class="example-ja"><ruby>新規<rt>しんき</rt></ruby>事業の'
            '<span class="target-word"><ruby>予算<rt>よさん</rt></ruby>を<ruby>組<rt>く</rt></ruby>み</span>、'
            '<ruby>限<rt>かぎ</rt></ruby>られた<ruby>費用<rt>ひよう</rt></ruby>で'
            '<ruby>最大<rt>さいだい</rt></ruby>の<ruby>成果<rt>せいか</rt></ruby>を'
            '<ruby>出<rt>だ</rt></ruby>せるよう<ruby>計画<rt>けいかく</rt></ruby>した。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★ 비즈니스·뉴스 단골] <b>予算を組む(예산을 짜다/편성하다)</b>, <b>予算を立てる(예산을 세우다)</b>, <b>予算を削る / 削減する(예산을 깎다/삭감하다)</b>, 予算をオーバーする(예산을 초과하다), 予算内におさめる(예산 내로 맞추다), 予算案(よさんあん, 예산안) / 한자 독음: 予(よ: 予定・予選・予測) + 算(さん: 計算・採算 さいさん)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">신규 사업의 예산을 짜고(予算を組み), 한정된 비용으로 최대의 성과를 낼 수 있도록 계획했다. (★비즈니스·뉴스 시험 1순위: 予算を組む/예산을 짜다, 予算を削る/예산을 깎다, 予算をオーバーする/초과하다)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">予 (미리 예) + 算 (셈할 산)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    사업이나 생활을 시작하기에 앞서 미리(予) 필요한 돈을 주판(竹 + 目 + 廾 = 算)으로 셈해 놓은 것 ➔ 예산(予算)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【予算 (よさん)】 예산</span>\n'
            '  <span class="mnemonic-parts">★음독: 予(よ: 予算・予定・予選) + 算(さん: 予算・計算・決算) ➔ よさん / 필수 연어: 予算を組む(예산을 짜다)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "비즈니스_경제", "명사", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0073",
        "kanji": "提案",
        "kana": "ていあん",
        "meaning": "제안 (명사 / する동사: 의안·의견·아이디어를 내놓아 제시함 / 비즈니스·청해 1순위)",
        "sentences": (
            '<div class="example-ja"><ruby>会議<rt>かいぎ</rt></ruby>で<ruby>業務<rt>ぎょうむ</rt></ruby><ruby>効率<rt>こうりつ</rt></ruby><ruby>化<rt>か</rt></ruby>のための'
            '<span class="target-word"><ruby>改善<rt>かいぜん</rt></ruby><ruby>策<rt>さく</rt></ruby>を<ruby>提案<rt>ていあん</rt></ruby>し</span>、'
            '<ruby>満場一致<rt>まんじょういっち</rt></ruby>で<ruby>採用<rt>さいよう</rt></ruby>された。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [초빈출 연어 ★★★ 비즈니스·청해 단골] <b>提案を受け入れる(제안을 수용하다/받아들이다)</b> ↔ <b>提案を断る / 却下する(ていあんをきゃっかする, 제안을 거절/각하하다)</b>, <b>提案を採用する(제안을 채택하다)</b>, 改善策を提案する(개선책을 제안하다), 魅力的な提案(매력적인 제안) / [한자 案 관련 필수어] <b>案の定(あんのじょう, 생각대로/아니나 다를까 ➔ N2 부사 초빈출!)</b>, 名案(めいあん, 좋은 생각/명안) / 한자 提: 提携(ていけい, 제휴), 提示(ていじ, 제시)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">회의에서 업무 효율화를 위한 개선책을 제안하여(提案し), 만장일치로 채택되었다. (★비즈니스·청해 1순위: 提案を受け入れる/받아들이다, 提案を採用する/채택하다, 提案を却下する/기각하다 / 부사 \'案の定(아니나 다를까)\'도 필수!)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n  <div class="visual-scan-header">\n    <span class="visual-scan-badge">提 (끌어낼/들 제) + 案 (생각/방안 안)</span>\n  </div>\n  <div class="visual-scan-desc">\n    손(扌)으로 내 마음속의 좋은 생각·방안(案)을 테이블 위에 들어올려(提) 내놓는 모습 ➔ 제안(提案)\n  </div>\n</div>\n<div class="mnemonic-item">\n  <span class="mnemonic-char">【提案 (ていあん)】 제안</span>\n  <span class="mnemonic-parts">★음독: 提(てい: 提案・提出・提携・提示) + 案(あん: 提案・案内・案の定・名案) ➔ ていあん / 관련어: 案の定(아니나 다를까)</span>\n</div>'
        ),
        "tags": ["독해_어휘", "청해_어휘", "비즈니스_회의", "명사", "JLPT_N2"]
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
