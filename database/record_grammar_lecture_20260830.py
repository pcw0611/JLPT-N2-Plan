"""Record a user-confirmed grammar lecture completion after midnight on 2026-08-30."""

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
LOG = ROOT / "JLPT_STUDY_LOG.md"
RESULT = ROOT / "database" / "results" / "grammar-lecture-20260830-user-report.json"
RECORD_ID = "grammar-lecture-20260830-user-report"
MARKER = f"[{RECORD_ID}]"

payload = {
    "record_id": RECORD_ID,
    "study_date": "2026-08-30",
    "activity": "문법 강의",
    "state": "completed",
    "reported_by": "user",
    "reported_minutes": None,
    "lecture_title": None,
    "lecture_range": "09~15",
    "date_basis": "사용자 메시지가 자정을 넘긴 뒤 접수됨",
    "note": "완료 및 범위 09~15는 사용자 확인. 시간과 정확한 강의명은 추정하지 않음.",
}

with sqlite3.connect(DB) as con:
    row = con.execute(
        "SELECT summary FROM study_sessions WHERE session_date='2026-08-30'"
    ).fetchone()
    if row is None:
        con.execute(
            """INSERT INTO study_sessions
               (session_date, verified_minutes, has_untracked_activity, summary)
               VALUES ('2026-08-30', 0, 1, ?)""",
            (
                "[grammar-lecture-20260830-user-report] 사용자 확인 문법 강의 완료. "
                "자정 이후 보고 기준으로 2026-08-30에 기록; 범위 09~15, 시간·정확한 강의명 미확인.",
            ),
        )
    elif MARKER not in (row[0] or ""):
        con.execute(
            """UPDATE study_sessions
               SET has_untracked_activity=1,
                   summary=summary || ?,
                   updated_at=CURRENT_TIMESTAMP
               WHERE session_date='2026-08-30'""",
            (
                " [grammar-lecture-20260830-user-report] 사용자 확인 문법 강의 완료. "
                "자정 이후 보고 기준으로 기록; 범위 09~15, 시간·정확한 강의명 미확인.",
            ),
        )

RESULT.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

log_text = LOG.read_text(encoding="utf-8")
if f"<!-- {RECORD_ID} -->" not in log_text:
    entry = """

<!-- grammar-lecture-20260830-user-report -->
## 2026-08-30 — 문법 강의

- 사용자 확인: 문법 강의 시청 완료.
- 자정을 넘긴 뒤 접수된 메시지 기준으로 2026-08-30 활동에 기록. 사용자가 전날 몫이었다고 정정하면 날짜를 수정함.
- 범위는 사용자 확인 **09~15**. 소요시간·정확한 강의명은 확인되지 않아 추정하거나 학습시간에 가산하지 않음.
- 오늘 학습 종료로 처리하지 않음.
"""
    LOG.write_text(log_text.rstrip() + entry + "\n", encoding="utf-8")

print(json.dumps(payload, ensure_ascii=False))
