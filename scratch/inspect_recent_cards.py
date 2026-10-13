# -*- coding: utf-8 -*-
import sqlite3
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_wal')
TEMP_DIR.mkdir(exist_ok=True)
ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TEMP_DIR / 'collection.anki2-shm')

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()

cur.execute('SELECT id, name FROM decks WHERE id = 1791842245520')
print("Deck 1791842245520:", cur.fetchall())

cur.execute('''
    SELECT c.id, c.nid, c.did, d.name, n.flds
    FROM cards c
    JOIN decks d ON c.did = d.id
    JOIN notes n ON c.nid = n.id
    WHERE n.id >= 1791842361000
''')
rows = cur.fetchall()
print(f"Cards found from recent notes: {len(rows)}")
for r in rows:
    flds = r[4].split('\x1f')
    kanji = flds[1] if len(flds) > 1 else ''
    print(f"Card {r[0]} | Note {r[1]} | Deck: {r[3]} ({r[2]}) | Word: {kanji}")

con.close()
