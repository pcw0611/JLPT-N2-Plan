import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "기사_어휘", "독해_어휘", "모의고사_어휘", "사용자_추가_20261021"]

words_data = [
    {
        "id": "READING-NEWS-0108",
        "kanji": "助言",
        "kana": "じょげん",
        "meaning": "조언, 충고",
        "sentences": "<div class=\"example-ja\"><ruby>専門家<rt>せんもんか</rt></ruby>の<span class=\"target-word\"><ruby>助言<rt>じょげん</rt></ruby></span>に<ruby>従<rt>したが</rt></ruby>って、<ruby>事業<rt>じぎょう</rt></ruby><ruby>計画<rt>け이かく</rt></ruby>を<ruby>修正<rt>しゅうせい</rt></ruby>した。<br><span style=\"color:#6b7280;font-size:13px\">※ 先輩からの適切な助言のおかげで、問題を無事に解決できた。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">전문가의 조언에 따라 사업 계획을 수정했다. (선배의 적절한 조언 덕분에 문제를 무사히 해결할 수 있었다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">助(도울 조) + 言(말씀 언)</span></div><div class=\"visual-scan-desc\">상대방을 돕기 위해(助) 건네는 말(言) → 조언/충고</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【助】 도울 조</span><span class=\"mnemonic-parts\">힘(力)을 보태어 도와줌</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【言】 말씀 언</span><span class=\"mnemonic-parts\">입(口)에서 나오는 말</span></div>"
    },
    {
        "id": "READING-NEWS-0109",
        "kanji": "搭乗口",
        "kana": "とうじょうぐち",
        "meaning": "탑승구, 게이트 (비행기·배 탑승 출입구)",
        "sentences": "<div class=\"example-ja\"><ruby>出発<rt>しゅっぱつ</rt></ruby>の20<ruby>分<rt>ぷん</rt></ruby><ruby>前<rt>まえ</rt></ruby>までに、15<ruby>番<rt>ばん</rt></ruby><span class=\"target-word\"><ruby>搭乗口<rt>とうじょうぐち</rt></ruby></span>へお<ruby>越<rt>こ</rt></ruby>しください。<br><span style=\"color:#6b7280;font-size:13px\">※ 搭乗口が急遽変更になったため、アナウンスに注意してください。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">출발 20분 전까지 15번 탑승구로 와 주십시오. (탑승구가 급히 변경되었으므로 안내 방송에 주의해 주십시오.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">搭(탈 탑) + 乗(탈 승) + 口(입 구)</span></div><div class=\"visual-scan-desc\">탈것에 탑승(搭乗)하기 위해 들어가는 문/출입구(口)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【搭】 탈 탑</span><span class=\"mnemonic-parts\">손(扌)으로 잡고 탈것에 올라탐</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【乗】 탈 승</span><span class=\"mnemonic-parts\">수레나 말을 탐</span></div>"
    },
    {
        "id": "READING-NEWS-0110",
        "kanji": "欠航",
        "kana": "けっこう",
        "meaning": "결항 (악천후 등으로 비행기·배의 운항이 취소됨)",
        "sentences": "<div class=\"example-ja\"><ruby>大型<rt>おおがた</rt></ruby>の<ruby>台風<rt>たいふう</rt></ruby>が<ruby>接近<rt>せっきん</rt></ruby>しているため、<ruby>本日<rt>ほんじつ</rt></ruby>の<ruby>全便<rt>ぜんびん</rt></ruby>が<span class=\"target-word\"><ruby>欠航<rt>けっこう</rt></ruby></span>となった。<br><span style=\"color:#6b7280;font-size:13px\">※ 吹雪による欠航のため、空港のロビーで一夜を明かした。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">대형 태풍이 접근하고 있어 오늘의 전 항공편이 결항되었다. (눈보라로 인한 결항 때문에 공항 로비에서 하룻밤을 지새웠다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">欠(이지러질/빠질 결) + 航(배 다닐/비행할 항)</span></div><div class=\"visual-scan-desc\">항공이나 항해(航)가 결석하듯 빠지고(欠) 쉼 → 결항</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【欠】 결할 결</span><span class=\"mnemonic-parts\">하품하듯 입을 벌려 결석함/모자람</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【航】 배다닐 항</span><span class=\"mnemonic-parts\">배(舟)가 물을 가르며 항해함</span></div>"
    },
    {
        "id": "READING-NEWS-0111",
        "kanji": "乗り換え",
        "kana": "のりかえ",
        "meaning": "환승, 갈아타기 (차량·비행기·노선 교체)",
        "sentences": "<div class=\"example-ja\"><ruby>次<rt>つぎ</rt></ruby>の<ruby>駅<rt>えき</rt></ruby>で<ruby>地下鉄<rt>ちかてつ</rt></ruby>への<span class=\"target-word\"><ruby>乗<rt>の</rt></ruby>り<ruby>換<rt>か</rt></ruby>え</span>が<ruby>便利<rt>べんり</rt></ruby>です。<br><span style=\"color:#6b7280;font-size:13px\">※ 直行便がないため、成田空港で乗り換えが必要だ。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">다음 역에서 지하철로의 환승이 편리합니다. (직항편이 없기 때문에 나리타 공항에서 환승이 필요하다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">乗(탈 승) + 換(바꿀 환)</span></div><div class=\"visual-scan-desc\">타던(乗) 교통수단을 다른 것으로 바꿈(換) → 환승</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【乗】 탈 승</span><span class=\"mnemonic-parts\">탈것에 올라탐</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【換】 바꿀 환</span><span class=\"mnemonic-parts\">손(扌)으로 교환하여 바꿈</span></div>"
    },
    {
        "id": "READING-NEWS-0112",
        "kanji": "手荷物",
        "kana": "てにもつ",
        "meaning": "수하물, 휴대품, 기내 반입 수하물",
        "sentences": "<div class=\"example-ja\"><ruby>機内<rt>かない</rt></ruby>に<ruby>持<rt>も</rt></ruby>ち<ruby>込<rt>こ</rt></ruby>める<span class=\"target-word\"><ruby>手荷物<rt>てにもつ</rt></ruby></span>のサイズには<ruby>制限<rt>せいげん</rt></ruby>があります。<br><span style=\"color:#6b7280;font-size:13px\">※ 貴重品は手荷物に入れて、身元から離さないようにしてください。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">기내에 반입할 수 있는 수하물의 크기에는 제한이 있습니다. (귀중품은 기내 휴대 수하물에 넣고 몸에서 떼지 않도록 해 주십시오.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">手(손 수) + 荷(짐 하) + 物(물건 물)</span></div><div class=\"visual-scan-desc\">손(手)에 직접 들고 다니는 짐(荷物) → 휴대 수하물</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【手】 손 수</span><span class=\"mnemonic-parts\">사람의 손 모양</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【荷】 짐 하</span><span class=\"mnemonic-parts\">어깨에 메는 짐</span></div>"
    },
    {
        "id": "READING-NEWS-0113",
        "kanji": "預け荷物",
        "kana": "あずけにもつ",
        "meaning": "위탁 수하물 (체크인 카운터에 부치는 짐)",
        "sentences": "<div class=\"example-ja\"><ruby>航空<rt>こうくう</rt></ruby>カウンターでスーツケースを<span class=\"target-word\"><ruby>預<rt>あず</rt></ruby>け<ruby>荷物<rt>にもつ</rt></ruby></span>として<ruby>預<rt>あず</rt></ruby>け<ruby>入<rt>い</rt></ruby>れた。<br><span style=\"color:#6b7280;font-size:13px\">※ 預け荷物の重量制限を超過すると、追加料金が発生します。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">항공사 카운터에서 여행 가방을 위탁 수하물로 부쳤다. (위탁 수하물의 무게 제한을 초과하면 추가 요금이 발생합니다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">預(맡길 예) + 荷(짐 하) + 物(물건 물)</span></div><div class=\"visual-scan-desc\">항공사에 맡겨서(預) 부치는 짐(荷物) → 위탁 수하물</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【預】 맡길 예</span><span class=\"mnemonic-parts\">돈이나 물건을 예치하고 맡김 (예금/보관)</span></div>"
    },
    {
        "id": "READING-NEWS-0114",
        "kanji": "保安検査",
        "kana": "ほあんけんさ",
        "meaning": "보안 검사 (공항 보안 검색대)",
        "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>保安検査<rt>ほあんけんさ</rt></ruby></span>では、パソコンや<ruby>液体類<rt>えきたいるい</rt></ruby>をバッグから<ruby>出<rt>だ</rt></ruby>す<ruby>必要<rt>ひつよう</rt></ruby>がある。<br><span style=\"color:#6b7280;font-size:13px\">※ 連休中は保安検査場が混雑するため、時間に余裕を持ってお越しください。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">보안 검사에서는 노트북이나 액체류를 가방에서 꺼낼 필요가 있다. (연휴 중에는 보안 검사장이 혼잡하므로 시간 여유를 가지고 와 주십시오.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">保安(보호할 보, 편안 안) + 検査(검사할 검, 조사할 사)</span></div><div class=\"visual-scan-desc\">안전(保安)을 지키기 위해 철저히 점검(検査)함 → 보안 검색</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【保】 지킬 보</span><span class=\"mnemonic-parts\">사람(亻)이 아이를 보호함</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【検】 검사할 검</span><span class=\"mnemonic-parts\">나무(木)나 규격을 맞추어 검사함</span></div>"
    },
    {
        "id": "READING-NEWS-0115",
        "kanji": "出国審査",
        "kana": "しゅっこくしんさ",
        "meaning": "출국 심사 (Immigration check)",
        "sentences": "<div class=\"example-ja\"><ruby>顔認証<rt>かおにんしょう</rt></ruby>ゲートの<ruby>導入<rt>どうにゅう</rt></ruby>により、<span class=\"target-word\"><ruby>出国審査<rt>しゅっこくしんさ</rt></ruby></span>がスムーズになった。<br><span style=\"color:#6b7280;font-size:13px\">※ パスポートにスタンプをもらって、無事に出国審査を終えた。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">안면 인식 게이트의 도입으로 출국 심사가 원활해졌다. (여권에 도장을 받고 무사히 출국 심사를 마쳤다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">出国(나갈 출, 나라 국) + 審査(살필 심, 조사할 사)</span></div><div class=\"visual-scan-desc\">나라 밖으로 나갈 때(出国) 여권과 자격을 심사함(審査)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【審】 살필 심</span><span class=\"mnemonic-parts\">집(宀) 안에서 자세히 살핌</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【査】 조사할 사</span><span class=\"mnemonic-parts\">나무(木) 위의 사실을 살피어 조사함</span></div>"
    },
    {
        "id": "READING-NEWS-0116",
        "kanji": "遅延",
        "kana": "ちえん",
        "meaning": "지연, 늦어짐",
        "sentences": "<div class=\"example-ja\"><ruby>信号<rt>しんごう</rt></ruby><ruby>故障<rt>こしょう</rt></ruby>の<ruby>影響<rt>えいきょう</rt></ruby>で、<ruby>電車<rt>でんしゃ</rt></ruby>に20<ruby>分<rt>ぷん</rt></ruby>の<span class=\"target-word\"><ruby>遅延<rt>ちえん</rt></ruby></span>が<ruby>発生<rt>はっせい</rt></ruby>している。<br><span style=\"color:#6b7280;font-size:13px\">※ 飛行機の出発遅延により、乗り継ぎ便に間に合わなかった。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">신호 고장의 영향으로 전철에 20분의 지연이 발생하고 있다. (비행기의 출발 지연으로 인해 환승 항공편에 늦었다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">遅(늦을 지) + 延(늘일 연)</span></div><div class=\"visual-scan-desc\">시간이 늦어지고(遅) 뒤로 길게 연장됨(延) → 지연</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【遅】 늦을 지</span><span class=\"mnemonic-parts\">길(辶)을 가는데 코뿔소(犀)처럼 걸음이 늦음</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【延】 늘일 연</span><span class=\"mnemonic-parts\">발을 뻗어 길게 연장함</span></div>"
    },
    {
        "id": "READING-NEWS-0117",
        "kanji": "宣伝する",
        "kana": "せんでんする",
        "meaning": "선전하다, 홍보하다, 광고하다",
        "sentences": "<div class=\"example-ja\"><ruby>新製品<rt>しんせいひん</rt></ruby>の<ruby>魅力<rt>みりょく</rt></ruby>を<ruby>若者<rt>わかもの</rt></ruby>に<ruby>向<rt>む</rt></ruby>けてSNSで<span class=\"target-word\"><ruby>宣伝<rt>せんでん</rt></ruby>する</span>。<br><span style=\"color:#6b7280;font-size:13px\">※ テレビCMだけでなく、インフルエンサーを活用して宣伝している。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">신제품의 매력을 젊은 층을 향해 SNS로 홍보하다. (TV 광고뿐만 아니라 인플루언서를 활용하여 홍보하고 있다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">宣(베풀/널리 펼 선) + 伝(전할 전)</span></div><div class=\"visual-scan-desc\">대중에게 널리 펴서(宣) 정보를 전달함(伝) → 선전/홍보</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【宣】 베풀 선</span><span class=\"mnemonic-parts\">집(宀)에서 널리 선언하고 공포함</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【伝】 전할 전</span><span class=\"mnemonic-parts\">사람(亻)이 전하여 알림</span></div>"
    },
    {
        "id": "READING-NEWS-0118",
        "kanji": "看板",
        "kana": "かんばん",
        "meaning": "간판; (가게의) 대표 상품, 간판 메뉴; 표지",
        "sentences": "<div class=\"example-ja\"><ruby>駅前<rt>えきまえ</rt></ruby>に<ruby>目立<rt>めだ</rt></ruby>つ<span class=\"target-word\"><ruby>看板<rt>かんばん</rt></ruby></span>を<ruby>出<rt>だ</rt></ruby>したことで、<ruby>新規<rt>しんき</rt></ruby>の<ruby>来店客<rt>らいてんきゃく</rt></ruby>が<ruby>増<rt>ふ</rt></ruby>えた。<br><span style=\"color:#6b7280;font-size:13px\">※ この店の看板メニューは、創業以来受け継がれている手打ちうどんだ。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">역 앞에 눈에 띄는 간판을 내건 덕분에 신규 방문 고객이 늘었다. (이 가게의 대표(간판) 메뉴는 창업 이래 이어져 내려온 수타 우동이다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">看(볼 간) + 板(판자 판)</span></div><div class=\"visual-scan-desc\">사람들이 잘 보도록(看) 글씨를 써 붙여놓은 널빤지(板) → 간판</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【看】 볼 간</span><span class=\"mnemonic-parts\">손(手)을 이마에 얹고 눈(目)으로 멀리 바라봄 (간호/간판)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【板】 널빤지 판</span><span class=\"mnemonic-parts\">나무(木)를 깎아 만든 판자</span></div>"
    },
    {
        "id": "READING-NEWS-0119",
        "kanji": "動画広告",
        "kana": "どうがこうこく",
        "meaning": "동영상 광고",
        "sentences": "<div class=\"example-ja\">スマートフォン<ruby>向<rt>む</rt></ruby>けの<span class=\"target-word\"><ruby>動画広告<rt>どうがこうこく</rt></ruby></span>は、<ruby>短時間<rt>たんじかん</rt></ruby>で<ruby>印象<rt>いんしょう</rt></ruby>に<ruby>残<rt>のこ</rt></ruby>すことが<ruby>重要<rt>じゅうよう</rt></ruby>だ。<br><span style=\"color:#6b7280;font-size:13px\">※ 静止画バナーよりも動画広告の方が、高いクリック率を記録している。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">스마트폰용 동영상 광고는 짧은 시간에 인상에 남기는 것이 중요하다. (정지 화상 배너보다 동영상 광고 쪽이 더 높은 클릭률을 기록하고 있다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">動画(움직일 동, 그림 화) + 広告(넓을 광, 알릴 고)</span></div><div class=\"visual-scan-desc\">움직이는 영상(動画)을 이용해 널리 대중에게 알리는(広告) 광고</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【動】 움직일 동</span><span class=\"mnemonic-parts\">무거운(重) 힘(力)으로 움직임</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【広】 넓을 광</span><span class=\"mnemonic-parts\">넓은 영역에 널리 퍼짐</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【告】 알릴 고</span><span class=\"mnemonic-parts\">말씀으로 고하고 보고함</span></div>"
    }
]

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

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))

# Verify final count in Deck 14
r_cnt = call_mcp('cards_stats', {'deck': DECK_NAME, 'limit': 1000})
txt = r_cnt['content'][0]['text']
d = json.loads(txt)
print(f"Total cards now in '{DECK_NAME}': {len(d.get('cards', []))}")
