import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('scratch/transcript_vol2_q4.json', 'r', encoding='utf-8') as f:
    segs = json.load(f)

for s in segs:
    t = s['text']
    if any(k in t for k in ['番', '山田', 'プリンター', '壁の色', 'サッカー', 'アンケート', '買い替え', 'レポート', '芝居', 'エアコン']):
        print(f"[{s['start']:6.2f} - {s['end']:6.2f}] {t}")
