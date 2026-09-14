"""Record Anki study stats and study session for 2026-09-08 with grammar review."""

import sqlite3
import json
import shutil
from pathlib import Path

ROOT = Path(r"c:\Users\pcw06\Documents\Codex\JLPT-N2-Plan")
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-09-08"

# Verified revlog metrics for 2026-09-08 (since 04:00 KST, updated after grammar review at 18:00)
# Total reviews: 1,968
# Total time: 16,524.05 seconds = 275분 24.05초 (4시간 35분 24.05초)
# N2 신규 66장 완료 (790 -> 724)
# N3 신규 20장 완료 (179 -> 159)
# N2 문법 001-150 예문 복습 59회 (24분 18.3초, 신규 11장 시작)

WHOLE_MINUTES = 275

SUMMARY_PAYLOAD = {
    "schema": "daily_summary_v1",
    "scope": "all_decks",
    "scopeLabel": "전체 덱",
    "answeredCards": 1968,
    "studyMinutes": 275.40,
    "secondsPerCard": 8.40,
    "againCount": 1398,
    "againPct": 71.04,
    "learningReviews": 1688,
    "reviewsDone": 280,
    "ratings": {
        "again": 1398,
        "hard": 171,
        "good": 152,
        "easy": 247
    },
    "cardsRemaining": {
        "new": 1590,
        "learning": 6,
        "review": 1324
    },
    "studyDay": "2026-09-08",
    "ankiResourceStudyDayRaw": "2026-09-08",
    "sourceNote": "Anki revlog 2026-09-08 실측치 (단어 1,909회 + 문법 59회). 총 1,968회(275분 24.1초, 4시간 35분 24.1초). 옵션 A 3일차 완수: N2 신규 66장 100% 완수(790->724), N3 신규 20장(179->159), N2 문법 예문 복습(59회, 24분 18초) 완수.",
    "inventory": {
        "n3_unseen": 159,
        "n2_unseen": 724,
        "n2_new_today": 66,
        "n3_new_today": 20,
        "grammar_new_today": 11,
        "new_cards_exposed_today": 97
    }
}

SESSION_SUMMARY = (
    "[2026-09-08] Anki 단어·문법 세션 1,968회(275분 24초, 4시간 35분 24초). "
    "옵션 A 3일차 완수: N2 신규 66장(790->724, 100% 달성), N3 신규 20장(179->159, 100% 달성) + "
    "N2 문법 001-150 예문 복습 59회(24분 18초, 신규 11장 시작). 잔여 24초 보존."
)

con = sqlite3.connect(DB)
with con:
    # 1. Update or Insert study_sessions
    row = con.execute("SELECT verified_minutes, summary FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()
    if row is None:
        con.execute(
            "INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary, created_at, updated_at) "
            "VALUES (?, ?, 0, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (DATE, WHOLE_MINUTES, SESSION_SUMMARY)
        )
    else:
        con.execute(
            "UPDATE study_sessions SET verified_minutes=?, summary=?, updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
            (WHOLE_MINUTES, SESSION_SUMMARY, DATE)
        )

    # 2. Update or Insert anki_daily_stats
    anki_row = con.execute("SELECT snapshot_date FROM anki_daily_stats WHERE snapshot_date=?", (DATE,)).fetchone()
    if anki_row:
        con.execute(
            "UPDATE anki_daily_stats SET scope_label=?, payload_json=?, source_filename=?, updated_at=CURRENT_TIMESTAMP WHERE snapshot_date=?",
            ("전체 덱", json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), "Anki revlog snapshot 2026-09-08 (grammar update)", DATE)
        )
    else:
        con.execute(
            "INSERT INTO anki_daily_stats (snapshot_date, scope_label, payload_json, source_filename, captured_at, updated_at) "
            "VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (DATE, "전체 덱", json.dumps(SUMMARY_PAYLOAD, ensure_ascii=False), "Anki revlog snapshot 2026-09-08 (grammar update)")
        )

    assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert not con.execute("PRAGMA foreign_key_check").fetchall()

print("Successfully updated Anki 2026-09-08 stats to DB.")
sess_check = con.execute("SELECT session_date, verified_minutes, summary FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()
print("study_sessions:", sess_check)
anki_check = con.execute("SELECT snapshot_date, scope_label, payload_json FROM anki_daily_stats WHERE snapshot_date=?", (DATE,)).fetchone()
print("anki_daily_stats date:", anki_check[0], "scope:", anki_check[1])
con.close()

# Copy to database folder
target_script = ROOT / "database" / "record_anki_20260908.py"
shutil.copy2(__file__, target_script)
print(f"Copied script to {target_script}")
