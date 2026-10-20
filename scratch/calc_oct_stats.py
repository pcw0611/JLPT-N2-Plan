# -*- coding: utf-8 -*-
import sqlite3
import shutil
import json
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / 'database' / 'jlpt_learning.db'

con_db = sqlite3.connect(DB)
cur_db = con_db.cursor()

# Get all study_sessions in October 2026
cur_db.execute("SELECT session_date, verified_minutes FROM study_sessions WHERE session_date >= '2026-10-01' ORDER BY session_date")
oct_sessions = cur_db.fetchall()
print("Current DB Oct sessions:")
tot_mins = 0
for d, m in oct_sessions:
    tot_mins += m
    print(f"  {d}: {m}m")
print(f"Total October DB minutes so far: {tot_mins}m")

# Check all anki_daily_stats in October 2026
cur_db.execute("SELECT snapshot_date, payload_json FROM anki_daily_stats WHERE snapshot_date >= '2026-10-01' ORDER BY snapshot_date")
oct_anki = cur_db.fetchall()
tot_anki_revs = 0
tot_anki_mins = 0.0
for d, p_str in oct_anki:
    p = json.loads(p_str)
    all_stats = p.get('allDecksStats', {})
    revs = all_stats.get('totalReviews') or p.get('answeredCards', 0)
    mins = all_stats.get('totalStudyMinutes') or p.get('studyMinutes', 0.0)
    tot_anki_revs += revs
    tot_anki_mins += mins
    # print(f"  {d}: {revs} revs, {mins}m")
print(f"Total October DB Anki so far: {tot_anki_revs} revs, {tot_anki_mins:.2f}m")

con_db.close()
