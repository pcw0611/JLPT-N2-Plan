# -*- coding: utf-8 -*-
import sqlite3
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DB = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_test\collection.anki2')
con = sqlite3.connect(TEMP_DB)
cur = con.cursor()

# Decks
cur.execute('SELECT id, name FROM decks')
decks = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

# Filter for JLPT decks (excluding TOEIC)
jlpt_deck_ids = [did for did, name in decks.items() if 'JLPT' in name or '한끝' in name]
print("JLPT Decks:", [decks[did] for did in jlpt_deck_ids])

placeholders = ','.join('?' for _ in jlpt_deck_ids)

# Card status for JLPT decks
cur.execute(f'''
    SELECT 
        queue,
        type,
        case 
            when queue = 0 then 'New'
            when queue in (1, 3) then 'Learning'
            when queue = 2 and ivl >= 21 then 'Mature'
            when queue = 2 and ivl < 21 then 'Young'
            when queue = -1 then 'Suspended'
            when queue = -2 then 'Buried'
            else 'Other'
        end as status,
        count(*),
        avg(ivl),
        max(ivl),
        avg(reps),
        avg(lapses)
    FROM cards
    WHERE did IN ({placeholders})
    GROUP BY status
''', jlpt_deck_ids)

print("\n--- JLPT Cards Status Breakdown ---")
for r in cur.fetchall():
    print(f"Status: {r[2]} | Count: {r[3]} | Avg Ivl: {r[4]:.1f}d | Max Ivl: {r[5]}d | Avg Reps: {r[6]:.1f} | Avg Lapses: {r[7]:.1f}")

# Detail for '한끝 Voca' specifically
voca_deck_ids = [did for did, name in decks.items() if '한끝 Voca' in name]
placeholders_voca = ','.join('?' for _ in voca_deck_ids)

cur.execute(f'''
    SELECT 
        case 
            when queue = 0 then 'New'
            when queue in (1, 3) then 'Learning'
            when queue = 2 and ivl >= 21 then 'Mature'
            when queue = 2 and ivl < 21 then 'Young'
            else 'Other'
        end as status,
        count(*),
        avg(ivl),
        max(ivl),
        avg(reps),
        avg(lapses)
    FROM cards
    WHERE did IN ({placeholders_voca})
    GROUP BY status
''', voca_deck_ids)

print("\n--- 한끝 Voca Cards Status Breakdown (Total 2,797 cards) ---")
for r in cur.fetchall():
    print(f"Status: {r[0]} | Count: {r[1]} | Avg Ivl: {r[2]:.1f}d | Max Ivl: {r[3]}d | Avg Reps: {r[4]:.1f} | Avg Lapses: {r[5]:.1f}")

# Interval bands for 한끝 Voca
cur.execute(f'''
    SELECT 
        case 
            when ivl >= 90 then '4. 90일 이상 (3개월+ 장기 기억)'
            when ivl >= 30 then '3. 30~89일 (1~3개월 성숙)'
            when ivl >= 21 then '2. 21~29일 (초기 성숙)'
            when ivl >= 7 then '1. 7~20일 (단기 정착)'
            else '0. 7일 미만'
        end as band,
        count(*)
    FROM cards
    WHERE did IN ({placeholders_voca}) AND queue = 2
    GROUP BY band
    ORDER BY band DESC
''', voca_deck_ids)
print("\n--- 한끝 Voca Review Cards Interval Bands ---")
for r in cur.fetchall():
    print(f"{r[0]}: {r[1]} cards ({r[1]/2797*100:.1f}%)")

# N2 deck specifically
n2_deck_ids = [did for did, name in decks.items() if '4-N2' in name]
cur.execute(f'''
    SELECT 
        case 
            when queue = 0 then 'New'
            when queue in (1, 3) then 'Learning'
            when queue = 2 and ivl >= 21 then 'Mature'
            when queue = 2 and ivl < 21 then 'Young'
            else 'Other'
        end as status,
        count(*),
        avg(ivl),
        max(ivl)
    FROM cards
    WHERE did IN ({','.join('?' for _ in n2_deck_ids)})
    GROUP BY status
''', n2_deck_ids)
print("\n--- 4-N2 Deck Status ---")
for r in cur.fetchall():
    print(f"Status: {r[0]} | Count: {r[1]} | Avg Ivl: {r[2]:.1f}d | Max Ivl: {r[3]}d")

# Total reviews in revlog for JLPT
cur.execute(f'''
    SELECT count(*), sum(r.time)/1000.0/60.0
    FROM revlog r
    JOIN cards c ON r.cid = c.id
    WHERE c.did IN ({placeholders_voca})
''', voca_deck_ids)
v_revs, v_mins = cur.fetchone()
print(f"\nTotal 한끝 Voca Reviews in Anki: {v_revs:,} reviews, {v_mins:.1f} mins ({v_mins/60:.1f} hours)")

con.close()
