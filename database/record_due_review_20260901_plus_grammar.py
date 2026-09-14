"""Record the submitted 2026-09-01 mixed due-review and grammar quiz exactly once."""
from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
TID = "due-review-20260901-review-plus-grammar"
DATE = "2026-09-01"
RAW = Path(r"C:\Users\pcw06\.codex\attachments\7a90f484-0af4-459b-b18b-a19a85d89f87\pasted-text.txt")
RESULT = ROOT / "database" / "results" / f"{TID}.json"
QUESTION_SOURCE = ROOT / "quiz_sites" / "due-review-20260831-44" / "app" / "questions.ts"
REVIEW_DATES = (("D+1", "2026-09-02"), ("D+3", "2026-09-04"), ("D+7", "2026-09-08"))


def item_type(category: str) -> str:
    if "유의표현" in category:
        return "paraphrase"
    if "문맥 규정" in category:
        return "context_vocabulary"
    if "문장 배열" in category:
        return "sentence_composition"
    if "글의 문법" in category:
        return "text_grammar"
    if "과제이해" in category:
        return "listening_task"
    if "포인트이해" in category:
        return "listening_point"
    if "표현 듣기" in category:
        return "listening_phrase_recognition"
    return "grammar_form"


payload = json.loads(RAW.read_text(encoding="utf-8"))
responses = sorted(payload["responses"], key=lambda row: row["itemNo"])
assert payload["testId"] == TID and payload["date"] == DATE
assert payload["total"] == len(responses) == 56
assert [row["itemNo"] for row in responses] == list(range(1, 57))
assert Counter(row["responseState"] for row in responses) == Counter(correct=43, wrong=12, unknown=1)
assert payload["correct"] == 43 and payload["wrong"] == 12 and payload["unknown"] == 1 and payload["unanswered"] == 0
assert payload["elapsedSeconds"] == 1561
assert payload["firstHalf"] == {"correct": 22, "total": 28, "seconds": 822}
assert payload["secondHalf"] == {"correct": 21, "total": 28, "seconds": 740}

normalized = {
    **payload,
    "resultClass": "submitted_normal",
    "questionSource": QUESTION_SOURCE.relative_to(ROOT).as_posix(),
    "questionSourceSha256": hashlib.sha256(QUESTION_SOURCE.read_bytes()).hexdigest(),
    "reviewDatesForWeakItems": [{"interval": interval, "date": date} for interval, date in REVIEW_DATES],
    "mappingNote": "기존 8/31 만기 큐 41건은 이미 completed 상태여서 재완료하지 않고, 이번 세션의 13개 오답·모름만 새 D+1/D+3/D+7로 연결함. reviewQueueId=0인 오늘 문법 15문항은 신규 문항으로 기록.",
}

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
existing = con.execute("SELECT notes FROM tests WHERE id=?", (TID,)).fetchone()
inserted = existing is None

if inserted:
    source_rows = {}
    for row in responses:
        queue_id = row["reviewQueueId"]
        if queue_id:
            source = con.execute(
                """SELECT r.*, q.item_type_id FROM review_queue r
                   JOIN question_attempts q ON q.id=r.attempt_id WHERE r.id=?""",
                (queue_id,),
            ).fetchone()
            assert source is not None and source["status"] == "completed"
            assert source["review_date"] == "2026-08-31"
            assert source["item_type_id"] == item_type(row["category"])
            source_rows[queue_id] = source

    weak = [row for row in responses if row["responseState"] in ("wrong", "unknown")]
    notes = {
        "submitted_result": normalized,
        "raw_result_file": str(RAW),
        "normalized_result_file": RESULT.relative_to(ROOT).as_posix(),
        "classification_note": "Self-made mixed repeat review with today's grammar 036-050; separate from official tests and official mock exams.",
        "weak_item_count": len(weak),
        "review_queue_policy": "Do not mutate already-completed source queues; create D+1/D+3/D+7 only for this session's wrong/unknown attempts.",
        "session_increment_seconds": 1561,
        "timing_note": "Only the submitted test timer was added; explanation time and other activity were not inferred.",
    }

    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DB, backup_dir / ("before-due-review-20260901-plus-grammar-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db"))

    with con:
        session = con.execute("SELECT * FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()
        assert session and session["verified_minutes"] == 207 and TID not in (session["summary"] or "")
        con.execute(
            """INSERT INTO tests
               (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,
                total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (TID, DATE, "만기 복습＋오늘 문법 59문항 중 56문항 제출", "self_made", "N2",
             "만기 재복습＋문법 036~050; 공식 난이도 미검증", "mixed_review", "multiple_choice",
             56, 43, 1, 0, 1561, None, 0.3, json.dumps(notes, ensure_ascii=False)),
        )
        for row in responses:
            seconds = int(round(row["responseSeconds"]))
            cur = con.execute(
                """INSERT INTO question_attempts
                   (test_id,item_no,item_type_id,level_label,response_state,response_seconds,
                    audio_seconds,decision_seconds,play_count,selected_text,correct_text,trap_hypothesis,trap_confidence)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (TID, row["itemNo"], item_type(row["category"]), "N2", row["responseState"], seconds,
                 None, None, row["playCount"], row["selectedText"], row["correctText"], None, None),
            )
            if row["responseState"] in ("wrong", "unknown"):
                for interval, review_date in REVIEW_DATES:
                    con.execute(
                        "INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,'pending')",
                        (cur.lastrowid, review_date, interval),
                    )
        con.execute(
            "UPDATE study_sessions SET verified_minutes=233,summary=summary||?,updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
            (f" [{TID}] 자체 제작 만기 재복습＋문법036~050 56문항 제출 43/56, 오답12·모름1·미응답0, 타이머1561초(26분01초). 기존 완료 큐는 재완료하지 않고 이번 약점13건 새복습39건 등록. 오늘 정확한 누적 확인시간 233분22.2초(정수233분). 사용자가 오늘 학습 종료를 명시함.", DATE),
        )
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
else:
    assert json.loads(existing["notes"])["submitted_result"] == normalized

saved = con.execute("SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no", (TID,)).fetchall()
assert len(saved) == 56
new_reviews = con.execute(
    """SELECT r.* FROM review_queue r JOIN question_attempts q ON q.id=r.attempt_id
       WHERE q.test_id=? ORDER BY q.item_no,r.review_date""", (TID,)
).fetchall()
assert len(new_reviews) == 39 and all(row["status"] == "pending" for row in new_reviews)
assert con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()[0] == 233
assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()
print(json.dumps({"test_id": TID, "inserted": inserted, "score": "43/56", "wrong": 12, "unknown": 1, "elapsed_seconds": 1561, "new_reviews": len(new_reviews), "session_minutes_field": 233, "session_remainder_seconds": 22.2, "integrity": "ok"}, ensure_ascii=False))
con.close()
