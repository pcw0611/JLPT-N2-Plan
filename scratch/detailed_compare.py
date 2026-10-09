import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    vtt_lines = f.readlines()

def to_sec(ts):
    parts = ts.split(':')
    return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])

cues = []
current_start = None
current_end = None
current_text = []

for line in vtt_lines:
    m = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})', line)
    if m:
        if current_start is not None and current_text:
            cleaned = " ".join(current_text)
            cues.append((current_start, current_end, cleaned))
        current_start = to_sec(m.group(1))
        current_end = to_sec(m.group(2))
        current_text = []
    elif current_start is not None and line.strip() and not line.startswith('NOTE') and not line.startswith('WEBVTT'):
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean:
            current_text.append(clean)

if current_start is not None and current_text:
    cues.append((current_start, current_end, " ".join(current_text)))

SLICES_EXAM2 = [
    (75, "問題1 3番 (留学生 役割分担/調べる国)", 190.0, 276.0),
    (76, "問題1 4番 (女の学生 応募申請書)", 276.0, 361.0),
    (77, "問題1 5番 (男の人 植物 日光窓際)", 361.0, 462.0),
    (78, "問題2 1番 (アナウンサー評価点)", 462.0, 572.0),
    (80, "問題2 3番 (着なくなったシャツ クッションカバー)", 680.0, 778.0),
    (82, "問題2 5番 (海岸 流木 イス・テーブル)", 892.0, 1026.0),
    (85, "問題3 2番 (地方への移住 支援)", 1356.0, 1459.0),
    (86, "問題3 3番 (果樹園 リンゴ ネズミ被害工夫)", 1459.0, 1561.0),
    (88, "問題3 5番 (和紙職人 きっかけ)", 1655.0, 1755.0),
    (89, "問題4 1番", 1805.0, 1835.0),
    (90, "問題4 2番", 1835.0, 1865.0),
    (91, "問題4 3番", 1865.0, 1895.0),
    (95, "問題4 7番 (今日の作業はこの辺で切り上げましょうか)", 1984.0, 2022.0),
    (97, "問題4 9番 (今日の花火大会は延期にしましょう)", 2049.0, 2087.0),
    (98, "問題4 10番 (課長の代わりに進行役)", 2087.0, 2119.0),
    (99, "問題4 11番 (私どもではお引き受けいたしかねます)", 2119.0, 2145.0),
    (101, "문제5 2번 (留学・寮 タイプ1)", 2326.0, 2515.0),
]

with open('scratch/perfect_dialogues_25.json', 'r', encoding='utf-8') as f:
    dialogues = json.load(f)

for qid, label, start_s, end_s in SLICES_EXAM2:
    # Build deduped stream of text for this interval
    text_chunks = []
    last_chunk = ""
    for c_start, c_end, c_text in cues:
        if (c_start >= start_s and c_start <= end_s) or (c_end >= start_s and c_end <= end_s):
            # VTT lines often duplicate the previous line as karaoke
            words = c_text.split()
            for w in words:
                if not text_chunks or text_chunks[-1] != w:
                    text_chunks.append(w)
    
    clean_audio_text = "".join(text_chunks)
    # clean repetition where lines repeat
    # Actually let's just print unique lines
    unique_lines = []
    for c_start, c_end, c_text in cues:
        if (c_start >= start_s and c_start <= end_s) or (c_end >= start_s and c_end <= end_s):
            lines = c_text.split('\n')
            for l in lines:
                l_s = l.strip()
                if l_s and (not unique_lines or unique_lines[-1] != l_s):
                    unique_lines.append(l_s)

    print(f"\n==================== Q{qid}: {label} ====================")
    print(f"AUDIO RAW:")
    full_str = " ".join(unique_lines)
    print(full_str[:300] + ("..." if len(full_str) > 300 else ""))
    print("\nCURRENT SCRIPT:")
    for d in dialogues.get(f"2회_{qid}", []):
        print(f"  {d['speaker']}: {d['ja']}")
