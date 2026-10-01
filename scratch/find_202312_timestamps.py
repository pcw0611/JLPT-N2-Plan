import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/transcript_202312.json', 'r', encoding='utf-8') as f:
    segments = json.load(f)

print(f"Total segments: {len(segments)}")

# Let's search for 問題 markers and 番 markers
for s in segments:
    t = s['text']
    # Check if text contains number markers or problem markers
    if any(k in t for k in ['問題', '番', '留学生', '植物', 'アナウンサー', '着物', '流木', '移住', '果樹園', '伝統工芸', 'タイプ', '寮']):
        print(f"[{s['start']:7.2f} - {s['end']:7.2f}] {t}")
