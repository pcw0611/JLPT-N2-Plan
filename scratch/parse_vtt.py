import re

with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find timestamps and lines
blocks = re.split(r'\n\n+', text)
cleaned = []
for b in blocks:
    lines = [l.strip() for l in b.splitlines() if l.strip()]
    if len(lines) >= 2 and '-->' in lines[0]:
        time_range = lines[0]
        sub_text = ' '.join(lines[1:])
        # remove vtt tags
        sub_text = re.sub(r'<[^>]+>', '', sub_text)
        if sub_text and (not cleaned or cleaned[-1][1] != sub_text):
            cleaned.append((time_range, sub_text))

print(f"Total subtitle cues: {len(cleaned)}")
print("\nFirst 20 cues:")
for t, s in cleaned[:25]:
    print(f"[{t}] {s}")

# Search for 問題1, 問題2, etc.
for t, s in cleaned:
    if any(k in s for k in ['問題', '１番', '２番', '３番', '４番', '５番', '質問']):
        print(f"-> [{t}] {s}")
