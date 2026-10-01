import sqlite3
import glob

col_path = glob.glob('C:/Users/pcw06/AppData/Roaming/Anki2/*/collection.anki2')[0]
print("Found collection path:", col_path)

conn = sqlite3.connect(col_path)
cur = conn.cursor()
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("Tables:", tables)

# Check decks in col
cur.execute("SELECT decks FROM col")
row = cur.fetchone()
if row:
    import json
    decks = json.loads(row[0])
    print("Found decks in collection:")
    for did, d in decks.items():
        if '오답노트' in d.get('name', ''):
            print(f"  did={did}, name={d.get('name')}")

