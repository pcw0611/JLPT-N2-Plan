import re

with open('scratch/cleaned_transcript.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_prob = None
current_item = None
current_lines = []

questions = []

for line in lines:
    t, text = line.strip().split(': ', 1)
    if '問題 1' in text or '問題1' in text:
        current_prob = 1
    elif '問題 2' in text or '問題2' in text:
        current_prob = 2
    elif '問題 3' in text or '問題3' in text:
        current_prob = 3
    elif '問題 4' in text or '問題4' in text:
        current_prob = 4
    elif '問題 5' in text or '問題5' in text:
        current_prob = 5

    m = re.search(r'([1-9]|1[0-2])番', text)
    if m:
        item_no = int(m.group(1))
        questions.append((t, current_prob, item_no, text))

print(f"Detected {len(questions)} item marks:")
for t, p, i, txt in questions:
    print(f"[{t}] 問題{p} {i}番: {txt[:50]}")
