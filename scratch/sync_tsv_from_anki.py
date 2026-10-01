import json, sys, os
sys.path.append(os.getcwd())
from scratch.test_anki_mcp import mcp

DECK_LISTENING = "JLPT N2::오답노트 (청해 25문항 · 실전 음원)"

res = mcp('find_notes', {'query': f'deck:"{DECK_LISTENING}"'})
note_ids = res.get('structuredContent', {}).get('noteIds', [])
info = mcp('notes_info', {'notes': note_ids})
notes = info.get('structuredContent', {}).get('notes', [])

tsv_lines = []
for n in notes:
    f = n.get('fields', {})
    front = f.get('Front', {}).get('value', '').replace('\t', ' ').replace('\n', '<br>')
    back = f.get('Back', {}).get('value', '').replace('\t', ' ').replace('\n', '<br>')
    tags = " ".join(n.get('tags', []))
    tsv_lines.append(f"{front}\t{back}\t{tags}")

with open('anki_error_notes_listening_25.tsv', 'w', encoding='utf-8') as out:
    out.write("\n".join(tsv_lines))

print(f"Updated anki_error_notes_listening_25.tsv with {len(tsv_lines)} notes containing scripts!")
