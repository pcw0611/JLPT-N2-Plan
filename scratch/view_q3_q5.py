import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== N2Q3 (問題3) ===")
with open('scratch/transcript_vol2_q3.json', 'r', encoding='utf-8') as f:
    segs3 = json.load(f)

for s in segs3:
    t = s['text']
    if any(k in t for k in ['番', '和紙', 'シャンプー', '絵本', '緑化', '環境', '地域', '祭り', '保存会', '市長']):
        print(f"[{s['start']:6.2f} - {s['end']:6.2f}] {t}")

print("\n=== N2Q5 (問題5) ===")
with open('scratch/transcript_vol2_q5.json', 'r', encoding='utf-8') as f:
    segs5 = json.load(f)

for s in segs5:
    t = s['text']
    if any(k in t for k in ['番', 'アルバイト', 'サクラガエル', '交通安全', '夫婦', 'ツアー', 'ハイキング', '温泉']):
        print(f"[{s['start']:6.2f} - {s['end']:6.2f}] {t}")
