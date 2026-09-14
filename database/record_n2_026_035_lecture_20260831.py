"""Record the user-confirmed N2 grammar 026-035 lecture and exact duration once."""
from __future__ import annotations

import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-08-31"
MARKER = "[n2-grammar-026-035-lecture-completed-20260831]"
RESULT = ROOT / "database" / "results" / "n2-grammar-026-035-lecture-completed-20260831.json"
PATTERNS = [
    {"number": "026", "pattern": "〜きる／〜きれない"},
    {"number": "027", "pattern": "〜くせに"},
    {"number": "028", "pattern": "〜こそ／〜からこそ"},
    {"number": "029", "pattern": "〜ことか"},
    {"number": "030", "pattern": "〜ことから／〜ところから"},
    {"number": "031", "pattern": "〜ことだから"},
    {"number": "032", "pattern": "〜ことなく"},
    {"number": "033", "pattern": "〜ことに"},
    {"number": "034", "pattern": "〜ことになる／〜ことにはならない／〜ことにする"},
    {"number": "035", "pattern": "〜ことはない"},
]
payload = {
    "id": "n2-grammar-026-035-lecture-completed-20260831",
    "date": DATE,
    "title": "다락원 N2 문법 026~035 강의",
    "status": "completed_user_confirmed",
    "elapsed_seconds": 31 * 60 + 49,
    "elapsed_text": "31분 49초",
    "pages": "p.214~219",
    "patterns": PATTERNS,
    "source": "https://www.darakwon.co.kr/planner/jlpt/grammar.asp?ver=2602&pkg_id=12556&pkg=n2&p_id=8568&ls_id=2463&lsi_id=52251",
    "source_note": "사용자가 연 내부 강의 화면의 026~035 목록을 직접 확인. 다른 다락원 교재의 공개 목차는 사용하지 않음.",
}

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
session = con.execute("SELECT * FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()
assert session is not None
inserted = MARKER not in (session["summary"] or "")
if inserted:
    assert session["verified_minutes"] == 221
    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DB, backup_dir / ("before-n2-026-035-lecture-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db"))
    extra = (
        f" {MARKER} 사용자 확인 N2 문법026~035 강의 완료, 정확한 시간31분49초. "
        "기존 정확한 누적221분08.009초에 가산해252분57.009초; DB정수252분. "
        "문형 목록은 사용자가 연 다락원 2026 개정판 내부 강의 화면 p.214~219에서 확인. 오늘 종료 아님."
    )
    with con:
        con.execute(
            "UPDATE study_sessions SET verified_minutes=252,summary=summary||?,updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
            (extra, DATE),
        )
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
else:
    assert session["verified_minutes"] == 252 and RESULT.exists()
    assert json.loads(RESULT.read_text(encoding="utf-8")) == payload

assert con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()[0] == 252
assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
print(json.dumps({"inserted": inserted, "verified_minutes": 252, "exact_total": "252분57.009초", "patterns": PATTERNS}, ensure_ascii=False))
con.close()
