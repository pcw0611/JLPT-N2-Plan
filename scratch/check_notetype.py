import sqlite3
import json

conn = sqlite3.connect('scratch/temp_collection.anki2')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('Tables:', [r[0] for r in c.fetchall()])

# In Anki 2.1+, notetypes table exists:
c.execute("SELECT id, name FROM notetypes")
print('Notetypes:', c.fetchall())

c.execute("SELECT config FROM notetypes WHERE id = 1787553295421")
row = c.fetchone()
if row:
    print('Config of 1787553295421:', row[0][:200])

c.execute("SELECT name, css FROM notetypes WHERE id = 1787553295421")
print('CSS of notetype:', c.fetchone())
