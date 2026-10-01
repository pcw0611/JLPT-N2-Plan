import sys, io
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/vol2_script.txt', 'r', encoding='utf-8') as f:
    vol2_text = f.read()

# Let's search for keywords in vol2_script.txt
keywords = [
    ("Q76", "休んだときは、私の研究室の前の掲示"),
    ("Q80", "ホテルの予約を一日延ばして"),
    ("Q90", "屋上緑化"),
    ("Q94", "社内アンケート"),
    ("Q97", "プリンター、修理に"),
    ("Q99", "壁の色変えたせいか"),
    ("Q102", "サッカーの決勝戦"),
    ("Q106", "信州へのご旅行")
]

for qid, kw in keywords:
    pos = vol2_text.find(kw)
    print(f"{qid} ('{kw}'): pos = {pos}")
    if pos != -1:
        print(vol2_text[pos-100:pos+200])
        print("="*40)
