# -*- coding: utf-8 -*-
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
temp_dir = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_test')
temp_dir.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', temp_dir / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', temp_dir / 'collection.anki2-wal')

con = sqlite3.connect(temp_dir / 'collection.anki2')
cur = con.cursor()

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur.fetchall())
new_rem = queue_counts.get(0, 0)
learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
rev_rem = queue_counts.get(2, 0)
print(f'Remaining cards: new {new_rem}, learn {learn_rem}, rev {rev_rem}, total {new_rem + learn_rem + rev_rem}')

cur.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

for d_str in ['2026-11-07', '2026-11-08']:
    y, m, d = map(int, d_str.split('-'))
    s_dt = datetime(y, m, d, 4, 0, 0, tzinfo=KST)
    e_dt = s_dt + timedelta(days=1)
    s_ms = int(s_dt.timestamp() * 1000)
    e_ms = int(e_dt.timestamp() * 1000)

    cur.execute('SELECT count(*), sum(time), count(distinct cid), min(id), max(id) FROM revlog WHERE id >= ? AND id < ?', (s_ms, e_ms))
    t_cnt, t_tms, t_dist, min_id, max_id = cur.fetchone()
    if not t_cnt:
        print(f'{d_str}: No reviews')
        continue
    t_sec = t_tms / 1000.0
    min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST)
    max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST)
    
    # 한끝 Voca
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

    # Reading deck
    cur.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
    ''', (s_ms, e_ms))
    read_row = cur_anki_reading = cur.fetchone()
    read_cnt = read_row[0] or 0
    read_sec = (read_row[1] or 0) / 1000.0
    read_dist = read_row[2] or 0

    # TOEIC decks
    cur.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%TOEIC%'
    ''', (s_ms, e_ms))
    toeic_row = cur.fetchone()
    toeic_cnt = toeic_row[0] or 0
    toeic_sec = (toeic_row[1] or 0) / 1000.0
    toeic_dist = toeic_row[2] or 0

    print(f'=== {d_str} ===')
    print(f'Total: {t_cnt} reviews, {t_sec:.2f}s ({t_sec/60:.2f}m), {min_dt.strftime("%H:%M")} ~ {max_dt.strftime("%H:%M")} KST, distinct: {t_dist}')
    print(f'Voca: {v_cnt} reviews, {v_sec:.2f}s ({v_sec/60:.2f}m), per_card: {v_sec_per_card}s')
    print(f'Ratings: Again {v_again} ({v_again_pct}%), Hard {v_hard}, Good {v_good}, Easy {v_easy}')
    print(f'Reading: {read_cnt} reviews, {read_sec:.2f}s')
    print(f'TOEIC: {toeic_cnt} reviews, {toeic_sec:.2f}s')

    # Decks breakdown
    cur.execute('''
        SELECT c.did, count(*), count(distinct c.id), sum(r.time)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        WHERE r.id >= ? AND r.id < ?
        GROUP BY c.did
        ORDER BY sum(r.time) DESC
    ''', (s_ms, e_ms))
    for did, d_cnt, d_dist, d_tms in cur.fetchall():
        d_name = deck_names.get(did, f'Deck {did}')
        d_sec = (d_tms or 0) / 1000.0
        print(f'  - {d_name}: {d_cnt} reviews, {d_sec/60:.1f}m ({d_sec:.1f}s), distinct {d_dist}')

con.close()
