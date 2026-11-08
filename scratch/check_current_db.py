import sqlite3

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
print('study_sessions:')
for row in cur.execute('SELECT session_date, verified_minutes, has_untracked_activity, summary FROM study_sessions WHERE session_date >= "2026-11-01" ORDER BY session_date').fetchall():
    print(row[0], row[1], row[2], row[3][:120] + '...')
print('\nanki_daily_stats:')
for row in cur.execute('SELECT snapshot_date, captured_at, scope_label FROM anki_daily_stats WHERE snapshot_date >= "2026-11-01" ORDER BY snapshot_date').fetchall():
    print(row)
print('\nstudy_intervals:')
for row in cur.execute('SELECT session_date, started_at, ended_at, duration_seconds, notes FROM study_intervals WHERE session_date >= "2026-11-01" ORDER BY session_date').fetchall():
    print(row)
con.close()
