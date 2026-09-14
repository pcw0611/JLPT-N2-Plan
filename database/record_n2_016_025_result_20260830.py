"""Record the N2 grammar 016-025 lecture check result once, then preserve all prior state."""

import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TID = "n2-grammar-016-025-check-20260830"
ATTACHMENT = Path(r"C:\Users\pcw06\.codex\attachments\f23d6998-73dd-49c0-af08-b7b889c97cec\pasted-text.txt")
RAW = ROOT / "database" / "results" / f"{TID}.json"
if not RAW.exists():
    RAW.write_text(ATTACHMENT.read_text(encoding="utf-8"), encoding="utf-8")
payload = json.loads(RAW.read_text(encoding="utf-8"))
attempts = payload["attempts"]
review_dates = [
    {"interval": "D+1", "date": "2026-08-31"},
    {"interval": "D+3", "date": "2026-09-02"},
    {"interval": "D+7", "date": "2026-09-06"},
]

assert payload["test_id"] == TID
assert payload["test_date"] == "2026-08-30"
assert payload["total_items"] == len(attempts) == 12
assert payload["correct_items"] == 9
assert payload["unknown_items"] == 0
assert payload["unanswered_items"] == 0
assert payload["elapsed_seconds"] == 443
assert [a["item_no"] for a in attempts if a["state"] == "wrong"] == [2, 4, 11]
assert all(a["state"] in ("correct", "wrong", "unknown", "unanswered") for a in attempts)

trap_hypotheses = {
    2: ("かねる(하기 어렵다)와 かねない(좋지 않은 가능성)를 혼동한 것으로 보임. "
        "정중한 창구 답변이므로 お答えしかねます가 맞음.", "high"),
    4: ("관점·평가를 나타내는 からいうと 대신 이유를 근거로 결론을 제한하는 "
        "からといって를 선택함. 観点이 관점 기준임을 놓친 것으로 보임.", "medium"),
    11: ("문장 배열에서 끝 표현 とは限らない를 먼저 고정하지 못하고, ★ 위치에 "
        "使うのが를 배치함. 마지막 결론의 구조를 먼저 잡아야 함.", "high"),
}

notes = {
    "submitted_result": payload,
    "raw_result": RAW.relative_to(ROOT).as_posix(),
    "classification_note": "강의 직후 자체 제작 선택형 확인시험. 실제 JLPT식 문법형식·문장배열·글의 문법 템플릿을 사용했지만 공식 기출·공식 모의고사·D+1 유지율과 분리.",
    "review_dates": review_dates,
    "timing_note": "443초(7분23초) 시험 타이머만 추가. 강의 26분과 해설 읽기 시간은 이 시험에 포함하거나 재추정하지 않음.",
    "interpretation_note": "9/12는 강의 직후 선택형 재인 결과이며 합격률·장기 유지율로 직접 환산하지 않음.",
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
    with sqlite3.connect(backup_dir / ("before-n2-016-025-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")) as backup:
        con.backup(backup)
    with con:
        session = con.execute("SELECT * FROM study_sessions WHERE session_date='2026-08-30'").fetchone()
        assert session is not None and session["verified_minutes"] == 101
        con.execute(
            """INSERT INTO tests
               (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,
                response_format,total_items,correct_items,unknown_items,unanswered_items,
                elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                TID, "2026-08-30", payload["title"], "self_made", "N2",
                "강의 직후 확인; 공식 난이도 미검증", "immediate_recognition",
                "multiple_choice", 12, 9, 0, 0, 443, 720, 0.1,
                json.dumps(notes, ensure_ascii=False),
            ),
        )
        for a in attempts:
            trap, confidence = trap_hypotheses.get(a["item_no"], (None, None))
            cur = con.execute(
                """INSERT INTO question_attempts
                   (test_id,item_no,item_type_id,level_label,response_state,response_seconds,
                    selected_text,correct_text,trap_hypothesis,trap_confidence)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (
                    TID, a["item_no"], a["item_type_id"], "N2", a["state"],
                    a.get("response_seconds"), a.get("selected_text"),
                    a.get("correct_text"), trap, confidence,
                ),
            )
            if a["state"] in ("wrong", "unknown"):
                for d in review_dates:
                    con.execute(
                        "INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,'pending')",
                        (cur.lastrowid, d["date"], d["interval"]),
                    )
        extra = (
            f" [{TID}] 자체 제작 JLPT식 문법 016~025 강의 직후 확인 9/12, 오답2·4·11·모름0, "
            "시험 타이머443초(7분23초). 기존 101분에 DB 정수 7분을 가산하여 오늘 108분, 잔여23초 보존. "
            "오답 3건 새 D+1·D+3·D+7 등록. 공식 시험·기존 점수·합격확률 보존. 오늘 종료 아님."
        )
        con.execute(
            """UPDATE study_sessions SET verified_minutes=108,summary=summary||?,updated_at=CURRENT_TIMESTAMP
               WHERE session_date='2026-08-30'""",
            (extra,),
        )
else:
    assert json.loads(existing["notes"])["submitted_result"] == payload

saved = con.execute("SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no", (TID,)).fetchall()
assert len(saved) == 12
reviews = con.execute(
    """SELECT q.item_no,r.review_date,r.interval_label FROM review_queue r
       JOIN question_attempts q ON q.id=r.attempt_id WHERE q.test_id=?""",
    (TID,),
).fetchall()
assert len(reviews) == 9
assert {(r["item_no"], r["review_date"], r["interval_label"]) for r in reviews} == {
    (n, d["date"], d["interval"]) for n in (2, 4, 11) for d in review_dates
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


study = """## 2026-08-30 — N2 문법 016~025 강의 후 확인시험

- `n2-grammar-016-025-check-20260830`: 다락원 강의 문형 016~025를 대상으로 한 자체 제작 선택형 확인. 실제 JLPT식 `文の文法1`·`文の文法2`·`文章の文法` 템플릿을 사용했지만 공식 기출·공식 모의고사와 분리.
- 결과 **9/12(75.0%)**, 오답 2·4·11, `分からない` 0, 미응답 0. 시험 타이머 **443초(7분23초)**, 제한 12분, 시간 초과 없음.
- 유형별: `文の文法1` 8/10, `文の文法2` 0/1, `文章の文法` 1/1. 문장 배열 1문항은 별도 소표본으로 해석.
- 오답은 `〜かねる`와 `〜かねない`의 기능 혼동, `〜からいうと`와 `〜からといって`의 관점·이유 구별, `とは限らない` 문장 배열의 끝 구조 미고정. 각각 오답노트에 원문·번역·접속·함정·유사 문형·예문·풀이 절차를 남김.
- 오답 3건만 D+1 **8/31**, D+3 **9/2**, D+7 **9/6**에 등록: 9건. 기존 점수·복습 상태·이후 일정 보존.
- 시간: 기존 DB 기준 101분에 시험 7분23초를 가산하여 DB 정수 **108분**, 잔여 23초를 요약에 보존. 강의 26분은 이미 별도 기록되어 중복 가산하지 않았고, 해설 시간은 미가산.
- 강의 직후 재인 결과이므로 공식 N2 점수, 지연 유지율, 합격 확률은 변경하지 않음. 오늘 학습 종료 아님.
"""
append_once("JLPT_STUDY_LOG.md", study)

error = """## 2026-08-30 — N2 문법 016~025 강의 후 확인시험 오답

### 2번 — 〜かねる

**카테고리: 문법 → 문법형식 판단 → 정중한 거절·곤란**

**문제 원문**

個人情報に関するご質問には、こちらでは（　）。

**번역**

개인정보에 관한 질문에는 이쪽에서 답변드리기 어렵습니다.

**선택 → 정답·완성 문장**

お答えしかねません → **お答えしかねます**

個人情報に関するご質問には、こちらではお答えしかねます。

**접속·의미**

Vます어간＋かねる: 사정상 하기 어렵거나 할 수 없다는 뜻의 정중한 거절입니다. `答えます`에서 `ます`를 떼어 `答え＋かねます`로 만듭니다.

**함정**

`かねない`는 좋지 않은 일이 일어날 가능성, `かねる`는 화자가 행동하기 곤란하다는 뜻입니다. `お答えしかねません`은 이 문맥의 정중한 거절이 되지 않습니다.

**유사 문형·예문**

`その要求には応じかねます`(그 요구에는 응하기 어렵습니다). `〜ことができません`보다 공식적이고 완곡합니다.

**다음번 풀이 절차**

1. 주어가 창구·회사인지 확인합니다. 2. 빈칸이 행동 불가인지 나쁜 결과 가능성인지 판별합니다. 3. 정중한 거절이면 Vます어간＋かねます를 고릅니다.

**정답 직전 체크**

“할 수도 있다”가 아니라 “답변하기 어렵다”인가?

**다음 복습일**

D+1 2026-08-31 · D+3 2026-09-02 · D+7 2026-09-06.

### 4번 — 〜からいうと

**카테고리: 문법 → 문법형식 판단 → 관점에서의 평가**

**문제 원문**

環境保護の観点（　）、この計画にはまだ改善の余地がある。

**번역**

환경 보호의 관점에서 말하면 이 계획에는 아직 개선의 여지가 있습니다.

**선택 → 정답·완성 문장**

からといって → **からいうと**

環境保護の観点からいうと、この計画にはまだ改善の余地がある。

**접속·의미**

N＋からいうと／からいって: 특정 관점·측면을 기준으로 평가합니다. `観点` 자체가 판단 기준임을 보여줍니다.

**함정**

`からといって`는 “~라고 해서”라는 이유 하나만으로 결론내리는 것을 부정할 때 씁니다. 여기서는 뒤에 부정 결론이 아니라 환경 관점의 평가가 이어집니다.

**유사 문형·예문**

`費用の面からいうと、A案のほうが現実的だ`(비용 면에서 보면 A안이 현실적이다). `からすると`는 관찰된 근거에서 추측할 때 중심적으로 씁니다.

**다음 복습일**

D+1 2026-08-31 · D+3 2026-09-02 · D+7 2026-09-06.

### 11번 — 문장 배열 `〜からといって`

**카테고리: 문법 → 문장 배열 → 이유에 따른 단정 부정**

**문제 원문**

便利だからといって、＿＿＿ ＿＿＿ ★ ＿＿＿。

**번역**

편리하다고 해서 언제나 사용하는 것이 옳다고는 할 수 없습니다.

**선택 → 정답**

`使うのが` → **`正しいとは`**

완성: `便利だからといって、いつでも使うのが正しいとは限らない。`

**접속·의미**

`〜からといって＋とは限らない`: 앞의 이유만으로 항상 성립한다고 단정할 수 없다는 뜻입니다. `とは限らない`를 끝 표현으로 한 덩어리로 잡아야 합니다.

**함정**

배열 문제에서 먼저 `とは限らない`를 고정하지 않고 의미가 익숙한 `使うのが`를 ★에 넣은 것이 핵심 오류입니다.

**유사 문형·예문**

`有名だからといって、品質がいいとは限らない。`(유명하다고 해서 품질이 좋은 것은 아니다.) `〜わけではない`는 전면 부정이 아님, `〜とは限らない`는 항상 그렇지는 않음에 초점을 둡니다.

**다음 복습일**

D+1 2026-08-31 · D+3 2026-09-02 · D+7 2026-09-06.

이번 시험은 강의 직후 재인이므로 9/12를 공식 N2 점수나 지연 유지율로 환산하지 않습니다. 시험 타이머 443초만 기록했습니다.
"""
append_once("JLPT_ERROR_NOTE.md", error)

result = {
    "test_id": TID,
    "inserted": inserted,
    "attempts": len(saved),
    "new_reviews": len(reviews),
    "session_minutes": con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-30'").fetchone()[0],
    "pending_due_today": con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date<='2026-08-30'").fetchone()[0],
    "pending_2026_08_31": con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date='2026-08-31'").fetchone()[0],
    "integrity": "ok",
}
print(json.dumps(result, ensure_ascii=False))
con.close()
