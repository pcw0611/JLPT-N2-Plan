import sys, io, re
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/vol2_script.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Clean furigana:
# In text, lines like "会\nかい\n社\nしゃ\nで..."
# Let's see all lines matching [1-5]番
lines = text.split('\n')
clean_lines = []
for l in lines:
    l_strip = l.strip()
    if re.match(r'^[0-9]番', l_strip):
        clean_lines.append(f"\n--- {l_strip} ---")
    elif l_strip.startswith('問題'):
        clean_lines.append(f"\n=== {l_strip} ===")
    elif l_strip.startswith('Ｍ') or l_strip.startswith('Ｆ'):
        clean_lines.append(l_strip[:30])

print("\n".join(clean_lines[:60]))
