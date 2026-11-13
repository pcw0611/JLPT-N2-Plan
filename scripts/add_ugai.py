import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "모의고사_어휘", "생활_어휘", "사용자_추가_20261112"]

word_data = {
    "id": "READING-NEWS-0146",
    "kanji": "うがい",
    "kana": "うがい",
    "meaning": "가글, 양치질, 입가심 (목구멍과 입안을 물로 헹구는 행위)",
    "sentences": "<div class=\"example-ja\"><ruby>風邪<rt>かぜ</rt></ruby>を<ruby>予防<rt>よぼう</rt></ruby>するため、<ruby>外<rt>そと</rt></ruby>から<ruby>帰<rt>かえ</rt></ruby>ったら<ruby>手洗<rt>てあら</rt></ruby>いと<span class=\"target-word\">うがい</span>を<ruby>徹底<rt>てってい</rt></ruby>しましょう。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解・聴解超頻出: 「手洗いとうがい(손 씻기와 가글)」는 일본의 대표적 감기 예방 국민 수칙! [관련어] うがい薬(가글액/양치약)・うがいをする(가글하다)</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">감기를 예방하기 위해, 밖에서 돌아오면 손 씻기와 가글(양치질)을 철저히 합시다. (청해 일상 대화 및 독해 건강·위생 지문 1순위 표현)</span></div>",
    "mp3": "",
    "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">うがい (가글 / 입가심 / 양치질)</span></div><div class=\"visual-scan-desc\">가마우지가 물고기를 삼켰다 토해내는 모습(鵜飼い, うかい)에서 유래하여 입과 목을 물로 헹구는 행위를 뜻함</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【의미 구별】</span><span class=\"mnemonic-parts\">칫솔질(歯磨き, はみがき)과 달리 '물로 목과 입안을 가글하여 헹구는 것'을 의미</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【초빈출 세트】</span><span class=\"mnemonic-parts\"><b>手洗い・うがい (손 씻기와 가글)</b> ➔ 일본 위생 안내문의 영원한 단골 콤보</span></div>"
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
