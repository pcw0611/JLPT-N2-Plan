import sqlite3

conn = sqlite3.connect('scratch/temp_collection.anki2')
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM notes WHERE flds LIKE '%#fef08a%' OR flds LIKE '%#fde047%'")
print('Notes with yellow highlight text:', c.fetchone()[0])

c.execute("SELECT DISTINCT mid FROM notes WHERE flds LIKE '%#fef08a%'")
print('Model IDs of these notes:', c.fetchall())
