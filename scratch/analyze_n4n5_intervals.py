# -*- coding: utf-8 -*-
import sqlite3
import shutil
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_current')
con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()

# Get decks
cur.execute('SELECT id, name FROM decks')
decks = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

KST = timezone(timedelta(hours=9))
s_dt = datetime(2026, 9, 29, 4, 0, 0, tzinfo=KST)
e_dt = datetime(2026, 9, 30, 4, 0, 0, tzinfo=KST)
s_ms = int(s_dt.timestamp() * 1000)
e_ms = int(e_dt.timestamp() * 1000)

for deck_pattern in ['N5', 'N4']:
    target_dids = [did for did, name in decks.items() if deck_pattern in name]
    print(f"\n==========================================")
    print(f"ANALYSIS FOR DECK: {deck_pattern}")
    print(f"==========================================")
    
    # Check revlog for these decks yesterday
    cur.execute('''
        SELECT r.cid, r.ease, r.ivl, r.lastIvl, r.type, r.id
        FROM revlog r
        JOIN cards c ON r.cid = c.id
        WHERE c.did IN ({}) AND r.id >= ? AND r.id < ?
        ORDER BY r.id ASC
    '''.format(','.join(map(str, target_dids))), (s_ms, e_ms))
    reviews = cur.fetchall()
    print(f"Total review entries yesterday: {len(reviews)}")
    
    # Group by cid: see the LAST review of each card yesterday
    card_last_rev = {}
    for r in reviews:
        card_last_rev[r[0]] = r  # overwrites with later reviews
    
    print(f"Unique cards reviewed yesterday: {len(card_last_rev)}")
    
    # What was the final ease and final ivl of each card yesterday?
    final_eases = {}
    final_ivls = {}
    for cid, r in card_last_rev.items():
        ease = r[1]
        ivl = r[2]
        final_eases[ease] = final_eases.get(ease, 0) + 1
        final_ivls[ivl] = final_ivls.get(ivl, 0) + 1
        
    print(f"Final ease pressed on cards (1:Again, 2:Hard, 3:Good, 4:Easy): {sorted(final_eases.items())}")
    print(f"Final ivl recorded in revlog: {sorted(final_ivls.items())[:20]}")
    
    # Let's inspect 5 sample cards that got ivl=3, ivl=4, ivl=5
    print("\nSample cards review history for cards with ivl >= 3:")
    sample_cids = [cid for cid, r in card_last_rev.items() if r[2] in (3, 4, 5)][:5]
    for cid in sample_cids:
        cur.execute('SELECT queue, due, ivl, reps, lapses FROM cards WHERE id = ?', (cid,))
        card_row = cur.fetchone()
        cur.execute('SELECT id, ease, ivl, lastIvl, type, factor FROM revlog WHERE cid = ? ORDER BY id ASC', (cid,))
        rev_history = cur.fetchall()
        print(f"  CID {cid}: current card state={card_row}")
        for rh in rev_history[-5:]:
            t_str = datetime.fromtimestamp(rh[0]/1000, tz=KST).strftime('%m-%d %H:%M:%S')
            print(f"    {t_str} ease={rh[1]}, ivl={rh[2]}, lastIvl={rh[3]}, type={rh[4]}, factor={rh[5]}")

con.close()
