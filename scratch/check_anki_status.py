# -*- coding: utf-8 -*-
import sqlite3
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_tmp')
TEMP_DIR.mkdir(exist_ok=True)

for f in ['collection.anki2', 'collection.anki2-wal', 'collection.anki2-shm']:
    p = ANKI_SRC / f
    if p.exists():
        shutil.copy2(p, TEMP_DIR / f)

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()

KST = timezone(timedelta(hours=9))

# Check max revlog id
cur.execute('SELECT count(*), max(id), min(id) FROM revlog')
cnt, max_id, min_id = cur.fetchone()
print(f"Total revlog: {cnt}")
if max_id:
    max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST)
    print(f"Latest review at: {max_dt.strftime('%Y-%m-%d %H:%M:%S KST')} (id: {max_id})")

# Check reviews per day for recent days (cutoff at 4:00 AM KST)
days = ['2026-11-10', '2026-11-11', '2026-11-12', '2026-11-13']
for d_str in days:
    y, m, d = map(int, d_str.split('-'))
    s_dt = datetime(y, m, d, 4, 0, 0, tzinfo=KST)
    e_dt = s_dt + timedelta(days=1)
    s_ms = int(s_dt.timestamp() * 1000)
    e_ms = int(e_dt.timestamp() * 1000)

    cur.execute('''
        SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
        FROM revlog
        WHERE id >= ? AND id < ?
    ''', (s_ms, e_ms))
    r_cnt, r_time, r_dist, r_min, r_max = cur.fetchone()
    if r_cnt:
        min_t = datetime.fromtimestamp(r_min / 1000.0, tz=KST).strftime('%H:%M:%S')
        max_t = datetime.fromtimestamp(r_max / 1000.0, tz=KST).strftime('%H:%M:%S')
        sec = (r_time or 0) / 1000.0
        print(f"[{d_str}] reviews: {r_cnt}, distinct: {r_dist}, time: {int(sec//60)}m {sec%60:.2f}s ({sec:.2f}s), span: {min_t} ~ {max_t}")
    else:
        print(f"[{d_str}] reviews: 0")

con.close()
