"""Record the submitted N2 grammar 026-035 immediate check exactly once."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TID = "n2-grammar-026-035-check-20260831"
DATE = "2026-08-31"
RAW = ROOT / "database" / "results" / f"{TID}.json"
payload = json.loads(RAW.read_text(encoding="utf-8"))
attempts = payload["responses"]
review_dates = [("D+1", "2026-09-01"), ("D+3", "2026-09-03"), ("D+7", "2026-09-07")]

assert payload["testId"] == TID and payload["date"] == DATE
assert payload["total"] == len(attempts) == 12
assert (payload["correct"], payload["wrong"], payload["unknown"], payload["unanswered"]) == (10, 2, 0, 0)
assert payload["elapsedSeconds"] == 334
assert [a["itemNo"] for a in attempts if a["responseState"] == "wrong"] == [3, 4]
assert round(sum(a["responseSeconds"] for a in attempts), 1) == 334.2

trap_hypotheses = {
    3: ("〜ことに와 〜ことなく을 혼동. 一度も와 뒤의 계속 동작은 '하지 않고'의 ことなく을 요구한다.", "high"),
    4: ("〜ことではない를 선택. 이 문맥은 '그럴 필요가 없다'는 조언이므로 V辞書形＋ことはない이다.", "high"),
}
notes = {
    "submitted_result": payload,
    "raw_result": RAW.relative_to(ROOT).as_posix(),
    "classification_note": "강의 직후 자체 제작 JLPT식 선택형 확인. 공식 기출·공식 모의고사·지연 유지율과 분리.",
    "review_dates": [{"interval": i, "date": d} for i, d in review_dates],
    "timing_note": "시험 타이머 334초만 가산. 강의·Anki·해설 시간과 중복하지 않음.",
    "stamina_note": "전반 4/6 186초, 후반 6/6 148초. 후반 정확도와 속도가 모두 개선됐으나 12문항 소표본.",
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
    backup_path = backup_dir / ("before-n2-026-035-result-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")
    with sqlite3.connect(backup_path) as backup:
        con.backup(backup)
    with con:
        session = con.execute("SELECT * FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()
        assert session is not None and session["verified_minutes"] == 252
        con.execute(
            """INSERT INTO tests
               (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,
                response_format,total_items,correct_items,unknown_items,unanswered_items,
                elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (TID, DATE, "N2 문법 026~035 강의 직후 확인 12문항", "self_made", "N2",
             "강의 직후 확인; 공식 난이도 미검증", "immediate_recognition", "multiple_choice",
             12, 10, 0, 0, 334, None, 0.1, json.dumps(notes, ensure_ascii=False)),
        )
        for a in attempts:
            item_type = "grammar_form" if a["itemNo"] <= 10 else ("sentence_composition" if a["itemNo"] == 11 else "text_grammar")
            trap, confidence = trap_hypotheses.get(a["itemNo"], (None, None))
            cur = con.execute(
                """INSERT INTO question_attempts
                   (test_id,item_no,item_type_id,level_label,response_state,response_seconds,
                    selected_text,correct_text,trap_hypothesis,trap_confidence)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (TID, a["itemNo"], item_type, "N2", a["responseState"], a["responseSeconds"],
                 a["selectedText"], a["correctText"], trap, confidence),
            )
            if a["responseState"] in ("wrong", "unknown"):
                for interval, review_date in review_dates:
                    con.execute(
                        "INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,'pending')",
                        (cur.lastrowid, review_date, interval),
                    )
        extra = (
            f" [{TID}] 자체 제작 문법026~035 강의 직후 확인 10/12, 오답3·4, 모름0, 미응답0, "
            "타이머334초(5분34초). 정확 누적252분57.009초에서 258분31.009초; DB정수252→258분. "
            "오답2건 D+1·D+3·D+7 6건 등록. 공식 점수·합격확률 보존. 오늘 종료 아님."
        )
        con.execute(
            "UPDATE study_sessions SET verified_minutes=258,summary=summary||?,updated_at=CURRENT_TIMESTAMP WHERE session_date=?",
            (extra, DATE),
        )
else:
    assert json.loads(existing["notes"])["submitted_result"] == payload

saved = con.execute("SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no", (TID,)).fetchall()
reviews = con.execute(
    """SELECT q.item_no,r.review_date,r.interval_label FROM review_queue r
       JOIN question_attempts q ON q.id=r.attempt_id WHERE q.test_id=?""", (TID,)
).fetchall()
assert len(saved) == 12 and len(reviews) == 6
assert {(r["item_no"], r["review_date"], r["interval_label"]) for r in reviews} == {
    (n, d, i) for n in (3, 4) for i, d in review_dates
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

append_once("JLPT_STUDY_LOG.md", """
## 2026-08-31 — N2 문법 026~035 강의 직후 확인시험

- `n2-grammar-026-035-check-20260831`: 다락원 문법 026~035 강의 직후 자체 제작 JLPT식 선택형 확인. 공식 기출·공식 모의고사·지연 유지율과 분리.
- 결과 **10/12(83.3%)**, 오답 3·4, `分からない` 0, 미응답 0. 타이머 **334초(5분34초)**.
- 유형별: `文の文法1` **8/10**, `文の文法2` **1/1**, `文章の文法` **1/1**. 전반 4/6·186초, 후반 6/6·148초로 이번 소표본에서는 후반 저하 없음.
- 오답은 `〜ことなく`을 `〜ことに`로 선택한 부정 동반 표현 혼동, `〜ことはない`를 `〜ことではない`로 선택한 필요 없음 표현 혼동.
- 오답 2건만 D+1 **9/1**, D+3 **9/3**, D+7 **9/7**에 등록: 총 6건. 기존 미래 일정 보존.
- 기존 정확 누적 252분57.009초에 시험 5분34초를 더해 오늘 **258분31.009초**. DB 정수 **258분**. 해설 시간 미가산, 오늘 종료 아님.
- 강의 직후 재인 결과이므로 공식 점수·장기 유지율·합격 가능성은 변경하지 않음.
""")

append_once("JLPT_ERROR_NOTE.md", """
## 2026-08-31 — N2 문법 026~035 확인시험 오답

### 3번 — 〜ことなく

**카테고리: 문법 → 文の文法1 → 부정 상태로 동작 계속**

**원문·번역**

`選手は一度も弱音を吐く（　）、最後まで走り続けた。`  
선수는 한 번도 약한 소리를 하지 않고 끝까지 계속 달렸다.

**선택 → 정답·완성**

`ことに` → **`ことなく`**  
`選手は一度も弱音を吐くことなく、最後まで走り続けた。`

**접속·핵심 의미**

V辞書形＋ことなく: 어떤 행동을 하지 않은 채 다른 행동을 계속함. `〜ないで`보다 문어적입니다.

**함정·유사 문형 차이**

`〜ことに`는 `驚いたことに`처럼 뒤 사실에 대한 감정·평가를 나타냅니다. 여기서는 `一度も`와 `走り続けた`가 부정 상태의 지속을 요구합니다.

**예문** `彼は休むことなく働き続けた。`

**풀이 절차** `一度も` 확인 → 뒤의 계속 동작 확인 → “하지 않고”이면 `ことなく` 선택.

**다음 복습일** D+1 9/1 · D+3 9/3 · D+7 9/7.

### 4번 — 〜ことはない

**카테고리: 문법 → 文の文法1 → 필요 없음·조언**

**원문·번역**

`まだ十分時間があるから、そんなに急ぐ（　）。`  
아직 시간이 충분히 있으니 그렇게 서두를 필요는 없다.

**선택 → 정답·완성**

`ことではない` → **`ことはない`**  
`まだ十分時間があるから、そんなに急ぐことはない。`

**접속·핵심 의미**

V辞書形＋ことはない: 그렇게 할 필요가 없다고 조언하거나 판단함.

**함정·유사 문형 차이**

`ことではない`는 이 문장의 고정 문형이 아닙니다. `〜たことがない`는 경험 부정이고, `〜ことにはならない`는 어떤 결과로 성립하지 않음을 뜻합니다.

**예문** `心配することはない。きっとうまくいく。`

**풀이 절차** 앞의 안심 근거 확인 → “할 필요 없다”로 바꿔 읽기 → V辞書形＋ことはない 선택.

**다음 복습일** D+1 9/1 · D+3 9/3 · D+7 9/7.
""")

result = {
    "test_id": TID, "inserted": inserted, "attempts": len(saved), "reviews": len(reviews),
    "session_minutes": con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date=?", (DATE,)).fetchone()[0],
    "pending": dict(con.execute("SELECT review_date,count(*) FROM review_queue WHERE status='pending' GROUP BY review_date ORDER BY review_date").fetchall()),
    "integrity": "ok",
}
print(json.dumps(result, ensure_ascii=False))
con.close()
