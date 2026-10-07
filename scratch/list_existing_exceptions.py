# -*- coding: utf-8 -*-
import sys, sqlite3, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect(r'C:\Users\pcw06\AppData\Local\Temp\anki_deck_check\collection.anki2')
cur = con.cursor()
cur.execute('''
    SELECT c.id, n.flds, n.tags
    FROM cards c
    JOIN notes n ON c.nid = n.id
    WHERE c.did = 1789368048385 AND n.tags LIKE '%1그룹예외%'
''')
rows = cur.fetchall()
print(f"Total 1그룹예외 cards in 03 동사 활용: {len(rows)}")
verbs = []
for cid, flds, tags in rows:
    front = flds.split(chr(0x1f))[0]
    m_title = re.search(r'class="vt-title">([^<]+)</div>', front)
    title = m_title.group(1).strip() if m_title else '?'
    m_sub = re.search(r'class="vt-sub">([^<]+)</div>', front)
    sub = m_sub.group(1).strip() if m_sub else ''
    verbs.append((title, sub))
    print(f"  CID {cid}: {title} ({sub})")
con.close()
