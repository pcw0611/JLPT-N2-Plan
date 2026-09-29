import sqlite3
import shutil
import os
import time
import datetime
from pathlib import Path

src = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
if not src.exists():
    base = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2')
    src = next(p for p in base.iterdir() if (p / 'collection.anki2').exists())

print('Using:', src)
dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_check_today')
dst.mkdir(exist_ok=True)
shutil.copy2(src / 'collection.anki2', dst / 'collection.anki2')
if (src / 'collection.anki2-wal').exists():
    shutil.copy2(src / 'collection.anki2-wal', dst / 'collection.anki2-wal')

con = sqlite3.connect(dst / 'collection.anki2')
cur = con.cursor()

cur.execute('SELECT max(id) FROM revlog')
max_id = cur.fetchone()[0]
if max_id:
    max_dt = datetime.datetime.fromtimestamp(max_id / 1000.0)
    print('Most recent review timestamp:', max_dt)

cur.execute("""
    SELECT date(id/1000, 'unixepoch', 'localtime') as rday, count(*), round(sum(time)/60000.0, 2)
    FROM revlog
    GROUP BY rday
    ORDER BY rday DESC
    LIMIT 15
""")
print('Recent daily revlog summary (day, count, minutes):')
for r in cur.fetchall():
    print(r)

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
print('Current queue distribution:', dict(cur.fetchall()))

con.close()
