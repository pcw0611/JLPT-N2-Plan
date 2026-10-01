import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/transcript_202312.json', 'r', encoding='utf-8') as f:
    segments = json.load(f)

def inspect_range(start_t, end_t):
    for s in segments:
        if start_t <= s['start'] <= end_t:
            print(f"[{s['start']:7.2f} - {s['end']:7.2f}] {s['text']}")

print("=== MONDAI 2 (600s - 1100s) ===")
inspect_range(600, 1100)

print("\n=== MONDAI 3 (1350s - 1750s) ===")
inspect_range(1350, 1750)
