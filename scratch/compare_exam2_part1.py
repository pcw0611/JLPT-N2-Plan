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

SLICES_EXAM2_PART1 = [
    (75, "問題1 3番 (留学生 役割分担/調べる国)", 190.0, 276.0),
    (76, "問題1 4番 (女の学生 応募申請書)", 276.0, 361.0),
    (77, "問題1 5番 (男の人 植物 日光窓際)", 361.0, 462.0),
    (78, "問題2 1番 (アナウンサー評価点)", 462.0, 572.0),
    (80, "問題2 3番 (着なくなったシャツ クッションカバー)", 680.0, 778.0),
    (82, "問題2 5番 (海岸 流木 イス・テーブル)", 892.0, 1026.0),
    (85, "問題3 2番 (地方への移住 支援)", 1356.0, 1459.0),
    (86, "問題3 3番 (果樹園 リンゴ ネズミ被害工夫)", 1459.0, 1561.0),
    (88, "問題3 5番 (和紙職人 きっかけ)", 1655.0, 1755.0),
]

with open('scratch/perfect_dialogues_25.json', 'r', encoding='utf-8') as f:
    dialogues = json.load(f)

for qid, label, start_s, end_s in SLICES_EXAM2_PART1:
    unique_lines = []
    for c_start, c_end, c_text in cues:
        if (c_start >= start_s and c_start <= end_s) or (c_end >= start_s and c_end <= end_s):
            lines = c_text.split('\n')
            for l in lines:
                l_s = l.strip()
                if l_s and (not unique_lines or unique_lines[-1] != l_s):
                    unique_lines.append(l_s)

    print(f"\n==================== Q{qid}: {label} ====================")
    full_str = " ".join(unique_lines)
    print(f"AUDIO RAW: {full_str[:400]}...")
    print("\nCURRENT SCRIPT:")
    for d in dialogues.get(f"2회_{qid}", []):
        print(f"  {d['speaker']}: {d['ja']}")
