import re

with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    text = f.read()

blocks = re.split(r'\n\n+', text)
cleaned = []
for b in blocks:
    lines = [l.strip() for l in b.splitlines() if l.strip()]
    if len(lines) >= 2 and '-->' in lines[0]:
        t = lines[0].split('-->')[0].strip()
        s = ' '.join(lines[1:])
        s = re.sub(r'<[^>]+>', '', s)
        s = re.sub(r'align:start position:0%', '', s).strip()
        if s and (not cleaned or cleaned[-1][1] != s):
            cleaned.append((t, s))

# Find all occurrences of "1番", "2番", etc.
full_text = " ".join([s for t, s in cleaned])

# Let's search for "問題1", "問題2", "問題3", "問題4", "問題5"
print("Cleaned subtitle length:", len(cleaned))
with open('scratch/cleaned_transcript.txt', 'w', encoding='utf-8') as f:
    for t, s in cleaned:
        f.write(f"{t}: {s}\n")

print("Saved scratch/cleaned_transcript.txt")
