# -*- coding: utf-8 -*-
import sqlite3
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1013_noon')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TEMP_DIR / 'collection.anki2-shm')

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()

KST = timezone(timedelta(hours=9))
s_dt = datetime(2026, 10, 13, 4, 0, 0, tzinfo=KST)
e_dt = s_dt + timedelta(days=1)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

cur.execute('SELECT id, name FROM decks')
decks = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

# Total
cur.execute('SELECT count(*), sum(time), count(distinct cid), min(id), max(id) FROM revlog WHERE id >= ? AND id < ?', (s_ms, e_ms))
cnt_all, time_all, dist_all, min_id, max_id = cur.fetchone()
min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST) if min_id else s_dt
max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST) if max_id else s_dt

print("=== ALL DECKS ===")
print(f"Reviews: {cnt_all}, Time: {(time_all or 0)/1000.0:.2f}s ({((time_all or 0)/1000.0)/60.0:.2f}m), Distinct: {dist_all}")
print(f"Range: {min_dt.strftime('%H:%M:%S')} ~ {max_dt.strftime('%H:%M:%S')} KST")

# By Deck
print("\n=== BY DECK ===")
cur.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s_ms, e_ms))
for did, cnt, dist, tms in cur.fetchall():
    dname = decks.get(did, f"Deck {did}")
    d_sec = (tms or 0) / 1000.0
    print(f"  [{dname}] ({did}): {cnt} reviews, {dist} cards, {d_sec/60.0:.2f}m ({d_sec:.1f}s)")

# Ratings ALL vs VOCA
print("\n=== RATINGS ===")
cur.execute('''
    SELECT ease, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY ease
''', (s_ms, e_ms))
print("All Ratings:", dict(cur.fetchall()))

cur.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%Voca%'
    GROUP BY r.ease
''', (s_ms, e_ms))
print("Voca Ratings:", dict(cur.fetchall()))

# Voca stats
cur.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%Voca%'
''', (s_ms, e_ms))
v_cnt, v_tms, v_dist = cur.fetchone()
v_sec = (v_tms or 0) / 1000.0
print(f"\nVoca only: {v_cnt} reviews, {v_sec/60.0:.2f}m, {v_dist} cards")

con.close()
