"""Record the submitted 2026-08-31 continuous 44-item due-review test once."""
from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
TID = "due-review-20260831-all-44"
DATE = "2026-08-31"
RAW = Path(r"C:\Users\pcw06\.codex\attachments\33fbd378-3ec7-4538-9d8d-6b73a1727d48\pasted-text.txt")
RESULT = ROOT / "database" / "results" / f"{TID}.json"
QUESTION_SOURCE = ROOT / "quiz_sites" / "due-review-20260831-44" / "app" / "questions.ts"
REVIEW_DATES = (("D+1", "2026-09-01"), ("D+3", "2026-09-03"), ("D+7", "2026-09-07"))


def item_type(category: str) -> str:
    if "유의표현" in category:
        return "paraphrase"
    if "문맥 규정" in category:
        return "context_vocabulary"
    if "문법 → 활용" in category:
        return "adjective_conjugation"
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
assert payload["total"] == len(responses) == 44
assert [row["itemNo"] for row in responses] == list(range(1, 45))
states = Counter(row["responseState"] for row in responses)
assert states == Counter(correct=28, wrong=14, unknown=2)
assert payload["correct"] == 28 and payload["wrong"] == 14
assert payload["unknown"] == 2 and payload["unanswered"] == 0
assert payload["elapsedSeconds"] == 1696
assert payload["firstHalf"] == {"correct": 16, "total": 22, "seconds": 954}
assert payload["secondHalf"] == {"correct": 12, "total": 22, "seconds": 743}
assert len({row["reviewQueueId"] for row in responses}) == 44

weak_items = [row for row in responses if row["responseState"] in ("wrong", "unknown")]
assert [row["itemNo"] for row in weak_items] == [4, 5, 7, 8, 15, 17, 23, 24, 26, 29, 30, 32, 34, 38, 39, 40]

trap_notes = {
    4: "추가의 うえに를 시간·절차의 うえで와 혼동한 것으로 추정.",
    5: "今ちょうど라는 진행 단서보다 완료형 書いた을 선택.",
    7: "외부 잠금이라는 논리적 부정 근거와 はずがない 연결이 인출되지 않음.",
    8: "昔를 문장 전체의 과거 단서로 처리해 현재 부정을 과거 부정으로 바꾼 것으로 추정.",
    15: "観点라는 직접 단서에도 결심·의무의 からには를 선택.",
    17: "な형용사 静か를 い형용사처럼 かった 활용.",
    23: "반복 경향 がち를 한 번의 미완료 かけ와 혼동.",
    24: "긴 과정 끝의 결과 あげく를 단순 정보 추가 うえに와 혼동.",
    26: "주어 私의 겸양 방향과 상대 행동의 존경 방향을 뒤집음.",
    29: "자연현상 雪が降る에 사역형 降らせる를 선택.",
    30: "理解しがたい의 접속·의미가 인출되지 않음.",
    32: "사장님의 말하기에 존경어 おっしゃる 대신 자기 행동을 낮추는 いたす를 선택.",
    34: "전체 배열보다 보이는 첫 조각 言い를 ★ 답으로 선택.",
    38: "첫 행동 番号札を取る 대신 이후 목적지 二階の窓口를 선택.",
    39: "最初に와 직접 연결된 접수 용지 수령을 놓치고 대본에 없는 名前を呼ばれる를 선택.",
    40: "まず의 창문 열기 대신 두 번째 행동인 테이블 닦기를 선택.",
}

normalized = {
    **payload,
    "resultClass": "submitted_normal",
    "questionSource": QUESTION_SOURCE.relative_to(ROOT).as_posix(),
    "questionSourceSha256": hashlib.sha256(QUESTION_SOURCE.read_bytes()).hexdigest(),
    "reviewDatesForWeakItems": [{"interval": i, "date": d} for i, d in REVIEW_DATES],
}

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
existing = con.execute("SELECT notes FROM tests WHERE id=?", (TID,)).fetchone()
inserted = existing is None

if inserted:
    source_rows = {}
    interval_scores: dict[str, Counter] = defaultdict(Counter)
    for row in responses:
        source = con.execute(
            """SELECT r.*, q.item_type_id FROM review_queue r
               JOIN question_attempts q ON q.id=r.attempt_id WHERE r.id=?""",
            (row["reviewQueueId"],),
        ).fetchone()
        assert source is not None
        assert source["review_date"] == DATE and source["status"] == "pending"
        assert source["interval_label"] in ("D+1", "D+3")
        assert source["item_type_id"] == item_type(row["category"])
        source_rows[row["reviewQueueId"]] = source
        interval_scores[source["interval_label"]][row["responseState"]] += 1
        interval_scores[source["interval_label"]]["total"] += 1
    assert interval_scores["D+1"] == Counter(total=22, correct=14, wrong=7, unknown=1)
    assert interval_scores["D+3"] == Counter(total=22, correct=14, wrong=7, unknown=1)

    type_scores: dict[str, Counter] = defaultdict(Counter)
    for row in responses:
        key = item_type(row["category"])
        type_scores[key][row["responseState"]] += 1
        type_scores[key]["total"] += 1

    notes = {
        "submitted_result": normalized,
        "raw_result_file": str(RAW),
        "normalized_result_file": RESULT.relative_to(ROOT).as_posix(),
        "classification_note": "Self-made delayed due-review variants; separate from official tests and official mock exams.",
        "question_source": normalized["questionSource"],
        "question_source_sha256": normalized["questionSourceSha256"],
        "due_interval_scores": {key: dict(value) for key, value in interval_scores.items()},
        "item_type_scores": {key: dict(value) for key, value in type_scores.items()},
        "stamina_signal": {
            "first_half": payload["firstHalf"],
            "second_half": payload["secondHalf"],
            "accuracy_drop_percentage_points": 18.2,
            "interpretation_limit": "Question-type mix differs by half, so the drop is not attributable to fatigue alone; second half was faster and may include rushing.",
        },
        "session_base_exact_seconds": 192 * 60 + 52.009,
        "session_increment_seconds": 1696,
        "session_total_exact_seconds": 221 * 60 + 8.009,
        "session_integer_minutes": 221,
        "timing_note": "Only the submitted test timer was added; explanation time and other activity were not inferred.",
    }

    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / ("before-due-review-20260831-all-44-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")
    shutil.copy2(DB, backup)

    with con:
        session = con.execute("SELECT * FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()
        assert session and session["verified_minutes"] == 192 and TID not in (session["summary"] or "")
        con.execute(
            """INSERT INTO tests
               (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,
                total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (TID, DATE, "만기 복습 44문항 연속 지구력 시험", "self_made", "N3 기반·N2",
             "만기 D+1·D+3 표적 변형; 공식 난이도 미검증", "delayed_due_review", "multiple_choice",
             44, 28, 2, 0, 1696, None, 0.3, json.dumps(notes, ensure_ascii=False)),
        )
        for row in responses:
            item_no = row["itemNo"]
            source = source_rows[row["reviewQueueId"]]
            seconds = int(round(row["responseSeconds"]))
            cur = con.execute(
                """INSERT INTO question_attempts
                   (test_id,item_no,item_type_id,level_label,response_state,response_seconds,
                    audio_seconds,decision_seconds,play_count,selected_text,correct_text,trap_hypothesis,trap_confidence)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (TID, item_no, item_type(row["category"]), "N3 기반·N2", row["responseState"], seconds,
                 None, None, row["playCount"], row["selectedText"], row["correctText"],
                 trap_notes.get(item_no), "medium" if item_no in trap_notes else None),
            )
            changed = con.execute(
                """UPDATE review_queue SET status='completed',result_state=?,result_seconds=?
                   WHERE id=? AND attempt_id=? AND review_date=? AND interval_label=? AND status='pending'""",
                (row["responseState"], seconds, row["reviewQueueId"], source["attempt_id"], DATE, source["interval_label"]),
            )
            assert changed.rowcount == 1
            if row["responseState"] in ("wrong", "unknown"):
                for interval, review_date in REVIEW_DATES:
                    con.execute(
                        "INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,'pending')",
                        (cur.lastrowid, review_date, interval),
                    )
        extra = (
            f" [{TID}] 자체 제작 만기 연속시험 28/44, 오답14·모름2·미응답0, 타이머1696초. "
            "정상제출44건 완료, 약점16건 새복습48건. 전반16/22·954초, 후반12/22·743초; "
            "유형 구성 차이로 피로 단독 귀속 불가. 오늘 정확한 확인시간221분08.009초; "
            "DB정수221분. 해설·기타시간 미가산. 오늘 종료 아님."
        )
        con.execute(
            "UPDATE study_sessions SET verified_minutes=221,summary=summary||?,updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
            (extra, DATE),
        )
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
else:
    old = json.loads(existing["notes"])
    assert old["submitted_result"] == normalized

saved = con.execute("SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no", (TID,)).fetchall()
assert len(saved) == 44
for raw, stored in zip(responses, saved):
    assert stored["item_no"] == raw["itemNo"]
    assert stored["response_state"] == raw["responseState"]
    assert stored["selected_text"] == raw["selectedText"] and stored["correct_text"] == raw["correctText"]
for raw in responses:
    source = con.execute("SELECT * FROM review_queue WHERE id=?", (raw["reviewQueueId"],)).fetchone()
    assert source["status"] == "completed" and source["result_state"] == raw["responseState"]
new_reviews = con.execute(
    """SELECT r.* FROM review_queue r JOIN question_attempts q ON q.id=r.attempt_id
       WHERE q.test_id=? ORDER BY q.item_no,r.review_date""",
    (TID,),
).fetchall()
assert len(new_reviews) == 48 and all(row["status"] == "pending" for row in new_reviews)
assert con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()[0] == 221
assert con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date<=?", (DATE,)).fetchone()[0] == 0
assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()

pending = {
    row["review_date"]: row["n"]
    for row in con.execute(
        "SELECT review_date,count(*) n FROM review_queue WHERE status='pending' GROUP BY review_date ORDER BY review_date"
    )
}
print(json.dumps({
    "test_id": TID,
    "inserted": inserted,
    "score": "28/44",
    "wrong": 14,
    "unknown": 2,
    "elapsed_seconds": 1696,
    "completed_due_reviews": 44,
    "new_reviews": len(new_reviews),
    "pending_by_date": pending,
    "session_minutes_field": 221,
    "session_remainder_seconds": 8.009,
    "integrity": "ok",
}, ensure_ascii=False))
con.close()
