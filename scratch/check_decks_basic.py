import sqlite3

conn = sqlite3.connect('scratch/temp_collection.anki2')
conn.create_collation('unicase', lambda a, b: (a > b) - (a < b))
c = conn.cursor()

c.execute("""
    SELECT DISTINCT c.did
    FROM cards c
    JOIN notes n ON c.nid = n.id
    WHERE n.mid = 1787553295421
""")
dids = [r[0] for r in c.fetchall()]
for did in dids:
    c.execute("SELECT name FROM decks WHERE id = ?", (did,))
    row = c.fetchone()
    print(did, row[0] if row else 'Unknown')
