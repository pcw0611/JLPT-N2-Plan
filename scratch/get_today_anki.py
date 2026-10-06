import sqlite3
import shutil
import sys
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_today')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TEMP_DIR / 'collection.anki2-shm')

con_anki = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur_anki = con_anki.cursor()

KST = timezone(timedelta(hours=9))
s_dt = datetime(2026, 10, 6, 4, 0, 0, tzinfo=KST)
e_dt = s_dt + timedelta(days=1)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s_ms, e_ms))
cnt, total_time_ms, distinct_cards, min_id, max_id = cur_anki.fetchone()

sec = (total_time_ms or 0) / 1000.0
mins = sec / 60.0

print(f"2026-10-06 Reviews: {cnt}")
print(f"Total time ms: {total_time_ms}")
print(f"Seconds: {sec:.2f} ({mins:.2f} min)")
print(f"Distinct cards: {distinct_cards}")

# Rating breakdown
cur_anki.execute('''
    SELECT ease, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY ease
''', (s_ms, e_ms))
ratings = dict(cur_anki.fetchall())
print("Ratings:", ratings)

# Type breakdown
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s_ms, e_ms))
types = dict(cur_anki.fetchall())
print("Types (0=learn, 1=review, 2=relearn):", types)

# Deck breakdown
cur_anki.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur_anki.fetchall()}

cur_anki.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
''', (s_ms, e_ms))
deck_breakdown = cur_anki.fetchall()
print("\nDeck breakdown:")
for did, d_cnt, d_dist, d_time in deck_breakdown:
    d_name = deck_names.get(did, f"Deck {did}")
    d_min = (d_time or 0) / 60000.0
    print(f"  {d_name}: {d_cnt} reviews ({d_min:.1f} min, {d_dist} cards)")

# Queue remaining
cur_anki.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur_anki.fetchall())
print("\nRemaining queues:", queue_counts)
con_anki.close()
