import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "모의고사_어휘", "생활_어휘", "사용자_추가_20261112"]

word_data = {
    "id": "READING-NEWS-0142",
    "kanji": "お年寄り",
    "kana": "おとしより",
    "meaning": "노인, 어르신 (나이가 지긋하신 분을 공손하고 정중하게 부르는 표현)",
    "sentences": "<div class=\"example-ja\"><ruby>電車<rt>でんしゃ</rt></ruby>の<ruby>中<rt>なか</rt></ruby>で、<span class=\"target-word\">お<ruby>年寄<rt>としよ</rt></ruby>り</span>に<ruby>席<rt>せき</rt></ruby>を<ruby>譲<rt>ゆず</rt></ruby>る<ruby>姿<rt>すがた</rt></ruby>は<ruby>見<rt>み</rt></ruby>ていて<ruby>微笑<rt>ほほえ</rt></ruby>ましい。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解・聴解超頻出: 고령화 사회·복지 지문 및 안내 방송의 1순위 단어. [유의어] 高齢者(こうれいしゃ)・老人(ろうじん). [연어] お年寄りに席を譲る(어르신께 자리를 양보하다)</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">전철 안에서 어르신에게 자리를 양보하는 모습은 보기에 훈훈하다. (N2 독해 고령화 사회 테마 및 청해 차내 안내 방송의 최다 빈출 어휘)</span></div>",
    "mp3": "",
    "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">お(접두사) + 年(해/나이 년) + 寄り(치우칠/기울어질 기)</span></div><div class=\"visual-scan-desc\">나이(年)가 지긋이 황혼으로 기울어지신(寄り) 어르신을 공손히(お) 지칭 → 어르신, 노인</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【年】 해/나이 년 (훈: とし)</span><span class=\"mnemonic-parts\">한 해 한 해 쌓여가는 나이 (연세)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【寄】 부칠/기울어질 기 (훈: より)</span><span class=\"mnemonic-parts\">어떤 쪽으로 다가가 기울어짐 (寄り添う/立ち寄る)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【뉘앙스】</span><span class=\"mnemonic-parts\">건조한 '老人(노인)'보다 배려와 공경을 담은 정중한 일상 표준어</span></div>"
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
