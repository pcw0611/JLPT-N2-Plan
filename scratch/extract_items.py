import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_transcript_lines.txt', 'r', encoding='utf-8') as f:
    raw_lines = f.readlines()

full_text = "".join(raw_lines)

# Let's inspect Problem 1, 2, 3, 4, 5
# Look at Problem 4 (即時応答 11 items)
# Look at Problem 3 (概要理解 5 items)
# Look at Problem 1 (課題理解 5 items)
# Look at Problem 2 (ポイント理解 6 items)
# Look at Problem 5 (統合理解 3 items)

# Let's find all occurrences of '1番', '2番', '3番', '4番', '5番', '6番', etc.
with open('scratch/all_numbered_items.txt', 'w', encoding='utf-8') as out:
    for line in raw_lines:
        if re.search(r'\b[1-9]番|\b10番|\b11番', line):
            out.write(line)

print("Extracted numbered items to scratch/all_numbered_items.txt")
