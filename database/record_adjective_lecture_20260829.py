"""Record 50 additional minutes of adjective lecture study on 2026-08-29."""

import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
LOG = ROOT / "JLPT_STUDY_LOG.md"
RESULT = ROOT / "database" / "results" / "adjective-lecture-20260829-user-report.json"
RECORD_ID = "adjective-lecture-20260829-user-report"
MARKER = f"[{RECORD_ID}]"
MINUTES = 50

payload = {
    "record_id": RECORD_ID,
    "study_date": "2026-08-29",
    "activity": "형용사 강의",
    "state": "completed",
    "reported_by": "user",
    "reported_minutes": MINUTES,
    "additional_time": True,
    "lecture_title": None,
    "lecture_range": None,
    "note": "기존 기록과 별도로 추가한 사용자 확인 시간. 정확한 강의명과 범위는 미확인.",
}

with sqlite3.connect(DB) as con:
    row = con.execute(
        "SELECT verified_minutes, summary FROM study_sessions WHERE session_date='2026-08-29'"
    ).fetchone()
    if row is None:
        raise RuntimeError("2026-08-29 study session is missing")
    if MARKER not in (row[1] or ""):
        con.execute(
            """UPDATE study_sessions
               SET verified_minutes = verified_minutes + ?,
                   summary = summary || ?,
                   updated_at = CURRENT_TIMESTAMP
               WHERE session_date='2026-08-29'""",
            (
                MINUTES,
                " [adjective-lecture-20260829-user-report] 사용자 확인 형용사 강의 50분 완료. "
                "기존 시간에 중복 없이 추가; 강의명·범위 미확인.",
            ),
        )

RESULT.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

log_text = LOG.read_text(encoding="utf-8")
if f"<!-- {RECORD_ID} -->" not in log_text:
    entry = """

<!-- adjective-lecture-20260829-user-report -->
## 2026-08-29 — 형용사 강의

- 사용자 확인: 형용사 강의 시청 완료, **50분**.
- 사용자가 추가 시간이라고 명시하여 기존 개인 공부 및 시험 타이머와 중복되지 않는 시간으로 가산.
- 정확한 강의명·문형·범위는 확인되지 않아 추정하지 않음.
- 오늘 누적 **약 4시간21분19초**. DB 정수 필드 261분, 기존 잔여 19초는 요약에 보존.
- 오늘 학습 종료로 처리하지 않음.
"""
    LOG.write_text(log_text.rstrip() + entry + "\n", encoding="utf-8")

with sqlite3.connect(DB) as con:
    minutes = con.execute(
        "SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-29'"
    ).fetchone()[0]

print(json.dumps({"ok": True, "record_id": RECORD_ID, "verified_minutes": minutes}, ensure_ascii=False))
