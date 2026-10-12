# -*- coding: utf-8 -*-
import sqlite3
import shutil
import sys
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1012')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TEMP_DIR / 'collection.anki2-shm')

con_anki = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur_anki = con_anki.cursor()

KST = timezone(timedelta(hours=9))
d_str = '2026-10-12'

s_dt = datetime(2026, 10, 12, 4, 0, 0, tzinfo=KST)
e_dt = s_dt + timedelta(days=1)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

cur_anki.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
queue_counts = dict(cur_anki.fetchall())
new_rem = queue_counts.get(0, 0)
learn_rem = queue_counts.get(1, 0) + queue_counts.get(3, 0)
rev_rem = queue_counts.get(2, 0)

cur_anki.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur_anki.fetchall()}

cur_anki.execute('''
    SELECT count(*), sum(time), count(distinct cid), min(id), max(id)
    FROM revlog
    WHERE id >= ? AND id < ?
''', (s_ms, e_ms))
cnt, total_time_ms, distinct_cards, min_id, max_id = cur_anki.fetchone()
cnt = cnt or 0
anki_sec = (total_time_ms or 0) / 1000.0
anki_mins = anki_sec / 60.0
sec_per_card = round(anki_sec / cnt, 2) if cnt else 0

min_dt = datetime.fromtimestamp(min_id / 1000.0, tz=KST) if min_id else s_dt
max_dt = datetime.fromtimestamp(max_id / 1000.0, tz=KST) if max_id else s_dt
min_dt_str = min_dt.strftime('%H:%M')
max_dt_str = max_dt.strftime('%H:%M')

# Ratings
cur_anki.execute('''
    SELECT ease, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY ease
''', (s_ms, e_ms))
rating_map = dict(cur_anki.fetchall())
again_c = rating_map.get(1, 0)
hard_c = rating_map.get(2, 0)
good_c = rating_map.get(3, 0)
easy_c = rating_map.get(4, 0)
again_pct = round((again_c / cnt * 100), 2) if cnt else 0.0

# Types (0=learn, 1=review, 2=relearn, 3=cram)
cur_anki.execute('''
    SELECT type, count(*)
    FROM revlog
    WHERE id >= ? AND id < ?
    GROUP BY type
''', (s_ms, e_ms))
type_map = dict(cur_anki.fetchall())
learn_revs = type_map.get(0, 0) + type_map.get(2, 0)
revs_done = type_map.get(1, 0) + type_map.get(3, 0)

# Check new cards studied today (first revlog entry for card in this day)
cur_anki.execute('''
    SELECT count(distinct cid)
    FROM revlog
    WHERE id >= ? AND id < ?
      AND cid NOT IN (SELECT cid FROM revlog WHERE id < ?)
''', (s_ms, e_ms, s_ms))
new_cards_studied_today = cur_anki.fetchone()[0] or 0

# Decks breakdown
cur_anki.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s_ms, e_ms))
deck_breakdown = []
deck_lines = []
for did, d_cnt, d_dist, d_tms in cur_anki.fetchall():
    d_sec = (d_tms or 0) / 1000.0
    d_min = round(d_sec / 60.0, 1)
    d_name = deck_names.get(did, f"Deck {did}")
    deck_breakdown.append({
        'deckId': did,
        'deckName': d_name,
        'reviews': d_cnt,
        'distinctCards': d_dist,
        'studyMinutes': d_min,
        'seconds': round(d_sec, 1)
    })
    deck_lines.append(f"{d_name} {d_cnt:,}회({d_min}분)")

# Grammar reviewed today
cur_anki.execute('''
    SELECT count(distinct r.cid)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ? AND c.did IN (
        SELECT id FROM decks WHERE name LIKE '%문법%' OR name LIKE '%JLPT N2%'
    )
''', (s_ms, e_ms))
grammar_reviewed_today = cur_anki.fetchone()[0] or 0

print(f"Date: {d_str}")
print(f"Total reviews: {cnt:,}")
print(f"Total time: {anki_sec:.2f}s ({anki_mins:.2f}m / {int(anki_sec//60)}m {round(anki_sec%60, 2)}s)")
print(f"Distinct cards: {distinct_cards}")
print(f"Sec per card: {sec_per_card}s")
print(f"Time span: {min_dt_str} ~ {max_dt_str} KST ({min_dt.strftime('%H:%M:%S')} ~ {max_dt.strftime('%H:%M:%S')})")
print(f"Ratings: Again {again_c} ({again_pct}%), Hard {hard_c} ({round(hard_c/cnt*100, 2)}%), Good {good_c} ({round(good_c/cnt*100, 2)}%), Easy {easy_c} ({round(easy_c/cnt*100, 2)}%)")
print(f"New cards studied today: {new_cards_studied_today}")
print(f"Grammar reviewed today: {grammar_reviewed_today}")
print(f"Queue remaining: new {new_rem:,}, learn {learn_rem:,}, review {rev_rem:,} (total {new_rem+learn_rem+rev_rem:,})")
print("Decks:")
for dl in deck_lines:
    print(f"  - {dl}")

con_anki.close()
