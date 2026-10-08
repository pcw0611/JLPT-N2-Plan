import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Load perfect mayoiuta json
with open('scratch/mayoiuta_perfect.json', 'r', encoding='utf-8') as f:
    mayoiuta_data = json.load(f)

# Read songs.ts
with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    songs_ts = f.read()

# Replace the mayoiuta entry in SONGS array
# Find mayoiuta start
start_marker = '  {\n    "id": "mayoiuta",'
if start_marker not in songs_ts:
    start_marker = '  {\r\n    "id": "mayoiuta",'

if start_marker not in songs_ts:
    # Try more flexible match
    idx_start = songs_ts.find('"id": "mayoiuta"')
    if idx_start != -1:
        # back up to preceding '  {'
        idx_brace = songs_ts.rfind('{', 0, idx_start)
        # find the end of this song object (before next song "id": "nanashigoe")
        idx_next = songs_ts.find('"id": "nanashigoe"')
        idx_end = songs_ts.rfind('},', 0, idx_next) + 1
    else:
        raise RuntimeError("mayoiuta not found in songs.ts")
else:
    idx_brace = songs_ts.find(start_marker)
    idx_next = songs_ts.find('"id": "nanashigoe"')
    idx_end = songs_ts.rfind('},', 0, idx_next) + 1

print(f"Replacing mayoiuta between index {idx_brace} and {idx_end}")

# Format mayoiuta_data to json with 2 indentation
formatted_mayoiuta = json.dumps(mayoiuta_data, ensure_ascii=False, indent=2)
# Add 2 spaces indentation
indented_mayoiuta = "\n".join("  " + line for line in formatted_mayoiuta.splitlines())

new_songs_ts = songs_ts[:idx_brace] + indented_mayoiuta + songs_ts[idx_end:]

with open('jlpt-calendar-site/app/typing/songs.ts', 'w', encoding='utf-8') as f:
    f.write(new_songs_ts)

print("Updated jlpt-calendar-site/app/typing/songs.ts successfully!")
