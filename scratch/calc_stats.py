# -*- coding: utf-8 -*-
import sqlite3
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ANKI_SRC = Path(r'C:\Users\pcw06\AppData\Roaming\Anki2\사용자 1')
TEMP_DIR = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_temp_stats')
TEMP_DIR.mkdir(exist_ok=True)
shutil.copy2(ANKI_SRC / 'collection.anki2', TEMP_DIR / 'collection.anki2')
if (ANKI_SRC / 'collection.anki2-wal').exists():
    shutil.copy2(ANKI_SRC / 'collection.anki2-wal', TEMP_DIR / 'collection.anki2-wal')

con_anki = sqlite3.connect(TEMP_DIR / 'collection.anki2')
cur_anki = con_anki.cursor()
cur_anki.execute('SELECT count(*) FROM revlog')
total_revlog = cur_anki.fetchone()[0]

con_db = sqlite3.connect('database/jlpt_learning.db')
cur_db = con_db.cursor()
cur_db.execute("SELECT session_date, verified_minutes FROM study_sessions WHERE session_date >= '2026-11-01' ORDER BY session_date")
nov_sessions = cur_db.fetchall()
print('Total revlog in anki:', total_revlog)
print('November sessions in DB:', nov_sessions)
print('November total minutes:', sum(r[1] for r in nov_sessions))

cur_db.execute("SELECT sum(json_extract(payload_json, '$.totalAnsweredCardsAllDecks')) FROM anki_daily_stats")
print('Total anki reviews in anki_daily_stats:', cur_db.fetchone()[0])
