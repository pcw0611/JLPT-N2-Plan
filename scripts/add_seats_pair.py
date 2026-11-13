import json
import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::14 독해・기사・모의고사 어휘"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["JLPT_N2", "독해_어휘", "모의고사_어휘", "생활_어휘", "사용자_추가_20261112"]

words_data = [
    {
        "id": "READING-NEWS-0144",
        "kanji": "優先席",
        "kana": "ゆうせんせき",
        "meaning": "우선석, 교통약자 배려석 (노약자·임산부·몸이 불편한 분을 위한 좌석)",
        "sentences": "<div class=\"example-ja\"><ruby>電車<rt>でんしゃ</rt></ruby>の<span class=\"target-word\"><ruby>優先席<rt>ゆうせんせき</rt></ruby></span><ruby>付近<rt>ふきん</rt></ruby>では、<ruby>混雑<rt>こんざつ</rt></ruby><ruby>時<rt>じ</rt></ruby>には<ruby>携帯<rt>けいたい</rt></ruby><ruby>電話<rt>でんわ</rt></ruby>の<ruby>電源<rt>でんげん</rt></ruby>を<ruby>切<rt>き</rt></ruby>るよう<ruby>呼<rt>よ</rt></ruby>びかけられている。<br><span style=\"color:#6b7280;font-size:13px\">※ 読解・聴解超頻出: 한국의 '노약자석+임산부석'을 일본에서는 통칭 '優先席'이라 부름. 안내 방송: 「お年寄りや妊婦、お体の不自由な方に席をお譲りください」</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">전철의 우선석(교통약자석) 부근에서는 혼잡 시 휴대폰 전원을 끄도록 당부하고 있다. (청해 차내 방송 및 공공 매너 독해의 최다 빈출 어휘)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">優先(넉넉할 우, 먼저 선) + 席(자리 석)</span></div><div class=\"visual-scan-desc\">배려가 필요한 교통약자에게 먼저(先) 양보하여 우대하는(優) 좌석(席) → 우선석 / 배려석</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【優】 넉넉할/우수할 우</span><span class=\"mnemonic-parts\">사람(亻)에게 근심(憂)을 덜어주듯 상냥하고 우대함 (우선/우대)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【先】 먼저 선</span><span class=\"mnemonic-parts\">발걸음을 남보다 먼저 옮김</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【席】 자리 석</span><span class=\"mnemonic-parts\">천막(广) 안의 자리나 좌석</span></div>"
    },
    {
        "id": "READING-NEWS-0145",
        "kanji": "妊婦",
        "kana": "にんぷ",
        "meaning": "임산부, 임부 (아이를 밴 여성)",
        "sentences": "<div class=\"example-ja\"><span class=\"target-word\"><ruby>妊婦<rt>にんぷ</rt></ruby></span>や<ruby>小<rt>ちい</rt></ruby>さな<ruby>子<rt>こ</rt></ruby>どもを<ruby>連<rt>つ</rt></ruby>れた<ruby>人<rt>ひと</rt></ruby>が<ruby>安心<rt>あんしん</rt></ruby>して<ruby>暮<rt>く</rt></ruby>らせる<ruby>社会<rt>しゃかい</rt></ruby>づくりが<ruby>求<rt>もと</rt></ruby>められる。<br><span style=\"color:#6b7280;font-size:13px\">※ 関連・頻出: 妊婦マーク/マタニティマーク(임산부 배지)・妊娠(にんしん, 임신)・産休(출산휴가). 優先席(우선석)의 대표적 대상자!</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">임산부나 어린아이를 동반한 사람이 안심하고 생활할 수 있는 사회 조성이 요구된다. (N2 독해 복지·저출산 테마 및 공공 매너 빈출)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">妊(아이밸 임) + 婦(며느리/여자 부)</span></div><div class=\"visual-scan-desc\">아이를 품고 임신한(妊) 여성(婦) → 임산부 / 임부 (にんぷ)</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【妊】 아이밸 임</span><span class=\"mnemonic-parts\">여자(女)가 뱃속에 아이의 짐(壬)을 지고 있음 (임신)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【婦】 여자/아내 부</span><span class=\"mnemonic-parts\">비(彗)를 들고 집안일을 정성스레 돌보는 여성(女) (주부/부인)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【발음 주의】</span><span class=\"mnemonic-parts\">단음 <b>にん + ぷ = にんぷ</b> (장음 にんぽう X)</span></div>"
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
