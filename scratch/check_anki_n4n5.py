# -*- coding: utf-8 -*-
import sqlite3
import shutil
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_current')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')

con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()

# Get decks
cur.execute('SELECT id, name FROM decks')
decks = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

cur.execute('SELECT crt, mod, dconf, conf FROM col')
col_row = cur.fetchone()
crt = col_row[0]
conf = json.loads(col_row[3]) if col_row[3] else {}
dconf = json.loads(col_row[2]) if col_row[2] else {}

print(f"Collection crt: {datetime.fromtimestamp(crt)}")
print(f"Col conf rollover hour: {conf.get('rollover')}")

cur.execute("PRAGMA table_info(decks)")
print("decks columns:", cur.fetchall())

cur.execute("SELECT * FROM decks")
decks_rows = cur.fetchall()
print(f"decks row count: {len(decks_rows)}")
for r in decks_rows[:5]:
    print("  deck sample:", r[:4])


# Let's check card status in N4 and N5 decks
for did, name in decks.items():
    if not any(k in name for k in ['N4', 'N5']):
        continue
    print(f"\n==========================================")
    print(f"DECK: {name} (did: {did})")
    print(f"==========================================")
    cur.execute('SELECT queue, count(*) FROM cards WHERE did = ? GROUP BY queue', (did,))
    print("Queue counts (0:new, 1:learn, 2:rev, 3:day-learn, -1:susp, -2:user-susp):")
    for q, cnt in cur.fetchall():
        print(f"  queue {q}: {cnt}")

    # Check reviews and due for queue 2 (review)
    cur.execute('SELECT ivl, count(*) FROM cards WHERE did = ? AND queue = 2 GROUP BY ivl ORDER BY ivl', (did,))
    ivls = cur.fetchall()
    print(f"Review intervals (ivl: count): {ivls[:15]}")

    # Check due for queue 2
    # In Anki SM-2: for review cards, due is day number since collection creation or absolute day
    cur.execute('SELECT due, count(*) FROM cards WHERE did = ? AND queue = 2 GROUP BY due ORDER BY due LIMIT 15', (did,))
    dues = cur.fetchall()
    print(f"Review dues (due: count): {dues}")

    # Check cards studied yesterday in revlog
    KST = timezone(timedelta(hours=9))
    s_dt = datetime(2026, 9, 29, 4, 0, 0, tzinfo=KST)
    e_dt = datetime(2026, 9, 30, 4, 0, 0, tzinfo=KST)
    s_ms = int(s_dt.timestamp() * 1000)
    e_ms = int(e_dt.timestamp() * 1000)

    cur.execute('''
        SELECT r.ease, count(*), r.type
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        WHERE c.did = ? AND r.id >= ? AND r.id < ?
        GROUP BY r.ease, r.type
    ''', (did, s_ms, e_ms))
    print("\nYesterday's ratings for this deck (ease, count, type):")
    for row in cur.fetchall():
        print(f"  ease {row[0]}, type {row[2]}: {row[1]}")

    # What are the ivls assigned to cards reviewed yesterday?
    cur.execute('''
        SELECT c.ivl, count(*)
        FROM cards c
        WHERE c.did = ? AND c.id IN (
            SELECT distinct r.cid FROM revlog r WHERE r.id >= ? AND r.id < ?
        )
        GROUP BY c.ivl ORDER BY c.ivl
    ''', (did, s_ms, e_ms))
    print("Current intervals of cards reviewed yesterday:")
    for row in cur.fetchall():
        print(f"  ivl {row[0]} days: {row[1]} cards")

    # Current due of cards reviewed yesterday
    cur.execute('''
        SELECT c.queue, c.due, count(*)
        FROM cards c
        WHERE c.did = ? AND c.id IN (
            SELECT distinct r.cid FROM revlog r WHERE r.id >= ? AND r.id < ?
        )
        GROUP BY c.queue, c.due ORDER BY c.queue, c.due LIMIT 20
    ''', (did, s_ms, e_ms))
    print("Current queue and due of cards reviewed yesterday:")
    for row in cur.fetchall():
        print(f"  queue {row[0]}, due {row[1]}: {row[2]} cards")

con.close()
