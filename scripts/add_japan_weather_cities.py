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

cities = [
    {
        "id": "GEO-WEATHER-0001",
        "kanji": "札幌",
        "kana": "さっぽろ",
        "meaning": "삿포로 (홋카이도 도청소재지, 홋카이도 최대 도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>札幌<rt>さっぽろ</rt></ruby></span>では'
            '<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>り、'
            '<ruby>最高<rt>さいこう</rt></ruby><ruby>気温<rt>きおん</rt></ruby>は20<ruby>度<rt>ど</rt></ruby>の'
            '<ruby>見込<rt>みこ</rt></ruby>みです。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [일기예보 방송 지문] 札幌・道央(どうおう)エリア</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">삿포로에는 비가 내리고, 최고 기온은 20도로 예상됩니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">札(패/문서 찰) + 幌(휘장 황)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    아이누어 \'사리・포로・펫(건조하고 넓은 강)\'의 음차 표기 ➔ 홋카이도 중심지 삿포로\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【札幌】 さっぽろ</span>\n'
            '  <span class="mnemonic-parts">홋카이도(北海道) 대표 도시</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0002",
        "kanji": "釧路",
        "kana": "くしろ",
        "meaning": "쿠시로 (홋카이도 동부 항구도시, 안개의 도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>釧路<rt>くしろ</rt></ruby></span>では'
            '<ruby>曇<rt>くも</rt></ruby>りのち<ruby>晴<rt>は</rt></ruby>れで、'
            '<ruby>降水<rt>こうすい</rt></ruby><ruby>確率<rt>かくりつ</rt></ruby>は20％です。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [특수 독음 주의] 釧(く) + 路(しろ). 釧路湿原(くしろしつげん) 등으로 빈출.</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">쿠시로에는 흐린 뒤 맑겠으며, 강수확률은 20%입니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">釧(팔찌 천/く) + 路(길 로/しろ)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    ★특수 독음 주의! 釧을 \'く\'로 읽음. 홋카이도 동부의 대표 항구도시.\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【釧路】 くしろ</span>\n'
            '  <span class="mnemonic-parts">홋카이도 동부(道東) 연안</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0003",
        "kanji": "仙台",
        "kana": "せんだい",
        "meaning": "센다이 (미야기현 현청소재지, 도호쿠 지방 최대 경제 중심도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>仙台<rt>せんだい</rt></ruby></span>の'
            '<ruby>今日<rt>きょう</rt></ruby>の<ruby>天気<rt>てんき</rt></ruby>は'
            '<ruby>曇<rt>くも</rt></ruby>りで、<ruby>最高<rt>さいこう</rt></ruby><ruby>気温<rt>きおん</rt></ruby>は22<ruby>度<rt>ど</rt></ruby>です。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [도호쿠 중심] 宮城県(みやぎけん) 仙台市(せんだいし)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">센다이의 오늘 날씨는 흐리겠고, 최고 기온은 22도입니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">仙(신선 선) + 台(대 대)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    도호쿠(東北) 지방의 관문이자 최대 경제·문화 거점 도시.\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【仙台】 せんだい</span>\n'
            '  <span class="mnemonic-parts">미야기현(宮城県) 청사 소재지</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0004",
        "kanji": "新潟",
        "kana": "にいがた",
        "meaning": "니가타 (니가타현 현청소재지, 동해 연안의 곡창 지대)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>新潟<rt>にいがた</rt></ruby></span>では'
            '<ruby>日中<rt>にっちゅう</rt></ruby>は<ruby>晴<rt>は</rt></ruby>れ<ruby>間<rt>ま</rt></ruby>が'
            '<ruby>広<rt>ひろ</rt></ruby>がり、28<ruby>度<rt>ど</rt></ruby>まで<ruby>上<rt>あ</rt></ruby>がるでしょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [훈독 주의] 新(にい) + 潟(がた). 일본 최대의 쌀 생산지.</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">니가타에서는 낮 동안 맑은 날씨가 이어지며 28도까지 오르겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">新(새로울 신/にい) + 潟(갯벌 석/がた)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    동해(日本海) 쪽 연안 석호 갯벌에 세워진 새로운 항구도시 ➔ にいがた\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【新潟】 にいがた</span>\n'
            '  <span class="mnemonic-parts">니가타현(新潟県)</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0005",
        "kanji": "金沢",
        "kana": "かなざわ",
        "meaning": "카나자와 (이시카와현 현청소재지, 호쿠리쿠 전통 문화 도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>金沢<rt>かなざわ</rt></ruby></span>は'
            '<ruby>晴<rt>は</rt></ruby>れ<ruby>時々<rt>ときどき</rt></ruby><ruby>曇<rt>くも</rt></ruby>りで、'
            '<ruby>寒暖<rt>かんだん</rt></ruby><ruby>差<rt>さ</rt></ruby>に<ruby>注意<rt>ちゅうい</rt></ruby>が<ruby>必要<rt>ひつよう</rt></ruby>です。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [훈독 주의] 金을 \'きん\'이 아닌 \'かな\'로 읽음! 石川県 金沢市.</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">카나자와는 맑고 때때로 흐리겠으며, 일교차에 주의가 필요합니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">金(쇠 금/かな) + 沢(못 택/ざわ)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    황금(金)이 솟아나던 못(沢)이라는 전설에서 유래 ➔ かなざわ\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【金沢】 かなざわ</span>\n'
            '  <span class="mnemonic-parts">호쿠리쿠(北陸) 중심 도시</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0006",
        "kanji": "東京",
        "kana": "とうきょう",
        "meaning": "도쿄 (일본의 수도, 도쿄도)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>東京<rt>とうきょう</rt></ruby></span>では'
            '<ruby>一日<rt>いちにち</rt></ruby>を<ruby>通<rt>つう</rt></ruby>じて'
            '<ruby>雲<rt>くも</rt></ruby>が<ruby>広<rt>ひろ</rt></ruby>がりやすい<ruby>天気<rt>てんき</rt></ruby>となるでしょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 日本の首都・東京都</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">도쿄에서는 하루 종일 구름이 많이 끼는 날씨가 되겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">東(동녘 동) + 京(서울 경)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    동쪽(東)에 위치한 수도(京) ➔ とうきょう\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【東京】 とうきょう</span>\n'
            '  <span class="mnemonic-parts">수도권(首都圏) 중심</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0007",
        "kanji": "名古屋",
        "kana": "なごや",
        "meaning": "나고야 (아이치현 현청소재지, 주부 지방 최대 산업 중심도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>名古屋<rt>なごや</rt></ruby></span>は'
            '<ruby>晴<rt>は</rt></ruby>れのち<ruby>曇<rt>くも</rt></ruby>りで、'
            '<ruby>昼間<rt>ひるま</rt></ruby>は28<ruby>度<rt>ど</rt></ruby>と<ruby>過<rt>す</rt></ruby>ごしやすいでしょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 愛知県(あいちけん) 名古屋市(なごやし)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">나고야는 맑은 후 흐리겠고, 낮에는 28도로 지내기 수월하겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">名(이름 명) + 古(옛 고) + 屋(집 옥)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    평온하고 온화하다는 뜻의 나고야카(和やか)에서 유래 ➔ なごや\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【名古屋】 なごや</span>\n'
            '  <span class="mnemonic-parts">도카이(東海)·주부 지방 최대 도시</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0008",
        "kanji": "大阪",
        "kana": "おおさか",
        "meaning": "오사카 (오사카부 부청소재지, 간사이 지방 최대 상업 도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>大阪<rt>おおさか</rt></ruby></span>では'
            '<ruby>日差<rt>ひざ</rt></ruby>しが<ruby>届<rt>とど</rt></ruby>きますが、'
            '<ruby>夕方<rt>ゆうがた</rt></ruby>から<ruby>雲<rt>くも</rt></ruby>が<ruby>多<rt>おお</rt></ruby>くなる<ruby>見込<rt>みこ</rt></ruby>みです。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 関西地方(かんさいちほう)の中心・大阪府</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">오사카에서는 햇살이 비추겠지만, 저녁부터 구름이 많아질 전망입니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">大(큰 대) + 阪(언덕 판)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    큰 비탈 언덕이 있던 땅 ➔ おおさか\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【大阪】 おおさか</span>\n'
            '  <span class="mnemonic-parts">긴키·간사이(近畿・関西) 중심</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0009",
        "kanji": "広島",
        "kana": "ひろしま",
        "meaning": "히로시마 (히로시마현 현청소재지, 주고쿠 지방 거점 도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>広島<rt>ひろしま</rt></ruby></span>では'
            '<ruby>晴<rt>は</rt></ruby>れのち<ruby>雨<rt>あめ</rt></ruby>で、'
            '<ruby>午後<rt>ごご</rt></ruby>は<ruby>傘<rt>かさ</rt></ruby>が<ruby>手放<rt>てばな</rt></ruby>せないでしょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 中国地方(ちゅうごくちほう)・広島県</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">히로시마는 맑은 후 비가 내리겠으며, 오후에는 우산을 챙기셔야겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">広(넓을 광) + 島(섬 도)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    넓은 삼각주 섬들이 이어진 땅 ➔ ひろしま\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【広島】 ひろしま</span>\n'
            '  <span class="mnemonic-parts">세토내해(瀬戸内海) 연안</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0010",
        "kanji": "高知",
        "kana": "こうち",
        "meaning": "코치 (시코쿠 고치현 현청소재지, 태평양 연안 남부 도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>高知<rt>こうち</rt></ruby></span>の'
            '<ruby>降水<rt>こうすい</rt></ruby><ruby>確率<rt>かくりつ</rt></ruby>は70％で、'
            '<ruby>所<rt>ところ</rt></ruby>により<ruby>雷<rt>かみなり</rt></ruby>を<ruby>伴<rt>ともな</rt></ruby>う<ruby>雨<rt>あめ</rt></ruby>となるでしょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 四国地方(しこくちほう)・太平洋側</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">코치의 강수확률은 70%로, 곳에 따라 천둥을 동반한 비가 내리겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">高(높을 고) + 知(알 지)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    시코쿠 남부 태평양을 마주한 고치현의 청사 소재지 ➔ こうち\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【高知】 こうち</span>\n'
            '  <span class="mnemonic-parts">시코쿠(四国) 남부</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0011",
        "kanji": "福岡",
        "kana": "ふくおか",
        "meaning": "후쿠오카 (규슈 후쿠오카현 현청소재지, 규슈 최대 경제 중심지)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>福岡<rt>ふくおか</rt></ruby></span>では'
            '<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>りやすく、'
            '<ruby>湿度<rt>しつど</rt></ruby>が<ruby>高<rt>たか</rt></ruby>く<ruby>蒸<rt>む</rt></ruby>し<ruby>暑<rt>あつ</rt></ruby>い<ruby>一日<rt>いちにち</rt></ruby>となります。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 九州地方(きゅうしゅうちほう)の玄関口</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">후쿠오카에는 비가 자주 내리겠고, 습도가 높아 무더운 하루가 되겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">福(복 복) + 岡(언덕 강)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    복이 깃든 언덕 ➔ 규슈 최대 중심도시 ふくおか\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【福岡】 ふくおか</span>\n'
            '  <span class="mnemonic-parts">규슈(九州) 북부</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0012",
        "kanji": "鹿児島",
        "kana": "かごしま",
        "meaning": "가고시마 (규슈 최남단 가고시마현 현청소재지, 사쿠라지마 화산)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>鹿児島<rt>かごしま</rt></ruby></span>は'
            '<ruby>曇<rt>くも</rt></ruby>り<ruby>一時<rt>いちじ</rt></ruby><ruby>雨<rt>あめ</rt></ruby>で、'
            '<ruby>最高<rt>さいこう</rt></ruby><ruby>気温<rt>きおん</rt></ruby>は29<ruby>度<rt>ど</rt></ruby>まで<ruby>上<rt>あ</rt></ruby>がる<ruby>見込<rt>みこ</rt></ruby>みです。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 九州南部・桜島(さくらじま)を望む港湾都市</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">가고시마는 흐리고 한때 비가 내리겠으며, 최고 기온은 29도까지 오를 전망입니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">鹿(사슴 록) + 児(아이 아) + 島(섬 도)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    어린 사슴(鹿児)이 살던 섬에서 유래 ➔ かごしま\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【鹿児島】 かごしま</span>\n'
            '  <span class="mnemonic-parts">규슈 최남단</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0013",
        "kanji": "那覇",
        "kana": "なは",
        "meaning": "나하 (오키나와현 현청소재지, 오키나와 본섬 남부 중심도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>那覇<rt>なは</rt></ruby></span>では'
            '<ruby>強<rt>つよ</rt></ruby>い<ruby>日差<rt>ひざ</rt></ruby>しが<ruby>照<rt>て</rt></ruby>りつけ、'
            '<ruby>真夏<rt>まなつ</rt></ruby><ruby>日<rt>び</rt></ruby>の30<ruby>度<rt>ど</rt></ruby>となるでしょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [특수 한자 표기] 沖縄県 那覇市(なはし)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">나하에서는 강한 햇살이 내리쬐며 한여름 날씨인 30도가 되겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">那(어찌 나/な) + 覇(으뜸 패/は)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    오키나와(沖縄)의 정치·경제·교통 중심 도시 ➔ なは\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【那覇】 なは</span>\n'
            '  <span class="mnemonic-parts">오키나와현 청사 소재지</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0014",
        "kanji": "長野",
        "kana": "ながの",
        "meaning": "나가노 (나가노현 현청소재지, 주부 지방의 고원·산악 분지)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>長野<rt>ながの</rt></ruby></span>は'
            '<ruby>秋<rt>あき</rt></ruby><ruby>晴<rt>ば</rt></ruby>れとなりますが、'
            '<ruby>朝<rt>あさ</rt></ruby>の<ruby>最低<rt>さいてい</rt></ruby><ruby>気温<rt>きおん</rt></ruby>は14<ruby>度<rt>ど</rt></ruby>まで<ruby>下<rt>さ</rt></ruby>がります。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 甲信越(こうしんえつ)エリア・長野県</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">나가노는 쾌청한 가을 날씨가 되겠으나, 아침 최저 기온은 14도까지 떨어집니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">長(길 장) + 野(들 야)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    길게 뻗은 고원 분지의 들판 ➔ ながの\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【長野】 ながの</span>\n'
            '  <span class="mnemonic-parts">중부 고원·동계올림픽 도시</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0015",
        "kanji": "前橋",
        "kana": "まえばし",
        "meaning": "마에바시 (군마현 현청소재지, 간토 북부 내륙 도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>前橋<rt>まえばし</rt></ruby></span>では'
            '<ruby>晴<rt>は</rt></ruby>れ<ruby>時々<rt>ときどき</rt></ruby><ruby>曇<rt>くも</rt></ruby>りで、'
            '<ruby>日中<rt>にっちゅう</rt></ruby>は25<ruby>度<rt>ど</rt></ruby>と<ruby>快適<rt>かいてき</rt></ruby>でしょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [탁음 주의] まえはし(X) ➔ まえばし(O)! 群馬県(ぐんまけん) 前橋市.</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">마에바시는 맑고 때때로 흐리겠으며, 낮에는 25도로 쾌적하겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">前(앞 전/まえ) + 橋(다리 교/ばし)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    ★탁음 \'ばし\'에 주의! 군마현(群馬県)의 중심 도시.\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【前橋】 まえばし</span>\n'
            '  <span class="mnemonic-parts">간토 북부 군마현 청사 소재지</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0016",
        "kanji": "宇都宮",
        "kana": "うつのみや",
        "meaning": "우츠노미야 (도치기현 현청소재지, 교자 만두로 유명한 간토 북부 거점)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>宇都宮<rt>うつのみや</rt></ruby></span>は'
            '<ruby>曇<rt>くも</rt></ruby>りのち<ruby>晴<rt>は</rt></ruby>れで、'
            '<ruby>雷<rt>かみなり</rt></ruby>の<ruby>心配<rt>しんぱい</rt></ruby>はないでしょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [3글자 특수 지명] 栃木県(とちぎけん) 宇都宮市(うつのみやし).</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">우츠노미야는 흐린 후 맑겠으며, 뇌우의 염려는 없겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">宇(우) + 都(도) + 宮(미야)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    신사(宮)가 있는 아름다운 도읍 ➔ うつのみや (도치기현 중심)\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【宇都宮】 うつのみや</span>\n'
            '  <span class="mnemonic-parts">도치기현(栃木県) 청사 소재지</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0017",
        "kanji": "水戸",
        "kana": "みと",
        "meaning": "미토 (이바라키현 현청소재지, 낫토와 역사 유적으로 유명한 도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>水戸<rt>みと</rt></ruby></span>では'
            '<ruby>沿岸<rt>えんがん</rt></ruby><ruby>部<rt>ぶ</rt></ruby>を<ruby>中心<rt>ちゅうしん</rt></ruby>に'
            '<ruby>雲<rt>くも</rt></ruby>が<ruby>出<rt>で</rt></ruby>やすく、24<ruby>度<rt>ど</rt></ruby>の<ruby>予報<rt>よほう</rt></ruby>です。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 茨城県(いばらきけん) 水戸市(みとし)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">미토에서는 연안부를 중심으로 구름이 많이 끼겠으며 24도로 예보되었습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">水(물 수/み) + 戸(문 호/と)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    나카강의 물(水) 어귀(戸)에 자리 잡은 도시 ➔ みと\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【水戸】 みと</span>\n'
            '  <span class="mnemonic-parts">이바라키현(茨城県) 청사 소재지</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0018",
        "kanji": "さいたま",
        "kana": "さいたま",
        "meaning": "사이타마 (사이타마현 현청소재지, 히라가나 표기 정령지정도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word">さいたま</span>では'
            '<ruby>穏<rt>おだ</rt></ruby>やかな<ruby>曇<rt>くも</rt></ruby>り<ruby>空<rt>ぞら</rt></ruby>が'
            '<ruby>広<rt>ひろ</rt></ruby>がり、<ruby>過<rt>す</rt></ruby>ごしやすいでしょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 埼玉県(さいたまけん) さいたま市 (시 이름 공식 표기가 히라가나!)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">사이타마에는 평온한 흐린 하늘이 이어지며 지내기 좋겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">さいたま (埼玉)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    도쿄 바로 북쪽에 인접한 대도시권. 행정구역명 공식 표기가 히라가나.\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【さいたま】</span>\n'
            '  <span class="mnemonic-parts">사이타마현(埼玉県) 청사 소재지</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0019",
        "kanji": "甲府",
        "kana": "こうふ",
        "meaning": "코후 (야마나시현 현청소재지, 후지산 인근 분지 도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>甲府<rt>こうふ</rt></ruby></span>は'
            '<ruby>盆地<rt>ぼんち</rt></ruby><ruby>特有<rt>とくゆう</rt></ruby>の<ruby>晴天<rt>せいてん</rt></ruby>となり、'
            '28<ruby>度<rt>ど</rt></ruby>まで<ruby>気温<rt>きおん</rt></ruby>が<ruby>上<rt>あ</rt></ruby>がります。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [음독 지명] 山梨県(やまなしけん) 甲府市(こうふし). 포도·와인 명산지.</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">코후는 분지 특유의 맑은 날씨가 되겠으며, 28도까지 기온이 오르겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">甲(갑옷 갑/こう) + 府(마을 부/ふ)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    가이국(甲斐国)의 중심 관부(府中) ➔ 음독으로 こうふ\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【甲府】 こうふ</span>\n'
            '  <span class="mnemonic-parts">야마나시현(山梨県) 분지 도시</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0020",
        "kanji": "横浜",
        "kana": "よこはま",
        "meaning": "요코하마 (가나가와현 현청소재지, 일본 제2의 거대 항구도시)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>横浜<rt>よこはま</rt></ruby></span>は'
            '<ruby>曇<rt>くも</rt></ruby>り<ruby>時々<rt>ときどき</rt></ruby><ruby>晴<rt>は</rt></ruby>れで、'
            '<ruby>心地<rt>ここち</rt></ruby>よい<ruby>海風<rt>うみかぜ</rt></ruby>が<ruby>吹<rt>ふ</rt></ruby>くでしょう。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 神奈川県(かながわけん) 横浜市(よこはまし)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">요코하마는 흐리고 때때로 맑겠으며, 기분 좋은 바닷바람이 불겠습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">横(옆/가로 횡) + 浜(물가 빈)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    옆으로 길게 뻗은 바닷가 모래사장(浜) ➔ よこはま\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【横浜】 よこはま</span>\n'
            '  <span class="mnemonic-parts">가나가와현(神奈川県) 국제 항구도시</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "GEO-WEATHER-0021",
        "kanji": "千葉",
        "kana": "ちば",
        "meaning": "지바 (지바현 현청소재지, 보소 반도 및 나리타 공항 인근)",
        "sentences": (
            '<div class="example-ja"><span class="target-word"><ruby>千葉<rt>ちば</rt></ruby></span>の'
            '<ruby>降水<rt>こうすい</rt></ruby><ruby>確率<rt>かくりつ</rt></ruby>は10％で、'
            '<ruby>雨<rt>あめ</rt></ruby>の<ruby>心配<rt>しんぱい</rt></ruby>はほとんどありません。<br>'
            '<span style="color:#6b7280;font-size:13px">※ 千葉県(ちばけん) 千葉市(ちばし)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">지바의 강수확률은 10%로 비 걱정은 거의 없습니다.</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">千(일천 천) + 葉(잎 엽)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    무성한 수천 개의 나뭇잎 ➔ ちば\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【千葉】 ちば</span>\n'
            '  <span class="mnemonic-parts">도쿄 동쪽 보소(房総) 반도</span>\n'
            '</div>'
        ),
        "tags": ["일본_지명", "일기예보", "독해_어휘", "청해_지명", "JLPT_N2"]
    },
    {
        "id": "READING-NEWS-0011",
        "kanji": "見込み",
        "kana": "みこみ",
        "meaning": "예상, 전망, 가망 (★초빈출 문형: 〜の見込みだ ~할 전망이다/예상이다)",
        "sentences": (
            '<div class="example-ja"><ruby>午後<rt>ごご</rt></ruby>から<ruby>天気<rt>てんき</rt></ruby>は'
            '<ruby>回復<rt>かいふく</rt></ruby>に向かう<span class="target-word"><ruby>見込<rt>みこ</rt></ruby>み</span>です。<br>'
            '<span style="color:#6b7280;font-size:13px">※ [기상/뉴스 초빈출 문형] 〜の見込みだ(〜할 전망이다). 見込みがある/ない(가망이 있다/없다), 見込み違い(오판/착오)</span></div>'
            '<div class="example-ko"><span class="translation-label">해석</span>'
            '<span class="translation-text">오후부터 날씨는 회복세를 보일 전망(예상)입니다. (가망이 있다, 예상과 다름)</span></div>'
        ),
        "mp3": "",
        "hanja_mnemonic": (
            '<div class="visual-scan-item">\n'
            '  <div class="visual-scan-header">\n'
            '    <span class="visual-scan-badge">見(볼 견) + 込(담을 입)</span>\n'
            '  </div>\n'
            '  <div class="visual-scan-desc">\n'
            '    앞날의 상황을 미리 내다보고(見) 마음속에 계산하여 넣음(込) ➔ 예상, 전망, 가망\n'
            '  </div>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【見込む】 みこむ</span>\n'
            '  <span class="mnemonic-parts">예상하다, 내다보다, 기대하다</span>\n'
            '</div>\n'
            '<div class="mnemonic-item">\n'
            '  <span class="mnemonic-char">【〜の見込み】 〜할 전망</span>\n'
            '  <span class="mnemonic-parts">JLPT N2 독해 및 일기예보 방송 결말 필수 문형</span>\n'
            '</div>'
        ),
        "tags": ["독해_어휘", "기사_어휘", "일기예보", "N2문형", "JLPT_N2"]
    }
]

added_count = 0
for card in cities:
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
    print(f"[{card['kanji']}] -> {card['kana']}: {res.get('structuredContent', {}).get('message') or res.get('content')}")
    added_count += 1

print(f"\nSuccessfully added all {added_count} weather cities to '{DECK_NAME}'!")
