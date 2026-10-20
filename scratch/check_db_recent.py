import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
print('tests:', con.execute('SELECT id, test_date, total_items, correct_items FROM tests WHERE test_date >= "2026-10-18"').fetchall())
print('study_intervals:', con.execute('SELECT session_date, source, duration_seconds, notes FROM study_intervals WHERE session_date >= "2026-10-18"').fetchall())
for row in con.execute('SELECT session_date, verified_minutes, summary FROM study_sessions WHERE session_date >= "2026-10-18"').fetchall():
    print(f'session: {row[0]}, mins={row[1]}, summary={row[2][:100]}...')
