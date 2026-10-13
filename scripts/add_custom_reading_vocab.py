# -*- coding: utf-8 -*-
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
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode('utf-8')
    for line in body.splitlines():
        if line.startswith('data: '):
            return json.loads(line[6:])['result']
    return None

cards_to_add = [
    {
        "id": "READING-NEWS-0001",
        "kanji": "駆け足",
        "kana": "かけあし",
        "meaning": "빠른 걸음, 속보, 달음박질; (일의 진행이) 급속함, 서두름",
        "sentences": (
            '<div class="example-ja"><ruby>午前<rt>ごぜん</rt></ruby><ruby>中<rt>ちゅう</rt></ruby>に'
            '<ruby>市内<rt>しない</rt></ruby>의 <ruby>名所<rt>めいしょ</rt></ruby>を'
            '<span class="target-word"><ruby>駆<rt>か</rt></ruby>け<ruby>足<rt>あし</rt></ruby></span>で'
            '<ruby>巡<rt>めぐ</rt></ruby>った。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 準備期間が短く、新企画は駆け足で進められた。</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">오전 중에 시내의 명소를 빠른 걸음으로 둘러보았다. (준비 기간이 짧아 새 기획은 서둘러 급하게 진행되었다.)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">駆(몰/달릴 구) + 足(발 족)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    말을 몰듯(駆) 발(足)을 바쁘게 놀려 빠르게 내달리는 모습\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【駆】 몰 구</span>\n'
            '  <span class="mnemonic-parts">말(馬)을 몰아 구역(区)을 내달림</span>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【足】 발 족</span>\n'
            '  <span class="mnemonic-parts">사람의 다리와 발 모양</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "모의고사_어휘", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0002",
        "kanji": "巡り",
        "kana": "めぐり",
        "meaning": "둘레, 주변; 순회, 돌아봄; (인연·운명의) 돌고 돎, 순환; ~을 둘러쌈 (〜を巡り)",
        "sentences": (
            '<div class="example-ja"><ruby>政策<rt>せいさく</rt></ruby>の<ruby>方針<rt>ほうしん</rt></ruby>を'
            '<span class="target-word"><ruby>巡<rt>めぐ</rt></ruby>り</span>、'
            '<ruby>激<rt>はげ</rt></ruby>しい<ruby>議論<rt>ぎろん</rt></ruby>が<ruby>交<rt>か</rt></ruby>わされた。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 季節の巡りを感じながら、古い寺や街を散策した。</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">정책 방침을 둘러싸고 격렬한 논의가 오갔다. (계절의 순환/돌고 돎을 느끼며 오래된 사찰과 거리를 산책했다.)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">巡(돌 순)의 명사형</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    물길(巛)처럼 굽이진 길을 걸어가며(辶) 주변을 순회하고 돎\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【巡】 돌 순</span>\n'
            '  <span class="mnemonic-parts">쉬엄쉬엄 갈 착(辶) + 내 천(巛 물길의 굽이): 주변을 순회함</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "모의고사_어휘", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0003",
        "kanji": "妻",
        "kana": "つま",
        "meaning": "아내, 처 (자신의 아내를 객관적/겸양으로 지칭)",
        "sentences": (
            '<div class="example-ja"><ruby>彼<rt>かれ</rt></ruby>は'
            '<span class="target-word"><ruby>妻<rt>つま</rt></ruby></span>と'
            '<ruby>共<rt>とも</rt></ruby>に<ruby>長年<rt>ながねん</rt></ruby>の<ruby>夢<rt>ゆめ</rt></ruby>だった'
            'カフェを<ruby>開<rt>ひら</rt></ruby>いた。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [구별 필수] 자신의 아내: 妻(つま)・家内(かない) ／ 남의 아내: 奥様(おくさま)・奥さん</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">그는 아내와 함께 오랜 꿈이었던 카페를 열었다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">妻(아내 처)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    자신의 배필인 아내. 남의 아내인 奥様(おくさま)와 호칭 구별 필수!\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【妻】 아내 처</span>\n'
            '  <span class="mnemonic-parts">머리장식을 한 여인(女)의 머리를 손으로 빗겨주며 맞이한 정식 배필</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "모의고사_어휘", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0004",
        "kanji": "善良",
        "kana": "ぜんりょう",
        "meaning": "선량함 (품사: な형용사 / 善良な市民 선량한 시민)",
        "sentences": (
            '<div class="example-ja"><ruby>犯罪<rt>はんざい</rt></ruby>から'
            '<span class="target-word"><ruby>善良<rt>ぜんりょう</rt></ruby></span>な'
            '<ruby>市民<rt>しみん</rt></ruby>を<ruby>守<rt>まも</rt></ruby>るため、'
            '<ruby>警察<rt>けいさつ</rt></ruby>は<ruby>警戒<rt>けいかい</rt></ruby>を'
            '<ruby>強<rt>つよ</rt></ruby>めている。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 彼は誰から見ても善良な人物で、人を騙すようなことは決してしない。</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">범죄로부터 선량한 시민을 지키기 위해 경찰은 경계를 강화하고 있다. (그는 누가 보아도 선량한 인물로, 남을 속이는 것 같은 일은 결코 하지 않는다.)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">善(착할 선) + 良(어질 량)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    선량한 시민(善良な市民)처럼 성품이 어질고 남에게 해를 끼치지 않는 온순함\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【善】 착할 선</span>\n'
            '  <span class="mnemonic-parts">양(羊)처럼 온순하고 언행(言)이 바르고 착함</span>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【良】 어질 량</span>\n'
            '  <span class="mnemonic-parts">잘 여문 좋은 곡식 낟알처럼 성품이 맑고 순수함</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "모의고사_어휘", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0005",
        "kanji": "平等",
        "kana": "びょうどう",
        "meaning": "평등 (품사: 명사 / な형용사, 차별 없이 고르고 한결같음)",
        "sentences": (
            '<div class="example-ja"><ruby>性別<rt>せいべつ</rt></ruby>や'
            '<ruby>国籍<rt>こくせき</rt></ruby>に<ruby>関係<rt>かんけい</rt></ruby>なく、'
            'すべての<ruby>人<rt>ひと</rt></ruby>に'
            '<span class="target-word"><ruby>平等<rt>びょうどう</rt></ruby></span>な'
            '<ruby>機会<rt>きかい</rt></ruby>が<ruby>与<rt>あた</rt></ruby>えられるべきだ。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [시험 신호] 平의 특수 음독: へいとう(X) ➔ びょうどう(O)! 法の下の平等(법 앞의 평등)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">성별이나 국적에 관계없이 모든 사람에게 평등한 기회가 주어져야 한다. (법 앞에서의 평등은 민주주의의 기본 원칙이다.)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">平(평평할 평/びょう) + 等(같을 등)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    차별 없이 평평하고(平) 동등하게(等) 대우함. ★음독 びょう 주의!\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【平】 평평할 평 (음독: びょう / へい)</span>\n'
            '  <span class="mnemonic-parts">수면이 잔잔하고 평평하게 고름 (平等: びょうどう)</span>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【等】 같을 등</span>\n'
            '  <span class="mnemonic-parts">대나무(竹) 마디를 관청(寺)의 규격대로 고르게 맞춤</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "모의고사_어휘", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0006",
        "kanji": "絶えず",
        "kana": "たえず",
        "meaning": "끊임없이, 끊이지 않고, 늘, 항상 (품사: 부사)",
        "sentences": (
            '<div class="example-ja"><ruby>現代<rt>げんだい</rt></ruby><ruby>社会<rt>しゃかい</rt></ruby>は'
            '<span class="target-word"><ruby>絶<rt>た</rt></ruby>えず</span>'
            '<ruby>変化<rt>へんか</rt></ruby>しており、'
            '<ruby>新<rt>あたら</rt></ruby>しい<ruby>技術<rt>ぎじゅつ</rt></ruby>への'
            '<ruby>適応<rt>てきおう</rt></ruby>が<ruby>求<rt>もと</rt></ruby>められる。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [동사/유사어] 絶える(끊어지다), 笑顔が絶えない(웃음이 끊이지 않다). 유의어: 常に, 絶え間なく</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">현대 사회는 끊임없이 변화하고 있으며, 새로운 기술에의 적응이 요구된다. (웃음소리가 끊이지 않는다.)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">絶(끊을 절) + 부정(〜ず)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    이어짐이 중간에 끊어지지(絶え) 않고(ず) 계속 이어짐 ➔ 끊임없이\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【絶】 끊을 절</span>\n'
            '  <span class="mnemonic-parts">실(糸)을 칼(刀)로 끊듯이 자름 (絶える: 끊어지다)</span>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【ず】 부정 조동사 ぬ의 연용형</span>\n'
            '  <span class="mnemonic-parts">~하지 않고, ~없이 (絶えず = 끊김 없이)</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "모의고사_어휘", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0007",
        "kanji": "対抗",
        "kana": "たいこう",
        "meaning": "대항, 맞섬, 경쟁 (품사: 명사 / スる동사)",
        "sentences": (
            '<div class="example-ja"><ruby>他社<rt>たしゃ</rt></ruby>의 '
            '<ruby>新<rt>しん</rt></ruby>サービスに'
            '<span class="target-word"><ruby>対抗<rt>たいこう</rt></ruby></span>するため、'
            '<ruby>大幅<rt>おおはば</rt></ruby>な<ruby>価格<rt>かかく</rt></ruby><ruby>引<rt>ひ</rt></ruby>き<ruby>下<rt>さ</rt></ruby>げを'
            '<ruby>決定<rt>けってい</rt></ruby>した。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [빈출 관용구] 対抗意識(たいこういしき, 대항의식/경쟁심), 対抗策(たいこうさく, 대항책)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">타사의 신규 서비스에 대항하기 위해 대폭적인 가격 인하를 결정했다. (대항의식을 불태우다)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">対(대할 대) + 抗(겨룰/막을 항)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    서로 마주 보고(対) 손을 들어 맞서 겨룸(抗) ➔ 대항, 경쟁\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【対】 대할 대</span>\n'
            '  <span class="mnemonic-parts">서로 마주 보며 맞대응함</span>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【抗】 막을/겨룰 항</span>\n'
            '  <span class="mnemonic-parts">손(扌)을 높이 들어(亢) 굽히지 않고 맞서 겨룸</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "모의고사_어휘", "JLPT_N2"]
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
    print(f"Added note for [{card['kanji']}]:", res.get('structuredContent') or res.get('content'))

print("All 7 cards added successfully!")
