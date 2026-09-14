"""Read-only, deterministic daily/as-of-date projections of the learning DB."""
from datetime import datetime, timezone
import json
import statistics
from pathlib import Path
import sqlite3

TAXONOMY = json.loads((Path(__file__).resolve().parents[1] / "lib/report-taxonomy.json").read_text(encoding="utf-8"))


def metadata(notes):
    try:
        value = json.loads(notes or "{}")
        return value if isinstance(value, dict) else {}
    except (ValueError, TypeError):
        return {}


def compatible_anki_stats(value):
    """Return a UI-compatible Anki stats payload, otherwise hide the panel safely."""
    if not isinstance(value, dict):
        return None
    if value.get("schema") == "daily_summary_v1":
        required = ("answeredCards", "studyMinutes", "secondsPerCard", "againCount", "againPct", "learningReviews", "reviewsDone")
        if any(not isinstance(value.get(key), (int, float)) for key in required):
            return None
        ratings = value.get("ratings")
        remaining = value.get("cardsRemaining")
        if not isinstance(ratings, dict) or any(not isinstance(ratings.get(key), (int, float)) for key in ("again", "hard", "good", "easy")):
            return None
        if not isinstance(remaining, dict) or any(not isinstance(remaining.get(key), (int, float)) for key in ("new", "learning", "review")):
            return None
        return value
    required_numbers = (
        "answeredCards", "studyMinutes", "secondsPerCard", "againCount", "againPct",
        "medianIntervalDays", "medianEasePct",
    )
    if any(not isinstance(value.get(key), (int, float)) for key in required_numbers):
        return None
    nested_numbers = {
        "forecast": ("tomorrowDue", "dailyLoad", "totalReviews"),
        "cards": ("total", "new", "newPct", "young", "youngPct", "mature"),
    }
    for group, keys in nested_numbers.items():
        row = value.get(group)
        if not isinstance(row, dict) or any(not isinstance(row.get(key), (int, float)) for key in keys):
            return None
    retention = value.get("retention")
    if not isinstance(retention, dict):
        return None
    for period in ("today", "lastWeek"):
        row = retention.get(period)
        if not isinstance(row, dict) or any(not isinstance(row.get(key), (int, float)) for key in ("pct", "count")):
            return None
    return value


def audio_error(row):
    info = metadata(row["notes"])
    return row["item_no"] in info.get("audio_error_items", []) or info.get("audio_error_flags", {}).get(str(row["item_no"])) is True


def aggregate(rows, listening=False):
    valid = [r for r in rows if not audio_error(r)]
    field = "decision_seconds" if listening else "response_seconds"
    times = [r[field] for r in valid if r[field] is not None and "속도 진단에서 제외" not in (r["notes"] or "")]
    return {
        "total": len(valid),
        "correct": sum(r["response_state"] == "correct" for r in valid),
        "wrong": sum(r["response_state"] == "wrong" for r in valid),
        "unknown": sum(r["response_state"] == "unknown" for r in valid),
        "unanswered": sum(r["response_state"] == "unanswered" for r in valid),
        "excluded": len(rows) - len(valid),
        "averageSeconds": round(statistics.mean(times), 1) if times else None,
        "medianSeconds": statistics.median(times) if times else None,
        "timedItems": len(times),
    }


def make_report(conn, date):
    conn.row_factory = sqlite3.Row
    session = conn.execute("SELECT * FROM study_sessions WHERE session_date=?", (date,)).fetchone()
    if session is None:
        raise ValueError(f"No study session for {date}")
    tests = conn.execute("SELECT * FROM tests WHERE test_date=? ORDER BY id", (date,)).fetchall()
    attempts = conn.execute("""SELECT q.*, t.test_date, t.notes FROM question_attempts q
        JOIN tests t ON t.id=q.test_id WHERE t.test_date<=? ORDER BY t.test_date,q.id""", (date,)).fetchall()
    daily = [r for r in attempts if r["test_date"] == date]
    snapshots = conn.execute("SELECT * FROM mastery_snapshots WHERE snapshot_date=?", (date,)).fetchall()
    domain_snapshots = {r["metric_key"]: r for r in snapshots if r["metric_group"] == "exam_domain"}
    type_snapshots = {r["metric_key"]: r for r in snapshots if r["metric_group"] == "item_type"}
    domains = []
    for category in TAXONOMY["domains"]:
        snapshot = domain_snapshots.get(category["key"])
        domains.append({**category, "low": snapshot["low_pct"] if snapshot else None,
                        "high": snapshot["high_pct"] if snapshot else None,
                        "grade": snapshot["internal_grade"] if snapshot else None})
    # Include every registered category every day, even without a snapshot or attempt.
    known = {t["key"] for t in TAXONOMY["types"]}
    definitions = list(TAXONOMY["types"])
    definitions += [{"key": r["id"], "domain": r["domain"], "label": r["label_ja"] or r["label_ko"]}
                    for r in conn.execute("SELECT * FROM item_types ORDER BY domain,id") if r["id"] not in known]
    domain_order = {d["key"]: i for i,d in enumerate(TAXONOMY["domains"])}
    definitions.sort(key=lambda d: domain_order.get(d["domain"], 99))
    metrics = []
    for definition in definitions:
        key = definition["key"]
        rows = [r for r in attempts if r["item_type_id"] == key]
        current = [r for r in rows if r["test_date"] == date]
        listening = definition["domain"] == "listening"
        today, cumulative = aggregate(current, listening), aggregate(rows, listening)
        snapshot = type_snapshots.get(key)
        metrics.append({**definition, **today, "cumulative": cumulative,
                        "timingBasis": "audio_end_to_answer" if listening else "question_total",
                        "grade": snapshot["internal_grade"] if snapshot else None,
                        "evaluationSampleCount": snapshot["sample_count"] if snapshot else 0,
                        "evaluationConfidence": snapshot["confidence"] if snapshot else None})
    probabilities = {}
    for row in conn.execute("SELECT * FROM pass_probability_snapshots WHERE snapshot_date=?", (date,)):
        probabilities[row["level"]] = {"low":row["current_low_pct"],"high":row["current_high_pct"],"projected":row["projected_exam_pct"]}
    anki = None
    has_anki_table = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='anki_daily_stats'").fetchone()
    if has_anki_table:
        anki_row = conn.execute("SELECT payload_json FROM anki_daily_stats WHERE snapshot_date=?", (date,)).fetchone()
        if anki_row:
            anki = compatible_anki_stats(json.loads(anki_row["payload_json"]))
    # Show the plan derived from evidence available by the selected date, not today's
    # mutable pending queue. Do not invent historical completion timestamps.
    review = conn.execute("""SELECT r.review_date, COUNT(*) count FROM review_queue r
        JOIN question_attempts q ON q.id=r.attempt_id JOIN tests t ON t.id=q.test_id
        WHERE t.test_date<=? AND r.review_date>? GROUP BY r.review_date ORDER BY r.review_date LIMIT 1""", (date,date)).fetchone()
    total = sum(t["total_items"] for t in tests)
    correct = sum(t["correct_items"] for t in tests)
    unknown = sum(t["unknown_items"] for t in tests)
    unanswered = sum(t["unanswered_items"] for t in tests)
    measured = [m for m in metrics if m["total"]]
    # Stable sorting keeps taxonomy order for tied scores.
    ranked = sorted(measured, key=lambda m:-m["correct"]/m["total"])
    return {
        "schemaVersion":2,"date":date,"syncedAt":datetime.now(timezone.utc).isoformat(),
        "studyMinutes":session["verified_minutes"],"hasUntrackedActivity":bool(session["has_untracked_activity"]),
        "tests":{"count":len(tests),"correct":correct,"total":total,"wrong":total-correct-unknown-unanswered,
                 "unknown":unknown,"unanswered":unanswered,"elapsedSeconds":sum(t["elapsed_seconds"] or 0 for t in tests),
                 "untimedTests":sum(t["elapsed_seconds"] is None for t in tests),
                 "unclassifiedItems":max(0,total-len(daily)),"excludedItems":sum(audio_error(r) for r in daily)},
        "testDetails":[{"id":t["id"],"title":t["title"],"sourceClass":t["source_class"],
                        "correct":t["correct_items"],"total":t["total_items"],"elapsedSeconds":t["elapsed_seconds"]} for t in tests],
        "probabilities":probabilities,"domains":domains,"types":metrics,"anki":anki,
        "nextReview":{"date":review["review_date"],"count":review["count"]} if review else None,
        "strengths":[m["label"] for m in ranked if m["correct"]/m["total"] >= .8][:3],
        "weaknesses":[m["label"] for m in metrics if m["total"] and m["correct"]/m["total"] < .8],
        "confidenceNote":"当日は選択日の解答、累積はその日までの記録です。少数問題・再生条件の違いがあり、参考評価と合格予測は正答率から換算しません。",
    }
