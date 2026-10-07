# -*- coding: utf-8 -*-
import sys, sqlite3, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect(r'C:\Users\pcw06\AppData\Local\Temp\anki_deck_check\collection.anki2')
cur = con.cursor()
cur.execute('''
    SELECT c.id, n.mid, n.flds, n.tags
    FROM cards c
    JOIN notes n ON c.nid = n.id
    WHERE c.did = 1789368048385
    LIMIT 10
''')
print("=== Sample Cards in JLPT N2::03 동사 활용 ===")
for cid, mid, flds, tags in cur.fetchall():
    parts = flds.split(chr(0x1f))
    clean_f = ' '.join(re.sub(r'<[^>]+>', ' ', parts[0]).split())[:80]
    clean_b = ' '.join(re.sub(r'<[^>]+>', ' ', parts[1]).split())[:80]
    print(f"CID {cid} (MID {mid}, tags: '{tags.strip()}'):")
    print(f"  Front: {clean_f}")
    print(f"  Back:  {clean_b}")
    print()

# Check notetype of these cards
cur.execute('SELECT name FROM notetypes WHERE id = ?', (mid,))
print(f"Notetype name: {cur.fetchone()[0]}")

con.close()
