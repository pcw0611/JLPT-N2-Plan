import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import re
import pykakasi
import jaconv

kks = pykakasi.kakasi()

# Basic Kana to Romaji mapping
KANA_TO_ROMAJI = {
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'を': 'wo', 'ん': 'n',
    'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
    'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
    'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
    'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
    'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
    'ゔ': 'vu',
}

SMALL_KANA_COMPOUNDS = {
    'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
    'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
    'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
    'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
    'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
    'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
    'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
    'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
    'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo',
    'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
    'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
    'てぃ': 'ti', 'でぃ': 'di', 'とぅ': 'tu', 'どぅ': 'du',
    'しぇ': 'she', 'じぇ': 'je', 'ちぇ': 'che',
    'ふぁ': 'fa', 'ふぃ': 'fi', 'ふぇ': 'fe', 'ふぉ': 'fo',
}

def is_kana(c):
    return ('\u3040' <= c <= '\u309f') or ('\u30a0' <= c <= '\u30ff')

def is_kanji(c):
    return ('\u4e00' <= c <= '\u9fff') or ('\u3400' <= c <= '\u4dbf')

KANJI_READINGS_CACHE = {}

def get_kanji_readings(k):
    if k in KANJI_READINGS_CACHE:
        return KANJI_READINGS_CACHE[k]
    res = kks.convert(k)
    readings = set()
    for r in res:
        h = jaconv.kata2hira(r['hira'])
        readings.add(h)
        readings.add(h.rstrip('う').rstrip('い'))
    # Also check common kunyomi from compounds if available
    KANJI_READINGS_CACHE[k] = list(readings)
    return KANJI_READINGS_CACHE[k]

def kana_to_romaji_str(hira_str, next_first_consonant=''):
    """Convert a hiragana string (like 'こう' or 'うた' or 'っ') to romaji."""
    res = ''
    i = 0
    n = len(hira_str)
    while i < n:
        # Check two-char compound
        if i + 1 < n and hira_str[i:i+2] in SMALL_KANA_COMPOUNDS:
            res += SMALL_KANA_COMPOUNDS[hira_str[i:i+2]]
            i += 2
        elif hira_str[i] == 'っ':
            res += next_first_consonant if next_first_consonant else 't'
            i += 1
        elif hira_str[i] == 'ー':
            # Repeat last vowel or empty
            if res and res[-1] in 'aiueo':
                res += res[-1]
            i += 1
        elif hira_str[i] in KANA_TO_ROMAJI:
            res += KANA_TO_ROMAJI[hira_str[i]]
            i += 1
        else:
            # Fallback kakasi
            c_res = kks.convert(hira_str[i])
            if c_res:
                res += c_res[0]['hepburn'].lower()
            else:
                res += hira_str[i].lower()
            i += 1
    return res

print("kana_to_romaji_str test:")
print("こう:", kana_to_romaji_str('こう'))
print("うた:", kana_to_romaji_str('うた'))
print("かん:", kana_to_romaji_str('かん'))
print("じょう:", kana_to_romaji_str('じょう'))
print("っ (before t):", kana_to_romaji_str('っ', 't'))
