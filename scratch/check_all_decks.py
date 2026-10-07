# -*- coding: utf-8 -*-
import sys, sqlite3, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
src = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_deck_check')
dst.mkdir(exist_ok=True)
shutil.copy2(src / 'collection.anki2', dst / 'collection.anki2')
if (src / 'collection.anki2-wal').exists():
    shutil.copy2(src / 'collection.anki2-wal', dst / 'collection.anki2-wal')
if (src / 'collection.anki2-shm').exists():
    shutil.copy2(src / 'collection.anki2-shm', dst / 'collection.anki2-shm')

con = sqlite3.connect(dst / 'collection.anki2')
cur = con.cursor()
cur.execute('SELECT id, name FROM decks')
print("=== All Decks in Collection ===")
for did, name in sorted(cur.fetchall(), key=lambda x: x[1]):
    clean_name = name.replace(chr(0x1f), "::")
    cur.execute('SELECT count(*) FROM cards WHERE did = ?', (did,))
    cnt = cur.fetchone()[0]
    print(f"  {did}: {clean_name} ({cnt} cards)")
con.close()
