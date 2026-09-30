import sqlite3

conn = sqlite3.connect('database/jlpt_learning.db')
cur = conn.cursor()
cur.execute('''
    SELECT rq.id, rq.attempt_id, rq.review_date, rq.interval_label, rq.status, qa.test_id, qa.item_no 
    FROM review_queue rq 
    JOIN question_attempts qa ON rq.attempt_id = qa.id 
    WHERE qa.test_id = 'official-vol2-full-mock-20260920' 
    LIMIT 6;
''')
for r in cur.fetchall():
    print(r)
