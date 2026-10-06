import sys
import os
import sqlite3
import json

sys.stdout.reconfigure(encoding='utf-8')

anki_db = os.path.join(os.environ['APPDATA'], 'Anki2', '사용자 1', 'collection.anki2')
conn = sqlite3.connect(f'file:{anki_db}?mode=ro', uri=True)
c = conn.cursor()

# Find note with 062 or 〜(の)であれば
c.execute("SELECT id, mid, flds, sfld, tags FROM notes WHERE flds LIKE '%であれば%' OR flds LIKE '%062%' LIMIT 5")
rows = c.fetchall()
print(f"Found {len(rows)} matching notes:")
for r in rows:
    nid, mid, flds, sfld, tags = r
    print(f"Note ID: {nid}, Model ID: {mid}, sfld: {sfld}, tags: {tags}")
    # split fields by \x1f (31)
    fields = flds.split('\x1f')
    for idx, f in enumerate(fields):
        print(f"  Field {idx} (len {len(f)}): {f[:150]}...")

# Get model info for this mid
if rows:
    target_mid = rows[0][1]
    c.execute("SELECT models FROM col")
    models_json = c.fetchone()[0]
    models = json.loads(models_json)
    target_model = models.get(str(target_mid))
    if target_model:
        print(f"\nModel Name: {target_model['name']}")
        print(f"CSS:\n{target_model['css']}")
        print(f"Templates:")
        for tmpl in target_model['tmpls']:
            print(f"  --- {tmpl['name']} ---")
            print(f"  Q:\n{tmpl['qfmt'][:300]}")
            print(f"  A:\n{tmpl['afmt'][:500]}")
