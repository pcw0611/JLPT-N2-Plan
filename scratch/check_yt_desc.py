import re

with open('scratch/yt_test.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

m = re.search(r'"shortDescription":"(.*?)"', text)
if m:
    print("Description:\n", m.group(1).encode('utf-8').decode('unicode_escape', errors='ignore'))
else:
    print("No shortDescription found")
