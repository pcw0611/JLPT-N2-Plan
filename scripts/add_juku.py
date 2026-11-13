import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "교육_어휘", "청해_어휘", "생활_어휘", "사용자_추가_20261112"]

words_data = [
    {
        "id": "READING-NEWS-0150",
        "kanji": "塾",
        "kana": "じゅく",
        "meaning": "학원, 사설 학원 (입시·보습 학원)",
        "sentences": "<div class=\"example-ja\"><ruby>高校<rt>こうこう</rt></ruby><ruby>受験<rt>じゅけん</rt></ruby>の<ruby>準備<rt>じゅんび</rt></ruby>のため、<ruby>週<rt>しゅう</rt></ruby>に<ruby>三日<rt>みっか</rt></ruby><span class=\"target-word\"><ruby>塾<rt>じゅく</rt></ruby></span>に<ruby>通<rt>かよ</rt></ruby>っている。<br><span style=\"color:#6b7280;font-size:13px\">※ 日韓 ニュアンス注意: 한국의 '학원(입시·보습)'은 学院이 아니라 반드시 「塾(じゅく)」! 聴解・読解(교육/청소년/가족 지문) 빈출: 「塾に通う(학원에 다니다)」「学習塾(がくしゅうじゅく)」「進学塾(しんがくじゅく)」</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">고등학교 입시 준비를 위해 일주일에 사흘 학원에 다니고 있다. (독해 청소년/교육/가족 지문 및 청해 일상 대화 최빈출)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">塾 (글방 숙 / 음: じゅく)</span></div><div class=\"visual-scan-desc\">흙(土)으로 터를 닦고 사설로 아이들을 모아 가르치던 사설 글방(서당) → 보습·입시 학원 (じゅく)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【한일 어휘 대응 주의】</span><span class=\"mnemonic-parts\"><b>입시·보습 학원</b>: <b>塾(じゅく)</b> (O) / 学院(がくいん) (X: 학교법인 명칭)<br><b>예체능·취미 학원</b>: <b>〜教室(きょうしつ)</b> (피아노, 요리 등)<br><b>회화 학원</b>: <b>英会話スクール</b>, 教室</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【주요 연어/복합어】</span><span class=\"mnemonic-parts\">塾に通(かよ)う: 학원에 다니다<br>学習塾(がくしゅうじゅく): 보습학원<br>進学塾(しんがくじゅく): 입시학원<br>塾講師(じゅくこうし): 학원 강사</span></div>"
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
