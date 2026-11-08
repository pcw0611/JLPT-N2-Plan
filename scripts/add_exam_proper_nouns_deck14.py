import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "청해_어휘", "단골_고유명사", "사용자_추가_20261103"]

words_data = [
    {
        "id": "READING-NEWS-0120",
        "kanji": "佐藤",
        "kana": "さとう",
        "meaning": "사토 (일본 최다 성씨 / N2 청해·독해 단골 인명)",
        "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>佐藤<rt>さとう</rt></ruby></span>さんは<ruby>企画部<rt>きかくぶ</rt></ruby>の<ruby>担当者<rt>たんとうしゃ</rt></ruby>として、<ruby>新<rt>あたら</rt></ruby>しいプロジェクトを<ruby>率<rt>ひき</rt></ruby>いている。<br><span style=\"color:#6b7280;font-size:13px\">※ 聴解ポイント: 설탕(砂糖, さとう)과 동음이며, 청해에서 加藤(かとう)와의 발음 혼동 트랩으로 자주 등장함.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">사토 씨는 기획부 담당자로서 새로운 프로젝트를 이끌고 있다. (청해 포인트: 설탕과 발음이 같고, 카토와의 발음 차이 주의)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">佐(도울 좌) + 藤(등나무 등)</span></div><div class=\"visual-scan-desc\">후지와라(藤原) 가문을 돕는(佐) 가계에서 유래한 일본 1위 성씨</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【佐】 도울 좌</span><span class=\"mnemonic-parts\">사람(亻)을 곁에서 보좌함(左)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【藤】 등나무 등</span><span class=\"mnemonic-parts\">풀(艹)과 물(氺)가에 피는 등나무</span></div>"
    },
    {
        "id": "READING-NEWS-0121",
        "kanji": "鈴木",
        "kana": "すずき",
        "meaning": "스즈키 (일본 2대 성씨 / N2 청해·독해 단골 인명)",
        "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>鈴木<rt>すずき</rt></ruby></span><ruby>課長<rt>かちょう</rt></ruby>から<ruby>指示<rt>しじ</rt></ruby>を<ruby>受<rt>う</rt></ruby>けて、<ruby>会議<rt>かいぎ</rt></ruby>の<ruby>資料<rt>しりょう</rt></ruby>を<ruby>準備<rt>じゅんび</rt></ruby>した。<br><span style=\"color:#6b7280;font-size:13px\">※ 聴解・読解: 佐藤 씨와 함께 비즈니스 상황 대화의 양대 주인공으로 빈출.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">스즈키 과장으로부터 지시를 받고 회의 자료를 준비했다. (청해·독해 비즈니스 지문의 단골 화자)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">鈴(방울 령) + 木(나무 목)</span></div><div class=\"visual-scan-desc\">방울(鈴) 달린 나무(木)처럼 맑게 울리는 성씨</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【鈴】 방울 령</span><span class=\"mnemonic-parts\">쇠(金)로 만들어 소리 내는 방울</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【木】 나무 목</span><span class=\"mnemonic-parts\">나무 모양 상형</span></div>"
    },
    {
        "id": "READING-NEWS-0122",
        "kanji": "高橋",
        "kana": "たかはし",
        "meaning": "타카하시 (일본 3대 성씨 / N2 청해 단골 인명)",
        "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>高橋<rt>たかはし</rt></ruby></span><ruby>先生<rt>せんせい</rt></ruby>の<ruby>研究室<rt>けんきゅうしつ</rt></ruby>を<ruby>訪問<rt>ほうもん</rt></ruby>して、<ruby>卒論<rt>そつろん</rt></ruby>の<ruby>相談<rt>そうだん</rt></ruby>をした。<br><span style=\"color:#6b7280;font-size:13px\">※ 聴解: 학교/연구소 대화에서 교수·선배·발표자 이름으로 빈출.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">타카하시 선생님 연구실을 방문하여 졸업 논문 상담을 했다. (대학·연구실 상황 청해 단골)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">高(높을 고) + 橋(다리 교)</span></div><div class=\"visual-scan-desc\">높은(高) 다리(橋)가 있는 마을에서 유래한 성씨</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【高】 높을 고</span><span class=\"mnemonic-parts\">높은 누각 모양</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【橋】 다리 교</span><span class=\"mnemonic-parts\">나무(木)로 높이 걸쳐놓은 다리</span></div>"
    },
    {
        "id": "READING-NEWS-0123",
        "kanji": "主任",
        "kana": "しゅにん",
        "meaning": "주임 (직함 / 실무 담당자)",
        "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>主任<rt>しゅにん</rt></ruby></span>に<ruby>確認<rt>かくにん</rt></ruby>したところ、<ruby>見積書<rt>みつもりしょ</rt></ruby>の<ruby>再提出<rt>さいていしゅつ</rt></ruby>を<ruby>求<rt>もと</rt></ruby>められた。<br><span style=\"color:#6b7280;font-size:13px\">※ 직급 순서: 부장(部長) > 과장(課長) > 계장(係長) > 주임(主任) > 사원(社員). 청해에서 실무 실행자로 자주 지정됨.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">주임에게 확인했더니 견적서 재제출을 요구받았다. (청해에서 과장의 지시를 받아 직접 행동하는 실무자로 빈출)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">主(주인 주) + 任(맡길 임)</span></div><div class=\"visual-scan-desc\">주된(主) 업무 책임을 맡아서(任) 수행하는 직급 → 주임</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【主】 주인 주</span><span class=\"mnemonic-parts\">촛대의 불꽃처럼 중심이 됨</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【任】 맡길 임</span><span class=\"mnemonic-parts\">사람(亻)에게 짐을 맡김</span></div>"
    },
    {
        "id": "READING-NEWS-0124",
        "kanji": "係長",
        "kana": "かかりちょう",
        "meaning": "계장 (직함 / 중간 관리자)",
        "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>係長<rt>かかりちょう</rt></ruby></span>に<ruby>相談<rt>そうだん</rt></ruby>してから、<ruby>取引先<rt>とりひきさき</rt></ruby>へ<ruby>連絡<rt>れんらく</rt></ruby>することになった。<br><span style=\"color:#6b7280;font-size:13px\">※ 読音주의: 'けいちょう'가 아니라 훈독 'かかり' + 음독 'ちょう'로 읽음! 과장 바로 아래 직급.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">계장과 상담한 후 거래처에 연락하기로 했다. (독음 주의: かかりちょう. 주임과 과장 사이의 관리직)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">係(맬 계) + 長(길/우두머리 장)</span></div><div class=\"visual-scan-desc\">해당 계/담당(係)의 장(長) → 계장</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【係】 맬 계</span><span class=\"mnemonic-parts\">사람(亻)과 실(糸)로 이어져 관계/담당함 (훈독: かかり)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【長】 어른 장</span><span class=\"mnemonic-parts\">머리칼이 긴 노인/우두머리</span></div>"
    },
    {
        "id": "READING-NEWS-0125",
        "kanji": "商事",
        "kana": "しょうじ",
        "meaning": "상사 (무역·상업 회사 / N2 가상 회사명 단골 접미사)",
        "sentences": "<div class=\"example-ja\">さくら<span class=\"target-word\"><ruby>商事<rt>しょうじ</rt></ruby></span>の<ruby>担当者<rt>たんとうしゃ</rt></ruby>から、<ruby>新製品<rt>しんせいひん</rt></ruby>の<ruby>見積もり<rt>みつもり</rt></ruby>が<ruby>届<rt>とど</rt></ruby>いた。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解・聴解: 'A商事', '東洋商事' 등 무역·유통 기업을 나타내는 가상 회사명으로 매 시험 등장.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">사쿠라 상사의 담당자로부터 신제품 견적서가 도착했다. (무역·비즈니스 지문의 단골 가상 회사명)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">商(장사 상) + 事(일 사)</span></div><div class=\"visual-scan-desc\">상업(商)에 관한 비즈니스 일(事)을 하는 회사 → 상사</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【商】 장사 상</span><span class=\"mnemonic-parts\">상품을 헤아려 거래함</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【事】 일 사</span><span class=\"mnemonic-parts\">손으로 붓을 잡고 일을 기록함</span></div>"
    },
    {
        "id": "READING-NEWS-0126",
        "kanji": "物産",
        "kana": "ぶっさん",
        "meaning": "물산 (물품 유통 회사 / 가상 회사명 단골 접미사)",
        "sentences": "<div class=\"example-ja\">ABC<span class=\"target-word\"><ruby>物産<rt>ぶっさん</rt></ruby></span>との<ruby>業務<rt>ぎょうむ</rt></ruby><ruby>提携<rt>ていけい</rt></ruby>により、<ruby>海外<rt>かいがい</rt></ruby>への<ruby>販路<rt>はんろ</rt></ruby>を<ruby>拡大<rt>かくだい</rt></ruby>する。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解・聴解: 商事와 함께 지문에 단골로 등장하는 종합 무역·물류 유통사 명칭.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">ABC 물산과의 업무 제휴를 통해 해외로의 판로를 확대한다. (무역·유통 가명 접미사)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">物(물건 물) + 産(낳을 산)</span></div><div class=\"visual-scan-desc\">생산된 여러 물건(物)과 산물(産)을 다루는 회사 → 물산</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【物】 만물 물</span><span class=\"mnemonic-parts\">소(牛)처럼 다양한 만물</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【産】 낳을 산</span><span class=\"mnemonic-parts\">새로운 것을 생산함</span></div>"
    },
    {
        "id": "READING-NEWS-0127",
        "kanji": "各駅停車",
        "kana": "かくえきていしゃ",
        "meaning": "각역정차, 완행열차 (보통열차, 모든 역에 서는 전철)",
        "sentences": "<div class=\"example-ja\"><ruby>急行<rt>きゅうこう</rt></ruby>はあの<ruby>駅<rt>えき</rt></ruby>に<ruby>止<rt>と</rt></ruby>まらないので、<span class=\"target-word\"><ruby>各駅停車<rt>かくえきていしゃ</rt></ruby></span>に<ruby>乗<rt>の</rt></ruby>り<ruby>換<rt>か</rt></ruby>える<ruby>必要<rt>ひつよう</rt></ruby>がある。<br><span style=\"color:#6b7280;font-size:13px\">※ 聴解トラップ: '各停(かくてい)' 또는 '普通(ふつう)'라고도 부름. 급행과 보통 사이 환승 시간 계산 문제에 빈출.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">급행은 저 역에 서지 않으므로 각역정차(완행)로 갈아탈 필요가 있다. (청해 교통 환승 트랩 단골)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">各(각각 각) + 駅(역 역) + 停車(정차할 정, 수레 차)</span></div><div class=\"visual-scan-desc\">모든 각각의 역(各駅)에 빠짐없이 정차함(停車) → 완행열차</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【各】 각각 각</span><span class=\"mnemonic-parts\">각자 따로따로 이름</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【停】 머무를 정</span><span class=\"mnemonic-parts\">사람(亻)이 정자(亭)에서 멈춤</span></div>"
    },
    {
        "id": "READING-NEWS-0128",
        "kanji": "快速",
        "kana": "かいそく",
        "meaning": "쾌속 (열차 등급 / 주요 역만 정차, 특급료 없음)",
        "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>快速<rt>かいそく</rt></ruby></span><ruby>電車<rt>でんしゃ</rt></ruby>を<ruby>利用<rt>りよう</rt></ruby>すれば、<ruby>終点<rt>しゅうてん</rt></ruby>まで30<ruby>分<rt>ぷん</rt></ruby><ruby>短縮<rt>たんしゅく</rt></ruby>できる。<br><span style=\"color:#6b7280;font-size:13px\">※ 聴解ポイント: 各駅停車보다 빠르지만 特急과 달리 별도 요금(特急券)이 들지 않는 점이 청해 문제의 힌트로 사용됨.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">쾌속 전철을 이용하면 종점까지 30분 단축할 수 있다. (각역정차보다 빠르고 특급과 달리 추가요금이 없는 열차)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">快(쾌할 쾌) + 速(빠를 속)</span></div><div class=\"visual-scan-desc\">상쾌할(快) 정도로 빠른(速) 속도로 달림 → 쾌속</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【快】 쾌할 쾌</span><span class=\"mnemonic-parts\">마음(忄)이 후련하고 빠름</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【速】 빠를 속</span><span class=\"mnemonic-parts\">길(辶)을 묶어(束) 빠르게 달림</span></div>"
    },
    {
        "id": "READING-NEWS-0129",
        "kanji": "中央口",
        "kana": "ちゅうおうぐち",
        "meaning": "중앙 출구, 중앙 개찰구",
        "sentences": "<div class=\"example-ja\"><ruby>駅<rt>えき</rt></ruby>の<span class=\"target-word\"><ruby>中央口<rt>ちゅうおうぐち</rt></ruby></span>を出たところにある時計台の前で待ち合わせよう。<br><span style=\"color:#6b7280;font-size:13px\">※ 聴解・読解: 北口(きたぐち), 南口(みなみぐち), 西口, 東口와 함께 약속 장소/길안내 위치 기준.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">역의 중앙 출구를 나온 곳에 있는 시계탑 앞에서 만나자. (역 출구 방향 안내의 기준점)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">中央(가운데 중, 중앙 앙) + 口(입 구)</span></div><div class=\"visual-scan-desc\">역이나 건물의 한가운데(中央)에 위치한 메인 출입구(口)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【央】 중앙 앙</span><span class=\"mnemonic-parts\">사람의 목에 칼을 씌운 가운데 모양</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【口】 입 구</span><span class=\"mnemonic-parts\">사람이나 물건이 드나드는 문/입구</span></div>"
    },
    {
        "id": "READING-NEWS-0130",
        "kanji": "早割",
        "kana": "はやわり",
        "meaning": "조기 할인 (조기 예약 할인, 早期割引의 약칭)",
        "sentences": "<div class=\"example-ja\">1か<ruby>月<rt>げつ</rt></ruby><ruby>前<rt>まえ</rt></ruby>までにチケットを<ruby>予約<rt>よやく</rt></ruby>すると、<span class=\"target-word\"><ruby>早割<rt>はやわり</rt></ruby></span>が<ruby>適用<rt>てきよう</rt></ruby>されて30％オフになる。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解問題13(情報検索): '〇日前までの申込で〇割引' 조건이 주어졌을 때 본문 표와 대조하는 1순위 키워드.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">1개월 전까지 티켓을 예약하면 조기 할인이 적용되어 30% 할인이 된다. (독해 정보검색 문제의 1순위 조건 키워드)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">早(이를 조) + 割(벨/나눌 할)</span></div><div class=\"visual-scan-desc\">이른(早) 시기에 미리 예약하여 가격을 할인(割)해 줌</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【早】 이를 조</span><span class=\"mnemonic-parts\">날(日)이 십(十)자로 밝아오는 이른 아침</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【割】 벨/나눌 할</span><span class=\"mnemonic-parts\">칼(刂)로 베어 나누어 할인함</span></div>"
    },
    {
        "id": "READING-NEWS-0131",
        "kanji": "平日限定",
        "kana": "へいじつげんてい",
        "meaning": "평일 한정 (월~금요일만 적용, 주말·공휴일 제외)",
        "sentences": "<div class=\"example-ja\">このランチコースは<span class=\"target-word\"><ruby>平日限定<rt>へいじつげんてい</rt></ruby></span>のため、<ruby>土日<rt>どにち</rt></ruby>や<ruby>祝日<rt>しゅくじつ</rt></ruby>には<ruby>注文<rt>ちゅうもん</rt></ruby>できない。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解情報検索トラップ: '日曜日に家族と行く' 경우 이 옵션은 즉시 소거해야 함!</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">이 런치 코스는 평일 한정이기 때문에 토·일요일이나 공휴일에는 주문할 수 없다. (독해 정보검색의 오답 소거 1순위 트랩)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">平日(평평할 평, 날 일) + 限定(한할 한, 정할 정)</span></div><div class=\"visual-scan-desc\">보통의 평일(平日) 날짜에만 범위를 한정(限定)함</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【限】 한할 한</span><span class=\"mnemonic-parts\">언덕(阝)으로 경계를 정하여 한정함</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【定】 정할 정</span><span class=\"mnemonic-parts\">집(宀) 안에서 자리를 정함</span></div>"
    },
    {
        "id": "READING-NEWS-0132",
        "kanji": "土日祝",
        "kana": "どにちしゅく",
        "meaning": "토·일·공휴일 (주말 및 법정 공휴일 묶음 표기)",
        "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>土日祝<rt>どにちしゅく</rt></ruby></span>は<ruby>利用料<rt>りようりょう</rt></ruby>が<ruby>割高<rt>わりだか</rt></ruby>になるため、<ruby>平日<rt>へいじつ</rt></ruby>の<ruby>利用<rt>りよう</rt></ruby>がお<ruby>得<rt>とく</rt></ruby>です。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解表의 단골 표기: '土・日・祝'로 가운데 점을 찍기도 하며, 요금표의 행/열을 구분하는 기준.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">토·일·공휴일은 이용료가 다소 비싸지므로 평일 이용이 이득입니다. (독해 요금표·일정표의 기준축)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">土(흙 토) + 日(날 일) + 祝(빌 축)</span></div><div class=\"visual-scan-desc\">토요일(土) + 일요일(日) + 축일/공휴일(祝)의 3단어 합성 축약어</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【祝】 빌 축 / 공휴일 축</span><span class=\"mnemonic-parts\">제단(礻) 앞에서 형(兄)이 복을 빎 → 경축일</span></div>"
    },
    {
        "id": "READING-NEWS-0133",
        "kanji": "市民センター",
        "kana": "しみんセンター",
        "meaning": "시민 센터 (구민회관·문화복지관 등 공공시설 가명)",
        "sentences": "<div class=\"example-ja\"><ruby>健康診断<rt>けんこうしんだん</rt></ruby>は<ruby>市役所<rt>しやくしょ</rt></ruby>ではなく、<ruby>駅前<rt>えきまえ</rt></ruby>の<span class=\"target-word\"><ruby>市民<rt>しみん</rt></ruby>センター</span>で<ruby>行<rt>おこな</rt></ruby>われます。<br><span style=\"color:#6b7280;font-size:13px\">※ 聴解・読解: '문화회관(文化会館)', '보건소(保健所)'와 함께 지문의 행사·강좌 장소로 빈출.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">건강검진은 시청이 아니라 역 앞 시민센터에서 실시됩니다. (공공 강좌·행사 지문의 대표 공공시설명)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">市民(시 시, 백성 민) + センター(Center)</span></div><div class=\"visual-scan-desc\">시의 주민(市民)들을 위해 행정·문화 서비스를 제공하는 중심 거점(Center)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【市】 저자/시 시</span><span class=\"mnemonic-parts\">시장이나 도시</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【民】 백성 민</span><span class=\"mnemonic-parts\">눈(目)을 가진 백성/시민</span></div>"
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
cards = d.get('cards', [])
print(f"Total cards now in '{DECK_NAME}': {len(cards)}")
