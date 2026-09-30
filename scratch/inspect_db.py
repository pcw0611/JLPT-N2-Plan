import sqlite3

conn = sqlite3.connect('database/jlpt_learning.db')
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cur.fetchall()]
print("Tables:", tables)

for table in tables:
    cur.execute(f"PRAGMA table_info({table});")
    cols = [f"{row[1]} ({row[2]})" for row in cur.fetchall()]
    print(f"\nTable {table}:", ", ".join(cols))

# Let's check exams or mock exam records
if 'mock_exams' in tables:
    cur.execute("SELECT * FROM mock_exams;")
    print("\nMock exams:", cur.fetchall())
elif 'exams' in tables:
    cur.execute("SELECT * FROM exams;")
    print("\nExams:", cur.fetchall())

if 'study_sessions' in tables:
    cur.execute("SELECT * FROM study_sessions ORDER BY date DESC LIMIT 5;")
    print("\nStudy sessions:", cur.fetchall())
