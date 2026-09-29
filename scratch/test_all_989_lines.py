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

# Small kana compound split
COMPOUND_SPLIT = {
    'kya': ('ky', 'a'), 'kyu': ('ky', 'u'), 'kyo': ('ky', 'o'),
    'sha': ('sh', 'a'), 'shu': ('sh', 'u'), 'sho': ('sh', 'o'),
    'cha': ('ch', 'a'), 'chu': ('ch', 'u'), 'cho': ('ch', 'o'),
    'nya': ('ny', 'a'), 'nyu': ('ny', 'u'), 'nyo': ('ny', 'o'),
    'hya': ('hy', 'a'), 'hyu': ('hy', 'u'), 'hyo': ('hy', 'o'),
    'mya': ('my', 'a'), 'myu': ('my', 'u'), 'myo': ('my', 'o'),
    'rya': ('ry', 'a'), 'ryu': ('ry', 'u'), 'ryo': ('ry', 'o'),
    'gya': ('gy', 'a'), 'gyu': ('gy', 'u'), 'gyo': ('gy', 'o'),
    'ja': ('j', 'a'), 'ju': ('j', 'u'), 'jo': ('j', 'o'),
    'bya': ('by', 'a'), 'byu': ('by', 'u'), 'byo': ('by', 'o'),
    'pya': ('py', 'a'), 'pyu': ('py', 'u'), 'pyo': ('py', 'o'),
    'ti': ('t', 'i'), 'di': ('d', 'i'), 'tu': ('t', 'u'), 'du': ('d', 'u'),
    'she': ('sh', 'e'), 'je': ('j', 'e'), 'che': ('ch', 'e'),
    'fa': ('f', 'a'), 'fi': ('f', 'i'), 'fe': ('f', 'e'), 'fo': ('f', 'o'),
}

SMALL_KANA_SET = {'ゃ', 'ゅ', 'ょ', 'ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'ャ', 'ュ', 'ョ', 'ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ゎ', 'ヮ'}

def align_line_to_romaji(ja, target_ro):
    tokens = kks.convert(ja)
    char_hiras = []

    for t in tokens:
        orig = t['orig']
        hira = jaconv.kata2hira(t['hira'])
        sub_hiras = align_orig_to_hira_scored(orig, hira)
        char_hiras.extend(sub_hiras)

    # In case length differs from ja
    if len(char_hiras) != len(ja):
        # Fallback character by character
        char_hiras = []
        for ch in ja:
            r = kks.convert(ch)
            char_hiras.append(jaconv.kata2hira(r[0]['hira']) if r else ch)

    # Step 2: Convert char_hiras to approximate romaji with small kana splitting
    raw_char_ro = []
    n = len(ja)
    for i in range(n):
        ch = ja[i]
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

        # Look ahead for compound if next char is small kana
        if i + 1 < n and ja[i+1] in SMALL_KANA_SET:
            next_h = char_hiras[i+1]
            pair_h = h + next_h
            pair_ro = kana_to_romaji_str(pair_h)
            if pair_ro in COMPOUND_SPLIT:
                raw_char_ro.append(COMPOUND_SPLIT[pair_ro][0])
                continue

        # If this char is small kana preceded by a base kana
        if ch in SMALL_KANA_SET and i > 0:
            prev_h = char_hiras[i-1]
            pair_h = prev_h + h
            pair_ro = kana_to_romaji_str(pair_h)
            if pair_ro in COMPOUND_SPLIT:
                raw_char_ro.append(COMPOUND_SPLIT[pair_ro][1])
                continue

        # Sokuon
        next_consonant = ''
        if h == 'っ' and i + 1 < n:
            next_h = char_hiras[i+1]
            next_ro = kana_to_romaji_str(next_h)
            if next_ro:
                next_consonant = next_ro[0]

        ro = kana_to_romaji_str(h, next_consonant)
        raw_char_ro.append(ro)

    # Step 3: Align raw_char_ro slices with target_ro using DP
    m = len(target_ro)
    dp = {}
    dp[(0, 0)] = (0, [])

    for i in range(n):
        expected = raw_char_ro[i]
        ch = ja[i]

        for j in range(m + 1):
            if (i, j) not in dp:
                continue
            cur_score, history = dp[(i, j)]

            cand_lens = set([len(expected)])
            if ch in ' はへを':
                cand_lens.update([0, 1, 2])
            if ch in 'んン':
                cand_lens.update([1, 2])
            if ch in 'っッ':
                cand_lens.update([0, 1, 2, 3])
            if ch in SMALL_KANA_SET:
                cand_lens.update([0, 1, 2])
            if ch in ' 　!?！？…、。.,・―-~〜()（）「」『』""\'':
                cand_lens.update([0, 1])
            for delta in [-2, -1, 1, 2, 3, 4]:
                if len(expected) + delta >= 0:
                    cand_lens.add(len(expected) + delta)

            for l in sorted(cand_lens):
                if j + l <= m:
                    slice_str = target_ro[j:j+l]
                    score = 0
                    if slice_str == expected:
                        score = 100
                    elif slice_str.lower() == expected.lower():
                        score = 90
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
                        overlap = sum(1 for c1, c2 in zip(slice_str, expected) if c1 == c2)
                        score = max(0, overlap * 20 - abs(len(slice_str) - len(expected)) * 12)

                    new_score = cur_score + score
                    key = (i + 1, j + l)
                    if key not in dp or new_score > dp[key][0]:
                        dp[key] = (new_score, history + [slice_str])

    if (n, m) in dp:
        return dp[(n, m)][1]

    # Fallback
    res = []
    pos = 0
    for i in range(n):
        rem_chars = n - i
        rem_ro = m - pos
        take = max(0, round(rem_ro / rem_chars))
        if i == n - 1:
            take = rem_ro
        res.append(target_ro[pos:pos+take])
        pos += take
    return res

total_lines = 0
exact_matches = 0
fallbacks = 0
failures = []

for s in songs:
    for p in s['parts']:
        for line in p['lines']:
            total_lines += 1
            ja = line['ja']
            ro = line['romaji']
            cr = align_line_to_romaji(ja, ro)
            if len(cr) != len(ja) or "".join(cr) != ro:
                failures.append((ja, ro, cr))
            else:
                exact_matches += 1

print(f"Total lines tested: {total_lines}")
print(f"Exact matches: {exact_matches} ({exact_matches/total_lines*100:.1f}%)")
print(f"Failures: {len(failures)}")

if failures:
    for ja, ro, cr in failures[:5]:
        print("FAIL:", ja, "ro:", ro, "cr:", cr)
