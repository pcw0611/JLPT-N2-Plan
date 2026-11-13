import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "모의고사_어휘", "생활_어휘", "사용자_추가_20261112"]

word_data = {
    "id": "READING-NEWS-0140",
    "kanji": "屋根",
    "kana": "やね",
    "meaning": "지붕 (가옥이나 건물의 맨 꼭대기를 덮은 덮개)",
    "sentences": "<div class=\"example-ja\"><ruby>昨夜<rt>さくや</rt></ruby>からの<ruby>大雪<rt>おおゆき</rt></ruby>で、<span class=\"target-word\"><ruby>屋根<rt>やね</rt></ruby></span>に<ruby>雪<rt>ゆき</rt></ruby>が<ruby>深<rt>ふか</rt></ruby>く<ruby>積<rt>つ</rt></ruby>もっている。<br><span style=\"color:#6b7280;font-size:13px\">※ 必須連語: 屋根に雪が積もる(지붕에 눈이 쌓이다)・屋根の雪下ろし(지붕 눈 치우기). [훈독 주의] 음독(おくこん)이 아닌 훈독 'やね'!</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">어젯밤부터 내린 폭설로 지붕에 눈이 깊게 쌓여 있다. (N2 청해 및 독해 일상 묘사의 최빈출 생활 어휘)</span></div>",
    "mp3": "",
    "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">屋(집 옥 / 훈: や) + 根(뿌리 근 / 훈: ね)</span></div><div class=\"visual-scan-desc\">집(屋)의 근본(根)이자 덮개가 되는 구조물 → 지붕 (やね)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【屋】 집 옥 (훈: や)</span><span class=\"mnemonic-parts\">집(尸)에 사람이 머무름 (八百屋: やおや, 部屋: へや)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【根】 뿌리 근 (훈: ね)</span><span class=\"mnemonic-parts\">나무(木)의 근본(艮) 뿌리 (屋根: やね, 根気: こんき)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【발음 주의】</span><span class=\"mnemonic-parts\">두 글자 모두 훈독으로 결합한 단어: <b>や(屋) + ね(根) = やね</b></span></div>"
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
