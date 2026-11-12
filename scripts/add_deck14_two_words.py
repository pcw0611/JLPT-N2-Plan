import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "모의고사_어휘", "사용자_추가_20261112"]

words_data = [
    {
        "id": "READING-NEWS-0134",
        "kanji": "養育者",
        "kana": "よういくしゃ",
        "meaning": "양육자 (아이를 기르고 돌보는 사람, 부모 또는 보호자)",
        "sentences": "<div class=\"example-ja\"><ruby>子<rt>こ</rt></ruby>どもの<ruby>健全<rt>けんぜん</rt></ruby>な<ruby>成長<rt>せいちょう</rt></ruby>には、<span class=\"target-word\"><ruby>養育者<rt>よういくしゃ</rt></ruby></span>との<ruby>愛着<rt>あいちゃく</rt></ruby><ruby>関係<rt>かんけい</rt></ruby>が<ruby>欠<rt>か</rt></ruby>かせない。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解: 육아·발달심리학·사회문제 지문에서 '부모(親)' 대신 대상을 포괄하는 학술 용어로 빈출.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">아이의 건전한 성장에는 양육자와의 애착 관계가 빠질 수 없다. (지문에서 부모 및 실질적 보호자를 통칭하는 표현)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">養(기를 양) + 育(기를 육) + 者(놈/사람 자)</span></div><div class=\"visual-scan-desc\">아이를 먹이고(養) 가르쳐 기르는(育) 사람(者) → 양육자 / 보호자</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【養】 기를 양</span><span class=\"mnemonic-parts\">양(羊)처럼 순한 아이에게 밥(食)을 먹여 건강히 기름</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【育】 기를 육</span><span class=\"mnemonic-parts\">아이(子)가 살(月=肉)이 오르고 자라도록 돌보아 기름</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【者】 사람 자</span><span class=\"mnemonic-parts\">그 역할을 수행하는 사람이나 주체</span></div>"
    },
    {
        "id": "READING-NEWS-0135",
        "kanji": "反抗",
        "kana": "はんこう",
        "meaning": "반항; 저항, 대듦, 거역함",
        "sentences": "<div class=\"example-ja\"><ruby>思春期<rt>ししゅんき</rt></ruby>の<ruby>子<rt>こ</rt></ruby>どもが<ruby>親<rt>おや</rt></ruby>に<span class=\"target-word\"><ruby>反抗<rt>はんこう</rt></ruby>する</span>のは、<ruby>自立<rt>じりつ</rt></ruby>への<ruby>第一<rt>だいいち</rt></ruby><ruby>歩<rt>ぽ</rt></ruby>でもある。<br><span style=\"color:#6b7280;font-size:13px\">※ 関連語: 反抗期(はんこうき, 사춘기 반항기)・反抗的(はんこうてき, 반항적)・抵抗(ていこう, 저항)</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">사춘기 아이가 부모에게 반항하는 것은 자립을 향한 첫걸음이기도 하다. (반항기·저항의 의미로 N2 독해 및 어휘 빈출)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">反(돌이킬/맞설 반) + 抗(겨룰/저항할 항)</span></div><div class=\"visual-scan-desc\">지시나 권위에 거슬러 반대로(反) 빳빳이 고개를 들고 맞섬(抗) → 반항 / 저항</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【反】 돌아올/맞설 반</span><span class=\"mnemonic-parts\">절벽(厂)을 손(又)으로 짚고 반대 방향으로 돌아섬</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【抗】 겨룰/막을 항</span><span class=\"mnemonic-parts\">손(扌)을 뻗고 목(亢)을 빳빳이 세워 대항함</span></div>"
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

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))

# Check note info
check = call_mcp('find_notes', {'query': 'READING-NEWS-0134 or READING-NEWS-0135'})
print("Find check:", check['content'][0]['text'])
