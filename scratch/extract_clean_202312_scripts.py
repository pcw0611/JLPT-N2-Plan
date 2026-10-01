import re
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's clean the VTT
blocks = re.split(r'\n\n+', text)
cues = []
for b in blocks:
    lines = [l.strip() for l in b.splitlines() if l.strip()]
    if len(lines) >= 2 and '-->' in lines[0]:
        time_range = lines[0]
        # remove tags
        cue_text = ' '.join(lines[1:])
        cue_text = re.sub(r'<[^>]+>', '', cue_text)
        if cue_text:
            cues.append((time_range, cue_text))

print(f"Total cues: {len(cues)}")

# Let's find cue ranges for each problem
# In 2023.12:
# Problem 1: cues where 問題1 appears
for i, (t, c) in enumerate(cues):
    if '問題1' in c or '問題１' in c or '問題 1' in c:
        print(f"Prob 1 start: cue {i} [{t}] {c}")
    if '問題2' in c or '問題２' in c or '問題 2' in c:
        print(f"Prob 2 start: cue {i} [{t}] {c}")
    if '問題3' in c or '問題３' in c or '問題 3' in c:
        print(f"Prob 3 start: cue {i} [{t}] {c}")
    if '問題4' in c or '問題４' in c or '問題 4' in c:
        print(f"Prob 4 start: cue {i} [{t}] {c}")
    if '問題5' in c or '問題５' in c or '問題 5' in c:
        print(f"Prob 5 start: cue {i} [{t}] {c}")
