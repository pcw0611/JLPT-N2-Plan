import sqlite3
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_detailed')
con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()
KST = timezone(timedelta(hours=9))

s_dt = datetime(2026, 11, 3, 4, 0, 0, tzinfo=KST)
e_dt = s_dt + timedelta(days=1)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

cur.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    WHERE r.id >= ? AND r.id < ?
      AND r.cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
''', (s_ms, e_ms, s_ms))
first_cards = cur.fetchone()[0] or 0
print("First-time cards exposed on 2026-11-03:", first_cards)

con.close()
