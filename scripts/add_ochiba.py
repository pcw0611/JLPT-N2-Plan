import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "모의고사_어휘", "생활_어휘", "사용자_추가_20261112"]

word_data = {
    "id": "READING-NEWS-0143",
    "kanji": "落ち葉",
    "kana": "おちば",
    "meaning": "낙엽, 떨어진 나뭇잎",
    "sentences": "<div class=\"example-ja\"><ruby>秋<rt>あき</rt></ruby>が<ruby>深<rt>ふか</rt></ruby>まり、<ruby>公園<rt>こうえん</rt></ruby>の<ruby>道<rt>みち</rt></ruby>に<span class=\"target-word\"><ruby>落<rt>お</rt></ruby>ち<ruby>葉<rt>ば</rt></ruby></span>が<ruby>一面<rt>いちめん</rt></ruby>に<ruby>広<rt>ひろ</rt></ruby>がっている。<br><span style=\"color:#6b7280;font-size:13px\">※ 発音・連濁注意: 'おちは'가 아닌 탁음 'おちば'! [빈출 연어] 落ち葉を掃く(낙엽을 쓸다)・落ち葉が詰まる(낙엽이 막히다)・落ち葉焚き(낙엽 태우기).</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">가을이 깊어가며 공원 길에 낙엽이 온통 깔려 있다. (N2 독해 수필·묘사 및 문자어휘 연탁 발음 빈출)</span></div>",
    "mp3": "",
    "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">落ち(떨어질 락) + 葉(잎 엽 / 탁음: ば)</span></div><div class=\"visual-scan-desc\">나무에서 땅으로 떨어진(落ち) 나뭇잎(葉) → 낙엽 (おちば)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【落】 떨어질 락 (훈: おちる)</span><span class=\"mnemonic-parts\">풀(艹)과 물방울(氵)이 각자(各) 아래로 떨어짐</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【葉】 잎 엽 (훈: は / 결합 시: ば)</span><span class=\"mnemonic-parts\">풀(艹)과 나무(木)의 잎 (言葉: ことば, 青葉: あおば)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【연탁 발음 주의】</span><span class=\"mnemonic-parts\">뒤에 붙어 탁음화: <b>おち + は ➔ おちば (O)</b></span></div>"
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
