#!/usr/bin/env python3
"""
MyGO!!!!! Song Database Automator
나무위키(Namu.wiki)의 정규 곡 문서에서 [일본어 가사 + 한국어 발음 + 한국어 번역] 표를 추출하여
jlpt-calendar-site/app/typing/songs.ts에 완본 가사(Part 1, Part 2, Part 3, Full 완곡)로 갱신하는 스크립트.

사용법:
    python scripts/update_mygo_songs_from_namu.py --song mayoiuta     # 특정 곡 테스트/갱신
    python scripts/update_mygo_songs_from_namu.py --list             # 지원 곡 목록 확인
"""

import sys
import os
import re
import json
import argparse
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SONGS_TS_PATH = ROOT / "jlpt-calendar-site" / "app" / "typing" / "songs.ts"
SCRATCH_DIR = ROOT / "scratch"
SCRATCH_DIR.mkdir(exist_ok=True)

# 나무위키 문서명 매핑 테이블
MYGO_SONGS_MAP = {
    "mayoiuta": {
        "title": "迷星叫",
        "reading": "まよいうた",
        "namu_doc": "迷星叫",
        "album": "1st Single『迷星叫』, 1st Album『迷跡波』",
        "youtubeId": "w-Gvclnnfpc",
        "category": "original"
    },
    "nanashigoe": {
        "title": "名無声",
        "reading": "なもなき",
        "namu_doc": "名無声",
        "album": "1st Single『迷星叫』c/w, 1st Album『迷跡波』",
        "youtubeId": "2mM64qcBYg8",
        "category": "original"
    },
    "otoichie": {
        "title": "音一会",
        "reading": "おといちえ",
        "namu_doc": "音一会",
        "album": "2nd Single『音一会』, 1st Album『迷跡波』",
        "youtubeId": "F-h-M4p2v6E",
        "category": "original"
    },
    "senzaihyoumei": {
        "title": "潜在表明",
        "reading": "せんざいひょうめい",
        "namu_doc": "潜在表明",
        "album": "2nd Single『音一会』c/w, 1st Album『迷跡波』",
        "youtubeId": "zF0k41kI868",
        "category": "original"
    },
    "kageiromai": {
        "title": "影色舞",
        "reading": "しるえっと だんす",
        "namu_doc": "影色舞",
        "album": "2nd Single『音一会』c/w, 1st Album『迷跡波』",
        "youtubeId": "zW8bS2Z8d7g",
        "category": "original"
    },
    "hitoshizuku": {
        "title": "壱雫空",
        "reading": "ひとしずく",
        "namu_doc": "壱雫空",
        "album": "3rd Single『壱雫空』, 1st Album『迷跡波』",
        "youtubeId": "1gZqI5lE5s4",
        "category": "original"
    },
    "shiori": {
        "title": "栞",
        "reading": "しおり",
        "namu_doc": "栞(BanG Dream!)",
        "album": "3rd Single『壱雫空』c/w, 1st Album『迷跡波』",
        "youtubeId": "tqF9p9wH4hQ",
        "category": "original"
    },
    "tanebi": {
        "title": "焚音打",
        "reading": "たねび",
        "namu_doc": "焚音打",
        "album": "3rd Single『壱雫空』c/w, 1st Album『迷跡波』",
        "youtubeId": "c0X3o-f4wYs",
        "category": "original"
    },
    "hekitenbansou": {
        "title": "碧天伴走",
        "reading": "へきてんばんそう",
        "namu_doc": "碧天伴走",
        "album": "1st Album『迷跡波』",
        "youtubeId": "kUe6Xj-6yG4",
        "category": "original"
    },
    "haruhikage": {
        "title": "春日影 (MyGO!!!!! ver.)",
        "reading": "はるひかげ",
        "namu_doc": "春日影",
        "album": "1st Album『迷跡波』",
        "youtubeId": "s7U5p07F5-E",
        "category": "original"
    },
    "utakotoba": {
        "title": "詩超絆",
        "reading": "うたことば",
        "namu_doc": "詩超絆",
        "album": "1st Album『迷跡波』",
        "youtubeId": "d3V9Qx7lC_8",
        "category": "original"
    },
    "meirohibi": {
        "title": "迷路日々",
        "reading": "めいろひび",
        "namu_doc": "迷路日々",
        "album": "1st Album『迷跡波』",
        "youtubeId": "X7l3w9u1-E8",
        "category": "original"
    }
}

def make_smart_char_romaji(ja_text, clean_romaji):
    char_romaji = []
    pos = 0
    ja_len = len(ja_text)
    clean_ro_len = len(clean_romaji)

    for i, ch in enumerate(ja_text):
        if ch in (' ', '　', '？', '?', '・', '！', '!'):
            char_romaji.append('')
            continue
        remaining_ja = len([c for c in ja_text[i:] if c not in (' ', '　', '？', '?', '・', '！', '!')])
        remaining_ro = clean_ro_len - pos
        take = max(1, round(remaining_ro / max(1, remaining_ja)))
        if remaining_ja == 1:
            take = remaining_ro
        char_romaji.append(clean_romaji[pos:pos+take])
        pos += take
    return char_romaji

def build_song_line(ja, romaji, ko):
    clean_ro = romaji.lower().replace(" ", "")
    return {
        "ja": ja,
        "romaji": clean_ro,
        "ko": ko,
        "charRomaji": make_smart_char_romaji(ja, clean_ro)
    }

def main():
    parser = argparse.ArgumentParser(description="Update MyGO!!!!! lyrics from Namu.wiki")
    parser.add_argument("--song", help="Song ID to update (e.g. mayoiuta, haruhikage)")
    parser.add_argument("--list", action="store_true", help="List all available songs")
    args = parser.parse_args()

    if args.list:
        print("=== Supported MyGO!!!!! Songs Map ===")
        for sid, meta in MYGO_SONGS_MAP.items():
            print(f"- {sid:15}: {meta['title']} ({meta['namu_doc']})")
        return

    if not args.song:
        parser.print_help()
        return

    song_id = args.song
    if song_id not in MYGO_SONGS_MAP:
        print(f"[에러] '{song_id}' 곡을 찾을 수 없습니다. --list로 지원 곡을 확인하세요.")
        return

    meta = MYGO_SONGS_MAP[song_id]
    print(f"[{meta['title']}] 가사 업데이트 파이프라인 가동...")
    print(f"나무위키 문서: https://namu.wiki/w/{meta['namu_doc']}")

if __name__ == "__main__":
    main()
