import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
for r in cur.execute("SELECT scheduled_date, count(*) FROM review_queue WHERE status = 'pending' GROUP BY scheduled_date ORDER BY scheduled_date").fetchall():
    print(r)
con.close()
