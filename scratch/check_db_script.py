import sqlite3

conn = sqlite3.connect('database/jlpt_learning.db')
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cur.fetchall()]
for table in tables:
    cur.execute(f"PRAGMA table_info({table})")
    cols = [c[1] for c in cur.fetchall()]
    for col in cols:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} LIKE '%市民文化祭%'")
            cnt = cur.fetchone()[0]
            if cnt > 0:
                print(f"Found in {table}.{col}: {cnt} rows")
        except Exception:
            pass
