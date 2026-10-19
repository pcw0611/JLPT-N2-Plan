# -*- coding: utf-8 -*-
import sqlite3
import shutil
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_full')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TEMP_DIR / 'collection.anki2-shm')

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()
KST = timezone(timedelta(hours=9))

cur.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur.fetchall())
new_rem = queue_counts.get(0, 0)
learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
rev_rem = queue_counts.get(2, 0)
print(f"Current Queue: new={new_rem}, learning={learn_rem}, review={rev_rem}, total={new_rem+learn_rem+rev_rem}")

dates = ['2026-10-16', '2026-10-17', '2026-10-18', '2026-10-19']

for d_str in dates:
    dt = datetime.strptime(d_str, '%Y-%m-%d').replace(tzinfo=KST)
    s_dt = dt.replace(hour=4, minute=0, second=0)
    e_dt = s_dt + timedelta(days=1)
    s_ms = int(s_dt.timestamp() * 1000)
    e_ms = int(e_dt.timestamp() * 1000)
    
    cur.execute('''
        SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
        FROM revlog
        WHERE id >= ? AND id < ?
    ''', (s_ms, e_ms))
    t_cnt, t_tms, t_dist, min_id, max_id = cur.fetchone()
    if not t_cnt:
        print(f"=== {d_str}: No reviews ===")
        continue
    t_sec = (t_tms or 0) / 1000.0
    t_min = t_sec / 60.0
    min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST)
    max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST)
    
    # Voca only
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
    again_c = r_voca.get(1, 0)
    hard_c = r_voca.get(2, 0)
    good_c = r_voca.get(3, 0)
    easy_c = r_voca.get(4, 0)
    again_pct = round((again_c / v_cnt * 100), 2) if v_cnt else 0.0
    
    # Reading deck stats
    cur.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
    ''', (s_ms, e_ms))
    read_row = cur.fetchone()
    read_cnt = read_row[0] or 0
    read_sec = (read_row[1] or 0) / 1000.0
    read_min = read_sec / 60.0
    read_dist = read_row[2] or 0
    
    # Types
    cur.execute('''
        SELECT type, count(*)
        FROM revlog
        WHERE id >= ? AND id < ?
        GROUP BY type
    ''', (s_ms, e_ms))
    type_map = dict(cur.fetchall())
    learn_revs = type_map.get(0, 0)
    revs_done = type_map.get(1, 0)
    relearn_revs = type_map.get(2, 0)
    
    # First time exposed cards
    cur.execute('''
        SELECT count(distinct r.cid)
        FROM revlog r
        WHERE r.id >= ? AND r.id < ?
          AND r.cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
    ''', (s_ms, e_ms, s_ms))
    first_cards = cur.fetchone()[0] or 0
    
    # Decks breakdown
    cur.execute('''
        SELECT c.did, count(*), count(distinct c.id), sum(r.time)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        WHERE r.id >= ? AND r.id < ?
        GROUP BY c.did
        ORDER BY count(*) DESC
    ''', (s_ms, e_ms))
    deck_rows = cur.fetchall()
    
    print(f"=== {d_str} ===")
    print(f"Total: {t_cnt} reviews, {t_sec:.2f}s ({t_min:.2f}m / {int(t_sec//60)}m {round(t_sec%60, 2)}s), distinct: {t_dist}, {min_dt.strftime('%H:%M')} ~ {max_dt.strftime('%H:%M')} KST")
    print(f"Voca: {v_cnt} reviews, {v_sec:.2f}s ({v_min:.2f}m), {v_dist} cards, {v_sec_per_card}s/card, Again: {again_c} ({again_pct}%), Hard: {hard_c}, Good: {good_c}, Easy: {easy_c}")
    if read_cnt:
        print(f"Reading vocab: {read_cnt} reviews, {read_sec:.2f}s ({read_min:.2f}m), {read_dist} cards")
    print(f"Types: Learn={learn_revs}, Review={revs_done}, Relearn={relearn_revs}, First-exposed={first_cards}")
    for did, d_cnt, d_dist, d_tms in deck_rows:
        d_name = deck_names.get(did, f'Deck {did}')
        d_m = round((d_tms or 0) / 60000.0, 1)
        print(f"  - {d_name}: {d_cnt} reviews, {d_dist} cards, {d_m}m")
    print()
con.close()
