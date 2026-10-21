# -*- coding: utf-8 -*-
import json
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pykakasi
from pathlib import Path

kks = pykakasi.kakasi()

# Curated contextual override dictionary for homographs & proper Japanese readings
CONTEXT_OVERRIDES = {
    '雨が降り': '雨<rt>あめ</rt>が降<rt>ふ</rt>り',
    '降り続いた': '降<rt>ふ</rt>り続<rt>つづ</rt>いた',
    '降り始めた': '降<rt>ふ</rt>り始<rt>はじ</rt>めた',
    '降りそう': '降<rt>ふ</rt>りそう',
    '日本の': '日本<rt>にほん</rt>の',
    '日本に': '日本<rt>にほん</rt>に',
    '日本で': '日本<rt>にほん</rt>で',
    '日本人': '日本人<rt>にほんじん</rt>',
    '日本文化': '日本文化<rt>にほんぶんか</rt>',
    '日本国内': '日本国内<rt>にほんこくない</rt>',
    '3日間': '3日間<rt>みっかかん</rt>',
    '一日': '一日<rt>ついたち</rt>',
    '二日': '二日<rt>ふつか</rt>',
    '何気なく': '何気<rt>なにげ</rt>なく',
    '行われ': '行<rt>おこな</rt>われ',
    '行った': '行<rt>おこな</rt>った',
    '行う': '行<rt>おこな</rt>う',
    '見当': '見当<rt>けんとう</rt>',
    '色あせて': '色<rt>いろ</rt>あせて',
    '辛い経験': '辛<rt>つら</rt>い経験<rt>けいけん</rt>',
    '辛い思い': '辛<rt>つら</rt>い思<rt>おも</rt>い',
    '角を': '角<rt>かど</rt>を',
    '道角': '道角<rt>みちかど</rt>',
    '開かれた': '開<rt>ひら</rt>かれた',
    '開いて': '開<rt>ひら</rt>いて',
    'お目にかかる': 'お目<rt>め</rt>にかかる',
    'おいでになる': 'おいでになる',
    'お詫び': 'お詫<rt>わ</rt>び',
    'ご覧': 'ご覧<rt>らん</rt>',
}

def to_ruby_sentence(text):
    if not text:
        return ''
    
    # Pre-substitute context overrides with unique placeholders
    placeholders = {}
    idx = 0
    work_text = text
    for phrase, replacement in CONTEXT_OVERRIDES.items():
        if phrase in work_text:
            token = f'__PH_{idx}__'
            # Format replacement as ruby tags
            ruby_rep = re.sub(r'([^<]+)<rt>([^<]+)</rt>', r'<ruby>\1<rt>\2</rt></ruby>', replacement)
            placeholders[token] = ruby_rep
            work_text = work_text.replace(phrase, token)
            idx += 1
            
    # Convert remainder with pykakasi
    converted = kks.convert(work_text)
    result_parts = []
    for item in converted:
        orig = item['orig']
        hira = item['hira']
        
        # If it's one of our placeholders
        found_ph = False
        for token, rep in placeholders.items():
            if token in orig:
                orig = orig.replace(token, rep)
                found_ph = True
        if found_ph:
            result_parts.append(orig)
            continue
            
        if orig != hira and any('\u4e00' <= ch <= '\u9fff' for ch in orig):
            # Strip trailing okurigana matching hiragana
            i = 0
            while i < len(orig) and i < len(hira) and orig[-(i+1)] == hira[-(i+1)]:
                i += 1
            if i > 0:
                kanji_part = orig[:-i]
                okuri_part = orig[-i:]
                reading_part = hira[:-i]
                result_parts.append(f'<ruby>{kanji_part}<rt>{reading_part}</rt></ruby>{okuri_part}')
            else:
                result_parts.append(f'<ruby>{orig}<rt>{hira}</rt></ruby>')
        else:
            result_parts.append(orig)
            
    res = ''.join(result_parts)
    # Restore any remaining placeholders
    for token, rep in placeholders.items():
        res = res.replace(token, rep)
    return res

print('Test ruby converter:')
print(to_ruby_sentence('3日間にわたって降り続いた雨が、ようやく上がった。'))
print(to_ruby_sentence('田中先生は今、研究室においでになりますか。'))
print(to_ruby_sentence('先生に直接お目にかかることができて光栄です。'))
