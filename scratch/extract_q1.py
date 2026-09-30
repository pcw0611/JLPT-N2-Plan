import re

with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    text = f.read()

blocks = re.split(r'\n\n+', text)
cleaned = []
for b in blocks:
    lines = [l.strip() for l in b.splitlines() if l.strip()]
    if len(lines) >= 2 and '-->' in lines[0]:
        t = lines[0]
        s = ' '.join(lines[1:])
        s = re.sub(r'<[^>]+>', '', s)
        cleaned.append((t, s))

for t, s in cleaned:
    if '00:00:10' <= t[:8] <= '00:01:45':
        print(f"[{t[:8]}] {s}")
