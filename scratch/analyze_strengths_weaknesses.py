import sqlite3

conn = sqlite3.connect('database/jlpt_learning.db')
c = conn.cursor()

query = '''
    SELECT 
        item_type_id,
        COUNT(*) as total_attempts,
        SUM(CASE WHEN response_state = 'correct' THEN 1 ELSE 0 END) as correct_count,
        ROUND(AVG(CASE WHEN response_state = 'correct' THEN 1.0 ELSE 0.0 END) * 100, 1) as accuracy_pct,
        ROUND(AVG(response_seconds), 1) as avg_seconds
    FROM question_attempts
    GROUP BY item_type_id
    ORDER BY total_attempts DESC
'''

c.execute(query)
rows = c.fetchall()

print(f"{'유형 (item_type_id)':<25} | {'총 시도':<6} | {'정답':<6} | {'정답률':<8} | {'평균시간(초)':<10}")
print("-" * 65)
for r in rows:
    print(f"{r[0]:<25} | {r[1]:<6} | {r[2]:<6} | {r[3]:<7}% | {r[4] if r[4] is not None else '-':<10}")

print("\n=== 최근 2대 공식 실전 모의고사 (제1회 09-20 vs 제2회 09-30) 비교 ===")
c.execute('''
    SELECT 
        test_id,
        item_type_id,
        COUNT(*) as total,
        SUM(CASE WHEN response_state = 'correct' THEN 1 ELSE 0 END) as correct
    FROM question_attempts
    WHERE test_id IN ('official-vol2-full-mock-20260920', 'official-past-202312-full-mock-20260930')
    GROUP BY test_id, item_type_id
    ORDER BY item_type_id, test_id
''')
mock_rows = c.fetchall()
mock_dict = {}
for t, itype, tot, corr in mock_rows:
    if itype not in mock_dict:
        mock_dict[itype] = {}
    mock_dict[itype][t] = (corr, tot, round(corr/tot*100, 1))

print(f"{'유형':<25} | {'제1회 (공식 제2집)':<20} | {'제2회 (2023.12)':<20}")
print("-" * 70)
for itype, data in mock_dict.items():
    m1 = data.get('official-vol2-full-mock-20260920', (0,0,0))
    m2 = data.get('official-past-202312-full-mock-20260930', (0,0,0))
    print(f"{itype:<25} | {m1[0]}/{m1[1]} ({m1[2]}%) | {m2[0]}/{m2[1]} ({m2[2]}%)")
