# -*- coding: utf-8 -*-
import sqlite3
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_tmp')

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()

# Find notes created recently (e.g. past 3 days)
cur.execute('''
    SELECT id, mid, flds, tags
    FROM notes
    ORDER BY id DESC
    LIMIT 25
''')
KST = timezone(timedelta(hours=9))
for nid, mid, flds, tags in cur.fetchall():
    cdt = datetime.fromtimestamp(nid / 1000.0, tz=KST)
    first_field = flds.split('\x1f')[0][:40]
    print(f"[{cdt.strftime('%Y-%m-%d %H:%M')}] Note {nid}: {first_field} (tags: {tags})")

con.close()
