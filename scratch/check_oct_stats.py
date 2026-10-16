import sqlite3
import json

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

cur.execute("SELECT sum(verified_minutes) FROM study_sessions WHERE session_date >= '2026-10-01'")
oct_mins = cur.fetchone()[0]
print(f"October total verified_minutes: {oct_mins}m ({oct_mins//60}h {oct_mins%60}m)")

cur.execute("SELECT snapshot_date, payload_json FROM anki_daily_stats WHERE snapshot_date >= '2026-10-01' ORDER BY snapshot_date")
tot_revs = 0
tot_min = 0.0
for dt, p_json in cur.fetchall():
    data = json.loads(p_json)
    revs = data.get('totalAnsweredCardsAllDecks', data.get('answeredCards', 0))
    m = data.get('studyMinutes', 0.0)
    tot_revs += revs
    tot_min += m

print(f"October 10/01~10/16 Anki total: {tot_revs:,} reviews, {tot_min:.1f}m ({int(tot_min//60)}h {int(tot_min%60)}m)")
