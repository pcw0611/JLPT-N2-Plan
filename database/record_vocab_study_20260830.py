"""Record the user's separately confirmed 120-minute vocabulary study session."""

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-08-30"
MINUTES = 120
MARKER = "[vocabulary-study-20260830-120m-user-report]"
NOTE = (
    f"{MARKER} 사용자 확인 단어 공부 120분 완료. "
    "오늘 Anki 49분과 별도의 단어 학습으로 보고 중복 없이 가산. 오늘 학습 종료 아님."
)

con = sqlite3.connect(DB)
row = con.execute(
    "SELECT id, verified_minutes, COALESCE(summary, '') FROM study_sessions WHERE session_date=?",
    (DATE,),
).fetchone()
if row is None:
    with con:
        con.execute(
            "INSERT INTO study_sessions (session_date, verified_minutes, has_untracked_activity, summary) VALUES (?, ?, 0, ?)",
            (DATE, MINUTES, NOTE),
        )
    changed = True
    total = MINUTES
elif MARKER in row[2]:
    changed = False
    total = row[1]
else:
    total = row[1] + MINUTES
    with con:
        con.execute(
            "UPDATE study_sessions SET verified_minutes=?, summary=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (total, (row[2] + " " + NOTE).strip(), row[0]),
        )
    changed = True

assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
print({"date": DATE, "added_minutes": MINUTES if changed else 0, "verified_minutes": total})
con.close()
