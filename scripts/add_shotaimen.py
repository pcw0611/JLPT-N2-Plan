import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "모의고사_어휘", "사용자_추가_20261112"]

word_data = {
    "id": "READING-NEWS-0139",
    "kanji": "初対面",
    "kana": "しょたいめん",
    "meaning": "초대면, 첫 대면 (처음으로 만남, 처음 만난 사람)",
    "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>初対面<rt>しょたいめん</rt></ruby></span>の<ruby>人<rt>ひと</rt></ruby>の<ruby>気持<rt>きも</rt></ruby>ちが<ruby>全部<rt>ぜんぶ</rt></ruby><ruby>分<rt>わ</rt></ruby>かりっこない。<ruby>無理<rt>むり</rt></ruby>な<ruby>期待<rt>きたい</rt></ruby>をしていたと<ruby>気<rt>き</rt></ruby>づいた。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解・聴解頻出: 初対面の人(처음 본 사람)・初対面の相手(처음 만난 상대)・初対面の挨拶(첫 대면 인사). 「初めて会った人」의 정석적 표현!</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">처음 만난 사람의 마음을 전부 알 턱이 없다. 무리한 기대를 하고 있었다고 깨달았다. (N2 독해·인간관계 지문 최다 빈출 어휘)</span></div>",
    "mp3": "",
    "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">初(처음 초) + 対(대할 대) + 面(낯 면)</span></div><div class=\"visual-scan-desc\">처음으로(初) 얼굴(面)을 서로 마주 대함(対) → 첫 대면, 처음 만남</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【初】 처음 초</span><span class=\"mnemonic-parts\">옷(衣)을 지을 때 칼(刀)로 천을 처음 자름 (초기/처음)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【対】 대할 대</span><span class=\"mnemonic-parts\">손(寸)을 모으고 서로 마주 대함 (대면/대상)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【面】 낯/얼굴 면</span><span class=\"mnemonic-parts\">사람의 얼굴 윤곽과 이목구비 (얼굴/방면)</span></div>"
}

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

res = call_mcp('add_notes', {
    'deck_name': DECK_NAME,
    'model_name': MODEL_NAME,
    'notes': [
        {
            "fields": {
                "id": word_data["id"],
                "kanji": word_data["kanji"],
                "kana": word_data["kana"],
                "meaning": word_data["meaning"],
                "sentences": word_data["sentences"],
                "mp3": word_data["mp3"],
                "hanja_mnemonic": word_data["hanja_mnemonic"]
            },
            "tags": TAGS
        }
    ],
    'allow_duplicate': True
})

print("Add result:", json.dumps(res, indent=2, ensure_ascii=False))

cnt_res = call_mcp('cards_stats', {'deck': DECK_NAME, 'limit': 1000})
txt = cnt_res['content'][0]['text']
d = json.loads(txt)
print(f"Total cards now in '{DECK_NAME}': {len(d.get('cards', []))}")
