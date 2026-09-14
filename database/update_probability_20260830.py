"""Add a conservative 2026-08-30 probability snapshot without treating self-made quizzes as official scores."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
SNAPSHOT_DATE = "2026-08-30"
reason = (
    "8/30 Anki APKG 대조(오늘 293회·고유209장, 마지막 Hard73장), N2 문법016~025 강의 직후 확인 9/12, "
    "당일 만기 변형 결과를 반영한 보수적 갱신. 모든 시험은 자체 제작·중복 표본이며 공식 종합 모의고사나 JLPT 환산점수가 아니므로 "
    "현재 범위와 시험일까지 전망 수치를 변경하지 않음. 공식 시간제 종합 모의고사 2~3회 후 재보정 필요."
)

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
existing = con.execute(
    "SELECT id FROM pass_probability_snapshots WHERE snapshot_date=? AND level=?",
    (SNAPSHOT_DATE, "N3"),
).fetchone()
if existing is None:
    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(backup_dir / ("before-probability-20260830-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")) as backup:
        con.backup(backup)
    with con:
        con.execute(
            "INSERT INTO pass_probability_snapshots (snapshot_date,level,current_low_pct,current_high_pct,projected_exam_pct,daily_change_pp,confidence,reason) VALUES (?,?,?,?,?,?,?,?)",
            (SNAPSHOT_DATE, "N3", 23.0, 39.0, 82.0, 0.0, "low", reason),
        )
        con.execute(
            "INSERT INTO pass_probability_snapshots (snapshot_date,level,current_low_pct,current_high_pct,projected_exam_pct,daily_change_pp,confidence,reason) VALUES (?,?,?,?,?,?,?,?)",
            (SNAPSHOT_DATE, "N2", 6.0, 16.0, 48.0, 0.0, "low", reason),
        )
    status = "inserted"
else:
    status = "already_present"

assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
rows = con.execute(
    "SELECT snapshot_date,level,current_low_pct,current_high_pct,projected_exam_pct,daily_change_pp,confidence FROM pass_probability_snapshots WHERE snapshot_date=? ORDER BY level",
    (SNAPSHOT_DATE,),
).fetchall()
print(json.dumps({"status": status, "rows": [dict(r) for r in rows], "integrity": "ok"}, ensure_ascii=False))
con.close()
