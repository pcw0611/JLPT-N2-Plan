# -*- coding: utf-8 -*-
import sqlite3
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TMP_ANKI = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_current.anki2')
shutil.copy2(ANKI_SRC / 'collection.anki2', TMP_ANKI)
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TMP_ANKI.parent / 'anki_inspect_current.anki2-wal')
if (ANKI_SRC / 'collection.anki2-shm').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-shm', TMP_ANKI.parent / 'anki_inspect_current.anki2-shm')

con = sqlite3.connect(TMP_ANKI)
cur = con.cursor()

cur.execute('SELECT id, name FROM decks')
decks = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

print('=== 덱별 카드 총 수 및 상태 ===')
cur.execute('''
    SELECT did, queue, count(*)
    FROM cards
    GROUP BY did, queue
''')
deck_stats = {}
for did, q, cnt in cur.fetchall():
    dname = decks.get(did, f'Deck {did}')
    if dname not in deck_stats:
        deck_stats[dname] = {'new': 0, 'learn': 0, 'review': 0, 'suspended': 0, 'total': 0}
    deck_stats[dname]['total'] += cnt
    if q == 0:
        deck_stats[dname]['new'] += cnt
    elif q in (1, 3):
        deck_stats[dname]['learn'] += cnt
    elif q == 2:
        deck_stats[dname]['review'] += cnt
    elif q < 0:
        deck_stats[dname]['suspended'] += cnt

for dname, s in sorted(deck_stats.items(), key=lambda x: x[1]['total'], reverse=True):
    print(f'{dname}: Total={s["total"]} (Review={s["review"]}, New={s["new"]}, Learn={s["learn"]}, Suspended={s["suspended"]})')

# Interval distribution for Voca N2 and others
print('\n=== N2 Voca 간격(Interval) 및 성숙도(Mature vs Young) 분석 ===')
cur.execute('''
    SELECT c.ivl, count(*)
    FROM cards c
    JOIN decks d ON c.did = d.id
    WHERE d.name LIKE '%4-N2%' AND c.queue = 2
    GROUP BY c.ivl
    ORDER BY c.ivl
''')
ivls = cur.fetchall()
young = sum(cnt for ivl, cnt in ivls if ivl < 21)
mature = sum(cnt for ivl, cnt in ivls if ivl >= 21)
print(f'N2 Voca Review 카드 총: {young + mature}장 (Young(<21일): {young}장, Mature(>=21일): {mature}장)')

# Lapse / Reps analysis for N2
cur.execute('''
    SELECT c.lapses, count(*)
    FROM cards c
    JOIN decks d ON c.did = d.id
    WHERE d.name LIKE '%4-N2%'
    GROUP BY c.lapses
    ORDER BY c.lapses
''')
print('N2 Lapses 분포 (망각 횟수):', cur.fetchall())

con.close()
