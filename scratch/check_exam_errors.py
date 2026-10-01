import json
import sqlite3

def check_errors():
    conn = sqlite3.connect('database/jlpt_learning.db')
    conn.row_factory = sqlite3.Row
    
    # 1. Exam 1
    e1_wrong = conn.execute("""
        SELECT item_no, item_type_id, selected_text, correct_text, response_seconds
        FROM question_attempts
        WHERE test_id = 'official-vol2-full-mock-20260920' AND response_state = 'wrong'
        ORDER BY item_no
    """).fetchall()
    print(f"Exam 1 wrong count: {len(e1_wrong)}")
    e1_ids = [r['item_no'] for r in e1_wrong]
    print("Exam 1 wrong IDs:", e1_ids)

    # 2. Exam 2
    e2_wrong = conn.execute("""
        SELECT item_no, item_type_id, selected_text, correct_text, response_seconds
        FROM question_attempts
        WHERE test_id = 'official-past-202312-full-mock-20260930' AND response_state = 'wrong'
        ORDER BY item_no
    """).fetchall()
    print(f"Exam 2 wrong count: {len(e2_wrong)}")
    e2_ids = [r['item_no'] for r in e2_wrong]
    print("Exam 2 wrong IDs:", e2_ids)

    # Check listening wrong IDs
    e1_listening_wrong = [r['item_no'] for r in e1_wrong if r['item_no'] >= 76]
    e2_listening_wrong = [r['item_no'] for r in e2_wrong if r['item_no'] >= 73]
    print("Exam 1 listening wrong IDs:", e1_listening_wrong)
    print("Exam 2 listening wrong IDs:", e2_listening_wrong)

if __name__ == '__main__':
    check_errors()
