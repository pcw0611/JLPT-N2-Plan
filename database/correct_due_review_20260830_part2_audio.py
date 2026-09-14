"""Exclude part-2 listening items after the user reported spoken speaker labels."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
TID = "due-review-20260830-part2-13"
RESULT = ROOT / "database" / "results" / f"{TID}.json"
AUDIO_ITEMS = {1, 2, 3, 4, 13}
SOURCE_QUEUES = {1: 53, 2: 56, 3: 62, 4: 63, 13: 193}
MARKER = "audio-speaker-label-correction-20260830"

payload = json.loads(RESULT.read_text(encoding="utf-8"))
for a in payload["attempts"]:
    if a["item_no"] in AUDIO_ITEMS:
        a["state"] = "audio_error"
        a["audio_error"] = True
payload["correct_items"] = 6
payload["valid_items"] = 8
payload["valid_correct_items"] = 6
payload["excluded_items"] = sorted(AUDIO_ITEMS)
payload["groups"]["課題理解"] = {"correct": 0, "total": 3, "excluded": 3}
payload["groups"]["ポイント理解"] = {"correct": 0, "total": 2, "excluded": 2}
payload["groups"]["文の文法1"] = {"correct": 6, "total": 8, "excluded": 0}
payload["audio_quality_correction"] = {
    "marker": MARKER,
    "reported_by_user": True,
    "reason": "TTS가 대화 내용뿐 아니라 男・女 화자 표기까지 소리 내어 읽음",
    "excluded_items": sorted(AUDIO_ITEMS),
    "score_policy": "음성 오류는 유효 성적과 만기 완료에서 제외",
}
payload["mapping_note"] += " 사용자 보고로 청해 1·2·3·4·13번의 TTS가 화자 표기까지 읽은 오류를 확인하여 유효 성적·만기 완료에서 제외."
RESULT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
test = con.execute("SELECT * FROM tests WHERE id=?", (TID,)).fetchone()
assert test is not None
notes = json.loads(test["notes"])
already = notes.get("audio_quality_correction", {}).get("marker") == MARKER

if not already:
    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(backup_dir / ("before-part2-audio-correction-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")) as backup:
        con.backup(backup)
    with con:
        rows = con.execute("SELECT id,item_no,response_state FROM question_attempts WHERE test_id=?", (TID,)).fetchall()
        by_no = {r["item_no"]: r for r in rows}
        assert set(by_no) == set(range(1, 14))
        for no in AUDIO_ITEMS:
            con.execute(
                """UPDATE question_attempts SET response_state='audio_error',
                   trap_hypothesis=?,trap_confidence='high' WHERE id=?""",
                ("TTS가 男・女 화자 표기까지 읽은 제작 오류. 학습자 오답으로 해석하지 않음.", by_no[no]["id"]),
            )
            qid = SOURCE_QUEUES[no]
            changed = con.execute(
                """UPDATE review_queue SET status='pending',result_state=NULL,result_seconds=NULL
                   WHERE id=? AND status='completed'""", (qid,)
            )
            assert changed.rowcount == 1
        # Item 2 was initially marked wrong; remove only the three reviews spawned by that invalid audio attempt.
        con.execute("DELETE FROM review_queue WHERE attempt_id=?", (by_no[2]["id"],))
        notes["effective_result"] = payload
        notes["audio_quality_correction"] = payload["audio_quality_correction"]
        notes["due_interval_scores"] = {
            "D+3": {"correct": 6, "valid": 8, "excluded": 4, "total": 12},
            "D+1": {"correct": 0, "valid": 0, "excluded": 1, "total": 1},
        }
        con.execute("UPDATE tests SET correct_items=6,notes=? WHERE id=?", (json.dumps(notes, ensure_ascii=False), TID))
        extra = (
            f" [{MARKER}] 사용자 보고: TTS가 화자표기까지 읽음. 청해1·2·3·4·13을 audio_error로 제외하고 "
            "원 만기큐5건 pending 복구, 청해2 파생복습3건 삭제. 유효 문법6/8. 타이머492초와 총학습시간75분21초는 유지."
        )
        con.execute(
            "UPDATE study_sessions SET summary=summary||?,updated_at=CURRENT_TIMESTAMP WHERE session_date='2026-08-30'",
            (extra,),
        )
else:
    assert notes["effective_result"] == payload

states = {r["item_no"]: r["response_state"] for r in con.execute(
    "SELECT item_no,response_state FROM question_attempts WHERE test_id=?", (TID,)
)}
assert all(states[i] == "audio_error" for i in AUDIO_ITEMS)
assert sum(states[i] == "correct" for i in states if i not in AUDIO_ITEMS) == 6
for no, qid in SOURCE_QUEUES.items():
    q = con.execute("SELECT status,result_state,result_seconds FROM review_queue WHERE id=?", (qid,)).fetchone()
    assert q["status"] == "pending" and q["result_state"] is None and q["result_seconds"] is None
item2_attempt = con.execute("SELECT id FROM question_attempts WHERE test_id=? AND item_no=2", (TID,)).fetchone()[0]
assert con.execute("SELECT count(*) FROM review_queue WHERE attempt_id=?", (item2_attempt,)).fetchone()[0] == 0
assert con.execute("SELECT correct_items FROM tests WHERE id=?", (TID,)).fetchone()[0] == 6
assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()

def append_once(filename: str, text: str) -> None:
    path = ROOT / filename
    old = path.read_text(encoding="utf-8")
    marker = f"<!-- {MARKER} -->"
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + marker + "\n" + text.strip() + "\n", encoding="utf-8")
    assert path.read_text(encoding="utf-8").count(marker) == 1

append_once("JLPT_STUDY_LOG.md", """## 2026-08-30 — 만기 복습 2차 청해 음성 오류 정정

- 사용자 보고로 청해 TTS가 대화뿐 아니라 `男：`·`女：` 화자 표기까지 읽은 제작 오류를 확인.
- 청해 1·2·3·4·13번을 `audio_error`로 변경하여 유효 성적과 만기 완료에서 제외. 원래 만기 큐 5건은 `pending`으로 복구.
- 무효 청해 2번에서 생성됐던 D+1·D+3·D+7 복습 3건 삭제. 학습자 청해 오답으로 해석하지 않음.
- 2차 유효 결과는 비청해 **6/8(75.0%)**, 오답 6·9번. 10번 복수 정답 인정은 유지.
- 시험 타이머 492초는 실제 수행시간이므로 유지. 오늘 확인 학습시간 **75분21초** 유지. 공식 점수·합격 확률 변경 없음.
- TTS 구현은 화자별 발화만 분리 재생하도록 수정. 이후 모든 퀴즈는 오른쪽 웹과 JLPT 템플릿을 사용.
""")
append_once("JLPT_ERROR_NOTE.md", """## 2026-08-30 — 만기 복습 2차 청해 오답 정정

- 1·2·3·4·13번은 TTS가 `男：`·`女：`까지 읽은 음성 제작 오류로 전부 제외.
- 2번의 `参加費を払う` 선택은 학습자 약점이나 정상 청해 오답으로 기록하지 않으며 새 복습도 취소.
- 다시 출제할 때는 화자 표기를 음성에서 제거하고 실제 JLPT 청해 형식의 새 변형 문항으로 재시험.
""")

print(json.dumps({
    "corrected": not already,
    "excluded_audio_items": sorted(AUDIO_ITEMS),
    "valid_score": "6/8",
    "restored_due_reviews": 5,
    "deleted_invalid_reviews": 3,
    "pending_due_today": con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date<='2026-08-30'").fetchone()[0],
    "session_minutes": 75,
    "session_remainder_seconds": 21,
    "integrity": "ok",
}, ensure_ascii=False))
con.close()
