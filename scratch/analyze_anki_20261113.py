# -*- coding: utf-8 -*-
import sqlite3
import shutil
import sys
import json
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

cur.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur_anki_q := cur.fetchall())
new_rem = queue_counts.get(0, 0)
learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
rev_rem = queue_counts.get(2, 0)
print(f"Cards queue: new {new_rem}, learn {learn_rem}, rev {rev_rem}, total {new_rem+learn_rem+rev_rem}")

# 2026-11-13 interval
s_dt = datetime(2026, 11, 13, 4, 0, 0, tzinfo=KST)
e_dt = s_dt + timedelta(days=1)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

cur.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s_ms, e_ms))
t_cnt, t_tms, t_dist, min_id, max_id = cur.fetchone()
t_sec = (t_tms or 0) / 1000.0
min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST)
max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST)

print(f"2026-11-13 Total Reviews: {t_cnt}, Distinct Cards: {t_dist}")
print(f"Total Time: {t_sec:.2f}s ({int(t_sec//60)}m {t_sec%60:.2f}s, {t_sec/60.0:.2f}min)")
print(f"Time Span: {min_dt.strftime('%H:%M:%S')} ~ {max_dt.strftime('%H:%M:%S')} KST")

# By Deck
cur.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY sum(r.time) DESC
''', (s_ms, e_ms))
for did, cnt, dist, tms in cur.fetchall():
    d_name = deck_names.get(did, f"Deck {did}")
    sec = (tms or 0) / 1000.0
    print(f"  - {d_name}: {cnt} reviews ({sec/60.0:.1f}m / {sec:.1f}s), {dist} distinct cards")

# Han kkeut Voca breakdown
cur.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
''', (s_ms, e_ms))
v_cnt, v_tms, v_dist = cur.fetchone()
v_cnt = v_cnt or 0
v_sec = (v_tms or 0) / 1000.0
v_min = v_sec / 60.0
v_sec_per_card = round(v_sec / v_cnt, 2) if v_cnt else 0

cur.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s_ms, e_ms))
r_voca = dict(cur.fetchall())
print(f"\nHankkeut Voca: {v_cnt} reviews ({v_min:.2f}m), {v_dist} distinct, {v_sec_per_card}s/card")
print(f"  Again: {r_voca.get(1, 0)} ({r_voca.get(1, 0)/v_cnt*100:.2f}%)")
print(f"  Hard:  {r_voca.get(2, 0)} ({r_voca.get(2, 0)/v_cnt*100:.2f}%)")
print(f"  Good:  {r_voca.get(3, 0)} ({r_voca.get(3, 0)/v_cnt*100:.2f}%)")
print(f"  Easy:  {r_voca.get(4, 0)} ({r_voca.get(4, 0)/v_cnt*100:.2f}%)")

# Mock vocab breakdown
cur.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%모의고사%' AND d.name NOT LIKE '%독해%'
''', (s_ms, e_ms))
mock_row = cur.fetchone()
print(f"\nMock vocab: {mock_row[0]} reviews, {mock_row[1]/1000.0/60.0:.1f}m, {mock_row[2]} distinct")

# Reading deck
cur.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
''', (s_ms, e_ms))
read_row = cur.fetchone()
print(f"Reading deck: {read_row[0]} reviews, {read_row[1]/1000.0/60.0:.1f}m, {read_row[2]} distinct")

# N1 Sampler
cur.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%15 실생활%'
''', (s_ms, e_ms))
samp_row = cur.fetchone()
print(f"N1 Sampler: {samp_row[0]} reviews, {samp_row[1]/1000.0/60.0:.1f}m, {samp_row[2]} distinct")

# TOEIC
cur.execute('''
    SELECT count(*), sum(r.time), count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%TOEIC%'
''', (s_ms, e_ms))
toeic_row = cur.fetchone()
print(f"TOEIC: {toeic_row[0]} reviews, {toeic_row[1]/1000.0/60.0:.1f}m, {toeic_row[2]} distinct")

con.close()
