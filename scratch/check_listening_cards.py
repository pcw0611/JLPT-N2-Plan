# -*- coding: utf-8 -*-
import sys, sqlite3, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_listening_check')
con = sqlite3.connect(dst / 'collection.anki2')
cur = con.cursor()

DECK_ID = 1790835146324

cur.execute('''
    SELECT c.id, c.nid, n.flds, n.tags
    FROM cards c
    JOIN notes n ON c.nid = n.id
    WHERE c.did = ?
    ORDER BY c.id
''', (DECK_ID,))

rows = cur.fetchall()

print(f"Total cards: {len(rows)}\n")
print(f"{'#':>3} {'Q':>5} {'Audio':>6} {'FrontChoice':>12} {'BackKorean':>11} Tags")
print('-' * 65)

for i, (cid, nid, flds, tags) in enumerate(rows):
    field_values = flds.split(chr(0x1f))
    front = field_values[0]
    back = field_values[1] if len(field_values) > 1 else ''

    # Audio check
    audio_refs = re.findall(r'\[sound:([^\]]+)\]', flds)
    has_audio = len(audio_refs) > 0
    audio_in_front = bool(re.search(r'\[sound:', front))

    # Front shows numbered choices? (1. 2. 3. 4.)
    front_shows_choices = bool(re.search(r'[1234]\s*[\.．]', front))

    # Back has Korean?
    back_has_korean = bool(re.search(r'[가-힣]', back))

    # Extract Q number from tags
    q_match = re.search(r'Q(\d+)', tags)
    q_num = f'Q{q_match.group(1)}' if q_match else '?'

    tag_snippet = tags.strip()[:35]

    a_str = 'YES' if has_audio else '***NO***'
    fc_str = 'YES' if front_shows_choices else 'no'
    bk_str = 'YES' if back_has_korean else 'no'

    print(f"{i+1:3d} {q_num:>5} {a_str:>8} {fc_str:>12} {bk_str:>11}  {tag_snippet}")

# Check media directory
print()
media_dir = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1\collection.media')
vol2_files = sorted([f.name for f in media_dir.glob('vol2_q*.mp3')])
e2_files = sorted([f.name for f in media_dir.glob('e2_q*.mp3')])
print(f"vol2_q*.mp3 in media dir ({len(vol2_files)}): {vol2_files}")
print(f"e2_q*.mp3 in media dir ({len(e2_files)}): {e2_files}")

# Show which cards reference audio but might not have the file
print()
all_audio = set(vol2_files + e2_files)
for i, (cid, nid, flds, tags) in enumerate(rows):
    audio_refs = re.findall(r'\[sound:([^\]]+)\]', flds)
    for ar in audio_refs:
        if ar not in all_audio:
            q_match = re.search(r'Q(\d+)', tags)
            q_num = f'Q{q_match.group(1)}' if q_match else '?'
            print(f"MISSING MEDIA: Card {i+1} ({q_num}) references '{ar}' but file not found")

con.close()
