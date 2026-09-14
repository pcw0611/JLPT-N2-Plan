"""Add the user-confirmed 15-minute Anki example review and close 2026-08-31."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY = "anki-example-review-20260831-15m"
CLOSE_KEY = "day-close-20260831"
DATE = "2026-08-31"
RAW = ROOT / "database" / "results" / f"{KEY}.json"
payload = json.loads(RAW.read_text(encoding="utf-8"))
assert payload["elapsed_seconds"] == 900 and payload["day_closed_after_activity"] is True

db = ROOT / "database" / "jlpt_learning.db"
con = sqlite3.connect(db)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
row = con.execute("SELECT * FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()
assert row is not None
already = f"[{KEY}]" in (row["summary"] or "")

if not already:
    assert row["verified_minutes"] == 258
    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(backup_dir / ("before-anki-example-review-close-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")) as backup:
        con.backup(backup)
    extra = (
        f" [{KEY}] 사용자 확인 Anki 예문 복습15분 완료. 정확 누적258분31.009초에서 "
        f"273분31.009초(4시간33분31.009초); DB정수273분. [{CLOSE_KEY}] 사용자가 '오늘 끝'으로 "
        "2026-08-31 학습 종료를 명시. 미확인 시간 추가 추정 없음."
    )
    with con:
        con.execute(
            "UPDATE study_sessions SET verified_minutes=273,summary=summary||?,updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
            (extra, DATE),
        )

assert con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()[0] == 273
assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()

def append_once(marker: str, text: str) -> None:
    path = ROOT / "JLPT_STUDY_LOG.md"
    old = path.read_text(encoding="utf-8")
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + marker + "\n" + text.strip() + "\n", encoding="utf-8")
    assert path.read_text(encoding="utf-8").count(marker) == 1

append_once(f"<!-- {KEY} -->", """
## 2026-08-31 — Anki 예문 복습 15분

- 사용자 확인: 기존 Anki 문법 예문 복습 **15분** 완료.
- 직전 정확 누적 258분31.009초에 15분을 더해 오늘 최종 **273분31.009초(4시간33분31.009초)**. DB 정수 **273분**.
- 예문 복습의 개별 정오답 자료는 없으므로 숙달도·합격 가능성은 이 시간만으로 변경하지 않음.
""")
append_once(f"<!-- {CLOSE_KEY} -->", """
## 2026-08-31 — 오늘 학습 종료

- 사용자가 `오늘 끝`으로 학습 종료를 명시함.
- 최종 확인 학습시간 **4시간33분31.009초**. 이외 미확인 활동 시간은 추정해 추가하지 않음.
- 최종 시험 결과와 복습 큐를 반영한 뒤 홈페이지 양쪽 주소를 동기화함.
""")

print(json.dumps({"inserted": not already, "date": DATE, "verified_minutes": 273, "exact": "273분31.009초", "closed": True}, ensure_ascii=False))
con.close()
