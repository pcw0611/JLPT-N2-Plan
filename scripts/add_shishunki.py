import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "모의고사_어휘", "사용자_추가_20261112"]

word_data = {
    "id": "READING-NEWS-0136",
    "kanji": "思春期",
    "kana": "ししゅんき",
    "meaning": "사춘기 (육체적·정신적으로 성인이 되어가는 과도기)",
    "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>思春期<rt>ししゅんき</rt></ruby></span>の<ruby>時期<rt>じき</rt></ruby>には、<ruby>身体<rt>しんたい</rt></ruby>の<ruby>変化<rt>へんか</rt></ruby>だけでなく<ruby>精神的<rt>せいしんてき</rt></ruby>な<ruby>葛藤<rt>かっとう</rt></ruby>も<ruby>大<rt>おお</rt></ruby>きくなる。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解: '養育者(양육자)', '反抗期(반항기)', '自己同一性(아이덴티티/정체성)'와 함께 교육·심리학 지문의 핵심 키워드.</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">사춘기 시기에는 신체의 변화뿐만 아니라 정신적인 갈등도 커진다. (독해 발달심리학 지문의 최다 빈출 테마)</span></div>",
    "mp3": "",
    "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">思(생각 사) + 春(봄 춘) + 期(때/시기 기)</span></div><div class=\"visual-scan-desc\">인생의 봄(春)을 맞아 생각이 깊어지고(思) 감성이 싹트는 시기(期) → 사춘기</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【思】 생각 사</span><span class=\"mnemonic-parts\">밭(田=머리/뇌)과 마음(心)으로 깊이 생각함</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【春】 봄 춘</span><span class=\"mnemonic-parts\">따스한 햇살(日) 아래 풀(艹)이 싹트는 봄</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【期】 기약할/시기 기</span><span class=\"mnemonic-parts\">달(月)이 차고 기우는 일정한 기간이나 시기</span></div>"
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

# Verify card count
cnt_res = call_mcp('cards_stats', {'deck': DECK_NAME, 'limit': 1000})
txt = cnt_res['content'][0]['text']
d = json.loads(txt)
print(f"Total cards now in '{DECK_NAME}': {len(d.get('cards', []))}")
