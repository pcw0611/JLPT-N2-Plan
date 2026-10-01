import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/official_vol2_full_script.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's clean up furigana
# In the PDF, furigana appears on subsequent lines or intermixed.
# Let's inspect pages 8 to 16
for line in text.splitlines():
    line_clean = line.strip()
    if any(line_clean.startswith(x) for x in ['問題 1', '問題 2', '問題 3', '問題 4', '問題 5', '1番', '2番', '3番', '4番', '5番', '6番', '7番', '8番', '9番', '10 番', '11 番', '12 番', '例']):
        print(line_clean)
