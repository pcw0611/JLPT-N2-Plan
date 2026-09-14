"""Record the current Anki study-day snapshot for 2026-09-01 without double counting."""

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-09-01"
MARKER = "[anki-live-time-sync-20260901-549]"
WHOLE_MINUTES = 147

SUMMARY = {
    "schema": "daily_summary_v1",
    "scope": "all_decks",
    "scopeLabel": "전체 덱",
    "answeredCards": 549,
    "studyMinutes": 147.37,
    "secondsPerCard": 16.11,
    "againCount": 164,
    "againPct": 29.87,
    "learningReviews": 259,
    "reviewsDone": 175,
    "ratings": {"again": 164, "hard": 168, "good": 138, "easy": 79},
    "cardsRemaining": {"new": 0, "learning": 15, "review": 0},
    "studyDay": "2026-09-01",
    "ankiResourceStudyDayRaw": "2026-08-31",
    "sourceNote": "Anki 학습일 경계 2026-09-01 04:00 KST 이후 revlog 실측. 리소스의 study_day는 경계 시각을 UTC 날짜로 표시해 2026-08-31로 보이므로 KST 학습일로 정규화.",
}

con = sqlite3.connect(DB)
with con:
    row = con.execute(
        "SELECT verified_minutes, summary FROM study_sessions WHERE session_date=?", (DATE,)
    ).fetchone()
    if row is None:
        raise RuntimeError("2026-09-01 study session is missing")
    minutes, notes = row[0], row[1] or ""
    if MARKER not in notes:
        notes = (
            notes.rstrip()
            + f"\n{MARKER} Anki 전체 덱 549회·147분22.2초 실측. "
              "강의60분과 별도이므로 DB 정수 시간147분 추가; 오늘 누적207분."
        ).strip()
        con.execute(
            "UPDATE study_sessions SET verified_minutes=?, summary=?, updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
            (minutes + WHOLE_MINUTES, notes, DATE),
        )

    old = con.execute(
        "SELECT payload_json FROM anki_daily_stats WHERE snapshot_date=?", (DATE,)
    ).fetchone()
    if old:
        previous = json.loads(old[0])
        if previous.get("schema") != "daily_summary_v1":
            SUMMARY["inventory"] = previous
        con.execute(
            "UPDATE anki_daily_stats SET scope_label=?, payload_json=?, source_filename=?, updated_at=CURRENT_TIMESTAMP WHERE snapshot_date=?",
            ("전체 덱", json.dumps(SUMMARY, ensure_ascii=False), "Anki MCP anki://stats/today", DATE),
        )
    else:
        con.execute(
            "INSERT INTO anki_daily_stats(snapshot_date,scope_label,payload_json,source_filename,captured_at,updated_at) VALUES(?,?,?,?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)",
            (DATE, "전체 덱", json.dumps(SUMMARY, ensure_ascii=False), "Anki MCP anki://stats/today"),
        )

assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
print(json.dumps({"date": DATE, "verifiedMinutes": con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()[0], "anki": SUMMARY}, ensure_ascii=False))
con.close()
