import sqlite3
import shutil
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_detailed')
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

for d_str in ['2026-11-02', '2026-11-03']:
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
    t_cnt, t_tms, t_dist, min_id, max_id = cur.fetchone()
    if not t_cnt:
        continue
    t_sec = (t_tms or 0) / 1000.0
    t_min = t_sec / 60.0
    min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST)
    max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST)

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
    v_again = r_voca.get(1, 0)
    v_hard = r_voca.get(2, 0)
    v_good = r_voca.get(3, 0)
    v_easy = r_voca.get(4, 0)
    v_again_pct = round((v_again / v_cnt * 100), 2) if v_cnt else 0.0

    cur.execute('''
        SELECT type, count(*)
        FROM revlog
        WHERE id >= ? AND id < ?
        GROUP BY type
    ''', (s_ms, e_ms))
    type_map = dict(cur.fetchall())

    cur.execute('''
        SELECT c.did, count(*), count(distinct c.id), sum(r.time)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        WHERE r.id >= ? AND r.id < ?
        GROUP BY c.did
        ORDER BY sum(r.time) DESC
    ''', (s_ms, e_ms))
    decks_info = []
    for did, d_cnt, d_dist, d_tms in cur.fetchall():
        d_sec = (d_tms or 0) / 1000.0
        decks_info.append((deck_names.get(did, did), d_cnt, d_sec, d_dist))

    print(f"=== {d_str} ===")
    print(f"Total: {t_cnt} reviews, {t_sec:.2f}s ({t_min:.2f}m), dist {t_dist}, range: {min_dt.strftime('%H:%M')}~{max_dt.strftime('%H:%M')} KST")
    print(f"Voca: {v_cnt} revs, {v_sec:.2f}s, card/sec: {v_sec_per_card}s, Again: {v_again} ({v_again_pct}%), Hard: {v_hard}, Good: {v_good}, Easy: {v_easy}")
    print(f"Types: {type_map}")
    print("Decks:")
    for name, d_cnt, d_sec, d_dist in decks_info:
        print(f"  - {name}: {d_cnt} revs, {d_sec:.1f}s ({d_sec/60.0:.1f}m), {d_dist} cards")

con.close()
