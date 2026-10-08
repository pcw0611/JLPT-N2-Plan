import sys
import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
import pykakasi

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SCRATCH_DIR = ROOT / "scratch"

kaka = pykakasi.kakasi()

def clean_soup(soup):
    for tag in soup.find_all(['rt', 'rp', 'style', 'script']):
        tag.decompose()
    for br in soup.find_all('br'):
        br.replace_with('__LINEBREAK__')

def make_clean_romaji(ja_text):
    converted = kaka.convert(ja_text)
    ro = "".join(item['hepburn'] for item in converted)
    ro = re.sub(r'[^a-zA-Z0-9]', '', ro).lower()
    return ro

def make_char_romaji(ja_text, clean_ro):
    char_romaji = []
    pos = 0
    clean_ro_len = len(clean_ro)
    delimiters = (' ', '　', '？', '?', '・', '！', '!', '…', '(', ')', '（', '）', '「', '」', '『', '』', '、', '。', ',', '.', '—', '―', '-', '~', '〜', ':', '：')
    for i, ch in enumerate(ja_text):
        if ch in delimiters:
            char_romaji.append('')
            continue
        remaining_ja = len([c for c in ja_text[i:] if c not in delimiters])
        remaining_ro = clean_ro_len - pos
        take = max(1, round(remaining_ro / max(1, remaining_ja)))
        if remaining_ja == 1:
            take = remaining_ro
        char_romaji.append(clean_ro[pos:pos+take])
        pos += take
    return char_romaji

def is_japanese_or_chorus(txt):
    if re.search(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf]', txt):
        return True
    if re.match(r'^[a-zA-Z0-9\s\.,!\?\'"\(\)~—–-]+$', txt) and not re.search(r'[\uac00-\ud7a3]', txt):
        return True
    return False

def clean_lyric_str(s):
    s = s.strip()
    s = re.sub(r'^가사\s*▼\s*', '', s)
    s = re.sub(r'^Full\s*ver\.\s*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'^Instrumental\s*ver\.\s*', '', s, flags=re.IGNORECASE)
    return s.strip()

def smart_parse_lyrics(raw_lines):
    triplets = []
    current_ja = None
    current_pron = None
    current_ko = None

    for line in raw_lines:
        line = clean_lyric_str(line)
        if not line:
            continue
        # 헤더 필터링
        if any(h in line for h in ('작사', '작곡', '편곡', 'BPM', '일러스트', '영상', '투고일', 'TJ', '금영', 'BAND', 'CRYCHIC', 'Full ver.', 'TV ver.', '가사 보기', '수록곡', '난이도 체계', 'Instrumental ver.')):
            continue
        if line.startswith('[') and line.endswith(']'):
            continue

        if is_japanese_or_chorus(line):
            if current_ja:
                triplets.append((current_ja, current_pron or "", current_ko or current_pron or current_ja))
            current_ja = line
            current_pron = None
            current_ko = None
        else:
            if current_ja is not None:
                if current_pron is None:
                    current_pron = line
                elif current_ko is None:
                    current_ko = line
                    triplets.append((current_ja, current_pron, current_ko))
                    current_ja = None
                    current_pron = None
                    current_ko = None

    if current_ja:
        triplets.append((current_ja, current_pron or "", current_ko or current_pron or current_ja))

    return triplets

def extract_from_html_smart(sid, html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    clean_soup(soup)

    # 곡별 정확한 가사 테이블 우선 처리
    if sid == "seishuncomplex":
        tables = soup.find_all('table')
        if len(tables) > 13:
            tbl13 = tables[13]
            trs = [tr.get_text().strip() for tr in tbl13.find_all('tr') if tr.get_text().strip()]
            return smart_parse_lyrics(trs)
            
    if sid == "swim":
        for tbl in soup.find_all('table'):
            txt = tbl.get_text()
            if 'あの日の自分が許せないな' in txt:
                lines = [l.strip() for l in txt.split('__LINEBREAK__') if l.strip()]
                return smart_parse_lyrics(lines)

    if sid == "zattouboku":
        for tbl in soup.find_all('table'):
            txt = tbl.get_text()
            if 'やり残した鼓동' in txt or 'やり残した鼓動が' in txt:
                lines = [l.strip() for l in txt.split('__LINEBREAK__') if l.strip()]
                return smart_parse_lyrics(lines)

    if sid == "moshimoinochi":
        for tbl in soup.find_all('table'):
            txt = tbl.get_text()
            if '月が綺麗な夜に' in txt and '__LINEBREAK__' in txt:
                lines = [l.strip() for l in txt.split('__LINEBREAK__') if l.strip()]
                res = smart_parse_lyrics(lines)
                if len(res) >= 20:
                    return res

    best_triplets = []

    for tbl in soup.find_all('table'):
        tbl_text = tbl.get_text()
        if any(bad in tbl_text for bad in ('난이도 체계', '수록 폴더', '아티스트 명의', '수록곡 일람', '음악 일람', '시리즈 난이도', '[~2021년 수록곡]', 'maimai DX', 'CHUNITHM')):
            continue

        # 케이스 1: 1개 셀에 <br>로 전체 가사가 들어있는 경우
        for tr in tbl.find_all('tr'):
            for td in tr.find_all(['td', 'th']):
                raw_text = td.get_text()
                if '__LINEBREAK__' in raw_text:
                    lines = [l.strip() for l in raw_text.split('__LINEBREAK__') if l.strip()]
                    if len(lines) >= 15:
                        cand = smart_parse_lyrics(lines)
                        if len(cand) > len(best_triplets):
                            best_triplets = cand

        # 케이스 2: tr 단위로 줄바꿈되어 있는 경우
        trs = tbl.find_all('tr')
        if len(trs) >= 15:
            lines = [tr.get_text().strip() for tr in trs if tr.get_text().strip()]
            cand = smart_parse_lyrics(lines)
            if len(cand) > len(best_triplets):
                best_triplets = cand

    return best_triplets

def main():
    extracted_db = {}
    id_aliases = {
        "ouran'in": "ouran",
    }

    files = list(SCRATCH_DIR.glob("namu_*.html"))
    print(f"Smart extracting lyrics from {len(files)} files...")

    for f in sorted(files):
        sid = f.stem.replace("namu_", "")
        html = f.read_text(encoding="utf-8")
        triplets = extract_from_html_smart(sid, html)
        
        if len(triplets) >= 10:
            lines = []
            for ja, pron, ko in triplets:
                clean_ro = make_clean_romaji(ja)
                if not clean_ro:
                    continue
                char_ro = make_char_romaji(ja, clean_ro)
                lines.append({
                    "ja": ja,
                    "romaji": clean_ro,
                    "ko": ko,
                    "charRomaji": char_ro
                })
            extracted_db[sid] = lines
            print(f"[OK] {sid:20} -> {len(lines):2d} lines. First: {lines[0]['ja'][:22]}")
        else:
            print(f"[SKIP] {sid:20} -> {len(triplets)} triplets")

    for alias_id, target_id in id_aliases.items():
        if target_id in extracted_db:
            extracted_db[alias_id] = extracted_db[target_id]
            print(f"[ALIAS] Mapped '{alias_id}' -> '{target_id}' ({len(extracted_db[alias_id])} lines)")

    out_file = SCRATCH_DIR / "all_extracted_lyrics.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(extracted_db, f, ensure_ascii=False, indent=2)

    print(f"\n==========================================")
    print(f"Total {len(extracted_db)} songs extracted to {out_file}!")
    print(f"==========================================")

if __name__ == "__main__":
    main()
