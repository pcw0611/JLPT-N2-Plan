import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    vtt = f.read()

# Let's get the text around 00:27:35 to 00:29:00
lines = vtt.split('\n')
capturing = False
extracted = []
for line in lines:
    if '00:27:30' in line:
        capturing = True
    if '00:29:10' in line:
        capturing = False
    if capturing and not line.startswith(('0', 'WEBVTT', 'NOTE')) and line.strip():
        extracted.append(line.strip())

# Clean up tags like <00:27:...><c>
import re
cleaned = [re.sub(r'<[^>]+>', '', l) for l in extracted]
# deduplicate consecutive identical lines
deduped = []
for l in cleaned:
    if not deduped or deduped[-1] != l:
        deduped.append(l)

print("\n".join(deduped[:35]))
