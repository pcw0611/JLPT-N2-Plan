"""Refresh the conservative JLPT readiness snapshot with the 2026-08-31 delayed review."""
from __future__ import annotations

import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-08-31"
OUT = ROOT / "outputs" / "probability-recalculation-20260831.json"
MARKER = "[recalculated-20260831-v1]"

GROUPS = {
    "grammar": {"grammar_form", "adjective_conjugation", "verb_conjugation", "sentence_composition", "text_grammar"},
    "vocabulary": {"context_vocabulary", "paraphrase", "kanji_reading"},
    "reading": {"short_claim", "short_content"},
    "listening": {"listening_point", "listening_task"},
}
EXCLUDED_TESTS = {
    "n2-grammar-009-015-correction-20260830",
    "listening-first-action-20260828-4",
    "listening-wrap-up-20260828-3",
}
WEIGHTS = {"grammar": 0.30, "vocabulary": 0.20, "reading": 0.20, "listening": 0.30}


def evidence_until(con: sqlite3.Connection, cutoff: str) -> dict:
    result = {}
    for domain, item_types in GROUPS.items():
        placeholders = ",".join("?" for _ in item_types)
        rows = con.execute(
            f"""SELECT q.response_state,q.test_id FROM question_attempts q
                JOIN tests t ON t.id=q.test_id
                WHERE q.item_type_id IN ({placeholders}) AND t.test_date<=?""",
            (*item_types, cutoff),
        ).fetchall()
        rows = [row for row in rows if row["test_id"] not in EXCLUDED_TESTS]
        total = len(rows)
        correct = sum(row["response_state"] == "correct" for row in rows)
        result[domain] = {"correct": correct, "total": total, "pct": round(correct * 100 / total, 1)}
    return result


def weighted(evidence: dict) -> float:
    return round(sum(evidence[key]["pct"] * WEIGHTS[key] for key in WEIGHTS), 1)


con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
assert con.execute("SELECT correct_items FROM tests WHERE id='due-review-20260831-all-44'").fetchone()[0] == 28

previous = evidence_until(con, "2026-08-30")
current = evidence_until(con, DATE)
previous_weighted = weighted(previous)
current_weighted = weighted(current)
assert previous == {
    "grammar": {"correct": 105, "total": 164, "pct": 64.0},
    "vocabulary": {"correct": 16, "total": 23, "pct": 69.6},
    "reading": {"correct": 9, "total": 12, "pct": 75.0},
    "listening": {"correct": 22, "total": 38, "pct": 57.9},
}
assert current == {
    "grammar": {"correct": 125, "total": 197, "pct": 63.5},
    "vocabulary": {"correct": 18, "total": 25, "pct": 72.0},
    "reading": {"correct": 9, "total": 12, "pct": 75.0},
    "listening": {"correct": 27, "total": 46, "pct": 58.7},
}
assert previous_weighted == 65.5 and current_weighted == 66.1

estimates = {
    "N3": {"low": 30.0, "high": 46.0, "projected": 80.0, "daily_change": 0.5},
    "N2": {"low": 5.0, "high": 15.0, "projected": 42.0, "daily_change": 0.5},
}
reason = (
    f"{MARKER} 공식형 호환 자체 문항 누적 재집계: 문법 {current['grammar']['correct']}/{current['grammar']['total']}={current['grammar']['pct']}%, "
    f"어휘 {current['vocabulary']['correct']}/{current['vocabulary']['total']}={current['vocabulary']['pct']}%, "
    f"독해 {current['reading']['correct']}/{current['reading']['total']}={current['reading']['pct']}%, "
    f"청해 {current['listening']['correct']}/{current['listening']['total']}={current['listening']['pct']}%, "
    f"가중 관측 {previous_weighted}%→{current_weighted}%(+{round(current_weighted-previous_weighted,1)}%p). "
    "문장 배열·글의 문법은 문법에 포함하고 비공식 표현 듣기는 제외. 즉시 교정·같은 학습 사슬 후속 연습은 독립 표본에서 제외. "
    "8/31 만기 44문항 28/44, D+1·D+3 각각14/22. 어휘·청해는 소폭 개선, 문법은 소폭 하락, 후반 정확도 18.2%p 하락은 유형 구성 차이로 피로 단독 귀속 불가. "
    "공식 종합 모의고사와 충분한 N2 범위 표본이 없어 현재 범위 상단만 1%p 확대하고 시험일까지 전망은 유지. 통계적으로 보정된 확률이 아니며 신뢰도 낮음."
)

existing = con.execute(
    "SELECT count(*) FROM pass_probability_snapshots WHERE snapshot_date=?", (DATE,)
).fetchone()[0]
inserted = existing == 0
if inserted:
    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DB, backup_dir / ("before-probability-20260831-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db"))
    with con:
        for level, values in estimates.items():
            con.execute(
                """INSERT INTO pass_probability_snapshots
                   (snapshot_date,level,current_low_pct,current_high_pct,projected_exam_pct,daily_change_pp,confidence,reason)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (DATE, level, values["low"], values["high"], values["projected"], values["daily_change"], "low", reason),
            )
else:
    rows = con.execute("SELECT * FROM pass_probability_snapshots WHERE snapshot_date=? ORDER BY level", (DATE,)).fetchall()
    assert len(rows) == 2 and all(row["reason"] == reason for row in rows)

assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
payload = {
    "date": DATE,
    "method": "official-compatible self-made item aggregation; uncalibrated readiness heuristic",
    "excluded_tests": sorted(EXCLUDED_TESTS),
    "previous_evidence_recomputed": previous,
    "current_evidence": current,
    "previous_weighted_pct": previous_weighted,
    "current_weighted_pct": current_weighted,
    "weighted_change_pp": round(current_weighted - previous_weighted, 1),
    "estimates": estimates,
    "confidence": "low",
    "reason": reason,
    "inserted": inserted,
}
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False))
con.close()
