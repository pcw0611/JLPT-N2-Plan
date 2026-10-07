# -*- coding: utf-8 -*-
import sys, sqlite3, html, re

sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect(r'C:\Users\pcw06\AppData\Local\Temp\anki_deck_check\collection.anki2')
cur = con.cursor()
cur.execute('''
    SELECT c.id, n.flds, n.tags
    FROM cards c
    JOIN notes n ON c.nid = n.id
    WHERE c.did = 1789368048385
''')
rows = cur.fetchall()
print(f"Total cards in JLPT N2::03 동사 활용: {len(rows)}")

# Group by tag
tag_map = {}
for cid, flds, tags in rows:
    tag_clean = tags.strip()
    tag_map.setdefault(tag_clean, []).append((cid, flds))

print("\n=== Tags distribution ===")
for t, lst in sorted(tag_map.items()):
    print(f"  [{len(lst)} cards] {t}")

print("\n=== Sample Card 1 Full Front/Back ===")
cid, flds = tag_map[list(tag_map.keys())[0]][0]
parts = flds.split(chr(0x1f))
print("FRONT:")
print(parts[0])
print("\nBACK:")
print(parts[1])

con.close()
