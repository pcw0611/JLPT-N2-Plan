# -*- coding: utf-8 -*-
"""
Add 24 tasting/sample cards across 4 categories:
1. N1/N2 upper abstract Hanzi words (6)
2. Real-life concrete nouns (8)
3. Essential compound verbs (5)
4. Contemporary spoken slang / colloquialisms (5)
Deck: 'JLPT N2::15 실생활・N1 고급어휘 맛보기'
"""

import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::15 실생활・N1 고급어휘 맛보기"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["맛보기_어휘", "실생활_일본어", "N1_고급한자어", "복합동사", "트렌드_슬랭"]

def call_mcp(name, arguments=None):
    if arguments is None:
        arguments = {}
    req = urllib.request.Request(
        'http://127.0.0.1:3141/',
        data=json.dumps({
            'jsonrpc': '2.0', 'id': 1,
            'method': 'tools/call',
            'params': {'name': name, 'arguments': arguments}
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        for line in resp.read().decode('utf-8').splitlines():
            if line.startswith('data: '):
                return json.loads(line[6:])['result']

# 1. Create deck
create_res = call_mcp('create_deck', {'deck_name': DECK_NAME})
print("Create deck:", json.dumps(create_res, ensure_ascii=False))

words_data = [
    # --- Category 1: N1 / N2 최상위 핵심 한자어 (뉴스/사설/비즈니스) ---
    {
        "id": "SAMPLE-N1-001",
        "kanji": "懸念",
        "kana": "けねん",
        "meaning": "우려, 걱정 (앞일에 대한 불안이나 염려)",
        "sentences": "<div class=\"example-ja\"><ruby>専門家<rt>せんもんか</rt></ruby>の<ruby>間<rt>あいだ</rt></ruby>では、<ruby>景気<rt>けいき</rt></ruby><ruby>後退<rt>こうたい</rt></ruby>への<span class=\"target-word\"><ruby>懸念<rt>けねん</rt></ruby></span>が<ruby>高<rt>たか</rt></ruby>まっている。<br><span style=\"color:#6b7280;font-size:13px\">※ 治安の悪化が懸念されている。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">전문가들 사이에서는 경기 후퇴에 대한 우려가 높아지고 있다. (치안의 악화가 우려되고 있다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">懸(매달릴 현) + 念(생각 념)</span></div><div class=\"visual-scan-desc\">마음속에 생각을 매달아 두고(懸) 끊임없이 걱정함(念) → 우려</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【懸】 매달릴 현</span><span class=\"mnemonic-parts\">마음(心)에 무거운 짐을 매달아 둠 (현안/현수막)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【念】 생각 념</span><span class=\"mnemonic-parts\">지금(今) 마음(心)에 품고 있는 생각</span></div>"
    },
    {
        "id": "SAMPLE-N1-002",
        "kanji": "示唆",
        "kana": "しさ",
        "meaning": "시사, 넌지시 암시함 (힌트를 주어 스스로 깨닫게 함)",
        "sentences": "<div class=\"example-ja\"><ruby>今回<rt>こんかい</rt></ruby>の<ruby>調査<rt>ちょうさ</rt></ruby><ruby>結果<rt>けっか</rt></ruby>は、<ruby>若者<rt>わかもの</rt></ruby>の<ruby>消費<rt>しょうひ</rt></ruby><ruby>傾向<rt>けいこう</rt></ruby>の<ruby>変化<rt>へんか</rt></ruby>を<span class=\"target-word\"><ruby>示唆<rt>しさ</rt></ruby></span>している。<br><span style=\"color:#6b7280;font-size:13px\">※ 彼の発言は、辞任の可能性を示唆するものだった。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">이번 조사 결과는 젊은 층의 소비 경향 변화를 시사하고 있다. (그의 발언은 사임 가능성을 시사하는 것이었다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">示(보일 시) + 唆(부추길/꾀일 사)</span></div><div class=\"visual-scan-desc\">가리켜 보여주며(示) 스스로 방향을 잡도록 유도함(唆) → 시사</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【示】 보일 시</span><span class=\"mnemonic-parts\">제단 위에 제물을 올려놓고 신에게 보임</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【唆】 부추길 사</span><span class=\"mnemonic-parts\">입(口)으로 말을 건네어 유도함 (교사/암시)</span></div>"
    },
    {
        "id": "SAMPLE-N1-003",
        "kanji": "迅速",
        "kana": "じんそく",
        "meaning": "신속, 매우 빠름 (지체 없이 민첩함)",
        "sentences": "<div class=\"example-ja\">トラブルが<ruby>発生<rt>はっせい</rt></ruby>した<ruby>際<rt>さい</rt></ruby>は、<span class=\"target-word\"><ruby>迅速<rt>じんそく</rt></ruby></span>な<ruby>対応<rt>たいおう</rt></ruby>が<ruby>求<rt>もと</rt></ruby>められる。<br><span style=\"color:#6b7280;font-size:13px\">※ 消防隊の迅速な消火活動により、被害を最小限に抑えた。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">문제가 발생했을 때는 신속한 대응이 요구된다. (소방대의 신속한 소화 활동 덕분에 피해를 최소한으로 억제했다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">迅(빠를 신) + 速(빠를 속)</span></div><div class=\"visual-scan-desc\">번개처럼(迅) 군더더기 없이 속도를 냄(速) → 신속</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【迅】 빠를 신</span><span class=\"mnemonic-parts\">길(辶)을 날쌔게 달려감</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【速】 빠를 속</span><span class=\"mnemonic-parts\">묶인 채 빠르게 달림 (속도/쾌속)</span></div>"
    },
    {
        "id": "SAMPLE-N1-004",
        "kanji": "把握",
        "kana": "はあく",
        "meaning": "파악, 확실히 이해함 (상황이나 핵심을 틀어쥠)",
        "sentences": "<div class=\"example-ja\">まずは<ruby>現状<rt>げんじょう</rt></ruby>の<ruby>問題点<rt>もんだいてん</rt></ruby>を<ruby>正確<rt>せいかく</rt></ruby>に<span class=\"target-word\"><ruby>把握<rt>はあく</rt></ruby></span>することが<ruby>重要<rt>じゅうよう</rt></ruby>だ。<br><span style=\"color:#6b7280;font-size:13px\">※ 全体のスケジュールを把握しておいてください。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">우선은 현상의 문제점을 정확하게 파악하는 것이 중요하다. (전체 일정을 파악해 두십시오.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">把(잡을 파) + 握(쥘 악)</span></div><div class=\"visual-scan-desc\">양손(扌)으로 사물의 핵심을 확실하게 틀어쥠 → 파악</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【把】 잡을 파</span><span class=\"mnemonic-parts\">손(扌)으로 단단히 잡음</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【握】 쥘 악</span><span class=\"mnemonic-parts\">손(扌)에 힘을 주어 쥠 (악수/장악)</span></div>"
    },
    {
        "id": "SAMPLE-N1-005",
        "kanji": "妥協",
        "kana": "だきょう",
        "meaning": "타협, 양보하여 합의함",
        "sentences": "<div class=\"example-ja\"><ruby>双方<rt>そうほう</rt></ruby>が<span class=\"target-word\"><ruby>妥協点<rt>だきょうてん</rt></ruby></span>を<ruby>見<rt>み</rt></ruby>いだしたことで、<ruby>交渉<rt>こうしょう</rt></ruby>は<ruby>無事<rt>ぶじ</rt></ruby>に<ruby>合意<rt>ごうい</rt></ruby>に<ruby>至<rt>いた</rt></ruby>った。<br><span style=\"color:#6b7280;font-size:13px\">※ 品質に関しては、一切の妥協を許さない。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">양측이 타협점을 찾아냄으로써 협상은 무사히 합의에 이르렀다. (품질에 관해서는 일체의 타협을 허용하지 않는다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">妥(온당할 타) + 協(화합할 협)</span></div><div class=\"visual-scan-desc\">서로 온당한 선에서(妥) 힘을 합쳐(協) 조율함 → 타협</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【妥】 온당할 타</span><span class=\"mnemonic-parts\">손(爪)으로 여인(女)을 평온하고 온당하게 달램</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【協】 화합할 협</span><span class=\"mnemonic-parts\">열 사람(十)의 힘(力)을 하나로 모음</span></div>"
    },
    {
        "id": "SAMPLE-N1-006",
        "kanji": "顕著",
        "kana": "けんちょ",
        "meaning": "현저함, 눈에 띄게 두드러짐",
        "sentences": "<div class=\"example-ja\"><ruby>地方<rt>ちほう</rt></ruby>における<ruby>人口<rt>じんこう</rt></ruby><ruby>減少<rt>げんしょう</rt></ruby>は、<ruby>年々<rt>ねんねん</rt></ruby><span class=\"target-word\"><ruby>顕著<rt>けんちょ</rt></ruby></span>になっている。<br><span style=\"color:#6b7280;font-size:13px\">※ 新薬の投与により、顕著な治療効果が見られた。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">지방의 인구 감소는 해마다 현저해지고 있다. (신약 투여로 인해 현저한 치료 효과가 나타났다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">顕(나타날 현) + 著(드러날 저)</span></div><div class=\"visual-scan-desc\">빛처럼 밝게 나타나(顕) 누구의 눈에도 분명히 드러남(著) → 현저</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【顕】 나타날 현</span><span class=\"mnemonic-parts\">햇볕 아래 밝게 드러남 (현시/현미경)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【著】 드러날 저</span><span class=\"mnemonic-parts\">뚜렷이 저술되어 드러남 (저명/저서)</span></div>"
    },

    # --- Category 2: 실생활 밀착형 필수 명사 (마트/식생활, 병원/약국, 주거/행정) ---
    {
        "id": "SAMPLE-LIFE-007",
        "kanji": "挽肉",
        "kana": "ひきにく",
        "meaning": "다진 고기, 민찌 (마트 정육 코너 필수 어휘)",
        "sentences": "<div class=\"example-ja\"><ruby>今日<rt>きょう</rt></ruby>の<ruby>夕飯<rt>ゆうはん</rt></ruby>は、<ruby>豚<rt>ぶた</rt></ruby>の<span class=\"target-word\"><ruby>挽肉<rt>ひきにく</rt></ruby></span>を<ruby>使<rt>つか</rt></ruby>ってハンバーグを<ruby>作<rt>つく</rt></ruby>る<ruby>予定<rt>よてい</rt></ruby>だ。<br><span style=\"color:#6b7280;font-size:13px\">※ 牛と豚の「合挽き肉（あいびきにく）」は使い勝手が良い。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">오늘 저녁은 돼지 다진 고기를 써서 햄버그스테이크를 만들 예정이다. (소고기와 돼지고기를 섞은 '혼합 다진 고기'는 활용도가 좋다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">挽(끌/갈 만) + 肉(고기 육)</span></div><div class=\"visual-scan-desc\">맷돌이나 분쇄기로 갈아서(挽) 잘게 부순 고기(肉) → 다진 고기</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【挽】 갈/끌 만</span><span class=\"mnemonic-parts\">손(扌)으로 돌려 갊 (커피 원두를 갈 때도 '豆を挽く'라 함)</span></div>"
    },
    {
        "id": "SAMPLE-LIFE-008",
        "kanji": "惣菜",
        "kana": "そうざい",
        "meaning": "반찬, 조리된 식품 (마트/백화점 지하 델리 코너)",
        "sentences": "<div class=\"example-ja\"><ruby>仕事<rt>しごと</rt></ruby><ruby>帰<rt>がえ</rt></ruby>りにスーパーで<span class=\"target-word\"><ruby>惣菜<rt>そうざい</rt></ruby></span>を<ruby>買<rt>か</rt></ruby>って<ruby>帰宅<rt>きたく</rt></ruby>した。<br><span style=\"color:#6b7280;font-size:13px\">※ デパ地下には、美味しそうな惣菜がずらりと並んでいる。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">퇴근길에 슈퍼마켓에서 반찬(즉석조리식품)을 사서 귀가했다. (백화점 지하에는 맛있어 보이는 반찬들이 줄지어 진열되어 있다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">惣(모두 총) + 菜(나물/반찬 채)</span></div><div class=\"visual-scan-desc\">갖가지 채소와 재료를 모아(惣) 조리한 일상 반찬(菜)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【惣】 다 총</span><span class=\"mnemonic-parts\">온갖 것들을 두루 모음</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【菜】 나물 채</span><span class=\"mnemonic-parts\">풀(艹)로 만든 반찬 (야채/채소)</span></div>"
    },
    {
        "id": "SAMPLE-LIFE-009",
        "kanji": "賞味期限",
        "kana": "しょうみきげん",
        "meaning": "상미기한 (맛있게 먹을 수 있는 품질 유지 기한, cf. 消費期限: 안전 소비기한)",
        "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>賞味期限<rt>しょうみきげん</rt></ruby></span>が<ruby>切<rt>き</rt></ruby>れても、すぐに<ruby>食<rt>た</rt></ruby>べられなくなるわけではない。<br><span style=\"color:#6b7280;font-size:13px\">※ 牛乳やおにぎりなど傷みやすい食品には「消費期限」が記載される。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">상미기한이 지나도 바로 먹을 수 없게 되는 것은 아니다. (우유나 삼각김밥처럼 상하기 쉬운 식품에는 '소비기한'이 기재된다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">賞味(맛볼 상, 맛 미) + 期限(기약할 기, 한계 한)</span></div><div class=\"visual-scan-desc\">식품 본래의 맛(味)을 가장 맛있게 음미(賞)할 수 있는 기한</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【賞】 맛볼 상</span><span class=\"mnemonic-parts\">감상하고 맛봄 (감상/상찬)</span></div>"
    },
    {
        "id": "SAMPLE-LIFE-010",
        "kanji": "処方箋",
        "kana": "しょほうせん",
        "meaning": "처방전 (병원 진료 후 조제약국에 약을 지으러 갈 때 내는 서류)",
        "sentences": "<div class=\"example-ja\"><ruby>病院<rt>びょういん</rt></ruby>で<ruby>診察<rt>しんさつ</rt></ruby>を<ruby>受<rt>う</rt></ruby>けた<ruby>後<rt>あと</rt></ruby>、<ruby>薬局<rt>やっきょく</rt></ruby>に<span class=\"target-word\"><ruby>処方箋<rt>しょほうせん</rt></ruby></span>を<ruby>持参<rt>じさん</rt></ruby>した。<br><span style=\"color:#6b7280;font-size:13px\">※ 処方箋の使用期間は、発行日を含めて原則4日間です。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">병원에서 진찰을 받은 뒤, 약국에 처방전을 지참했다. (처방전의 사용 기간은 발급일을 포함하여 원칙적으로 4일간입니다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">処方(처리할 처, 방법 방) + 箋(쪽지 전)</span></div><div class=\"visual-scan-desc\">환자를 치료하는 방법(処方)을 적어놓은 서류 쪽지(箋) → 처방전</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【箋】 쪽지 전</span><span class=\"mnemonic-parts\">대나무(竹)에 글을 적은 종이/쪽지 (서한/메모)</span></div>"
    },
    {
        "id": "SAMPLE-LIFE-011",
        "kanji": "胃もたれ",
        "kana": "いもたれ",
        "meaning": "속 쓰림, 소화불량, 속 더부룩함",
        "sentences": "<div class=\"example-ja\"><ruby>油<rt>あぶら</rt></ruby>っこいものを<ruby>食<rt>た</rt></ruby>べすぎて、<ruby>翌朝<rt>よくあさ</rt></ruby>ひどい<span class=\"target-word\"><ruby>胃<rt>い</rt></ruby>もたれ</span>がした。<br><span style=\"color:#6b7280;font-size:13px\">※ 胃もたれを解消するために、消化に良い温かいスープを飲んだ。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">기름진 음식을 너무 많이 먹어서 다음 날 아침 심한 속 더부룩함(소화불량)이 있었다. (속 더부룩함을 해소하기 위해 소화에 좋은 따뜻한 수프를 마셨다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">胃(밥통 위) + もたれる(체하다/기대다)</span></div><div class=\"visual-scan-desc\">음식물이 위장(胃)에 무겁게 기댄 채 얹혀 있음 → 소화불량/더부룩함</div></div>"
    },
    {
        "id": "SAMPLE-LIFE-012",
        "kanji": "捻挫",
        "kana": "ねんざ",
        "meaning": "염좌, 삠 (관절이 삐끗하여 인대가 다침)",
        "sentences": "<div class=\"example-ja\"><ruby>階段<rt>かいだん</rt></ruby>を<ruby>踏<rt>ふ</rt></ruby>み<ruby>外<rt>はず</rt></ruby>して<ruby>足首<rt>あしくび</rt></ruby>を<span class=\"target-word\"><ruby>捻挫<rt>ねんざ</rt></ruby></span>してしまった。<br><span style=\"color:#6b7280;font-size:13px\">※ 捻挫した部位をすぐに氷水で冷やした。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">계단을 헛디뎌 발목을 삐어(염좌를 입어) 버렸다. (삔 부위를 즉시 얼음물로 식혔다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">捻(비틀 념) + 挫(꺾일 좌)</span></div><div class=\"visual-scan-desc\">손(扌)으로 비틀듯 관절이 비틀려(捻) 꺾임(挫) → 삐다/염좌</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【捻】 비틀 념</span><span class=\"mnemonic-parts\">비틀어 돌림 (염출/비틀림)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【挫】 꺾일 좌</span><span class=\"mnemonic-parts\">부러지고 꺾임 (좌절)</span></div>"
    },
    {
        "id": "SAMPLE-LIFE-013",
        "kanji": "住民票",
        "kana": "じゅうみんひょう",
        "meaning": "주민표 (주민등록등본, 일본 거주 증명의 절대 1순위 서류)",
        "sentences": "<div class=\"example-ja\"><ruby>銀行<rt>ぎんこう</rt></ruby><ruby>口座<rt>こうざ</rt></ruby>を<ruby>開設<rt>かいせつ</rt></ruby>するために、<ruby>区役所<rt>くやくしょ</rt></ruby>で<span class=\"target-word\"><ruby>住民票<rt>じゅうみんひょう</rt></ruby></span>を<ruby>取得<rt>しゅとく</rt></ruby>した。<br><span style=\"color:#6b7280;font-size:13px\">※ マイナンバーカードがあれば、コンビニで住民票を発行できる。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">은행 계좌를 개설하기 위해 구청에서 주민표(주민등록등본)를 발급받았다. (마이넘버 카드가 있으면 편의점에서 주민표를 발행할 수 있다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">住民(살 주, 백성 민) + 票(표 표)</span></div><div class=\"visual-scan-desc\">어디에 거주하는 주민(住民)인지 공적으로 증명하는 문서 표(票)</div></div>"
    },
    {
        "id": "SAMPLE-LIFE-014",
        "kanji": "敷金",
        "kana": "しききん",
        "meaning": "보증금 (일본에서 집 렌트할 때 집주인에게 맡기는 담보금)",
        "sentences": "<div class=\"example-ja\"><ruby>賃貸<rt>ちんたい</rt></ruby><ruby>契約<rt>けいやく</rt></ruby>を<ruby>結<rt>むす</rt></ruby>ぶ<ruby>際<rt>さい</rt></ruby>、<ruby>家賃<rt>やちん</rt></ruby>2か月分の<span class=\"target-word\"><ruby>敷金<rt>しききん</rt></ruby></span>を<ruby>支払<rt>しはら</rt></ruby>った。<br><span style=\"color:#6b7280;font-size:13px\">※ 敷金は退去時の原状回復費用を差し引いた後、返還される。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">임대차 계약을 맺을 때 월세 2개월분의 보증금을 지불했다. (보증금은 퇴거 시 원상복구 비용을 공제한 뒤 반환된다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">敷(깔 부) + 金(쇠/돈 금)</span></div><div class=\"visual-scan-desc\">계약 바닥에 미리 깔아두는(敷) 담보금(金) → 보증금 (cf. 礼金: 사례금, 안 돌려줌)</div></div>"
    },

    # --- Category 3: 일본어 필수 복합동사 (결합 공식 체감용) ---
    {
        "id": "SAMPLE-VERB-015",
        "kanji": "引き受ける",
        "kana": "ひきうける",
        "meaning": "떠맡다, 맡아서 처리하다",
        "sentences": "<div class=\"example-ja\"><ruby>忙<rt>いそが</rt></ruby>しい<ruby>先輩<rt>せんぱい</rt></ruby>に<ruby>代<rt>か</rt></ruby>わって、プロジェクトの<ruby>進行<rt>しんこう</rt></ruby>を<span class=\"target-word\"><ruby>引<rt>ひ</rt></ruby>き<ruby>受<rt>う</rt></ruby>けた</span>。<br><span style=\"color:#6b7280;font-size:13px\">※ 責任を持ってその仕事を引き受けます。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">바쁜 선배를 대신하여 프로젝트의 진행을 떠맡았다. (책임을 지고 그 일을 도맡겠습니다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">引く(당기다) + 受ける(받다)</span></div><div class=\"visual-scan-desc\">남의 짐이나 일을 내 쪽으로 당겨와서(引) 전적으로 받음(受) → 떠맡다</div></div>"
    },
    {
        "id": "SAMPLE-VERB-016",
        "kanji": "見落とす",
        "kana": "みおとす",
        "meaning": "간과하다, 못 보고 지나치다/놓치다",
        "sentences": "<div class=\"example-ja\"><ruby>書類<rt>しょるい</rt></ruby>をしっかり<ruby>確認<rt>かくにん</rt></ruby>したつもりだったが、<ruby>重大<rt>じゅうだい</rt></ruby>な<ruby>誤字<rt>ごじ</rt></ruby>を<span class=\"target-word\"><ruby>見落<rt>みお</rt></ruby>としていた</span>。<br><span style=\"color:#6b7280;font-size:13px\">※ 重要な手がかりを見落とさないように注意してください。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">서류를 꼼꼼히 확인했다고 생각했으나 중대한 오타를 못 보고 지나쳤다. (중요한 단서를 놓치지 않도록 주의해 주십시오.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">見る(보다) + 落とす(떨어뜨리다)</span></div><div class=\"visual-scan-desc\">눈으로 보면서도(見) 시야 밑으로 떨어뜨려 놓침(落) → 간과하다/놓치다</div></div>"
    },
    {
        "id": "SAMPLE-VERB-017",
        "kanji": "思い付く",
        "kana": "おもいつく",
        "meaning": "문득 생각해 내다, 좋은 아이디어가 떠오르다",
        "sentences": "<div class=\"example-ja\"><ruby>散歩<rt>さんぽ</rt></ruby>をしているときに、<ruby>新<rt>あたら</rt></ruby>しい<ruby>企画<rt>きかく</rt></ruby>のアイデアを<span class=\"target-word\"><ruby>思<rt>おも</rt></ruby>い<ruby>付<rt>つ</rt></ruby>いた</span>。<br><span style=\"color:#6b7280;font-size:13px\">※ 何か良い解決策を思い付いたら教えてください。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">산책을 하고 있을 때 새로운 기획 아이디어가 문득 떠올랐다. (무언가 좋은 해결책이 떠오르면 알려주세요.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">思う(생각하다) + 付く(달라붙다)</span></div><div class=\"visual-scan-desc\">좋은 생각이(思) 머릿속에 번뜩 착 달라붙음(付) → 문득 떠오르다</div></div>"
    },
    {
        "id": "SAMPLE-VERB-018",
        "kanji": "気を配る",
        "kana": "きをくばる",
        "meaning": "두루 세심하게 신경 쓰다, 배려하다",
        "sentences": "<div class=\"example-ja\"><ruby>幹事<rt>かんじ</rt></ruby>は<ruby>参加者<rt>さんかしゃ</rt></ruby><ruby>全員<rt>ぜんいん</rt></ruby>が<ruby>楽<rt>たの</rt></ruby>しめるよう、<ruby>細<rt>こま</rt></ruby>やかに<span class=\"target-word\"><ruby>気<rt>き</rt></ruby>を<ruby>配<rt>くば</rt></ruby>る</span><ruby>必要<rt>ひつよう</rt></ruby>がある。<br><span style=\"color:#6b7280;font-size:13px\">※ 周りの人々に常に気を配っている素晴らしいリーダーだ。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">간사는 참가자 전원이 즐길 수 있도록 세심하게 신경을 쓸 필요가 있다. (주변 사람들에게 항상 신경을 쓰는 훌륭한 리더다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">気(마음/신경 기) + 配る(나누어 주다 배)</span></div><div class=\"visual-scan-desc\">내 신경과 배려심(気)을 사방 곳곳에 골고루 나누어 줌(配) → 세심히 신경 쓰다</div></div>"
    },
    {
        "id": "SAMPLE-VERB-019",
        "kanji": "やり直す",
        "kana": "やりなおす",
        "meaning": "다시 고쳐 하다, 처음부터 다시 하다",
        "sentences": "<div class=\"example-ja\"><ruby>途中<rt>とちゅう</rt></ruby>でミスに<ruby>気<rt>き</rt></ruby>づいたので、<ruby>最初<rt>さいしょ</rt></ruby>から<ruby>作業<rt>さぎょう</rt></ruby>を<span class=\"target-word\">やり<ruby>直<rt>なお</rt></ruby>した</span>。<br><span style=\"color:#6b7280;font-size:13px\">※ 何度でもやり直せばいいから、諦めないで。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">도중에 실수를 알아채서 처음부터 작업을 다시 고쳐 했다. (몇 번이고 다시 하면 되니까 포기하지 마.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">やる(하다) + 直す(고치다)</span></div><div class=\"visual-scan-desc\">행한 것(やる)을 바르게 바로잡아(直) 다시 함 → 다시 하다 (~直す 패턴 공식)</div></div>"
    },

    # --- Category 4: 요즘 일본 현지 구어체 / 트렌드 슬랭 (5개) ---
    {
        "id": "SAMPLE-SLANG-020",
        "kanji": "ガチ",
        "kana": "がち",
        "meaning": "찐으로, 진심으로, 리얼 (스모의 진검승부 'ガチンコ' 유래)",
        "sentences": "<div class=\"example-ja\"><ruby>今日<rt>きょう</rt></ruby>のテスト、ノー<ruby>勉<rt>べん</rt></ruby>だったから<span class=\"target-word\">ガチ</span>で<ruby>焦<rt>あせ</rt></ruby>った。<br><span style=\"color:#6b7280;font-size:13px\">※ 彼はガチの天才だと思う。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">오늘 시험 공부 하나도 안 해서 찐으로 식은땀 흘렸어(당황했어). (그는 리얼 천재라고 생각해.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">【語源】 ガチンコ (진검승부)</span></div><div class=\"visual-scan-desc\">스모에서 서로 격렬히 부딪히며 승부하던 말에서 유래. '장난이 아닌 진심, 찐'을 의미하는 국민 유행어.</div></div>"
    },
    {
        "id": "SAMPLE-SLANG-021",
        "kanji": "ワンチャン",
        "kana": "わんちゃん",
        "meaning": "원 찬스, 혹시라도/어쩌면, 각 (영어 One Chance 유래)",
        "sentences": "<div class=\"example-ja\"><ruby>今<rt>いま</rt></ruby>から<ruby>走<rt>はし</rt></ruby>れば、<span class=\"target-word\">ワンチャン</span><ruby>終電<rt>しゅうでん</rt></ruby>に<ruby>間<rt>ま</rt></ruby>に<ruby>合<rt>あ</rt></ruby>うかもしれない。<br><span style=\"color:#6b7280;font-size:13px\">※ ワンチャン合格できるかも！</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">지금부터 달리면 어쩌면(원찬스) 막차를 탈 수 있을지도 몰라. (혹시 합격할 수 있을지도!)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">【語源】 One Chance (한 번의 기회)</span></div><div class=\"visual-scan-desc\">'혹시 모를 일말의 가능성이나 찬스'를 가리키며, 젊은 층에서 '혹시~, ~각이다'로 사용됨.</div></div>"
    },
    {
        "id": "SAMPLE-SLANG-022",
        "kanji": "詰む",
        "kana": "つむ",
        "meaning": "망했다, 완전히 막히다, 끝장났다 (일본 장기 '외통수' 유래)",
        "sentences": "<div class=\"example-ja\"><ruby>財布<rt>さいふ</rt></ruby>もスマホも<ruby>忘<rt>わす</rt></ruby>れて<ruby>家<rt>いえ</rt></ruby>を<ruby>出<rt>で</rt></ruby>てしまった。<ruby>完全<rt>かんぜん</rt></ruby>に<span class=\"target-word\"><ruby>詰<rt>つ</rt></ruby>んだ</span>。<br><span style=\"color:#6b7280;font-size:13px\">※ レポートの締め切りが明日なのに、1文字も書いてなくて詰んでる。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">지갑도 스마트폰도 두고 집을 나와 버렸다. 완전히 망했다(끝장났다). (보고서 마감이 내일인데 1글자도 안 써서 망해 있다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">【詰】 막힐/가득 찰 힐(길)</span></div><div class=\"visual-scan-desc\">장기(将棋)에서 왕이 도망칠 곳 없이 포위되어 패배가 확정된 상태(詰み)에서 유래. 해결책이 없는 진퇴양난의 상황.</div></div>"
    },
    {
        "id": "SAMPLE-SLANG-023",
        "kanji": "エグい",
        "kana": "えぐい",
        "meaning": "쩐다, 미쳤다, 대박이다 / 독하다/심하다",
        "sentences": "<div class=\"example-ja\">このラーメン、チャーシューの<ruby>量<rt>りょう</rt></ruby>が<span class=\"target-word\">エグい</span>！<br><span style=\"color:#6b7280;font-size:13px\">※ 今日の日差し、エグいほど暑いね。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">이 라멘, 차슈 양이 진짜 미쳤다(쩐다)! (오늘 햇살 지독할 정도로 덥네.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">【語源】 목이 아릴 정도로 자극적임</span></div><div class=\"visual-scan-desc\">원래 목을 자극할 정도로 독하거나 떫은 맛을 뜻하던 말에서, 상식을 뛰어넘는 충격/감탄을 나타내는 말로 정착.</div></div>"
    },
    {
        "id": "SAMPLE-SLANG-024",
        "kanji": "草生える",
        "kana": "くさはえる",
        "meaning": "ㅋㅋㅋ, 개웃기다, 뿜었다 (인터넷 'www'가 풀밭 같음에서 유래)",
        "sentences": "<div class=\"example-ja\">推しのリアクションが面白すぎて<span class=\"target-word\"><ruby>草<rt>くさ</rt></ruby><ruby>生<rt>は</rt></ruby>える</span>。<br><span style=\"color:#6b7280;font-size:13px\">※ 誤字のせいで意味が変わってて草。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">최애의 리액션이 너무 웃겨서 뿜었다(풀 돋는다 www). (오타 때문에 뜻이 완전히 바뀌어서 개웃김.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">草(풀 초) + 生える(돋아나다 생)</span></div><div class=\"visual-scan-desc\">웃음(笑い)의 w를 여러 개 쓰면 'wwww'처럼 풀밭 모양이 된다고 하여 '풀이 자란다(草)' ➔ '웃기다/ㅋㅋㅋ'로 사용.</div></div>"
    }
]

note_entries = []
for item in words_data:
    note_entries.append({
        "fields": {
            "id": item["id"],
            "kanji": item["kanji"],
            "kana": item["kana"],
            "meaning": item["meaning"],
            "sentences": item["sentences"],
            "mp3": item["mp3"],
            "hanja_mnemonic": item["hanja_mnemonic"]
        },
        "tags": TAGS
    })

res = call_mcp('add_notes', {
    'deck_name': DECK_NAME,
    'model_name': MODEL_NAME,
    'notes': note_entries,
    'allow_duplicate': True
})

print("Add notes result:", json.dumps(res, indent=2, ensure_ascii=False))
