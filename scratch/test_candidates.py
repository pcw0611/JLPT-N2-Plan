import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
import pykakasi

kks = pykakasi.kakasi()

# Let's inspect kana candidates
KANA_CANDIDATES = {
    'あ': ['a'], 'い': ['i'], 'う': ['u', 'w'], 'え': ['e'], 'お': ['o'],
    'か': ['ka'], 'き': ['ki'], 'く': ['ku'], 'け': ['ke'], 'こ': ['ko'],
    'さ': ['sa'], 'し': ['shi', 'si'], 'す': ['su'], 'せ': ['se'], 'そ': ['so'],
    'た': ['ta'], 'ち': ['chi', 'ti'], 'つ': ['tsu', 'tu'], 'て': ['te'], 'と': ['to'],
    'な': ['na'], 'に': ['ni'], 'ぬ': ['nu'], 'ね': ['ne'], 'の': ['no'],
    'は': ['ha', 'wa'], 'ひ': ['hi'], 'ふ': ['fu', 'hu'], 'へ': ['he', 'e'], 'ほ': ['ho'],
    'ま': ['ma'], 'み': ['mi'], 'む': ['mu'], 'め': ['me'], 'も': ['mo'],
    'や': ['ya'], 'ゆ': ['yu'], 'よ': ['yo'],
    'ら': ['ra'], 'り': ['ri'], 'る': ['ru'], 'れ': ['re'], 'ろ': ['ro'],
    'わ': ['wa'], 'を': ['wo', 'o'], 'ん': ['n', 'nn', 'm'],
    'が': ['ga'], 'ぎ': ['gi'], 'ぐ': ['gu'], 'げ': ['ge'], 'ご': ['go'],
    'ざ': ['za'], 'じ': ['ji', 'zi'], 'ず': ['zu'], 'ぜ': ['ze'], 'ぞ': ['zo'],
    'だ': ['da'], 'ぢ': ['ji', 'di'], 'づ': ['zu', 'du'], 'で': ['de'], 'ど': ['do'],
    'ば': ['ba'], 'び': ['bi'], 'ぶ': ['bu'], 'べ': ['be'], 'ぼ': ['bo'],
    'ぱ': ['pa'], 'ぴ': ['pi'], 'ぷ': ['pu'], 'ぺ': ['pe'], 'ぽ': ['po'],
    'ゔ': ['vu'],
    # Katakana
    'ア': ['a'], 'イ': ['i'], 'ウ': ['u'], 'エ': ['e'], 'オ': ['o'],
    'カ': ['ka'], 'キ': ['ki'], 'ク': ['ku'], 'ケ': ['ke'], 'コ': ['ko'],
    'サ': ['sa'], 'シ': ['shi', 'si'], 'ス': ['su'], 'セ': ['se'], 'ソ': ['so'],
    'タ': ['ta'], 'チ': ['chi', 'ti'], 'ツ': ['tsu', 'tu'], 'テ': ['te'], 'ト': ['to'],
    'ナ': ['na'], 'ニ': ['ni'], 'ヌ': ['nu'], 'ネ': ['ne'], 'ノ': ['no'],
    'ハ': ['ha', 'wa'], 'ヒ': ['hi'], 'フ': ['fu', 'hu'], 'ヘ': ['he', 'e'], 'ホ': ['ho'],
    'マ': ['ma'], 'ミ': ['mi'], 'ム': ['mu'], 'メ': ['me'], 'モ': ['mo'],
    'ヤ': ['ya'], 'ユ': ['yu'], 'ヨ': ['yo'],
    'ラ': ['ra'], 'リ': ['ri'], 'ル': ['ru'], 'レ': ['re'], 'ロ': ['ro'],
    'ワ': ['wa'], 'ヲ': ['wo', 'o'], 'ン': ['n', 'nn', 'm'],
    'ガ': ['ga'], 'ギ': ['gi'], 'ぐ': ['gu'], 'ゲ': ['ge'], 'ゴ': ['go'],
    'ザ': ['za'], 'ジ': ['ji', 'zi'], 'ズ': ['zu'], 'ゼ': ['ze'], 'ゾ': ['zo'],
    'ダ': ['da'], 'ヂ': ['ji', 'di'], 'ヅ': ['zu', 'du'], 'デ': ['de'], 'ド': ['do'],
    'バ': ['ba'], 'ビ': ['bi'], 'ブ': ['bu'], 'ベ': ['be'], 'ボ': ['bo'],
    'パ': ['pa'], 'ピ': ['pi'], 'プ': ['pu'], 'ペ': ['pe'], 'ぽ': ['po'],
    'ヴ': ['vu'],
    'ー': ['a', 'i', 'u', 'e', 'o', '-', ''],
}

# Small kana
SMALL_KANA = {
    'ゃ': ['ya', 'a'], 'ゅ': ['yu', 'u'], 'ょ': ['yo', 'o'],
    'ぁ': ['a'], 'ぃ': ['i'], 'ぅ': ['u'], 'ぇ': ['e'], 'ぉ': ['o'],
    'ャ': ['ya', 'a'], 'ュ': ['yu', 'u'], 'ョ': ['yo', 'o'],
    'ァ': ['a'], 'ィ': ['i'], 'ゥ': ['u'], 'ェ': ['e'], 'ォ': ['o'],
    'ゎ': ['wa'], 'ヮ': ['wa'],
}

def get_candidates(ch, next_ch=None, prev_ch=None, token_ro=None):
    cands = []
    # Space / Punctuation
    if ch in ' \t\u3000':
        return ['', ' ']
    if ch in '!?！？…、。.,・―-~〜()（）「」『』""\'':
        return ['', ' ', ch]
    if 'a' <= ch.lower() <= 'z' or '0' <= ch <= '9':
        return [ch.lower()]

    # Sokuon
    if ch in 'っッ':
        cands.extend(['t', 'k', 's', 'p', 'c', 'd', 'g', 'b', 'z', 'j', 'tsu', 'xtsu', ''])
        return cands

    # Small kana
    if ch in SMALL_KANA:
        return SMALL_KANA[ch] + ['']

    # Basic kana
    if ch in KANA_CANDIDATES:
        cands.extend(KANA_CANDIDATES[ch])
        # If preceding a small kana: e.g. 'き' in 'きゃ' might be 'k' or 'ky'
        if next_ch and next_ch in SMALL_KANA:
            base = KANA_CANDIDATES[ch][0]
            if len(base) >= 2:
                cands.extend([base[0], base[0] + 'y', base[:-1]])
            if ch in 'しシ': cands.extend(['sh', 's'])
            if ch in 'ちチ': cands.extend(['ch', 't'])
            if ch in 'じジ': cands.extend(['j', 'z'])
        return cands

    # Kanji
    # 1. Single kanji conversion via Kakasi
    res = kks.convert(ch)
    if res:
        for r in res:
            hep = r['hepburn'].lower()
            if hep not in cands:
                cands.append(hep)
            kun = r['kunrei'].lower()
            if kun not in cands:
                cands.append(kun)

    # If part of token_ro, any substring might be candidate
    if token_ro:
        token_ro = token_ro.lower()
        if token_ro not in cands:
            cands.append(token_ro)

    return cands

print('Candidates test:')
print('流:', get_candidates('流'))
print('行:', get_candidates('行'))
print('り:', get_candidates('り'))
print('歌:', get_candidates('歌'))
print('は:', get_candidates('は'))
print('っ:', get_candidates('っ'))
