import sqlite3, json

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()
cur.execute("SELECT snapshot_date, payload_json FROM anki_daily_stats WHERE snapshot_date >= '2026-10-01' ORDER BY snapshot_date")
rows = cur.fetchall()
total_revs = 0
total_mins = 0
for d, p in rows:
    data = json.loads(p)
    revs = data.get('answeredCards', 0)
    mins = data.get('studyMinutes', 0)
    total_revs += revs
    total_mins += mins
    print(f'{d}: {revs} reviews, {mins} mins')
print(f'Total Oct: {total_revs:,} reviews, {total_mins:.2f} mins ({total_mins/60:.2f} hours / {int(total_mins//60)}시간 {int(total_mins%60)}분)')
