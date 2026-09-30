import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_transcript_lines.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Let's extract text by timestamp intervals
# 問題1: 00:00:11 to 00:07:43
# 問題2: 00:07:43 to 00:18:50
# 問題3: 00:18:50 to 00:29:17
# 問題4: 00:29:17 to 00:35:55
# 問題5: 00:35:55 to end

def get_text_range(start_time, end_time):
    res = []
    for l in lines:
        t = l[:12]
        if start_time <= t <= end_time:
            res.append(l[14:].strip())
    return " ".join(res)

with open('scratch/sections_extracted.txt', 'w', encoding='utf-8') as out:
    out.write("=== MONDAI 1 ===\n")
    out.write(get_text_range("00:00:11", "00:07:40") + "\n\n")
    out.write("=== MONDAI 2 ===\n")
    out.write(get_text_range("00:07:40", "00:18:50") + "\n\n")
    out.write("=== MONDAI 3 ===\n")
    out.write(get_text_range("00:18:50", "00:29:15") + "\n\n")
    out.write("=== MONDAI 4 ===\n")
    out.write(get_text_range("00:29:15", "00:35:55") + "\n\n")
    out.write("=== MONDAI 5 ===\n")
    out.write(get_text_range("00:35:55", "00:43:00") + "\n\n")

print("Wrote scratch/sections_extracted.txt")
