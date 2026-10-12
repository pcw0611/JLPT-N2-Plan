# -*- coding: utf-8 -*-
import sqlite3
import shutil
import sys
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1013')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TEMP_DIR / 'collection.anki2-shm')

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()
KST = timezone(timedelta(hours=9))

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur.fetchall())
new_rem = queue_counts.get(0, 0)
learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
rev_rem = queue_counts.get(2, 0)

cur.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

s_dt = datetime(2026, 10, 13, 4, 0, 0, tzinfo=KST)
e_dt = s_dt + timedelta(days=1)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

cur.execute('SELECT count(*), sum(time), count(distinct cid), min(id), max(id) FROM revlog WHERE id >= ? AND id < ?', (s_ms, e_ms))
cnt, total_time_ms, distinct_cards, min_id, max_id = cur.fetchone()
anki_sec = (total_time_ms or 0) / 1000.0
anki_mins = anki_sec / 60.0
sec_per_card = round(anki_sec / cnt, 2) if cnt else 0

min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST) if min_id else s_dt
max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST) if max_id else s_dt

cur.execute('SELECT ease, count(*) FROM revlog WHERE id >= ? AND id < ? GROUP BY ease', (s_ms, e_ms))
rating_map = dict(cur.fetchall())
again_c = rating_map.get(1, 0)
hard_c = rating_map.get(2, 0)
good_c = rating_map.get(3, 0)
easy_c = rating_map.get(4, 0)
again_pct = round((again_c / cnt * 100), 2) if cnt else 0.0

cur.execute('SELECT type, count(*) FROM revlog WHERE id >= ? AND id < ? GROUP BY type', (s_ms, e_ms))
type_map = dict(cur.fetchall())
learn_revs = type_map.get(0, 0) + type_map.get(2, 0)
revs_done = type_map.get(1, 0) + type_map.get(3, 0)

cur.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s_ms, e_ms))

print(f"Reviews: {cnt}, Total Sec: {anki_sec:.2f}s ({anki_mins:.2f}m), Distinct: {distinct_cards}, Per Card: {sec_per_card}s")
print(f"Time range: {min_dt.strftime('%H:%M:%S')} ~ {max_dt.strftime('%H:%M:%S')} KST")
print(f"Ratings: Again {again_c} ({again_pct}%), Hard {hard_c}, Good {good_c}, Easy {easy_c}")
print(f"Types: Learn {learn_revs}, Review {revs_done}")
print(f"Queue Remaining: New {new_rem}, Learn {learn_rem}, Review {rev_rem}")
print("Decks:")
for did, d_cnt, d_dist, d_tms in cur.fetchall():
    d_sec = (d_tms or 0) / 1000.0
    d_min = round(d_sec / 60.0, 1)
    d_name = deck_names.get(did, f"Deck {did}")
    print(f"  - {d_name}: {d_cnt}회 ({d_dist}장, {d_min}분, {d_sec:.1f}초)")

con.close()
