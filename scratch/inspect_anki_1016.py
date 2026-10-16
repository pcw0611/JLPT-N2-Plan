# -*- coding: utf-8 -*-
import sqlite3
import shutil
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

src = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1\collection.anki2')
temp = Path(r'C:\Users\pcw06\AppData\Local\Temp\inspect_anki_1016.anki2')
shutil.copy2(src, temp)
wal = src.with_name('collection.anki2-wal')
if wal.exists():
    shutil.copy2(wal, temp.with_name('inspect_anki_1016.anki2-wal'))

con = sqlite3.connect(temp)
cur = con.cursor()
KST = timezone(timedelta(hours=9))

cur.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur.fetchall())
new_rem = queue_counts.get(0, 0)
learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
rev_rem = queue_counts.get(2, 0)

print(f"Queue remaining: new={new_rem:,}, learning={learn_rem:,}, review={rev_rem:,}, total={new_rem+learn_rem+rev_rem:,}")

s15_ms = int(datetime(2026, 10, 15, 4, 0, 0, tzinfo=KST).timestamp() * 1000)
s16_ms = int(datetime(2026, 10, 16, 4, 0, 0, tzinfo=KST).timestamp() * 1000)
e16_ms = int(datetime(2026, 10, 17, 4, 0, 0, tzinfo=KST).timestamp() * 1000)

for d_label, s_ms, e_ms in [('2026-10-15', s15_ms, s16_ms), ('2026-10-16', s16_ms, e16_ms)]:
    print(f"\n=== {d_label} ===")
    cur.execute('SELECT count(*), sum(time), count(distinct cid), min(id), max(id) FROM revlog WHERE id >= ? AND id < ?', (s_ms, e_ms))
    t_cnt, t_tms, t_dist, min_id, max_id = cur.fetchone()
    if not t_cnt:
        print("No reviews")
        continue
    t_sec = (t_tms or 0) / 1000.0
    min_dt = datetime.fromtimestamp(min_id/1000.0, tz=KST)
    max_dt = datetime.fromtimestamp(max_id/1000.0, tz=KST)
    print(f"Total: {t_cnt:,} reviews, {t_sec:.2f}s ({t_sec/60:.2f}m / {int(t_sec//60)}m {round(t_sec%60, 2)}s), {t_dist} distinct cards")
    print(f"Span: {min_dt.strftime('%H:%M:%S')} ~ {max_dt.strftime('%H:%M:%S')} KST")

    # Overall review types
    cur.execute('SELECT type, count(*) FROM revlog WHERE id >= ? AND id < ? GROUP BY type', (s_ms, e_ms))
    type_map = dict(cur.fetchall())
    print(f"Review types: learn(0)={type_map.get(0,0)}, review(1)={type_map.get(1,0)}, relearn(2)={type_map.get(2,0)}, filtered(3)={type_map.get(3,0)}")

    # First time exposed cards
    cur.execute('''
        SELECT count(distinct r.cid)
        FROM revlog r
        WHERE r.id >= ? AND r.id < ?
          AND r.cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
    ''', (s_ms, e_ms, s_ms))
    first_cards = cur.fetchone()[0] or 0
    print(f"First-time cards exposed: {first_cards}")

    # Voca only
    cur.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
    ''', (s_ms, e_ms))
    v_cnt, v_tms, v_dist = cur.fetchone()
    v_sec = (v_tms or 0) / 1000.0
    v_sec_per_card = round(v_sec / v_cnt, 2) if v_cnt else 0
    print(f"Voca only: {v_cnt:,} reviews, {v_sec:.2f}s ({v_sec/60:.2f}m), {v_dist} cards, sec/card={v_sec_per_card}")

    cur.execute('''
        SELECT r.ease, count(*)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%한끝 Voca%'
        GROUP BY r.ease
    ''', (s_ms, e_ms))
    v_ease = dict(cur.fetchall())
    v_again = v_ease.get(1, 0)
    v_hard = v_ease.get(2, 0)
    v_good = v_ease.get(3, 0)
    v_easy = v_ease.get(4, 0)
    v_again_pct = round(v_again / v_cnt * 100, 2) if v_cnt else 0
    print(f"Voca ease: Again {v_again} ({v_again_pct}%), Hard {v_hard}, Good {v_good}, Easy {v_easy}")

    # Reading deck
    cur.execute('''
        SELECT count(*), sum(r.time), count(distinct r.cid)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        JOIN decks d ON c.did = d.id
        WHERE r.id >= ? AND r.id < ? AND d.name LIKE '%독해・기사・모의고사%'
    ''', (s_ms, e_ms))
    r_cnt, r_tms, r_dist = cur.fetchone()
    r_sec = (r_tms or 0) / 1000.0
    print(f"Reading deck: {r_cnt:,} reviews, {r_sec:.2f}s ({r_sec/60:.2f}m), {r_dist} cards")

    # Decks breakdown
    print("Decks breakdown:")
    cur.execute('''
        SELECT c.did, count(*), count(distinct c.id), sum(r.time)
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        WHERE r.id >= ? AND r.id < ?
        GROUP BY c.did
        ORDER BY count(*) DESC
    ''', (s_ms, e_ms))
    for did, d_cnt, d_dist, d_tms in cur.fetchall():
        d_sec = (d_tms or 0) / 1000.0
        d_m = round(d_sec / 60.0, 1)
        d_name = deck_names.get(did, f"Deck {did}")
        print(f"  - {d_name}: {d_cnt:,} reviews, {d_m}m ({d_sec:.1f}s), {d_dist} cards")
