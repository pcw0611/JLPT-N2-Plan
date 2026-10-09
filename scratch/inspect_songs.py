import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/app/typing/songs.ts', encoding='utf-8') as f:
    content = f.read()

# Extract song objects
# Each song has id: '...', title: '...', album: '...', category: '...', youtubeId: '...'
songs = []
for block in re.finditer(r"id:\s*'([^']+)',\s*title:\s*'([^']+)',\s*reading:\s*'([^']+)',\s*album:\s*'([^']+)',\s*category:\s*'([^']+)',\s*youtubeId:\s*'([^']*)'", content):
    songs.append({
        "id": block.group(1),
        "title": block.group(2),
        "reading": block.group(3),
        "album": block.group(4),
        "category": block.group(5),
        "youtubeId": block.group(6),
    })

print(f"Total songs parsed: {len(songs)}")
for s in songs:
    print(f"{s['id']}: {s['title']} | album: {s['album']} | cat: {s['category']} | yt: {s['youtubeId']}")
