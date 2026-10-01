import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/transcript_202312.json', 'r', encoding='utf-8') as f:
    segments = json.load(f)

for s in segments:
    if 650 <= s['start'] <= 920:
        print(f"[{s['start']:7.2f} - {s['end']:7.2f}] {s['text']}")
