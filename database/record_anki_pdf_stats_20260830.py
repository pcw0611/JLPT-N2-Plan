"""Record the read-only Anki statistics PDF snapshot without adding study time."""

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-08-30"
SOURCE = "anki-통계-2026-08-30@23-09-49.pdf"
SCOPE = "deck:current"

payload = {
    "scope": SCOPE,
    "scopeLabel": "현재 덱",
    "answeredCards": 402,
    "studyMinutes": 50.51,
    "secondsPerCard": 7.54,
    "againCount": 59,
    "againPct": 14.68,
    "learningCards": 381,
    "reviewCards": 21,
    "relearningCards": 0,
    "filteredCards": 0,
    "forecast": {"periodDays": 30, "totalReviews": 140, "dailyAverage": 5, "tomorrowDue": 46, "dailyLoad": 58},
    "history": {"periodDays": 31, "studyDays": 7, "studyDayPct": 22.58, "totalReviews": 924, "calendarDailyAverage": 30, "studyDayAverage": 132},
    "cards": {"total": 1169, "new": 1029, "newPct": 88.02, "young": 140, "youngPct": 11.98, "mature": 0, "suspended": 0, "buried": 0},
    "medianIntervalDays": 4,
    "medianEasePct": 250,
    "retention": {
        "today": {"pct": 100.0, "count": 21},
        "yesterday": {"pct": 85.7, "count": 21},
        "lastWeek": {"pct": 79.8, "count": 99},
        "lastMonth": {"pct": 79.8, "count": 99},
        "lastYear": {"pct": 79.8, "count": 99},
    },
    "sourceNote": "Anki 통계 화면에서 deck:current 및 최근 12달 필터로 출력. 전체 덱 통계와 합산하지 않음.",
}

con = sqlite3.connect(DB)
with con:
    con.execute("""CREATE TABLE IF NOT EXISTS anki_daily_stats (
        snapshot_date TEXT PRIMARY KEY,
        scope_label TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        source_filename TEXT NOT NULL,
        captured_at TEXT,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""")
    con.execute("""INSERT INTO anki_daily_stats
        (snapshot_date, scope_label, payload_json, source_filename, captured_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(snapshot_date) DO UPDATE SET
          scope_label=excluded.scope_label,
          payload_json=excluded.payload_json,
          source_filename=excluded.source_filename,
          captured_at=excluded.captured_at,
          updated_at=CURRENT_TIMESTAMP""",
        (DATE, SCOPE, json.dumps(payload, ensure_ascii=False), SOURCE, "2026-08-30T23:09:49+09:00"))

assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
print(json.dumps({"date": DATE, "scope": SCOPE, "answeredCards": 402, "studyMinutesAdded": 0}, ensure_ascii=False))
con.close()
