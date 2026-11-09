import sqlite3, shutil, os, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

KST = timezone(timedelta(hours=9))
ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_tmp')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()

cur.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

for d_str in ['2026-11-08', '2026-11-09']:
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
    t_sec = (t_tms or 0)/1000.0
    min_dt = datetime.fromtimestamp(min_id/1000.0, tz=KST) if min_id else None
    max_dt = datetime.fromtimestamp(max_id/1000.0, tz=KST) if max_id else None
    print(f'=== {d_str} ===')
    print(f'Total: {t_cnt} reviews, {t_sec:.2f}s ({t_sec/60:.2f}m / {int(t_sec//60)}m {t_sec%60:.2f}s), distinct cards: {t_dist}')
    if min_dt:
        print(f'Time range: {min_dt.strftime("%H:%M:%S")} ~ {max_dt.strftime("%H:%M:%S")} KST')
    
    # Decks
    cur.execute('''
        SELECT c.did, count(*), count(distinct c.id), sum(r.time)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        WHERE r.id >= ? AND r.id < ?
        GROUP BY c.did
        ORDER BY sum(r.time) DESC
    ''', (s_ms, e_ms))
    for did, d_cnt, d_dist, d_tms in cur.fetchall():
        d_sec = (d_tms or 0)/1000.0
        print(f'  - {deck_names.get(did, did)}: {d_cnt} reviews, {d_sec/60:.2f}m ({d_sec:.1f}s), distinct: {d_dist}')

    # Ratings in 한끝 Voca
    cur.execute('''
        SELECT r.ease, count(*)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
        GROUP BY r.ease
    ''', (s_ms, e_ms))
    ratings = dict(cur.fetchall())
    v_again = ratings.get(1, 0)
    v_hard = ratings.get(2, 0)
    v_good = ratings.get(3, 0)
    v_easy = ratings.get(4, 0)
    v_tot = sum(ratings.values())
    print(f'  한끝 Voca ratings ({v_tot} reviews): Again {v_again} ({v_again/v_tot*100:.2f}%), Hard {v_hard} ({v_hard/v_tot*100:.2f}%), Good {v_good} ({v_good/v_tot*100:.2f}%), Easy {v_easy} ({v_easy/v_tot*100:.2f}%)')

    # Reading deck
    cur.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
    ''', (s_ms, e_ms))
    read_row = cur.fetchone()
    print(f'  독해어휘: {read_row[0]} reviews, {(read_row[1] or 0)/60000.0:.2f}m, distinct: {read_row[2]}')

# Queue counts
cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur.fetchall())
new_rem = queue_counts.get(0, 0)
learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
rev_rem = queue_counts.get(2, 0)
print(f'\nCurrent queue: new {new_rem}, learning {learn_rem}, review {rev_rem} (total {new_rem+learn_rem+rev_rem})')
