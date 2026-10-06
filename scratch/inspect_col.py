import os
import shutil
import sqlite3
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

src = os.path.join(os.environ['APPDATA'], 'Anki2', '사용자 1', 'collection.anki2')
dst = 'scratch/temp_collection.anki2'
shutil.copy2(src, dst)
if os.path.exists(src + '-wal'):
    shutil.copy2(src + '-wal', dst + '-wal')

conn = sqlite3.connect(dst)
c = conn.cursor()

# Find cards in grammar deck
c.execute("SELECT id, name FROM decks WHERE name LIKE '%01 문법%'")
deck_row = c.fetchone()
print('Deck:', deck_row)

if deck_row:
    did = deck_row[0]
    c.execute("""
        SELECT c.id, c.nid, n.mid, n.flds, n.tags
        FROM cards c
        JOIN notes n ON c.nid = n.id
        WHERE c.did = ?
        LIMIT 5
    """, (did,))
    cards = c.fetchall()
    print(f"Cards in deck: {len(cards)}")
    for card in cards:
        cid, nid, mid, flds, tags = card
        fields = flds.split('\x1f')
        print(f"\nCard ID: {cid}, Note ID: {nid}, Model ID: {mid}")
        print("FRONT:", fields[0][:100])
        print("BACK:\n", fields[1][:600])

    # Now let's check the model for this grammar deck!
    mid = cards[0][2]
    c.execute("SELECT models FROM col")
    models = json.loads(c.fetchone()[0])
    model = models.get(str(mid))
    print(f"\nModel name: {model['name']}")
    print(f"Model CSS:\n{model['css']}")
