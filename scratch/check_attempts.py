import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()

for tid in ['official-vol2-full-mock-20260920', 'official-past-202312-full-mock-20260930']:
    print(f'=== {tid} ===')
    rows = c.execute('''
        SELECT item_no, response_state, selected_text, correct_text 
        FROM question_attempts 
        WHERE test_id = ? AND response_state != 'correct' AND item_no >= 70 
        ORDER BY item_no
    ''', (tid,)).fetchall()
    print(f'Total wrong listening items: {len(rows)}')
    for r in rows:
        print(f'  Q{r[0]:03d} | {r[1]} | user: {r[2]} | ans: {r[3]}')
