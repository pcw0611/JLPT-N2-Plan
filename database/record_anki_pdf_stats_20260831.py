"""Record the 2026-08-31 Anki PDF snapshot and its user-approved study time."""

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-08-31"
SOURCE = "anki-통계-2026-08-31@10-01-01.pdf"
MARKER = "[anki-pdf-stats-20260831]"
MINUTES = 95

payload = {
    "scope": "deck:current",
    "scopeLabel": "현재 덱",
    "answeredCards": 522,
    "studyMinutes": 95.11,
    "secondsPerCard": 10.93,
    "againCount": 160,
    "againPct": 30.65,
    "learningCards": 292,
    "reviewCards": 187,
    "relearningCards": 43,
    "filteredCards": 0,
    "forecast": {"periodDays": 30, "totalReviews": 793, "dailyAverage": 26, "tomorrowDue": 139, "dailyLoad": 179},
    "history": {"periodDays": 31, "studyDays": 8, "studyDayPct": 25.81, "totalReviews": 4266, "calendarDailyAverage": 138, "studyDayAverage": 533},
    "cards": {"total": 2810, "new": 2017, "newPct": 71.78, "young": 793, "youngPct": 28.22, "mature": 0, "suspended": 0, "buried": 0},
    "medianIntervalDays": 5,
    "medianEasePct": 250,
    "retention": {
        "today": {"pct": 95.2, "count": 187},
        "yesterday": {"pct": 98.3, "count": 179},
        "lastWeek": {"pct": 92.9, "count": 992},
        "lastMonth": {"pct": 92.9, "count": 992},
        "lastYear": {"pct": 92.9, "count": 992},
    },
    "addedCards": {"total": 76, "dailyAverage": 2},
    "sourceNote": "Anki 통계 PDF의 deck:current·최근 12달 화면. 사용자의 명시적 요청에 따라 95.11분을 오늘 학습시간에 추가함.",
}

summary_text = (
    f"{MARKER} Anki 현재 덱 522회, 정확한 화면 시간 95.11분(95분 06.6초). "
    "DB 정수 시간 95분 반영; 오늘 학습 종료 아님."
)

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
        (DATE, "deck:current", json.dumps(payload, ensure_ascii=False), SOURCE, "2026-08-31T10:01:01+09:00"))

    row = con.execute(
        "SELECT verified_minutes, has_untracked_activity, summary FROM study_sessions WHERE session_date=?",
        (DATE,),
    ).fetchone()
    if row is None:
        con.execute(
            "INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary) VALUES (?, ?, 0, ?)",
            (DATE, MINUTES, summary_text),
        )
    elif MARKER not in (row[2] or ""):
        merged = ((row[2] or "").rstrip() + "\n" + summary_text).strip()
        con.execute(
            "UPDATE study_sessions SET verified_minutes=?, summary=?, updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
            (row[0] + MINUTES, merged, DATE),
        )

assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
recorded = con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()[0]
print(json.dumps({"date": DATE, "answeredCards": 522, "exactMinutes": 95.11, "verifiedMinutes": recorded}, ensure_ascii=False))
con.close()
