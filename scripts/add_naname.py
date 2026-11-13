import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "청해_어휘", "위치_표현", "독해_어휘", "관용구", "사용자_추가_20261112"]

words_data = [
    {
        "id": "READING-NEWS-0149",
        "kanji": "斜め",
        "kana": "ななめ",
        "meaning": "대각선, 비스듬함, 사선, 비스듬히 (청해 약도·배치도 및 관용구 핵심 어휘)",
        "sentences": "<div class=\"example-ja\"><ruby>郵便局<rt>ゆうびんきょく</rt></ruby>は、<ruby>駅<rt>えき</rt></ruby>の<ruby>交番<rt>こうばん</rt></ruby>の<span class=\"target-word\"><ruby>斜<rt>なな</rt></ruby>め<ruby>向<rt>む</rt></ruby>かい</span>にあります。<br><span style=\"color:#6b7280;font-size:13px\">※ 聴解(약도·배치도) 필수: 「斜め向かい(대각선 맞은편)」「斜め前(비스듬히 앞)」「斜め後ろ(대각선 뒤)」</span><br><ruby>部長<rt>ぶちょう</rt></ruby>は<ruby>朝<rt>あさ</rt></ruby>から<span class=\"target-word\">ご<ruby>機嫌<rt>きげん</rt></ruby><ruby>斜<rt>なな</rt></ruby>め</span>だ。<br><span style=\"color:#6b7280;font-size:13px\">※ 慣用句: 「ご機嫌斜め(기분이 언짢음, 심기 불편)」 독해·어휘 빈출!</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">우체국은 역 파출소의 대각선 맞은편에 있습니다. (청해 길안내/위치 문제) / 부장님은 아침부터 기분이 언짢으시다(심기 불편). (N2 핵심 관용표현)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">斜 (비낄 사 / 훈: ななめ, 음: しゃ)</span></div><div class=\"visual-scan-desc\">곡식을 됫박(斗)에 잴 때 여분(余)을 비스듬히 깎아내는 모습 → 비끼다, 비스듬하다, 대각선 (ななめ)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【훈독】 ななめ (대각선, 비스듬함)</span><span class=\"mnemonic-parts\"><b>斜め向かい(ななめむかい)</b>: 대각선 맞은편<br><b>斜め前(ななめまえ)</b>: 대각선 앞<br><b>ご機嫌斜め(ごきげんななめ)</b>: 기분이 삐딱함/언짢음</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【음독】 しゃ</span><span class=\"mnemonic-parts\">傾斜(けいしゃ): 경사<br>斜面(しゃめん): 사면, 경사면</span></div>"
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
