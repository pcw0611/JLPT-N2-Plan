import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('jlpt-calendar-site/app/typing/songs.ts', encoding='utf-8') as f:
    text = f.read()

# Find JSON array
start_arr = text.find('[', text.find('='))
end_arr = text.rfind(']') + 1
songs_json = text[start_arr:end_arr]
print("Slice length:", len(songs_json), "starts with:", repr(songs_json[:20]), "ends with:", repr(songs_json[-20:]))
try:
    songs = json.loads(songs_json)
    print(f"Total songs loaded: {len(songs)}")
    for i, s in enumerate(songs):
        print(f"[{i+1}] {s['id']}: {s['title']} ({s['reading']}) | album: {s['album']} | cat: {s['category']} | yt: {s.get('youtubeId', '')}")
except Exception as e:
    print("Error parsing json:", e)

