# -*- coding: utf-8 -*-
"""Extract all 25 notes data (tags, nid, front, back, script) into a JSON for easy reference."""
import sys, sqlite3, json, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_listening_check')
con = sqlite3.connect(dst / 'collection.anki2')
cur = con.cursor()

cur.execute('''
    SELECT c.id, c.nid, n.flds, n.tags
    FROM cards c
    JOIN notes n ON c.nid = n.id
    WHERE c.did = 1790835146324
    ORDER BY c.id
''')

rows = cur.fetchall()
items = []

for cid, nid, flds, tags in rows:
    f = flds.split(chr(0x1f))
    front = f[0]
    back = f[1] if len(f) > 1 else ''
    
    q_match = re.search(r'Q(\d+)', tags)
    qid = int(q_match.group(1)) if q_match else 0
    exam = '1회' if '1회' in tags else '2회'
    
    # Extract sound
    sounds = re.findall(r'\[sound:([^\]]+)\]', flds)
    sound_fn = sounds[0] if sounds else ''
    
    items.append({
        'cid': cid,
        'nid': nid,
        'exam': exam,
        'qid': qid,
        'tags': tags.strip(),
        'sound': sound_fn,
        'front': front,
        'back': back
    })

with open('scratch/all_25_listening_cards.json', 'w', encoding='utf-8') as out:
    json.dump(items, out, ensure_ascii=False, indent=2)

print(f"Extracted {len(items)} items to scratch/all_25_listening_cards.json")
con.close()
