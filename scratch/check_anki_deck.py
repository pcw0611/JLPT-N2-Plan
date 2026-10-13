# -*- coding: utf-8 -*-
import sqlite3
import shutil
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_decks')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TEMP_DIR / 'collection.anki2-shm')

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()

print("--- Decks ---")
cur.execute('SELECT id, name FROM decks')
decks = sorted(cur.fetchall(), key=lambda x: x[1])
for did, name in decks:
    clean_name = name.replace('\x1f', '::')
    cur.execute('SELECT count(*) FROM cards WHERE did = ?', (did,))
    card_cnt = cur.fetchone()[0]
    print(f"ID: {did} | Name: {clean_name} | Cards: {card_cnt}")

print("\n--- Models (Note Types) ---")
cur.execute('SELECT models FROM col')
models_json = cur.fetchone()[0]
if models_json:
    models = json.loads(models_json)
    for mid, mdata in models.items():
        flds = [f['name'] for f in mdata.get('flds', [])]
        print(f"ID: {mid} | Name: {mdata.get('name')} | Fields: {flds}")

print("\n--- Recent notes (last 5) ---")
cur.execute('SELECT id, mid, flds, tags FROM notes ORDER BY id DESC LIMIT 5')
for nid, mid, flds, tags in cur.fetchall():
    fields_list = flds.split('\x1f')
    print(f"Note {nid} (Model {mid}): {fields_list[:3]} | Tags: {tags}")

con.close()
