# -*- coding: utf-8 -*-
import sqlite3
import json

con = sqlite3.connect('database/jlpt_learning.db')
cur = con.cursor()

cur.execute('SELECT snapshot_date, payload_json FROM anki_daily_stats ORDER BY snapshot_date')
rows = cur.fetchall()

oct_reviews = 0
oct_mins = 0.0

all_reviews = 0

for d, p in rows:
    data = json.loads(p)
    cnt = data.get('totalAnsweredCardsAllDecks') or data.get('answeredCards') or 0
    mins = data.get('studyMinutes') or 0.0
    all_reviews += cnt
    if d.startswith('2026-10'):
        oct_reviews += cnt
        oct_mins += mins

print(f"October in DB: {oct_reviews} reviews, {oct_mins:.1f} mins")
print(f"All dates in anki_daily_stats: {all_reviews} reviews across {len(rows)} days")
con.close()
