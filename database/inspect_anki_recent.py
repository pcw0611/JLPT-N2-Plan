import sqlite3
import json
import sys
from pathlib import Path

dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_recent')
con = sqlite3.connect(dst / 'collection.anki2')
cur = con.cursor()

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
print('Queue counts overall:', dict(cur.fetchall()))

cur.execute('SELECT id, name FROM decks')
decks = cur.fetchall()
for did, dname in decks:
    if '4-N2' in dname:
        cur.execute('SELECT queue, count(*) FROM cards WHERE did = ? GROUP BY queue', (did,))
        print(f'{dname} queue:', dict(cur.fetchall()))

con.close()
