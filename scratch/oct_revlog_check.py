# -*- coding: utf-8 -*-
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1020_detailed')

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()
KST = timezone(timedelta(hours=9))

s_dt = datetime(2026, 10, 1, 4, 0, 0, tzinfo=KST)
e_dt = datetime(2026, 10, 21, 4, 0, 0, tzinfo=KST)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

cur.execute('''
    SELECT count(*), sum(time), count(distinct cid)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s_ms, e_ms))
cnt, tms, dist = cur.fetchone()
sec = tms / 1000.0
mins = sec / 60.0
print(f"October 1~20 Anki total from revlog: {cnt:,} reviews, {mins:.2f} mins ({sec:.2f}s, {mins/60:.2f} hours), {dist:,} distinct cards")
