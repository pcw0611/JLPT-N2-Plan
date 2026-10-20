import sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')
con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
print('=== daily_records for 2026-10-18+ ===')
cur.execute('SELECT date, total_study_minutes, target_minutes, completed, is_late, notes FROM daily_records WHERE date >= "2026-10-18"')
for row in cur.fetchall():
    print(row)

print('\n=== study_sessions for 2026-10-18+ ===')
cur.execute('SELECT id, date, session_type, material_name, duration_minutes, summary FROM study_sessions WHERE date >= "2026-10-18"')
for row in cur.fetchall():
    print(row)
