import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "모의고사_어휘", "생활_어휘", "청해_어휘", "사용자_추가_20261112"]

words_data = [
    {
        "id": "READING-NEWS-0147",
        "kanji": "倉庫",
        "kana": "そうこ",
        "meaning": "창고, 물품 보관소",
        "sentences": "<div class=\"example-ja\"><ruby>出荷<rt>しゅっか</rt></ruby><ruby>前<rt>まえ</rt></ruby>の<ruby>製品<rt>せいひん</rt></ruby>は、<ruby>温度<rt>おんど</rt></ruby><ruby>管理<rt>かんり</rt></ruby>がされた<span class=\"target-word\"><ruby>倉庫<rt>そうこ</rt></ruby></span>に<ruby>保管<rt>ほかん</rt></ruby>されている。<br><span style=\"color:#6b7280;font-size:13px\">※ 発音注意: 'そう'는 장음(そうこ)! 聴解(과제이해) 초빈출: 「倉庫から資料を持ってきて」「予備の椅子を倉庫に運ぶ」</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">출하 전의 제품은 온도 관리가 된 창고에 보관되어 있다. (청해 행동순서 문제 및 비즈니스 물류 지문의 최다 빈출 어휘)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">倉(곳집 창) + 庫(곳집 고)</span></div><div class=\"visual-scan-desc\">곡식을 저장하는 곳집(倉)과 수레나 물건을 넣어두는 곳집(庫) → 물품을 보관하는 창고 (そうこ)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【倉】 곳집 창 (음: そう)</span><span class=\"mnemonic-parts\">지붕 아래 곡식을 모아 저장함 (장음 そう)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【庫】 곳집/차고 고 (음: こ)</span><span class=\"mnemonic-parts\">집(广) 안에 수레(車)나 물품을 넣어둠 (金庫: きんこ)</span></div>"
    },
    {
        "id": "READING-NEWS-0148",
        "kanji": "目印",
        "kana": "めじるし",
        "meaning": "표식, 안표, 랜드마크, 길잡이 표지 (위치를 찾거나 구별하기 위한 표지)",
        "sentences": "<div class=\"example-ja\"><ruby>駅前<rt>えきまえ</rt></ruby>の<ruby>大<rt>おお</rt></ruby>きな<ruby>時計台<rt>とけいだい</rt></ruby>を<span class=\"target-word\"><ruby>目印<rt>めじるし</rt></ruby></span>にして、<ruby>交差点<rt>こうさてん</rt></ruby>を<ruby>右<rt>みぎ</rt></ruby>へ<ruby>曲<rt>ま</rt></ruby>がってください。<br><span style=\"color:#6b7280;font-size:13px\">※ 連濁注意: 'めしるし'가 아닌 탁음 'めじるし'! 聴解(길 안내/약속 장소) 절대 빈출: 「〜を目印にする(〜를 표식으로 삼다)」</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">역 앞의 커다란 시계탑을 표식(길잡이)으로 삼아, 교차로에서 오른쪽으로 도세요. (청해 길 안내 및 독해 오시는 길 안내문 핵심 표현)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">目(눈 목 / 훈: め) + 印(도장/표 인 / 훈: じるし)</span></div><div class=\"visual-scan-desc\">눈(目)에 잘 띄도록 해놓은 표지나 표시(印) → 안표 / 길잡이 표식 (めじるし)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【目】 눈 목 (훈: め)</span><span class=\"mnemonic-parts\">사람의 눈 (目印: めじるし, 目覚まし: めざまし)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【印】 도장/표 인 (훈: しるし ➔ 탁음 じるし)</span><span class=\"mnemonic-parts\">결합하여 탁음화: <b>め + しるし ➔ めじるし (O)</b></span></div>"
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
        body = resp.read().decode('utf-8')
        m = re.search(r'^data:\s*(.+)$', body, re.MULTILINE)
        if m:
            return json.loads(m.group(1))['result']
        raise ValueError("Could not parse SSE response")

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

print("Add result:", json.dumps(res, indent=2, ensure_ascii=False))

cnt_res = call_mcp('cards_stats', {'deck': DECK_NAME, 'limit': 1000})
txt = cnt_res['content'][0]['text']
d = json.loads(txt)
print(f"Total cards now in '{DECK_NAME}': {len(d.get('cards', []))}")
