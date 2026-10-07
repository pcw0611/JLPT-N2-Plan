# -*- coding: utf-8 -*-
"""Inspect the 'unknown' type cards to identify their problem type."""
import sys, sqlite3, re, html
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

def strip_html(text):
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    return text.strip()

# Inspect unknown cards: index 1 (Q80 1회), 2 (Q90 1회), 6 (Q102 1회), 7 (Q106 1회)
for idx in [1, 2, 6, 7]:
    cid, nid, flds, tags = rows[idx]
    field_values = flds.split(chr(0x1f))
    front_text = strip_html(field_values[0])
    back_text = strip_html(field_values[1]) if len(field_values) > 1 else ''
    
    q_match = re.search(r'Q(\d+)', tags)
    q_num = f'Q{q_match.group(1)}' if q_match else '?'
    
    print(f"=== Card {idx+1}: {q_num} | {tags.strip()} ===")
    # Show first 600 chars of front
    print("FRONT (first 600 chars):")
    print(front_text[:600])
    print()
    # Show first 300 chars of back
    print("BACK (first 300 chars):")
    print(back_text[:300])
    print()
    print()

con.close()
