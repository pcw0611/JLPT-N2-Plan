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

def align_orig_to_hira(orig, hira):
    """
    Given orig (e.g. '流行り') and hira (e.g. 'はやり'),
    return a list of hira strings for each character in orig,
    so that len(result) == len(orig) and ''.join(result) == hira.
    """
    # Normalize hira to hiragana
    hira = jaconv.kata2hira(hira)
    orig_norm = jaconv.kata2hira(orig)

    # If orig and hira have same length and all chars match:
    if orig_norm == hira:
        return list(hira)

    # If orig has only 1 character:
    if len(orig) == 1:
        return [hira]

    # Find kana anchors in orig that appear in hira in order
    # Let's do dynamic programming / LCS to find optimal alignment between orig and hira
    n, m = len(orig), len(hira)

    # dp[i][j] = can orig[:i] be mapped to hira[:j]?
    # Store parent pointers
    dp = {}
    dp[(0, 0)] = []

    for i in range(n):
        c = orig[i]
        c_hira = jaconv.kata2hira(c)
        for j in range(m + 1):
            if (i, j) not in dp:
                continue
            history = dp[(i, j)]

            # What lengths of hira can character c take?
            if not is_kanji(c):
                # Kana, punctuation, space, latin
                if c_hira in hira[j:j+1] and j < m and hira[j] == c_hira:
                    # Exact kana match: length 1
                    key = (i + 1, j + 1)
                    if key not in dp:
                        dp[key] = history + [hira[j:j+1]]
                elif c in 'っッ' and j < m:
                    # Sokuon: might match 'っ' in hira or next consonant
                    if hira[j] == 'っ':
                        key = (i + 1, j + 1)
                        if key not in dp:
                            dp[key] = history + ['っ']
                elif c in 'ー':
                    # Chouon
                    key = (i + 1, j + 1) if j < m and hira[j] in 'あいうえおー' else (i + 1, j)
                    if key not in dp:
                        dp[key] = history + [hira[j:key[1]]]
                else:
                    # In case of mismatch or punctuation
                    # Try length 0 or 1
                    for l in [0, 1]:
                        if j + l <= m:
                            key = (i + 1, j + l)
                            if key not in dp:
                                dp[key] = history + [hira[j:j+l]]
            else:
                # Kanji: typically 1 to 4 kana characters (e.g. 1, 2, 3, 4)
                # First let's check single kanji reading from kakasi
                k_res = kks.convert(c)
                k_hira = jaconv.kata2hira(k_res[0]['hira']) if k_res else ''
                
                # Check candidate lengths: 1 to 5
                # Try exact match with k_hira first
                cand_lens = []
                if k_hira and hira[j:].startswith(k_hira):
                    cand_lens.append(len(k_hira))
                for l in range(1, min(6, m - j + 1)):
                    if l not in cand_lens:
                        cand_lens.append(l)

                for l in cand_lens:
                    if j + l <= m:
                        key = (i + 1, j + l)
                        if key not in dp:
                            dp[key] = history + [hira[j:j+l]]

    if (n, m) in dp:
        return dp[(n, m)]

    # Fallback if no exact path found
    # Distribute proportionally
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

# Test on lines from song 1
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
    res = align_orig_to_hira(orig, hira)
    print(f'{orig} ({hira}) -> {res} (sum={"".join(res)})')
