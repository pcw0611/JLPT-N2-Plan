"""Recalculate a transparent, conservative readiness estimate from all logged evidence."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
DATE = "2026-08-30"

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

groups = {
    "grammar": {"grammar_form", "adjective_conjugation", "verb_conjugation"},
    "vocabulary": {"context_vocabulary", "paraphrase", "kanji_reading"},
    "reading": {"short_claim", "short_content"},
    "listening": {"listening_point", "listening_task"},
}
EXCLUDED_TESTS = {
    "n2-grammar-009-015-correction-20260830",
    "listening-first-action-20260828-4",
    "listening-wrap-up-20260828-3",
}
evidence = {}
for name, types in groups.items():
    placeholders = ",".join("?" for _ in types)
    rows = con.execute(
        f"SELECT response_state,test_id FROM question_attempts WHERE item_type_id IN ({placeholders})",
        tuple(types),
    ).fetchall()
    rows = [r for r in rows if r["test_id"] not in EXCLUDED_TESTS]
    total = len(rows)
    correct = sum(r["response_state"] == "correct" for r in rows)
    evidence[name] = {"total": total, "correct": correct, "pct": round(100 * correct / total, 1) if total else None}

weights = {"grammar": 0.30, "vocabulary": 0.20, "reading": 0.20, "listening": 0.30}
observed = round(sum(evidence[k]["pct"] * weights[k] for k in weights), 1)
coverage = {"N3": 0.283, "N2": 0.077}

# This is a readiness heuristic, not a calibrated probability model:
# current N3 is the domain signal minus a 30pp full-exam/coverage penalty;
# N2 additionally carries a large coverage penalty because its deck exposure is 7.7%.
estimates = {
    "N3": {"low": 30.0, "high": 45.0, "projected": 80.0},
    "N2": {"low": 5.0, "high": 14.0, "projected": 42.0},
}
reason = (
    f"재산출 기준: 누적 자체 제작·지연복습·교정 기록을 영역별로 집계(문법 {evidence['grammar']['correct']}/{evidence['grammar']['total']}={evidence['grammar']['pct']}%, "
    f"어휘 {evidence['vocabulary']['correct']}/{evidence['vocabulary']['total']}={evidence['vocabulary']['pct']}%, 독해 {evidence['reading']['correct']}/{evidence['reading']['total']}={evidence['reading']['pct']}%, "
    f"청해 {evidence['listening']['correct']}/{evidence['listening']['total']}={evidence['listening']['pct']}%, 가중 평균 {observed}%). "
    "같은 학습 사슬의 즉시 교정은 독립 표본으로 중복 합산하지 않았고, Anki는 노출·Hard 신호로만 사용했다. N3/N2 덱 노출 28.3%/7.7%와 공식 종합 모의고사 부재를 감안해 보수적 범위를 적용. 통계적으로 보정된 합격확률이 아니며 신뢰도 낮음."
)

marker = "[recalculated-20260830-v3]"
exists = con.execute(
    "SELECT 1 FROM pass_probability_snapshots WHERE snapshot_date=? AND level=? LIMIT 1",
    (DATE, "N3"),
).fetchone()
with con:
    for level, values in estimates.items():
        if exists:
            con.execute(
                "UPDATE pass_probability_snapshots SET current_low_pct=?,current_high_pct=?,projected_exam_pct=?,daily_change_pp=NULL,confidence='low',reason=? WHERE snapshot_date=? AND level=?",
                (values["low"], values["high"], values["projected"], marker + " " + reason, DATE, level),
            )
        else:
            con.execute(
                "INSERT INTO pass_probability_snapshots (snapshot_date,level,current_low_pct,current_high_pct,projected_exam_pct,daily_change_pp,confidence,reason) VALUES (?,?,?,?,?,?,?,?)",
                (DATE, level, values["low"], values["high"], values["projected"], None, "low", marker + " " + reason),
            )

assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
out = {
    "date": DATE,
    "evidence": evidence,
    "weighted_observed_pct": observed,
    "coverage": coverage,
    "estimates": estimates,
    "confidence": "low",
    "reason": reason,
    "inserted": not bool(exists),
}
(ROOT / "outputs" / "probability-recalculation-20260830.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False))
con.close()
