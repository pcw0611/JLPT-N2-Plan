# -*- coding: utf-8 -*-
"""Deep inspection of listening error note cards - front/back content detail."""
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
    """Remove HTML tags and decode entities for readable output."""
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_audio(text):
    return re.findall(r'\[sound:([^\]]+)\]', text)

# Inspect a sample of cards in detail
# Card 1 (vol2 Q76), Card 9 (e2 Q75), and Card 3 (vol2 Q90) 
# to see different patterns
for idx in [0, 2, 8, 14]:
    if idx >= len(rows):
        continue
    cid, nid, flds, tags = rows[idx]
    field_values = flds.split(chr(0x1f))
    front = field_values[0]
    back = field_values[1] if len(field_values) > 1 else ''
    
    q_match = re.search(r'Q(\d+)', tags)
    q_num = f'Q{q_match.group(1)}' if q_match else '?'
    
    front_audio = extract_audio(front)
    back_audio = extract_audio(back)
    
    front_text = strip_html(front)
    back_text = strip_html(back)
    
    print(f"{'='*70}")
    print(f"Card {idx+1}: {q_num} | {tags.strip()}")
    print(f"{'='*70}")
    print(f"--- FRONT (audio: {front_audio}) ---")
    print(front_text[:1200])
    print(f"\n--- BACK (audio: {back_audio}) ---")
    print(back_text[:1200])
    print()

con.close()
