import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    vtt_lines = f.readlines()

def to_sec(ts):
    parts = ts.split(':')
    return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])

# Parse all cues
cues = []
current_start = None
current_end = None
current_text = []

for line in vtt_lines:
    m = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})', line)
    if m:
        if current_start is not None and current_text:
            cues.append((current_start, current_end, " ".join(current_text)))
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
    (75, "問題1 3番 (留学生 役割分担/調べる国)", 190.0, 276.0, "e2_q75.mp3"),
    (76, "問題1 4番 (女の学生 応募申請書)", 276.0, 361.0, "e2_q76.mp3"),
    (77, "問題1 5番 (男の人 植物 日光窓際)", 361.0, 462.0, "e2_q77.mp3"),
    (78, "問題2 1番 (アナウンサー評価点)", 462.0, 572.0, "e2_q78.mp3"),
    (80, "問題2 3番 (着なくなったシャツ クッションカバー)", 680.0, 778.0, "e2_q80.mp3"),
    (82, "問題2 5番 (海岸 流木 イス・テーブル)", 892.0, 1026.0, "e2_q82.mp3"),
    (85, "問題3 2番 (地方への移住 支援)", 1356.0, 1459.0, "e2_q85.mp3"),
    (86, "問題3 3番 (果樹園 リンゴ ネズミ被害工夫)", 1459.0, 1561.0, "e2_q86.mp3"),
    (88, "問題3 5番 (和紙職人 きっかけ)", 1655.0, 1755.0, "e2_q88.mp3"),
    (89, "問題4 1番", 1805.0, 1835.0, "e2_q89.mp3"),
    (90, "問題4 2番", 1835.0, 1865.0, "e2_q90.mp3"),
    (91, "問題4 3番", 1865.0, 1895.0, "e2_q91.mp3"),
    (95, "問題4 7番 (今日の作業はこの辺で切り上げましょうか)", 1984.0, 2022.0, "e2_q95.mp3"),
    (97, "問題4 9番 (今日の花火大会は延期にしましょう)", 2049.0, 2087.0, "e2_q97.mp3"),
    (98, "問題4 10番 (課長の代わりに進行役)", 2087.0, 2119.0, "e2_q98.mp3"),
    (99, "問題4 11番 (私どもではお引き受けいたしかねます)", 2119.0, 2145.0, "e2_q99.mp3"),
    (101, "問題5 2番 (留学・寮 タイプ1)", 2326.0, 2515.0, "e2_q101.mp3"),
]

with open('scratch/perfect_dialogues_25.json', 'r', encoding='utf-8') as f:
    dialogues = json.load(f)

for qid, label, start_s, end_s, fn in SLICES_EXAM2:
    key = f"2회_{qid}"
    matched_cues = []
    for c_start, c_end, c_text in cues:
        if (c_start >= start_s and c_start <= end_s) or (c_end >= start_s and c_end <= end_s):
            # deduplicate
            if not matched_cues or matched_cues[-1] != c_text:
                matched_cues.append(c_text)
    
    print(f"\n==================== Q{qid}: {label} ({start_s}s - {end_s}s) ====================")
    print("--- REAL AUDIO VTT TRANSCRIPT ---")
    print(" ".join(matched_cues))
    print("\n--- CURRENT DIALOGUE IN POOL/JSON ---")
    cur = dialogues.get(key, [])
    for line in cur:
        print(f"  {line['speaker']}: {line['ja']}")
