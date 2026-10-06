import os
import shutil
import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

dst = 'scratch/temp_collection.anki2'
conn = sqlite3.connect(dst)
c = conn.cursor()

c.execute("SELECT id, mid, flds FROM notes WHERE flds LIKE '%062%であれば%' OR flds LIKE '%062%〜(の)であれば%'")
row = c.fetchone()
if not row:
    c.execute("SELECT id, mid, flds FROM notes WHERE flds LIKE '%062%' AND flds LIKE '%접속%'")
    row = c.fetchone()

if row:
    print(f"Note ID: {row[0]}, Model ID: {row[1]}")
    fields = row[2].split('\x1f')
    print("=== FRONT ===")
    print(fields[0])
    print("=== BACK ===")
    print(fields[1])
else:
    print("Not found, searching with flds LIKE '%062%' in grammar deck...")
    c.execute("SELECT n.id, n.flds FROM cards c JOIN notes n ON c.nid = n.id WHERE c.did = 1788792649376 AND n.flds LIKE '%062%'")
    rows = c.fetchall()
    for r in rows:
        print(r[0])
        print(r[1][:500])
