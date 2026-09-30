with open('scratch/cleaned_transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Split by 問題 or 番
# Let's inspect where the questions start
pattern = r'(\d{2}:\d{2}:\d{2}\.\d{3}:\s*(?:問題\s*\d|(?:\d+番)))'
parts = re.split(pattern, text)

print(f"Total parts: {len(parts)}")
with open('scratch/split_parts.txt', 'w', encoding='utf-8') as out:
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i+1].strip()[:300].replace('\n', ' ')
        out.write(f"=== {header} ===\n{body}\n\n")

print("Done writing split_parts.txt")
