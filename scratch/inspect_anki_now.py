import sqlite3
import shutil
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_check')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TEMP_DIR / 'collection.anki2-shm')

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()
KST = timezone(timedelta(hours=9))

for d_str in ['2026-11-01', '2026-11-02', '2026-11-03']:
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
    row = cur.fetchone()
    cnt, tms, dist, min_id, max_id = row
    if cnt:
        min_dt = datetime.fromtimestamp(min_id/1000.0, tz=KST)
        max_dt = datetime.fromtimestamp(max_id/1000.0, tz=KST)
        t_sec = tms / 1000.0
        print(f"{d_str}: {cnt} reviews, {t_sec:.2f}s ({t_sec/60.0:.2f} mins), {dist} cards, range: {min_dt.strftime('%H:%M')}~{max_dt.strftime('%H:%M')}")
    else:
        print(f"{d_str}: 0 reviews")

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
print('Queue counts:', dict(cur.fetchall()))

# Check decks for 2026-11-02 and 2026-11-03
cur.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

for d_str in ['2026-11-02', '2026-11-03']:
    y, m, d = map(int, d_str.split('-'))
    s_dt = datetime(y, m, d, 4, 0, 0, tzinfo=KST)
    e_dt = s_dt + timedelta(days=1)
    s_ms = int(s_dt.timestamp() * 1000)
    e_ms = int(e_dt.timestamp() * 1000)
    print(f"\n--- {d_str} Breakdown ---")
    cur.execute('''
        SELECT c.did, count(*), count(distinct c.id), sum(r.time)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        WHERE r.id >= ? AND r.id < ?
        GROUP BY c.did
        ORDER BY sum(r.time) DESC
    ''', (s_ms, e_ms))
    for did, d_cnt, d_dist, d_tms in cur.fetchall():
        d_sec = (d_tms or 0) / 1000.0
        print(f"  {deck_names.get(did, did)}: {d_cnt} revs, {d_sec/60.0:.2f}m, {d_dist} cards")

    cur.execute('''
        SELECT r.ease, count(*)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
        GROUP BY r.ease
    ''', (s_ms, e_ms))
    print(f"  한끝 Voca ease counts: {dict(cur.fetchall())}")

con.close()
