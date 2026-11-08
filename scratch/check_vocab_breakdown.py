import sys, sqlite3
sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

vocab_types = [
    'kanji_reading', 'kanji_orthography', 'word_formation', 
    'context_definition', 'context_vocabulary', 'paraphrase', 'word_usage'
]

print("=== ALL TESTS VOCABULARY PERFORMANCE ===")
cur.execute(f'''
    SELECT item_type_id, count(*), 
           sum(case when response_state = 'correct' then 1 else 0 end),
           sum(case when response_state = 'unknown' then 1 else 0 end),
           sum(case when response_state = 'incorrect' then 1 else 0 end),
           avg(response_seconds)
    FROM question_attempts
    WHERE item_type_id IN ({','.join('?' for _ in vocab_types)})
    GROUP BY item_type_id
''', vocab_types)
for r in cur.fetchall():
    pct = round(r[2]/r[1]*100, 1) if r[1] else 0
    print(f"{r[0]:20s} | {r[2]}/{r[1]} ({pct:5.1f}%) | unk: {r[3]} | inc: {r[4]} | avg_sec: {r[5]:.1f}s")

print("\n=== MOCK EXAM 1 (2026-09-20 公式 問題集 第2集) VOCABULARY ===")
cur.execute(f'''
    SELECT item_type_id, count(*), 
           sum(case when response_state = 'correct' then 1 else 0 end)
    FROM question_attempts
    WHERE test_id = 'official-vol2-full-mock-20260920' AND item_type_id IN ({','.join('?' for _ in vocab_types)})
    GROUP BY item_type_id
''', vocab_types)
t_c = t_t = 0
for r in cur.fetchall():
    t_c += r[2]
    t_t += r[1]
    pct = round(r[2]/r[1]*100, 1) if r[1] else 0
    print(f"{r[0]:20s} | {r[2]}/{r[1]} ({pct:5.1f}%)")
print(f"Total Moji/Goi: {t_c}/{t_t} ({t_c/t_t*100:.1f}%)")

print("\n=== MOCK EXAM 2 (2026-09-30 2023.12 過去問) VOCABULARY ===")
cur.execute(f'''
    SELECT item_type_id, count(*), 
           sum(case when response_state = 'correct' then 1 else 0 end)
    FROM question_attempts
    WHERE test_id = 'official-past-202312-full-mock-20260930' AND item_type_id IN ({','.join('?' for _ in vocab_types)})
    GROUP BY item_type_id
''', vocab_types)
t_c = t_t = 0
for r in cur.fetchall():
    t_c += r[2]
    t_t += r[1]
    pct = round(r[2]/r[1]*100, 1) if r[1] else 0
    print(f"{r[0]:20s} | {r[2]}/{r[1]} ({pct:5.1f}%)")
print(f"Total Moji/Goi: {t_c}/{t_t} ({t_c/t_t*100:.1f}%)")

con.close()
