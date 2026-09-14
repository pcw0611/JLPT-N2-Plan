"""Record the immediate selection-based correction once."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TID = "n2-grammar-009-015-correction-20260830"
RAW = ROOT / "database" / "results" / f"{TID}.json"
payload = json.loads(RAW.read_text(encoding="utf-8"))
attempts = payload["attempts"]
review_dates = [
    {"interval": "D+1", "date": "2026-08-31"},
    {"interval": "D+3", "date": "2026-09-02"},
    {"interval": "D+7", "date": "2026-09-06"},
]

assert payload["test_id"] == TID
assert payload["test_date"] == "2026-08-30"
assert payload["total_items"] == len(attempts) == 7
assert payload["correct_items"] == 6
assert payload["wrong_items"] == 1
assert payload["unknown_items"] == 0
assert payload["elapsed_seconds"] == 69
assert [a["item_no"] for a in attempts if a["state"] == "wrong"] == [1]
assert all(a["state"] in ("correct", "wrong", "unknown") for a in attempts)

notes = {
    "submitted_result": payload,
    "raw_result": RAW.relative_to(ROOT).as_posix(),
    "classification_note": "Immediate selection-based correction after explanations. JLPT-style item template, but self-made and not an official item, independent diagnostic, or D+1 retention test.",
    "review_dates": review_dates,
    "session_base_seconds": 56 * 60 + 5,
    "session_increment_seconds": 69,
    "session_total_seconds": 57 * 60 + 14,
    "session_integer_minutes": 57,
    "session_remainder_seconds": 14,
    "timing_note": "Only the 69-second quiz timer was added. Explanation and other study time were not inferred.",
    "interpretation_note": "6/7 shows immediate recognition improved after feedback. It does not replace the earlier 0/10 result or establish delayed retention.",
}

db = ROOT / "database" / "jlpt_learning.db"
con = sqlite3.connect(db)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
existing = con.execute("SELECT notes FROM tests WHERE id=?", (TID,)).fetchone()
inserted = existing is None

if inserted:
    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(backup_dir / ("before-n2-correction-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")) as backup:
        con.backup(backup)
    with con:
        session = con.execute("SELECT * FROM study_sessions WHERE session_date='2026-08-30'").fetchone()
        assert session is not None and session["verified_minutes"] == 56
        assert TID not in (session["summary"] or "")
        con.execute(
            """INSERT INTO tests
               (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,
                response_format,total_items,correct_items,unknown_items,unanswered_items,
                elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                TID, "2026-08-30", payload["title"], "self_made", "N2",
                "해설 직후 표적 교정; 공식 난이도 미검증", "immediate_correction",
                "multiple_choice", 7, 6, 0, 0, 69, None, 0.05,
                json.dumps(notes, ensure_ascii=False),
            ),
        )
        for a in attempts:
            trap = None
            confidence = None
            if a["state"] == "wrong":
                trap = (
                    "理解しないかぎり를 의도한 것으로 보이나, 빈칸 앞이 理解し로 끝나므로 "
                    "ないかぎり를 넣으면 理解しないかぎり가 된다. 그러나 뒤의 点がある는 "
                    "조건 결과가 아니라 '이해하기 어려운 점이 있다'는 명사수식이 필요함. "
                    "선택 결과만 확인되며 실제 사고 과정은 미확인."
                )
                confidence = "medium"
            cur = con.execute(
                """INSERT INTO question_attempts
                   (test_id,item_no,item_type_id,level_label,response_state,response_seconds,
                    selected_text,correct_text,trap_hypothesis,trap_confidence)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (TID, a["item_no"], "grammar_form", "N2", a["state"], None,
                 a["selected_text"], a["correct_text"], trap, confidence),
            )
            if a["state"] in ("wrong", "unknown"):
                for d in review_dates:
                    con.execute(
                        "INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,?)",
                        (cur.lastrowid, d["date"], d["interval"], "pending"),
                    )
        extra = (
            f" [{TID}] N2 문법009~015 해설 직후 선택형 교정 6/7, 오답1·모름0, 타이머69초. "
            "기존 확인56분05초+1분09초=57분14초; DB 정수57분, 잔여14초 보존. "
            "새복습3건, 기존 0/10 결과·일정·점수·합격확률 보존. 오늘 종료 아님."
        )
        con.execute(
            """UPDATE study_sessions SET verified_minutes=57,summary=summary||?,updated_at=CURRENT_TIMESTAMP
               WHERE session_date='2026-08-30'""",
            (extra,),
        )
else:
    assert json.loads(existing["notes"])["submitted_result"] == payload

saved = con.execute("SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no", (TID,)).fetchall()
assert len(saved) == 7
reviews = con.execute(
    """SELECT q.item_no,r.review_date,r.interval_label
       FROM review_queue r JOIN question_attempts q ON q.id=r.attempt_id
       WHERE q.test_id=?""",
    (TID,),
).fetchall()
assert len(reviews) == 3
assert {(r["item_no"], r["review_date"], r["interval_label"]) for r in reviews} == {
    (1, d["date"], d["interval"]) for d in review_dates
}
assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()

marker = f"<!-- {TID} -->"


def append_once(filename: str, text: str) -> None:
    path = ROOT / filename
    old = path.read_text(encoding="utf-8")
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + marker + "\n" + text.strip() + "\n", encoding="utf-8")
    assert path.read_text(encoding="utf-8").count(marker) == 1


study = """## 2026-08-30 — N2 문법 009~015 선택형 교정

- `n2-grammar-009-015-correction-20260830`: 오답 해설 직후 자체 제작 선택형 교정. JLPT 문법형식 판단 템플릿을 사용했으나 공식 기출·공식 시험·독립 진단·D+1 유지율과 분리.
- 결과 **6/7(85.7%)**, 오답 1, 모름 0, 미응답 0. 타이머 **69초**. 문항별 시간과 별도 제한시간은 수집되지 않음.
- 정답: 〜か〜ないかのうちに, 〜かいがある, 〜ないかぎり, 〜かける, 〜がち, 〜かというと. 미고정: **〜がたい**.
- 해설 직후 선택형 재인에서 6개를 구별했으므로 즉시 교정 반응은 확인. 앞선 냉각 확인 0/10을 정정하거나 장기 기억·약점 해결로 처리하지 않음.
- 오답 1번만 새 D+1 **8/31**, D+3 **9/2**, D+7 **9/6**에 등록: 3건. 기존 일정·점수·복습 상태 보존.
- 시간: 기존 확인 56분05초+시험 1분09초=오늘 **57분14초**. DB 정수 57분, 잔여14초 보존. 해설·기타 학습시간 미가산.
- 공식 N2 점수·합격 확률·숙달 스냅샷은 변경하지 않음. 오늘 학습 종료 아님.
"""
append_once("JLPT_STUDY_LOG.md", study)

error = """## 2026-08-30 — N2 문법 009~015 선택형 교정 오답

### 1번 — 〜がたい

**카테고리: 문법 → 문법형식 판단 → 심리적·추상적 어려움**

**문제 원문**

その説明には理解し（　）点がある。

1. がたい
2. がち
3. かける
4. ないかぎり

**번역**

그 설명에는 이해하기 어려운 점이 있다.

**선택 → 정답·완성 문장**

ないかぎり → **がたい**

その説明には理解しがたい点がある。

**접속·의미**

Vます語幹＋がたい: 능력 부족이라기보다 심리적·추상적으로 받아들이거나 실행하기 매우 어렵다는 뜻입니다. 理解します의 ます를 떼어 理解し＋がたい가 됩니다.

**함정·선택 분석**

`理解しないかぎり` 자체는 “이해하지 않는 한”이라는 조건절이지만, 그 뒤에는 조건의 결과가 와야 합니다. 여기서는 바로 `点`을 수식해야 하므로 `理解しがたい点`이 필요합니다. 선택 결과만 확인되며 실제 사고 과정은 미확인입니다.

**유사 문형 차이**

- `〜がたい`: 심리적·추상적으로 하기 어렵다 — `信じがたい事実`
- `〜ないかぎり`: ~하지 않는 한 — `説明を聞かないかぎり、理解できない`
- `〜にくい`: 물리적·기능적으로 하기 어려운 경우에도 널리 사용 — `読みにくい字`

**추가 예문**

彼の行動は受け入れがたい。 → 그의 행동은 받아들이기 어렵다.

**다음번 풀이 절차**

1. 빈칸 뒤가 명사인지 확인한다.
2. 명사수식이면 앞에서 의미가 완성되어야 한다.
3. `理解し＋がたい＋点`으로 연결한다.

**정답 직전 체크**

빈칸 뒤의 `点`을 자연스럽게 수식하는가? “이해하지 않는 한 점”이 아니라 “이해하기 어려운 점”인가?

**다음 복습일**

D+1 2026-08-31 · D+3 2026-09-02 · D+7 2026-09-06. 새 교정 시도에 연결해 등록, 기존 일정 보존.

문항별 체류시간은 수집되지 않음. 전체 타이머만 69초.
"""
append_once("JLPT_ERROR_NOTE.md", error)

result = {
    "test_id": TID,
    "inserted": inserted,
    "attempts": len(saved),
    "new_reviews": len(reviews),
    "session_minutes": con.execute(
        "SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-30'"
    ).fetchone()[0],
    "pending_due_today": con.execute(
        "SELECT count(*) FROM review_queue WHERE status='pending' AND review_date<='2026-08-30'"
    ).fetchone()[0],
    "pending_2026_08_31": con.execute(
        "SELECT count(*) FROM review_queue WHERE status='pending' AND review_date='2026-08-31'"
    ).fetchone()[0],
    "integrity": "ok",
}
print(json.dumps(result, ensure_ascii=False))
con.close()
