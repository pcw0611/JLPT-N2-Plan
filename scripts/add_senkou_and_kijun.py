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
        "id": "READING-NEWS-0137",
        "kanji": "選考",
        "kana": "せんこう",
        "meaning": "심사, 전형, 선발 (서류 심사·입사 시험·장학생 선발 등에서 지원자를 심사하여 뽑음)",
        "sentences": "<div class=\"example-ja\"><ruby>厳正<rt>げんせい</rt></ruby>な<span class=\"target-word\"><ruby>選考<rt>せんこう</rt></ruby></span>の<ruby>結果<rt>けっか</rt></ruby>、<ruby>採用<rt>さいよう</rt></ruby><ruby>候補者<rt>こうほしゃ</rt></ruby>が<ruby>決定<rt>けってい</rt></ruby>した。<br><span style=\"color:#6b7280;font-size:13px\">※ 関連・頻出: 書類選考(서류 심사/전형)・一次選考(1차 전형)・選考基準(심사 기준). [동음이의어 주의] 専攻(전공)・先行(선행)</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">엄정한 심사(전형) 결과, 채용 후보자가 결정되었다. (정보검색 안내문 및 실무 비즈니스 독해의 최다 빈출 단어)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">選(가릴/뽑을 선) + 考(생각할/살필 고)</span></div><div class=\"visual-scan-desc\">지원자 중에서 적임자를 가려내고(選) 깊이 살펴서(考) 선발·심사함 → 전형 / 심사</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【選】 가릴/뽑을 선</span><span class=\"mnemonic-parts\">손(巳)으로 함께(共) 골라내어 길(辶)을 가게 함 (선택/선발)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【考】 생각할/살필 고</span><span class=\"mnemonic-parts\">노인(耂)처럼 지혜롭게 깊이 생각하고 검토함 (고려/시험)</span></div>"
    },
    {
        "id": "READING-NEWS-0138",
        "kanji": "基準",
        "kana": "きじゅん",
        "meaning": "기준, 척도, 표준 (사물의 가치·행동·판단의 척도가 되는 표준 규격)",
        "sentences": "<div class=\"example-ja\"><ruby>明確<rt>めいかく</rt></ruby>な<ruby>判断<rt>はんだん</rt></ruby><span class=\"target-word\"><ruby>基準<rt>きじゅん</rt></ruby></span>を<ruby>設<rt>もう</rt></ruby>けることで、<ruby>評価<rt>ひょうか</rt></ruby>の<ruby>公平性<rt>こうへいせい</rt></ruby>を<ruby>保<rt>たも</rt></ruby>つ。<br><span style=\"color:#6b7280;font-size:13px\">※ 関連・慣用: 基準を満たす(기준을 충족하다)・選考基準(심사 기준)・合格基準(합격 기준). [구별] 規準(도덕적 규범 척도)</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">명확한 판단 기준을 마련함으로써 평가의 공정성을 유지한다. (독해 지문의 논리적 근거 제시 및 안내문의 필수 조건 단어)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">基(터 기) + 準(수평/본받을 준)</span></div><div class=\"visual-scan-desc\">건물의 밑바탕이 되는 터(基)처럼 흔들리지 않고 수평(準)을 맞추는 표준 → 기준 / 척도</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【基】 터 기</span><span class=\"mnemonic-parts\">흙(土) 위에 키(其)로 다져놓은 기초와 터</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【準】 수평/본받을 준</span><span class=\"mnemonic-parts\">물(氵)의 수평과 매(隼)의 날카로운 눈금처럼 정확한 표준</span></div>"
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

# Check final count
cnt_res = call_mcp('cards_stats', {'deck': DECK_NAME, 'limit': 1000})
txt = cnt_res['content'][0]['text']
d = json.loads(txt)
print(f"Total cards now in '{DECK_NAME}': {len(d.get('cards', []))}")
