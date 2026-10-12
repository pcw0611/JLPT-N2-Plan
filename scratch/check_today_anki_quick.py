# -*- coding: utf-8 -*-
import sqlite3
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_today')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TEMP_DIR / 'collection.anki2-shm')

con_anki = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur_anki = con_anki.cursor()

KST = timezone(timedelta(hours=9))
# Check 2026-10-12 and 2026-10-13
for date_str, y, m, d in [('2026-10-12', 2026, 10, 12), ('2026-10-13', 2026, 10, 13)]:
    s_dt = datetime(y, m, d, 4, 0, 0, tzinfo=KST)
    e_dt = s_dt + timedelta(days=1)
    s_ms = int(s_dt.timestamp() * 1000)
    e_ms = int(e_dt.timestamp() * 1000)
    
    cur_anki.execute('SELECT count(*), sum(time), count(distinct cid), min(id), max(id) FROM revlog WHERE id >= ? AND id < ?', (s_ms, e_ms))
    cnt, total_time_ms, distinct_cards, min_id, max_id = cur_anki.fetchone()
    print(f"=== Date: {date_str} ===")
    print(f"Count: {cnt}, Time: {(total_time_ms or 0)/1000.0:.2f}s ({((total_time_ms or 0)/1000.0)/60.0:.2f}m), Distinct cards: {distinct_cards}")
    if min_id and max_id:
        min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST)
        max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST)
        print(f"Time range: {min_dt.strftime('%H:%M:%S')} ~ {max_dt.strftime('%H:%M:%S')}")

# Also check max revlog id overall
cur_anki.execute('SELECT max(id) FROM revlog')
max_all = cur_anki.fetchone()[0]
if max_all:
    dt_all = datetime.fromtimestamp(max_all / 1000.0, tz=KST)
    print(f"Latest review in revlog: {dt_all.strftime('%Y-%m-%d %H:%M:%S')}")

con_anki.close()
