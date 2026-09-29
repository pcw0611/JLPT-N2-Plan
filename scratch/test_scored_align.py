import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
import pykakasi
import jaconv

kks = pykakasi.kakasi()

def is_kana(c):
    return ('\u3040' <= c <= '\u309f') or ('\u30a0' <= c <= '\u30ff')

def is_kanji(c):
    return ('\u4e00' <= c <= '\u9fff') or ('\u3400' <= c <= '\u4dbf')

# Precompute common kanji readings for fast lookup
KANJI_READINGS_CACHE = {}

def get_kanji_readings(k):
    if k in KANJI_READINGS_CACHE:
        return KANJI_READINGS_CACHE[k]
    res = kks.convert(k)
    readings = set()
    for r in res:
        h = jaconv.kata2hira(r['hira'])
        readings.add(h)
        # Also common variants
        readings.add(h.rstrip('う').rstrip('い'))
    KANJI_READINGS_CACHE[k] = list(readings)
    return KANJI_READINGS_CACHE[k]

def align_orig_to_hira_scored(orig, hira):
    hira = jaconv.kata2hira(hira)
    orig_norm = jaconv.kata2hira(orig)

    if orig_norm == hira:
        return list(hira)
    if len(orig) == 1:
        return [hira]

    n, m = len(orig), len(hira)

    # DP with scoring: best_score[(i, j)] = (max_score, history_list)
    best = {}
    best[(0, 0)] = (0, [])

    for i in range(n):
        c = orig[i]
        c_hira = jaconv.kata2hira(c)

        for j in range(m + 1):
            if (i, j) not in best:
                continue
            cur_score, history = best[(i, j)]

            if not is_kanji(c):
                # Kana anchor
                if j < m and hira[j] == c_hira:
                    key = (i + 1, j + 1)
                    new_score = cur_score + 100  # High bonus for exact kana match
                    if key not in best or new_score > best[key][0]:
                        best[key] = (new_score, history + [hira[j:j+1]])
                elif c in 'っッ' and j < m and hira[j] == 'っ':
                    key = (i + 1, j + 1)
                    new_score = cur_score + 100
                    if key not in best or new_score > best[key][0]:
                        best[key] = (new_score, history + ['っ'])
                elif c in 'ー':
                    # Chouon
                    if j < m and hira[j] in 'あいうえおー':
                        key = (i + 1, j + 1)
                        new_score = cur_score + 50
                        if key not in best or new_score > best[key][0]:
                            best[key] = (new_score, history + [hira[j:j+1]])
                    else:
                        key = (i + 1, j)
                        new_score = cur_score + 10
                        if key not in best or new_score > best[key][0]:
                            best[key] = (new_score, history + [''])
                else:
                    # Fallback for non-matching symbol/punctuation
                    for l in [0, 1]:
                        if j + l <= m:
                            key = (i + 1, j + l)
                            new_score = cur_score
                            if key not in best or new_score > best[key][0]:
                                best[key] = (new_score, history + [hira[j:j+l]])
            else:
                # Kanji
                k_readings = get_kanji_readings(c)
                # Try all candidate lengths 1..5
                for l in range(1, min(6, m - j + 1)):
                    sub = hira[j:j+l]
                    # Score matches with known readings
                    score = 0
                    if sub in k_readings:
                        score = 80
                    elif any(sub.startswith(r) or r.startswith(sub) for r in k_readings if r):
                        score = 40
                    else:
                        score = 10

                    key = (i + 1, j + l)
                    new_score = cur_score + score
                    if key not in best or new_score > best[key][0]:
                        best[key] = (new_score, history + [sub])

    if (n, m) in best:
        return best[(n, m)][1]

    # Fallback proportional
    res = []
    pos = 0
    for i in range(n):
        rem_chars = n - i
        rem_hira = m - pos
        take = max(1, round(rem_hira / rem_chars))
        if i == n - 1:
            take = rem_hira
        res.append(hira[pos:pos+take])
        pos += take
    return res

test_cases = [
    ('交差点', 'こうさてん'),
    ('真ん中', 'まんなか'),
    ('急ぐ', 'いそぐ'),
    ('紛れ', 'まぎれ'),
    ('流行り', 'はやり'),
    ('歌っ', 'うたっ'),
    ('僕', 'ぼく'),
    ('笑い', 'わらい'),
    ('感情', 'かんじょう'),
    ('下書き', 'したがき'),
    ('埋め尽くして', 'うめつくして'),
    ('迷子', 'まいご')
]

for orig, hira in test_cases:
    res = align_orig_to_hira_scored(orig, hira)
    print(f'{orig} ({hira}) -> {res}')
