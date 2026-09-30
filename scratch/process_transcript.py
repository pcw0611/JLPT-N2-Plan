import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/cleaned_transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove line duplicates
lines = []
for line in text.split('\n'):
    line = line.strip()
    if not line:
        continue
    # Keep timestamp and text
    m = re.match(r'^(\d{2}:\d{2}:\d{2}\.\d{3}):\s*(.*)$', line)
    if m:
        t, c = m.group(1), m.group(2).strip()
        lines.append((t, c))

with open('scratch/all_transcript_lines.txt', 'w', encoding='utf-8') as out:
    for t, c in lines:
        out.write(f"{t}: {c}\n")

print(f"Total lines: {len(lines)}")
