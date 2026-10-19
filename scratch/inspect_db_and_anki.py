import sqlite3
from pathlib import Path

DB = Path('database/jlpt_learning.db')
con = sqlite3.connect(DB)
cur = con.cursor()

print('--- tables ---')
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print(tables)

for t in ['daily_logs', 'anki_daily_summary', 'anki_reviews']:
    if t in tables:
        print(f'\n--- {t} (schema) ---')
        cur.execute(f"PRAGMA table_info({t})")
        print([(c[1], c[2]) for c in cur.fetchall()])
        print(f'--- {t} (recent 5) ---')
        cur.execute(f"SELECT * FROM {t} ORDER BY 1 DESC LIMIT 5")
        for r in cur.fetchall():
            print(r)
