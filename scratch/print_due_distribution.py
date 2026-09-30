# -*- coding: utf-8 -*-
import sqlite3
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_current')
con = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur = con.cursor()

# Check future due distribution for N4 and N5
cur.execute('''
    SELECT c.due, 
           count(CASE WHEN c.did = 1787554037894 THEN 1 END) as n4,
           count(CASE WHEN c.did = 1787554037893 THEN 1 END) as n5
    FROM cards c
    WHERE c.queue = 2 AND c.due >= 37 AND c.due <= 45
    GROUP BY c.due
    ORDER BY c.due
''')
rows = cur.fetchall()

days = [
    '2026-09-30 (오늘 수)',
    '2026-10-01 (내일 목)',
    '2026-10-02 (모레 금)',
    '2026-10-03 (토)',
    '2026-10-04 (일)',
    '2026-10-05 (월)',
    '2026-10-06 (화)',
    '2026-10-07 (수)',
    '2026-10-08 (목)',
]

print("=== N4 / N5 일자별 복습 대기(Due) 분포 ===")
for i, (due, n4, n5) in enumerate(rows):
    d_label = days[i] if i < len(days) else f"due {due}"
    print(f"Due {due} | {d_label:<18} | N4: {n4:>3}장 | N5: {n5:>3}장 | 소계: {n4+n5:>3}장")

# Also check other decks for today
cur.execute('SELECT id, name FROM decks')
decks = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

cur.execute('''
    SELECT c.did, count(*)
    FROM cards c
    WHERE c.queue = 2 AND c.due <= 37
    GROUP BY c.did
    ORDER BY count(*) DESC
''')
print("\n=== 오늘(9/30) 전체 덱 복습 대기 현황 ===")
for did, cnt in cur.fetchall():
    print(f"  - {decks.get(did, did)}: {cnt}장")

# Learning cards
cur.execute('''
    SELECT c.did, count(*)
    FROM cards c
    WHERE c.queue IN (1, 3)
    GROUP BY c.did
''')
print("\n=== 재학습(Learning) 대기 현황 ===")
for did, cnt in cur.fetchall():
    print(f"  - {decks.get(did, did)}: {cnt}장")

con.close()
