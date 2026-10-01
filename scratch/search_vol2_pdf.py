import sys, io, re
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/vol2_script.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Clean out furigana lines (short hiragana lines right below kanji)
# In N2_listening_script.pdf, lines are alternating or split
# Let's inspect pages
pages = "".join(lines).split('--- Page ')
print(f"Total pages in vol2_script.txt: {len(pages)}")

# Print sample from Page 1, 2, 3
for p in pages[1:4]:
    header = p.split('\n', 1)[0]
    print(f"Page {header}: length {len(p)}")
