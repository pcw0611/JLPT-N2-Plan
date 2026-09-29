import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
import pykakasi
import jaconv

kks = pykakasi.kakasi()

from test_scored_align import align_orig_to_hira_scored, is_kanji, is_kana
from test_kana_to_ro import kana_to_romaji_str

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'export const SONGS:\s*Song\[\]\s*=\s*(\[.*\]);?\s*$', text, re.DOTALL)
songs = json.loads(m.group(1))

def align_line_to_romaji(ja, target_ro):
    tokens = kks.convert(ja)
    char_hiras = []
    
    for t in tokens:
        orig = t['orig']
        hira = jaconv.kata2hira(t['hira'])
        # If token is pure kana or kanji
        sub_hiras = align_orig_to_hira_scored(orig, hira)
        char_hiras.extend(sub_hiras)

    if len(char_hiras) != len(ja):
        print(f"Length mismatch: len(char_hiras)={len(char_hiras)}, len(ja)={len(ja)}")
        return None

    # Step 2: Convert char_hiras to approximate romaji
    raw_char_ro = []
    for i, ch in enumerate(ja):
        h = char_hiras[i]
        if ch in ' 　':
            raw_char_ro.append(' ' if ' ' in target_ro else '')
            continue
        if ch in '!?！？…、。.,・―-~〜()（）「」『』""\'':
            raw_char_ro.append('')
            continue
        if 'a' <= ch.lower() <= 'z' or '0' <= ch <= '9':
            raw_char_ro.append(ch.lower())
            continue

        # Look ahead for sokuon consonant
        next_consonant = ''
        if h == 'っ' and i + 1 < len(ja):
            next_h = char_hiras[i+1]
            next_ro = kana_to_romaji_str(next_h)
            if next_ro:
                next_consonant = next_ro[0]

        ro = kana_to_romaji_str(h, next_consonant)
        raw_char_ro.append(ro)

    # Step 3: Align raw_char_ro slices with target_ro using DP
    # We want to partition target_ro into len(ja) slices
    n = len(ja)
    m = len(target_ro)

    # dp[i][j] = best alignment of ja[:i] with target_ro[:j]
    dp = {}
    dp[(0, 0)] = (0, [])

    for i in range(n):
        expected = raw_char_ro[i]
        ch = ja[i]

        for j in range(m + 1):
            if (i, j) not in dp:
                continue
            cur_score, history = dp[(i, j)]

            # Candidate lengths in target_ro
            # Usually len(expected) +/- 1 or 2
            cand_lens = set([len(expected)])
            if ch in ' はへを':
                cand_lens.update([0, 1, 2])
            if ch in 'んン':
                cand_lens.update([1, 2])
            if ch in 'っッ':
                cand_lens.update([0, 1, 2, 3])
            if ch in ' 　!?！？…、。.,・―-~〜()（）「」『』""\'':
                cand_lens.update([0, 1])
            # Also allow slight variation for kanji
            for delta in [-2, -1, 1, 2, 3]:
                if len(expected) + delta >= 0:
                    cand_lens.add(len(expected) + delta)

            for l in sorted(cand_lens):
                if j + l <= m:
                    slice_str = target_ro[j:j+l]
                    # Score
                    score = 0
                    if slice_str == expected:
                        score = 100
                    elif slice_str.lower() == expected.lower():
                        score = 90
                    # ha vs wa
                    elif ch in 'は' and slice_str in ['ha', 'wa']:
                        score = 95
                    elif ch in 'を' and slice_str in ['wo', 'o']:
                        score = 95
                    elif ch in 'へ' and slice_str in ['he', 'e']:
                        score = 95
                    elif ch in 'んン' and slice_str in ['n', 'nn', 'm']:
                        score = 95
                    elif ch in 'っッ' and len(slice_str) == 1 and l == 1:
                        score = 85
                    elif ch in ' 　!?！？…、。.,・―-~〜()（）「」『』""\'' and l == 0:
                        score = 90
                    else:
                        # Character overlap
                        overlap = sum(1 for c1, c2 in zip(slice_str, expected) if c1 == c2)
                        score = max(0, overlap * 20 - abs(len(slice_str) - len(expected)) * 15)

                    new_score = cur_score + score
                    key = (i + 1, j + l)
                    if key not in dp or new_score > dp[key][0]:
                        dp[key] = (new_score, history + [slice_str])

    if (n, m) in dp:
        res = dp[(n, m)][1]
        return res

    # Fallback if no exact path reaches (n, m):
    # Proportional
    print(f"Fallback proportional for: {ja} (ro={target_ro})")
    res = []
    pos = 0
    for i in range(n):
        rem_chars = n - i
        rem_ro = m - pos
        take = max(1, round(rem_ro / rem_chars))
        if i == n - 1:
            take = rem_ro
        res.append(target_ro[pos:pos+take])
        pos += take
    return res

# Test on first 10 lines of song 1
part1_lines = songs[0]['parts'][0]['lines']
for line in part1_lines[:6]:
    ja = line['ja']
    ro = line['romaji']
    aligned = align_line_to_romaji(ja, ro)
    print("JA: ", ja)
    print("RO: ", ro)
    print("CR: ", aligned)
    print("EQ? ", "".join(aligned) == ro, f"len={len(aligned)} vs {len(ja)}")
    print("-"*60)
