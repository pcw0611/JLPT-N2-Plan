# -*- coding: utf-8 -*-
import sqlite3, shutil, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
sys.stdout.reconfigure(encoding='utf-8')

KST = timezone(timedelta(hours=9))
src = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
temp = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1008')
shutil.copy2(src / 'collection.anki2', temp / 'collection.anki2')
if (src / 'collection.anki2-wal').exists():
    shutil.copy2(src / 'collection.anki2-wal', temp / 'collection.anki2-wal')

con = sqlite3.connect(temp / 'collection.anki2')
cur = con.cursor()

s = datetime(2026, 10, 8, 4, 0, 0, tzinfo=KST)
e = s + timedelta(days=1)
s_ms, e_ms = int(s.timestamp()*1000), int(e.timestamp()*1000)

cur.execute('SELECT count(*), sum(time), count(distinct cid), min(id), max(id) FROM revlog WHERE id >= ? AND id < ?', (s_ms, e_ms))
cnt, total_time_ms, distinct_cards, min_id, max_id = cur.fetchone()
sec = (total_time_ms or 0)/1000.0
min_dt = datetime.fromtimestamp(min_id/1000.0, tz=KST) if min_id else None
max_dt = datetime.fromtimestamp(max_id/1000.0, tz=KST) if max_id else None
print(f"2026-10-08 Anki: {cnt} reviews, {sec:.2f}s ({sec/60:.2f}m), {distinct_cards} cards")
if min_dt and max_dt:
    print(f"Time range: {min_dt.strftime('%H:%M')} ~ {max_dt.strftime('%H:%M')}")
