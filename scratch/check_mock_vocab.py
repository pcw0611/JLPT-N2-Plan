import sys, sqlite3
sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

print('--- Official Mock Exams in DB ---')
cur.execute('''
    SELECT id, test_date, title, source_class, correct_items, total_items, elapsed_seconds, notes 
    FROM tests 
    WHERE source_class = 'official_mock' OR id LIKE '%mock%' 
    ORDER BY test_date
''')
for r in cur.fetchall():
    print(r[0], r[1], r[2], f"{r[4]}/{r[5]} ({r[4]/r[5]*100:.1f}%)")

print('\n--- Question Attempts by Section ---')
cur.execute('''
    SELECT section, count(*), sum(case when is_correct = 1 then 1 else 0 end)
    FROM question_attempts
    GROUP BY section
''')
for r in cur.fetchall():
    pct = round(r[2]/r[1]*100, 1) if r[1] else 0
    print(f'{r[0]}: {r[2]}/{r[1]} ({pct}%)')

print('\n--- Question Attempts for Vocabulary/Language Knowledge ---')
cur.execute('''
    SELECT question_type, count(*), sum(case when is_correct = 1 then 1 else 0 end)
    FROM question_attempts
    WHERE section LIKE '%어휘%' OR section LIKE '%문자%'
    GROUP BY question_type
''')
for r in cur.fetchall():
    pct = round(r[2]/r[1]*100, 1) if r[1] else 0
    print(f'{r[0]}: {r[2]}/{r[1]} ({pct}%)')

con.close()
