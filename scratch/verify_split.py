import sys, io, os
sys.path.append(os.getcwd())
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from scratch.test_anki_mcp import mcp

decks = mcp('list_decks')
for d in decks.get('structuredContent', {}).get('decks', []):
    if '오답노트' in d['name']:
        find_res = mcp('find_notes', {'query': f'deck:"{d["name"]}"'})
        count = len(find_res.get('structuredContent', {}).get('noteIds', []))
        print(f"Deck: {d['name']} -> {count} notes")
