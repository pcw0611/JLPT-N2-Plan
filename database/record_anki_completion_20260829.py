"""Record the user's 2026-08-29 Anki completion without inventing time/card counts."""

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
LOG = ROOT / "JLPT_STUDY_LOG.md"
RESULT = ROOT / "database" / "results" / "anki-complete-20260829-user-report.json"
MARKER = "[anki-complete-20260829-user-report]"


payload = {
    "record_id": "anki-complete-20260829-user-report",
    "study_date": "2026-08-29",
    "activity": "Anki",
    "state": "completed",
    "reported_by": "user",
    "reported_minutes": None,
    "reviewed_cards": None,
    "new_cards": None,
    "note": "완료 사실만 확인됨. 소요시간과 카드 수는 추정하거나 학습시간에 가산하지 않음.",
}


with sqlite3.connect(DB) as con:
    row = con.execute(
        "SELECT summary FROM study_sessions WHERE session_date='2026-08-29'"
    ).fetchone()
    if row is None:
        raise RuntimeError("2026-08-29 study session is missing")
    if MARKER not in (row[0] or ""):
        con.execute(
            """UPDATE study_sessions
               SET summary = summary || ?, updated_at = CURRENT_TIMESTAMP
               WHERE session_date='2026-08-29'""",
            (
                " [anki-complete-20260829-user-report] 사용자 확인 Anki 완료. "
                "소요시간·복습 카드 수·새 카드 수 미확인으로 시간 및 수량 미가산.",
            ),
        )

RESULT.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

log_text = LOG.read_text(encoding="utf-8")
if f"<!-- {payload['record_id']} -->" not in log_text:
    entry = """

<!-- anki-complete-20260829-user-report -->
## 2026-08-29 — Anki 완료

- 사용자 확인: 오늘 Anki 완료.
- 소요시간, 복습 카드 수, 새 카드 수는 확인되지 않아 추정하거나 학습시간에 가산하지 않음.
- 오늘 학습 종료로 처리하지 않음.
"""
    LOG.write_text(log_text.rstrip() + entry + "\n", encoding="utf-8")

print(json.dumps(payload, ensure_ascii=False))
