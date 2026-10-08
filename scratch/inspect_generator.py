import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Match song objects
# Let's inspect scratch/generate_all_official_songs.py to see how songs were generated originally!
with open('scratch/generate_all_official_songs.py', 'r', encoding='utf-8') as f:
    gen_content = f.read()

print("generate_all_official_songs.py length:", len(gen_content))
print("Sample of generator:")
print(gen_content[:1500])
