import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "모의고사_어휘", "생활_어휘", "사용자_추가_20261112"]

word_data = {
    "id": "READING-NEWS-0141",
    "kanji": "臨時",
    "kana": "りんじ",
    "meaning": "임시, 비정기 (정해진 때가 아닌 특별한 때, 일시적인 상황)",
    "sentences": "<div class=\"example-ja\"><ruby>店舗<rt>てんぽ</rt></ruby><ruby>改装<rt>かいそう</rt></ruby>のため、<ruby>明日<rt>あす</rt></ruby>は<span class=\"target-word\"><ruby>臨時<rt>りんじ</rt></ruby></span><ruby>休業<rt>きゅうぎょう</rt></ruby>とさせていただきます。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解(情報検索)・聴解超頻出: 臨時休業(임시 휴업)・臨時列車/臨時便(임시 열차/운항편)・臨時収入(임시 수입)・臨時総会(임시 총회). [대립어] 定期(정기)・常時(상시)</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">매장 리모델링 공사로 인해 내일은 임시 휴업으로 운영하겠습니다. (독해 정보검색 안내문 및 청해 역내/점내 방송의 최다 빈출 단어)</span></div>",
    "mp3": "",
    "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">臨(임할 림) + 時(때 시)</span></div><div class=\"visual-scan-desc\">평상시가 아니라 어떤 특별한 상황에 직면하여(臨) 일시적으로 맞이한 때(時) → 임시 (りんじ)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【臨】 임할 림</span><span class=\"mnemonic-parts\">신하(臣)들이 몸을 숙여 아래를 굽어보며 직면함 (임석/임기응변)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【時】 때 시</span><span class=\"mnemonic-parts\">해(日)가 뜨고 지는 시간이나 때</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【발음 주의】</span><span class=\"mnemonic-parts\">단음 <b>りん + じ = りんじ</b> (장음 りょう・りゅう X)</span></div>"
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
