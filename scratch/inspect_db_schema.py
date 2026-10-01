import sqlite3

conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()
c.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
for name, sql in c.fetchall():
    print(f"TABLE {name}:")
    print(sql)
    print()
