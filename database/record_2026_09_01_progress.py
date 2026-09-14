"""Record 2026-09-01 lecture progress and the verified Anki inventory snapshot."""
from __future__ import annotations

import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-09-01"
LECTURE_MARKER = "[n2-grammar-036-050-lecture-completed-20260901]"
ANKI_MARKER = "[anki-n3-n2-inventory-20260901]"

anki_payload = {
    "scope": "N3+N2",
    "scopeLabel": "N3·N2 새 카드 재고",
    "capturedDate": DATE,
    "source": "Anki MCP cards_stats after successful AnkiWeb sync",
    "n3Vocabulary": {"total": 512, "unseen": 277, "seen": 235},
    "n2Vocabulary": {"total": 1169, "unseen": 1009, "seen": 160},
    "n2GrammarAndError": {"total": 83, "unseen": 15, "seen": 68},
    "unseenNow": 1301,
    "futureGrammarCardsThrough150": 100,
    "totalFirstExposuresDueBy20260919": 1401,
    "excludedDecks": ["N4", "N5"],
    "note": "학습시간·당일 답변 횟수 통계가 아니라 동기화 직후 카드 스케줄 재고다.",
}

lecture_result = {
    "id": "n2-grammar-036-050-lecture-completed-20260901",
    "date": DATE,
    "status": "completed_user_confirmed",
    "title": "다락원 N2 문법 036~050 강의 2개",
    "ranges": [
        {"range": "036~043", "pages": "p.219~223"},
        {"range": "044~050", "pages": "p.224~227"},
    ],
    "elapsed_seconds": 3600,
    "anki_cards_added": 15,
    "source": "https://www.darakwon.co.kr/planner/jlpt/package.asp?ver=2602&pkg=n2&pkg_id=12556",
}

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
row = con.execute(
    "SELECT verified_minutes, COALESCE(summary, '') summary FROM study_sessions WHERE session_date=?",
    (DATE,),
).fetchone()
summary = row["summary"] if row else ""
needs_lecture = LECTURE_MARKER not in summary
needs_anki = ANKI_MARKER not in summary

if needs_lecture or needs_anki:
    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DB, backup_dir / ("before-20260901-progress-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db"))

with con:
    if row is None:
        summary_parts = []
        minutes = 0
        if needs_lecture:
            minutes += 60
            summary_parts.append(
                f"{LECTURE_MARKER} 사용자 확인: 다락원 N2 문법036~043·044~050 강의 2개 완료, "
                "확인 학습시간 합계60분. 기존 Anki 문법 덱에 문형 카드15장 추가. 오늘 종료 아님."
            )
        if needs_anki:
            summary_parts.append(
                f"{ANKI_MARKER} AnkiWeb 동기화 후 N3·N2만 집계: N3 새277, N2 어휘 새1009, "
                "N2 문법·오답 새15. 현재 새 카드1301장; 문법051~150에서 추가될100장을 포함해 "
                "9/19까지 첫 노출 대상1401장. N4·N5 제외. 재고 조회는 학습시간에 미가산."
            )
        con.execute(
            "INSERT INTO study_sessions(session_date,verified_minutes,has_untracked_activity,summary) VALUES(?,?,0,?)",
            (DATE, minutes, " ".join(summary_parts)),
        )
    else:
        additions = []
        minutes = row["verified_minutes"]
        if needs_lecture:
            minutes += 60
            additions.append(
                f" {LECTURE_MARKER} 사용자 확인: 다락원 N2 문법036~043·044~050 강의 2개 완료, "
                "확인 학습시간 합계60분. 기존 Anki 문법 덱에 문형 카드15장 추가. 오늘 종료 아님."
            )
        if needs_anki:
            additions.append(
                f" {ANKI_MARKER} AnkiWeb 동기화 후 N3·N2만 집계: N3 새277, N2 어휘 새1009, "
                "N2 문법·오답 새15. 현재 새 카드1301장; 문법051~150에서 추가될100장을 포함해 "
                "9/19까지 첫 노출 대상1401장. N4·N5 제외. 재고 조회는 학습시간에 미가산."
            )
        con.execute(
            "UPDATE study_sessions SET verified_minutes=?,summary=summary||?,updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
            (minutes, "".join(additions), DATE),
        )

    con.execute(
        """INSERT INTO anki_daily_stats(snapshot_date,scope_label,payload_json,source_filename,captured_at,updated_at)
           VALUES(?,?,?,?,?,CURRENT_TIMESTAMP)
           ON CONFLICT(snapshot_date) DO UPDATE SET
             scope_label=excluded.scope_label,
             payload_json=excluded.payload_json,
             source_filename=excluded.source_filename,
             captured_at=excluded.captured_at,
             updated_at=CURRENT_TIMESTAMP""",
        (DATE, "N3+N2", json.dumps(anki_payload, ensure_ascii=False), "Anki MCP cards_stats", f"{DATE}T00:00:00+09:00"),
    )

result_dir = ROOT / "database" / "results"
result_dir.mkdir(parents=True, exist_ok=True)
(result_dir / "n2-grammar-036-050-lecture-completed-20260901.json").write_text(
    json.dumps(lecture_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
(result_dir / "anki-n3-n2-inventory-20260901.json").write_text(
    json.dumps(anki_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
recorded = con.execute(
    "SELECT verified_minutes,summary FROM study_sessions WHERE session_date=?", (DATE,)
).fetchone()
print(json.dumps({
    "date": DATE,
    "verified_minutes": recorded["verified_minutes"],
    "lecture_recorded": LECTURE_MARKER in recorded["summary"],
    "anki_recorded": ANKI_MARKER in recorded["summary"],
    "anki_unseen_now": anki_payload["unseenNow"],
    "first_exposures_due": anki_payload["totalFirstExposuresDueBy20260919"],
}, ensure_ascii=False))
con.close()
