# -*- coding: utf-8 -*-
import sqlite3, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
sys.stdout.reconfigure(encoding='utf-8')

KST = timezone(timedelta(hours=9))
temp = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1008')
con = sqlite3.connect(temp / 'collection.anki2')
cur = con.cursor()

cur.execute('SELECT id, name FROM decks')
deck_names = {r[0]: r[1].replace('\x1f', '::') for r in cur.fetchall()}

s = datetime(2026, 10, 8, 4, 0, 0, tzinfo=KST)
e = s + timedelta(days=1)
s_ms, e_ms = int(s.timestamp()*1000), int(e.timestamp()*1000)

cur.execute('SELECT count(*), sum(time), count(distinct cid), min(id), max(id) FROM revlog WHERE id >= ? AND id < ?', (s_ms, e_ms))
cnt, total_time_ms, distinct_cards, min_id, max_id = cur.fetchone()
sec = (total_time_ms or 0) / 1000.0
min_dt = datetime.fromtimestamp(min_id/1000.0, tz=KST)
max_dt = datetime.fromtimestamp(max_id/1000.0, tz=KST)

print('=== 2026-10-08 통계 ===')
print(f'총 리뷰: {cnt}회, 시간: {sec:.2f}초 ({sec/60:.2f}분), 카드: {distinct_cards}장, 평균: {sec/cnt:.2f}초/카드')
print(f'시간대: {min_dt.strftime("%H:%M")} ~ {max_dt.strftime("%H:%M")}')

cur.execute('SELECT ease, count(*) FROM revlog WHERE id >= ? AND id < ? GROUP BY ease', (s_ms, e_ms))
ratings = dict(cur.fetchall())
for k in [1, 2, 3, 4]:
    print(f'Ease {k}: {ratings.get(k, 0)} ({ratings.get(k, 0)/cnt*100:.2f}%)')

cur.execute('SELECT type, count(*) FROM revlog WHERE id >= ? AND id < ? GROUP BY type', (s_ms, e_ms))
types = dict(cur.fetchall())
print(f'Types: Learn/Relearn={types.get(0,0)+types.get(2,0)}, Review={types.get(1,0)+types.get(3,0)}')

cur.execute('''
    SELECT c.did, count(*), count(distinct c.id), sum(r.time)
    FROM revlog r JOIN cards c ON r.cid = c.id
    WHERE r.id >= ? AND r.id < ?
    GROUP BY c.did ORDER BY count(*) DESC
''', (s_ms, e_ms))
print('덱별:')
for did, d_cnt, d_dist, d_tms in cur.fetchall():
    d_sec = (d_tms or 0)/1000.0
    d_min = round(d_sec / 60.0, 1)
    print(f'  {deck_names.get(did, did)}: {d_cnt}회, {d_min}분 ({d_sec:.1f}초), {d_dist}장')

cur.execute('SELECT queue, count(*) FROM cards GROUP BY queue')
q = dict(cur.fetchall())
print(f'잔여 큐: new={q.get(0,0)}, learn={q.get(1,0)+q.get(3,0)}, review={q.get(2,0)}')
