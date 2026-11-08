# -*- coding: utf-8 -*-
"""
Add 稼ぐ (かせぐ) and 経済 (けいざい) to Deck 15
"""

import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECK_NAME = "JLPT N2::15 실생활・N1 고급어휘 맛보기"
MODEL_NAME = "JLPT 한권으로 끝내기 단어장"
TAGS = ["맛보기_어휘", "실생활_일본어", "N2_핵심어휘", "경제_어휘"]

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
        for line in resp.read().decode('utf-8').splitlines():
            if line.startswith('data: '):
                return json.loads(line[6:])['result']

cards_to_add = [
    {
        "id": "SAMPLE-VERB-025",
        "kanji": "稼ぐ",
        "kana": "かせぐ",
        "meaning": "돈을 벌다, 벌이를 하다; (시간·점수를) 벌다/얻다",
        "sentences": "<div class=\"example-ja\"><ruby>留学<rt>りゅうがく</rt></ruby><ruby>費用<rt>ひよう</rt></ruby>を<span class=\"target-word\"><ruby>稼<rt>かせ</rt></ruby>ぐ</span>ために、<ruby>夜遅<rt>よるおそ</rt></ruby>くまでアルバイトをした。<br><span style=\"color:#6b7280;font-size:13px\">※ 警察が到着するまでの「時間を稼ぐ（じかんをかせぐ）」ことができた。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">유학 비용을 벌기 위해 밤늦게까지 아르바이트를 했다. (경찰이 도착할 때까지의 '시간을 벌' 수 있었다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">稼(심을/벌 가)</span></div><div class=\"visual-scan-desc\">벼(禾)를 부지런히 가꾸어 집(家)으로 수확해 들여 양식을 마련함 → 농사지어 벌다/돈을 벌다</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【稼】 일할/벌 가</span><span class=\"mnemonic-parts\">禾(벼 화) + 家(집 가) → 집안의 생계를 위해 곡식을 수확함 (가동/출가)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">★ 필수 연어</span><span class=\"mnemonic-parts\">金を稼ぐ(돈을 벌다), 時間を稼ぐ(시간을 벌다), 点数を稼ぐ(점수를 따다/벌다)</span></div>"
    },
    {
        "id": "SAMPLE-N1-026",
        "kanji": "経済",
        "kana": "けいざい",
        "meaning": "경제, 살림살이; 절약 (경세제민: 세상을 다스리고 백성을 구함에서 유래)",
        "sentences": "<div class=\"example-ja\"><ruby>世界<rt>せかい</rt></ruby><span class=\"target-word\"><ruby>経済<rt>けいざい</rt></ruby></span>の<ruby>回復<rt>かいふく</rt></ruby>には、まだかなりの<ruby>時間<rt>じかん</rt></ruby>がかかりそうだ。<br><span style=\"color:#6b7280;font-size:13px\">※ 電車よりバスを使う方が、費用的にずっと経済的（けいざいてき）だ。</span></div><div class=\"example-ko\"><span class=\"translation-label\">해석</span><span class=\"translation-text\">세계 경제의 회복에는 아직 상당한 시간이 걸릴 것 같다. (전철보다 버스를 이용하는 편이 비용적으로 훨씬 경제적(절약적)이다.)</span></div>",
        "mp3": "",
        "hanja_mnemonic": "<div class=\"visual-scan-item\"><div class=\"visual-scan-header\"><span class=\"visual-scan-badge\">経(지날/다스릴 경) + 済(건널/구제할 제)</span></div><div class=\"visual-scan-desc\">고대 동양 사상의 '経世済民(경세제민: 세상을 다스려 백성을 고통에서 구제함)'의 줄임말 → 근대 Economy의 번역어</div></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【経】 다스릴 경</span><span class=\"mnemonic-parts\">실(糸)의 날실처럼 근본이 되는 도리를 펴서 다스림 (경영/경력)</span></div><div class=\"mnemonic-item\"><span class=\"mnemonic-char\">【済】 건널/구제할 제</span><span class=\"mnemonic-parts\">물(氵)을 건너듯 백성을 어려움에서 구제함 (구제/결제)</span></div>"
    }
]

notes = []
for c in cards_to_add:
    notes.append({
        "fields": {
            "id": c["id"],
            "kanji": c["kanji"],
            "kana": c["kana"],
            "meaning": c["meaning"],
            "sentences": c["sentences"],
            "mp3": c["mp3"],
            "hanja_mnemonic": c["hanja_mnemonic"]
        },
        "tags": TAGS
    })

res = call_mcp('add_notes', {
    'deck_name': DECK_NAME,
    'model_name': MODEL_NAME,
    'notes': notes,
    'allow_duplicate': True
})

print("Result:", json.dumps(res, indent=2, ensure_ascii=False))

# Verify final card count in Deck 15
stats = call_mcp('cards_stats', {'deck': DECK_NAME})
cards = json.loads(stats['content'][0]['text'])['cards']
print(f"Total cards now in '{DECK_NAME}': {len(cards)}")
