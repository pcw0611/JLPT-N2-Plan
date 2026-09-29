# -*- coding: utf-8 -*-
import urllib.request
import re
import urllib.parse
import socket
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

_orig = socket.getaddrinfo
def _ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _ipv4

def find_yt(query):
    url = 'https://www.youtube.com/results?search_query=' + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'\"videoId\":\"([a-zA-Z0-9_-]{11})\"', html)
            # return unique first few
            seen = set()
            res = []
            for m in matches:
                if m not in seen:
                    seen.add(m)
                    res.append(m)
            return res[:3]
    except Exception as e:
        print('Error for', query, e)
        return []

songs = [
    ("mayoiuta", "MyGO!!!!! 迷星叫 MV"),
    ("nanashigoe", "MyGO!!!!! 名無声 MV"),
    ("otoichie", "MyGO!!!!! 音一会 MV"),
    ("senzaihyoumei", "MyGO!!!!! 潜在表明 MV"),
    ("kageiromai", "MyGO!!!!! 影色舞 MV"),
    ("hitoshizuku", "MyGO!!!!! 壱雫空"),
    ("shiori", "MyGO!!!!! 栞"),
    ("tanebi", "MyGO!!!!! 焚音打"),
    ("hekitenbansou", "MyGO!!!!! 碧天伴走 MV"),
    ("utaimashou", "MyGO!!!!! 歌いましょう鳴らしましょう MV"),
    ("haruhikage", "MyGO!!!!! 春日影 MV"),
    ("utakotoba", "MyGO!!!!! 詩超絆 MV"),
    ("meirohibi", "MyGO!!!!! 迷路日々"),
    ("noroshi", "MyGO!!!!! 無路矢 MV"),
    ("sasunso", "MyGO!!!!! 砂寸奏 MV"),
    ("kaisoufu", "MyGO!!!!! 回層浮 MV"),
    ("shokyuusei", "MyGO!!!!! 処救生 MV"),
    ("hashidoyama", "MyGO!!!!! 端程山"),
    ("rinpuu", "MyGO!!!!! 輪符雨"),
    ("kokairou", "MyGO!!!!! 孤壊牢"),
    ("hoshuudou", "MyGO!!!!! 歩拾道"),
    ("meigenon", "MyGO!!!!! 明弦音"),
    ("kadagen", "MyGO!!!!! 過惰幻"),
    ("yaonzen", "MyGO!!!!! 夜隠染"),
    ("mushuutou", "MyGO!!!!! 霧周途"),
    ("egakumirai", "MyGO!!!!! エガクミライ"),
    ("shoumeisanka", "MyGO!!!!! 証命讃歌"),
    ("nonbreath", "MyGO!!!!! ノンブレス・オブリージュ"),
    ("kiminokamisama", "MyGO!!!!! 君の神様になりたい"),
    ("charles", "MyGO!!!!! シャルル"),
    ("moudoku", "MyGO!!!!! 猛独が襲う"),
    ("swim", "MyGO!!!!! swim"),
    ("seishuncomplex", "MyGO!!!!! 青春コンプレックス"),
    ("whitenoise", "MyGO!!!!! ホワイトノイズ"),
    ("soraniutaeba", "MyGO!!!!! 空に歌えば"),
    ("zattou", "MyGO!!!!! 雑踏、僕らの街")
]

for sid, q in songs:
    vids = find_yt(q)
    print(f'"{sid}": "{vids[0] if vids else ""}", // {q}')
