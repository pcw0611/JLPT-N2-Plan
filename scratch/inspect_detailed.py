import sqlite3
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

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

cur.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

# Let's inspect revlog intervals
print("=== REVLOG BY SESSIONS / DATES ===")
# 10-16 04:00 to 10-17 04:00
s16 = datetime(2026, 10, 16, 4, 0, 0, tzinfo=KST)
e16 = datetime(2026, 10, 17, 4, 0, 0, tzinfo=KST)
s16_ms, e16_ms = int(s16.timestamp()*1000), int(e16.timestamp()*1000)

cur.execute('SELECT count(*), sum(time)/1000.0, count(distinct cid), min(id), max(id) FROM revlog WHERE id >= ? AND id < ?', (s16_ms, e16_ms))
r16 = cur.fetchone()
print(f"10-16 (04:00 ~ next 04:00): {r16[0]} revs, {r16[1] or 0:.2f}s ({(r16[1] or 0)/60:.2f}m), dist {r16[2]}")
if r16[3]:
    print(f"  Start: {datetime.fromtimestamp(r16[3]/1000.0, tz=KST)}, End: {datetime.fromtimestamp(r16[4]/1000.0, tz=KST)}")

# 10-17 04:00 to now (2026-10-18 ~01:25)
s17 = datetime(2026, 10, 17, 4, 0, 0, tzinfo=KST)
e17_now = datetime.now(tz=KST)
s17_ms = int(s17.timestamp()*1000)
e17_ms = int(e17_now.timestamp()*1000)

cur.execute('SELECT count(*), sum(time)/1000.0, count(distinct cid), min(id), max(id) FROM revlog WHERE id >= ? AND id <= ?', (s17_ms, e17_ms))
r17 = cur.fetchone()
print(f"\n10-17 (04:00 ~ now): {r17[0]} revs, {r17[1] or 0:.2f}s ({(r17[1] or 0)/60:.2f}m), dist {r17[2]}")
if r17[3]:
    print(f"  Start: {datetime.fromtimestamp(r17[3]/1000.0, tz=KST)}, End: {datetime.fromtimestamp(r17[4]/1000.0, tz=KST)}")

# Breakdown of 10-17 (04:00 ~ now) by deck
print("\n--- 10-17 Breakdown by Deck ---")
cur.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id <= ?
    GROUP BY c.did
    ORDER BY count(*) DESC
''', (s17_ms, e17_ms))
for did, cnt, dist, tms in cur.fetchall():
    sec = (tms or 0) / 1000.0
    print(f"  {deck_names.get(did, f'Deck {did}')}: {cnt} reviews ({sec/60:.1f}m, {dist} cards)")

# Ratings for 10-17
print("\n--- 10-17 Ratings (All vs Voca) ---")
cur.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    WHERE r.id >= ? AND r.id <= ?
    GROUP BY r.ease
''', (s17_ms, e17_ms))
print("All ratings:", dict(cur_anki.fetchall() if False else cur.fetchall()))

cur.execute('''
    SELECT r.ease, count(*)
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    JOIN decks d ON c.did = d.id
    WHERE r.id >= ? AND r.id <= ? AND d.name LIKE '%한끝 Voca%'
    GROUP BY r.ease
''', (s17_ms, e17_ms))
print("Voca ratings:", dict(cur.fetchall()))

# Also check 10-16 in database
con_db = sqlite3.connect('database/jlpt_learning.db')
cur_db = con_db.cursor()
print("\n=== DB CURRENT STATE ===")
cur_db.execute("SELECT session_date, verified_minutes, summary FROM study_sessions WHERE session_date >= '2026-10-15'")
for r in cur_db.fetchall():
    print(f"[{r[0]}] {r[1]}m: {r[2][:80]}...")

cur_db.execute("SELECT session_date, source, duration_seconds, notes FROM study_intervals WHERE session_date >= '2026-10-15'")
for r in cur_db.fetchall():
    print(f"[{r[0]}] {r[1]} {r[2]}s: {r[3][:80]}...")
