# -*- coding: utf-8 -*-
"""Inspect Anki reviews and calculate statistics for 2026-09-18 study day."""
import sqlite3
import shutil
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

src = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_0918')
dst.mkdir(exist_ok=True)
shutil.copy2(src / 'collection.anki2', dst / 'collection.anki2')
if (src / 'collection.anki2-wal').exists():
    shutil.copy2(src / 'collection.anki2-wal', dst / 'collection.anki2-wal')

con = sqlite3.connect(dst / 'collection.anki2')
cur = con.cursor()

# Inspect schema
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]

deck_names = {}
if 'decks' in tables:
    cur.execute("SELECT id, name FROM decks")
    deck_names = {r[0]: r[1] for r in cur.fetchall()}
else:
    cur.execute('SELECT decks FROM col')
    row = cur.fetchone()
    if row and row[0]:
        try:
            decks = json.loads(row[0])
            deck_names = {int(k): v.get('name', 'Unknown') for k, v in decks.items()}
        except Exception as e:
            print('Could not load decks json:', e)

# KST timezone
KST = timezone(timedelta(hours=9))
start_dt = datetime(2026, 9, 18, 4, 0, 0, tzinfo=KST)
end_dt = datetime(2026, 9, 19, 4, 0, 0, tzinfo=KST)
start_ms = int(start_dt.timestamp() * 1000)
end_ms = int(end_dt.timestamp() * 1000)

print(f'Querying revlog between {start_dt} ({start_ms}) and {end_dt} ({end_ms})')

cur.execute('''
    SELECT r.id, r.cid, r.ease, r.time, r.type, c.did
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    ORDER BY r.id ASC
''', (start_ms, end_ms))

rows = cur.fetchall()
print(f'Total reviews for 2026-09-18 study day: {len(rows)}')

if rows:
    first_time = datetime.fromtimestamp(rows[0][0]/1000, tz=KST)
    last_time = datetime.fromtimestamp(rows[-1][0]/1000, tz=KST)
    print(f'First review: {first_time}, Last review: {last_time}')
    
    total_time_ms = sum(r[3] for r in rows)
    total_time_sec = total_time_ms / 1000.0
    total_time_min = total_time_sec / 60.0
    print(f'Total time: {total_time_sec:.2f}s ({total_time_min:.2f}m, {total_time_min/60:.2f}h)')
    print(f'Seconds per card: {total_time_sec / len(rows):.2f}s')

    # Unique cards
    unique_cids = set(r[1] for r in rows)
    print(f'Unique cards studied: {len(unique_cids)}')
    
    # Eases: 1=Again, 2=Hard, 3=Good, 4=Easy
    ease_counts = {}
    for r in rows:
        ease_counts[r[2]] = ease_counts.get(r[2], 0) + 1
    print('Ease counts (1=Again, 2=Hard, 3=Good, 4=Easy):', ease_counts)
    again_cnt = ease_counts.get(1, 0)
    again_pct = (again_cnt / len(rows)) * 100.0
    print(f'Again count: {again_cnt} ({again_pct:.2f}%)')

    # Review type counts (0=learn, 1=review, 2=relearn, 3=cram)
    type_counts = {}
    for r in rows:
        type_counts[r[4]] = type_counts.get(r[4], 0) + 1
    print('Type counts (0=learn, 1=review, 2=relearn, 3=cram):', type_counts)
    learn_relearn_cnt = type_counts.get(0, 0) + type_counts.get(2, 0)
    review_done_cnt = type_counts.get(1, 0)
    print(f'Learning reviews (learn+relearn): {learn_relearn_cnt}, Review reviews: {review_done_cnt}')
    
    # By deck
    deck_stats = {}
    for r in rows:
        did = r[5]
        dname = deck_names.get(did, f'Deck {did}')
        if dname not in deck_stats:
            deck_stats[dname] = {'count': 0, 'time_ms': 0, 'cards': set(), 'eases': {}}
        deck_stats[dname]['count'] += 1
        deck_stats[dname]['time_ms'] += r[3]
        deck_stats[dname]['cards'].add(r[1])
        deck_stats[dname]['eases'][r[2]] = deck_stats[dname]['eases'].get(r[2], 0) + 1
        
    print('\n--- Deck breakdown ---')
    for dname, st in sorted(deck_stats.items(), key=lambda x: x[1]['count'], reverse=True):
        t_sec = st['time_ms'] / 1000.0
        print(f"{dname}: {st['count']} reviews, {t_sec:.1f}s ({t_sec/60:.2f}m), {len(st['cards'])} unique cards, eases: {st['eases']}")

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
print('\nCurrent queue counts (across all cards):', dict(cur.fetchall()))

# Find how many new cards were first studied today
cur.execute('''
    SELECT count(distinct cid)
    FROM revlog
    WHERE id >= ? AND id < ?
      AND cid NOT IN (
          SELECT cid FROM revlog WHERE id < ?
      )
''', (start_ms, end_ms, start_ms))
new_today_count = cur.fetchone()[0]
print(f'\nTotal brand new cards first studied today: {new_today_count}')

# Break down brand new cards by deck
cur.execute('''
    SELECT c.did, count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
      AND r.cid NOT IN (
          SELECT cid FROM revlog WHERE id < ?
      )
    GROUP BY c.did
''', (start_ms, end_ms, start_ms))
for did, cnt in cur.fetchall():
    dname = deck_names.get(did, f'Deck {did}')
    print(f'New cards in {dname}: {cnt}')

# Check unseen cards in N2 and N3 etc.
print('\n--- Queues per deck ---')
for did, dname in sorted(deck_names.items(), key=lambda x: x[1]):
    cur.execute('SELECT queue, count(*) FROM cards WHERE did = ? GROUP BY queue', (did,))
    q_cnt = dict(cur.fetchall())
    if q_cnt:
        print(f"Deck '{dname}' (did={did}) queues: {q_cnt}")

con.close()
