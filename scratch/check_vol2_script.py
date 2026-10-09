import sys, json

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/vol2_script.txt', 'r', encoding='utf-8') as f:
    vol2_text = f.read()

print("Length of vol2_script.txt:", len(vol2_text))

# Let's search for some keywords from Vol 2 questions:
# Q76: 授業を休んだとき
# Q80: お茶の葉
# Q90: 健康のためには
# Q94: 山田さんを除いて
# Q97: プリンター
# Q99: 会議室、壁の色
# Q102: スキー
# Q106: 交通安全
keywords = [
    ("Q76", "授業を休んだとき"),
    ("Q80", "お茶の葉"),
    ("Q90", "健康のためには"),
    ("Q94", "山田さんを除いて"),
    ("Q97", "プリンター"),
    ("Q99", "壁の色"),
    ("Q102", "スキー"),
    ("Q106", "交通安全")
]

for q, kw in keywords:
    pos = vol2_text.find(kw)
    print(f"{q} ({kw}): found at {pos}")
    if pos != -1:
        print("  Snippet:", repr(vol2_text[pos:pos+150]))
