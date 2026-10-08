import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/app/typing/songs.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Match song objects
matches = re.findall(r'\"id\":\s*\"([^\"]+)\",\s*\"title\":\s*\"([^\"]+)\",\s*\"reading\":\s*\"([^\"]+)\",\s*\"category\":\s*\"([^\"]+)\"', text)
print(f"Total songs: {len(matches)}")
for i, (sid, title, reading, cat) in enumerate(matches):
    print(f"{i+1:2d}. [{cat:8s}] {sid:18s} : {title} ({reading})")
