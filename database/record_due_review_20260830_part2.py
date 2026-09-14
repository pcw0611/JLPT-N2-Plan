"""Record the corrected effective result for due-review-20260830-part2-13 once."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
TID = "due-review-20260830-part2-13"
RAW = ROOT / "database" / "results" / f"{TID}-submitted.json"
EFFECTIVE = ROOT / "database" / "results" / f"{TID}.json"
submitted = json.loads(RAW.read_text(encoding="utf-8"))
payload = json.loads(EFFECTIVE.read_text(encoding="utf-8"))
attempts = sorted(payload["attempts"], key=lambda x: x["item_no"])
review_dates = payload["review_dates"]

assert submitted["correct_items"] == 9
assert payload["correct_items"] == payload["valid_correct_items"] == 10
assert payload["grading_correction"]["item_no"] == 10
assert next(a for a in attempts if a["item_no"] == 10)["state"] == "correct"
assert [a["item_no"] for a in attempts if a["state"] == "wrong"] == [2, 6, 9]
assert len(attempts) == 13 and not payload["excluded_items"]
assert sum(a["due_interval"] == "D+3" for a in attempts) == 12
assert sum(a["due_interval"] == "D+1" for a in attempts) == 1

traps = {
    2: "마지막에 언급된 참가비 지불을 첫 행동으로 선택. 원문 없는 동일 유형 변형 문항이며 실제 청취 판단 과정은 미확인.",
    6: "현재 문맥에서 과거 부정 ではありませんでした를 선택. 시제 단서와 な형용사 부정 활용을 함께 확인해야 함.",
    9: "ずっと＋지속동작 문맥에서 한 시점의 間に를 선택. 전체 기간 지속을 나타내는 間이 필요함.",
}

notes = {
    "submitted_result": submitted,
    "effective_result": payload,
    "raw_result": RAW.relative_to(ROOT).as_posix(),
    "effective_result_file": EFFECTIVE.relative_to(ROOT).as_posix(),
    "grading_correction": payload["grading_correction"],
    "classification_note": "Self-made due-review variants using JLPT-style templates; separate from official tests. Listening items 1 and 2 are same-type variants because original audio/source text was unavailable.",
    "due_interval_scores": {"D+3": {"correct": 9, "total": 12}, "D+1": {"correct": 1, "total": 1}},
    "session_base_seconds": 67 * 60 + 9,
    "session_increment_seconds": 492,
    "session_total_seconds": 75 * 60 + 21,
    "session_integer_minutes": 75,
    "session_remainder_seconds": 21,
    "timing_note": "Only the 492-second test timer was added. Audio duration, explanation time, and other study time were not inferred.",
}

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
existing = con.execute("SELECT notes FROM tests WHERE id=?", (TID,)).fetchone()
inserted = existing is None

if existing:
    existing_notes = json.loads(existing["notes"])
    if existing_notes.get("audio_quality_correction"):
        print(json.dumps({"test_id": TID, "inserted": False, "superseded_by": "audio_quality_correction"}, ensure_ascii=False))
        con.close()
        raise SystemExit(0)

if inserted:
    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(backup_dir / ("before-due-review-20260830-part2-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")) as backup:
        con.backup(backup)
    with con:
        session = con.execute("SELECT * FROM study_sessions WHERE session_date='2026-08-30'").fetchone()
        assert session and session["verified_minutes"] == 67 and TID not in (session["summary"] or "")
        for a in attempts:
            row = con.execute(
                """SELECT r.*,q.item_type_id FROM review_queue r
                   JOIN question_attempts q ON q.id=r.attempt_id WHERE r.id=?""",
                (a["review_queue_id"],),
            ).fetchone()
            assert row and row["attempt_id"] == a["source_attempt_id"]
            assert row["review_date"] == "2026-08-30" and row["interval_label"] == a["due_interval"]
            assert row["status"] == "pending" and row["item_type_id"] == a["item_type_id"]
            assert a["visited"] and not a["audio_error"] and a["state"] in ("correct", "wrong", "unknown")
        con.execute(
            """INSERT INTO tests
               (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,
                total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (TID,"2026-08-30",payload["title"],"self_made","N3 기반",
             "만기 D+3·D+1 표적 변형; 공식 난이도 미검증",payload["memory_timing"],"multiple_choice",
             13,10,0,0,492,1080,0.2,json.dumps(notes,ensure_ascii=False)),
        )
        for a in attempts:
            cur = con.execute(
                """INSERT INTO question_attempts
                   (test_id,item_no,item_type_id,level_label,response_state,response_seconds,
                    audio_seconds,decision_seconds,play_count,selected_text,correct_text,trap_hypothesis,trap_confidence)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (TID,a["item_no"],a["item_type_id"],"N3 기반",a["state"],a["response_seconds"],
                 a.get("audio_seconds"),a.get("decision_seconds"),a.get("play_count"),a["selected_text"],
                 a["correct_text"],traps.get(a["item_no"]),"medium" if a["item_no"] in traps else None),
            )
            changed = con.execute(
                """UPDATE review_queue SET status='completed',result_state=?,result_seconds=?
                   WHERE id=? AND attempt_id=? AND review_date='2026-08-30' AND interval_label=? AND status='pending'""",
                (a["state"],a["response_seconds"],a["review_queue_id"],a["source_attempt_id"],a["due_interval"]),
            )
            assert changed.rowcount == 1
            if a["state"] in ("wrong", "unknown"):
                for d in review_dates:
                    con.execute(
                        "INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,'pending')",
                        (cur.lastrowid,d["date"],d["interval"]),
                    )
        extra = (
            f" [{TID}] 자체 제작 만기 변형 교정후10/13, D+3 9/12·D+1 1/1, 타이머492초. "
            "10번 복수정답 인정; 정상제출13건 완료, 실제오답3건 새복습9건. "
            "오늘 정확한 확인시간75분21초; DB정수75분, 잔여21초. 해설·기타시간 미가산. 오늘 종료 아님."
        )
        con.execute(
            "UPDATE study_sessions SET verified_minutes=75,summary=summary||?,updated_at=CURRENT_TIMESTAMP WHERE session_date='2026-08-30'",
            (extra,),
        )
else:
    old = json.loads(existing["notes"])
    assert old["submitted_result"] == submitted and old["effective_result"] == payload

saved = con.execute("SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no", (TID,)).fetchall()
assert len(saved) == 13
for a, row in zip(attempts, saved):
    assert row["item_no"] == a["item_no"] and row["response_state"] == a["state"]
    assert row["selected_text"] == a["selected_text"] and row["correct_text"] == a["correct_text"]
for a in attempts:
    row = con.execute("SELECT * FROM review_queue WHERE id=?", (a["review_queue_id"],)).fetchone()
    assert row["attempt_id"] == a["source_attempt_id"] and row["interval_label"] == a["due_interval"]
    assert row["status"] == "completed" and row["result_state"] == a["state"]
reviews = con.execute(
    """SELECT q.item_no,r.review_date,r.interval_label,r.status FROM review_queue r
       JOIN question_attempts q ON q.id=r.attempt_id WHERE q.test_id=?""", (TID,)
).fetchall()
expected = {(i,d["date"],d["interval"]) for i in (2,6,9) for d in review_dates}
assert {(r["item_no"],r["review_date"],r["interval_label"]) for r in reviews} == expected
assert len(reviews) == 9 and all(r["status"] == "pending" for r in reviews)
assert con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-30'").fetchone()[0] == 75
assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()

marker = f"<!-- {TID} -->"


def append_once(filename: str, text: str) -> None:
    path = ROOT / filename
    old = path.read_text(encoding="utf-8")
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + marker + "\n" + text.strip() + "\n", encoding="utf-8")
    assert path.read_text(encoding="utf-8").count(marker) == 1


append_once("JLPT_STUDY_LOG.md", """## 2026-08-30 — 만기 복습 2차: 청해·형용사·문법 13문항

- `due-review-20260830-part2-13` 사용자 실제 제출. 자체 제작 만기 변형 재시험이며 공식 시험·공식 모의고사와 분리.
- 화면 원채점 9/13에서 10번 `ことにしました／ようになりました`가 문맥상 모두 가능한 복수 정답임을 확인. 사용자 답 `ようになりました`를 정답 인정해 **유효 결과 10/13(76.9%)**으로 교정. 원제출도 별도 보존.
- 실제 오답 2·6·9, 모름·미응답·음성 오류·중단 0. 제한 18분 중 **8분12초(492초)**, 시간 초과 없음.
- 만기별 **D+3 9/12(75.0%)**, **D+1 1/1(100%)**. 공식 점수·합격 확률로 환산하지 않음.
- `review_queue_id`·`source_attempt_id`·`due_interval`·문항 유형 13건 대조. 정상 제출 13건만 결과와 함께 완료 처리. 기존 이후 일정·점수·복습 상태 보존.
- 실제 오답 3건만 D+1 **8/31**, D+3 **9/2**, D+7 **9/6**에 새 복습 9건 등록. 10번에는 복습을 등록하지 않음.
- 청해 1·2번은 원문을 확인할 수 없어 동일 유형의 새 변형 문항이며 동일 원문 재시험이 아님. 청해 4문항 모두 audio_error=false, 재생 1·1·1·2회. 음성 길이는 수집되지 않아 추정하지 않음.
- 타이머 492초만 가산: 기존 67분09초에서 오늘 **75분21초**. DB 정수 75분, 잔여 21초 보존. 해설·기타시간 미가산. 오늘 종료 아님.
""")

append_once("JLPT_ERROR_NOTE.md", """## 2026-08-30 — 만기 복습 2차 실제 오답

### 2번 — 첫 행동

**카테고리: 청해 → 과제이해(課題理解) → 준비물·첫 행동**

**원문·번역**  男の人は、この後まず何をしますか。 → 남자는 이 뒤 먼저 무엇을 합니까?

**선택 → 정답**  参加費を払う → **受付で用紙をもらう**.

**대본**  料理教室に参加するなら、三階へ行く前に受付でこの用紙をもらってください。参加費は用紙に名前を書いたあと、三階で払います。

**접속·의미**  `三階へ行く前に` 앞에서 용지를 받고, 이름을 쓴 다음 참가비를 냅니다.

**함정**  참가비가 대화 뒤쪽에 등장하지만 첫 행동이 아닙니다. 원문 없는 동일 유형 변형 문항이며 실제 청취 판단 과정은 미확인입니다.

**유사 표현**  `まず／〜前に`는 선행, `そのあと／〜てから`는 후속 행동입니다.

**예문**  教室へ行く前に、受付で用紙をもらいます。

**복습일**  D+1 8/31 · D+3 9/2 · D+7 9/6.

**풀이 절차**  질문의 `まず` 표시 → 들리는 행동을 순서대로 메모 → 마지막 정보가 아니라 최초 미완료 행동 선택.

**정답 직전 체크**  이 행동은 실제로 가장 먼저 해야 하는가?

### 6번 — な형용사 현재 부정

**카테고리: 문법 → 문법형식 판단 → な형용사 현재 부정**

**원문·번역**  この道は夜になると、あまり安全（　）。 → 이 길은 밤이 되면 별로 안전하지 않습니다.

**선택 → 정답·완성문**  ではありませんでした → **ではありません** / この道は夜になると、あまり安全ではありません。

**접속·의미**  な형용사 현재 부정은 어간＋`ではありません`입니다.

**함정**  `夜になると`는 반복되는 일반 상태이며 과거 단서가 없습니다. `ではありませんでした`는 과거 부정입니다.

**유사 활용**  安全です / 安全ではありません / 安全でした / 安全ではありませんでした.

**예문**  この場所はあまり静かではありません。

**복습일**  D+1 8/31 · D+3 9/2 · D+7 9/6.

**풀이 절차**  기본형 `安全だ` 확인 → 시제 단서 탐색 → 과거 단서가 없으면 현재 부정 선택.

**정답 직전 체크**  문장에 과거를 요구하는 표현이 있는가?

### 9번 — 間／間に

**카테고리: 문법 → 문법형식 판단 → 間·지속 기간**

**원문·번역**  母が料理をしている（　）、私はずっと台所を掃除していました。 → 어머니가 요리하는 동안 나는 계속 부엌을 청소했습니다.

**선택 → 정답·완성문**  間に → **間** / 母が料理をしている間、私はずっと台所を掃除していました。

**접속·의미**  `間`는 기준 기간과 주절 동작이 계속 겹치고, `間に`는 그 기간 안의 한 시점에 사건이 발생하거나 행동이 완료됩니다.

**함정**  `ずっと＋掃除していました`가 전체 기간 지속을 명시하므로 `間に`가 아니라 `間`입니다.

**유사 문형**  母が料理をしている間に、買い物に行ってきました는 그 사이 완료된 행동이라 `間に`입니다.

**예문**  夏休みの間、毎日日本語を勉強しました。

**복습일**  D+1 8/31 · D+3 9/2 · D+7 9/6.

**풀이 절차**  주절에서 `ずっと`·진행형 확인 → 전체 기간 지속이면 間 → 한 번 발생·완료면 間に.

**정답 직전 체크**  주절 행동이 기간 내내 계속되는가, 한 시점에 끝나는가?

### 채점 정정 — 10번

`健康のため、毎朝三十分歩く（　）。`는 `ことにしました`(걷기로 결정했다)와 `ようになりました`(걷는 습관이 생겼다)가 모두 자연스럽습니다. 추가 문맥이 없어 구별할 수 없으므로 사용자 답 `ようになりました`를 정답 인정했습니다. 오답 및 새 복습 대상이 아닙니다.
""")

result = {
    "test_id": TID, "inserted": inserted, "submitted_correct": 9,
    "effective_correct": 10, "attempts": len(saved), "completed_due_reviews": 13,
    "new_reviews": len(reviews), "pending_due_today": con.execute(
        "SELECT count(*) FROM review_queue WHERE status='pending' AND review_date<='2026-08-30'"
    ).fetchone()[0], "pending_2026_08_31": con.execute(
        "SELECT count(*) FROM review_queue WHERE status='pending' AND review_date='2026-08-31'"
    ).fetchone()[0], "session_minutes_field": 75, "session_remainder_seconds": 21,
    "integrity": "ok",
}
print(json.dumps(result, ensure_ascii=False))
con.close()
