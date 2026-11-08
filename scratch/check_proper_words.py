import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

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

words = [
    ("田中", "たなか"),
    ("佐藤", "さとう"),
    ("鈴木", "すずき"),
    ("山田", "やまだ"),
    ("主任", "しゅにん"),
    ("係長", "かかりちょう"),
    ("商事", "しょうじ"),
    ("物産", "ぶっさん"),
    ("各駅停車", "かくえきていしゃ"),
    ("快速", "かいそく"),
    ("急行", "きゅうこう"),
    ("特急", "とっきゅう"),
    ("早割", "はやわり"),
    ("平日限定", "へいじつげんてい"),
    ("土日祝", "どにちしゅく"),
    ("中央口", "ちゅうおうぐち")
]

for kanji, kana in words:
    res = call_mcp('find_notes', {'query': f'"{kanji}"'})
    data = json.loads(res['content'][0]['text'])
    nids = data.get('noteIds', [])
    print(f"{kanji}({kana}): {len(nids)} notes found")
