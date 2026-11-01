# -*- coding: utf-8 -*-
import sqlite3, shutil, json, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_now')
TEMP_DIR.mkdir(exist_ok=True)
for f in ['collection.anki2', 'collection.anki2-wal', 'collection.anki2-shm']:
    p = ANKI_SRC / f
    if p.exists():
        shutil.copy2(p, TEMP_DIR / f)

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()
KST = timezone(timedelta(hours=9))

cur.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur.fetchall())
print('queue_counts:', queue_counts)

s_dt = datetime(2026, 11, 1, 4, 0, 0, tzinfo=KST)
e_dt = s_dt + timedelta(days=1)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

cur.execute('SELECT count(*), sum(time), count(distinct cid), min(id), max(id) FROM revlog WHERE id >= ? AND id < ?', (s_ms, e_ms))
t_cnt, t_tms, t_dist, min_id, max_id = cur.fetchone()
min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST)
max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST)
t_sec = t_tms / 1000.0
print(f"Total: {t_cnt} reviews, {t_sec:.2f}s ({t_sec/60:.2f}m), distinct: {t_dist}, {min_dt.strftime('%H:%M:%S')} ~ {max_dt.strftime('%H:%M:%S')} KST")

# Decks breakdown
cur.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY sum(r.time) DESC
''', (s_ms, e_ms))
for did, cnt, dist, tms in cur.fetchall():
    dname = deck_names.get(did, str(did))
    sec = tms / 1000.0
    print(f"  {dname}: {cnt} reviews, {sec:.1f}s ({sec/60:.1f}m), {dist} cards")

# 한끝 Voca stats
cur.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
''', (s_ms, e_ms))
v_cnt, v_tms, v_dist = cur.fetchone()
v_sec = (v_tms or 0) / 1000.0
print(f"한끝 Voca: {v_cnt} reviews, {v_sec:.1f}s ({v_sec/60:.2f}m), {v_dist} cards")

cur.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s_ms, e_ms))
print('한끝 Voca ratings:', dict(cur.fetchall()))
