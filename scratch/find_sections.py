import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/cleaned_transcript.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines):
    if any(w in line for w in ['問題 1', '問題 2', '問題 3', '問題 4', '問題 5', '問題1', '問題2', '問題3', '問題4', '問題5']):
        print(f"Line {i+1}: {line.strip()}")
