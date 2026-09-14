"""Record the user-confirmed 49-minute Anki session on 2026-08-30."""

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
LOG = ROOT / "JLPT_STUDY_LOG.md"
RESULT = ROOT / "database" / "results" / "anki-20260830-user-report.json"
RECORD_ID = "anki-20260830-user-report"
MARKER = f"[{RECORD_ID}]"
MINUTES = 49

payload = {
    "record_id": RECORD_ID,
    "study_date": "2026-08-30",
    "activity": "Anki",
    "state": "completed",
    "reported_by": "user",
    "reported_minutes": MINUTES,
    "reviewed_cards": None,
    "new_cards": None,
    "note": "사용자 확인 49분. 카드 수는 미확인으로 추정하지 않음.",
}

with sqlite3.connect(DB) as con:
    row = con.execute(
        "SELECT summary FROM study_sessions WHERE session_date='2026-08-30'"
    ).fetchone()
    if row is None:
        con.execute(
            """INSERT INTO study_sessions
               (session_date, verified_minutes, has_untracked_activity, summary)
               VALUES ('2026-08-30', ?, 0, ?)""",
            (MINUTES, f"{MARKER} 사용자 확인 Anki 49분 완료. 카드 수 미확인."),
        )
    elif MARKER not in (row[0] or ""):
        con.execute(
            """UPDATE study_sessions
               SET verified_minutes=verified_minutes+?,
                   summary=summary||?,
                   updated_at=CURRENT_TIMESTAMP
               WHERE session_date='2026-08-30'""",
            (MINUTES, f" {MARKER} 사용자 확인 Anki 49분 완료. 카드 수 미확인."),
        )

RESULT.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

log_text = LOG.read_text(encoding="utf-8")
if f"<!-- {RECORD_ID} -->" not in log_text:
    entry = """

<!-- anki-20260830-user-report -->
## 2026-08-30 — Anki

- 사용자 확인: Anki 완료, **49분**.
- 카드 수·신규 카드 수·정답률은 확인되지 않아 추정하지 않음.
- 오늘 확인 학습시간 **49분**. 시간 미확인 문법 강의는 합산하지 않음.
- 오늘 학습 종료로 처리하지 않음.
"""
    LOG.write_text(log_text.rstrip() + entry + "\n", encoding="utf-8")

with sqlite3.connect(DB) as con:
    minutes = con.execute(
        "SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-30'"
    ).fetchone()[0]
print(json.dumps({"ok": True, "record_id": RECORD_ID, "verified_minutes": minutes}, ensure_ascii=False))
