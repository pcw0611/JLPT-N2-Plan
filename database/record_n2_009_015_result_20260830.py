"""Persist the submitted N2 grammar 009-015 check once and create reviews."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TID = "n2-grammar-009-015-check-20260830"
RAW = ROOT / "database" / "results" / f"{TID}.json"
payload = json.loads(RAW.read_text(encoding="utf-8"))

assert payload["test_id"] == TID
assert payload["test_date"] == "2026-08-30"
assert payload["total_items"] == 10
assert payload["correct_items"] == 0
assert payload["wrong_items"] == 9
assert payload["unknown_items"] == 1
assert payload["unanswered_items"] == 0
assert payload["elapsed_seconds"] == 425
assert payload["timed_out"] is False
attempts = payload["attempts"]
assert len(attempts) == 10
assert [a["item_no"] for a in attempts if a["state"] == "wrong"] == list(range(1, 10))
assert [a["item_no"] for a in attempts if a["state"] == "unknown"] == [10]
assert all(a["visited"] for a in attempts)

extra_types = {
    "sentence_composition": (
        "grammar", "문장 배열", "文の文法2", 1,
        "공식 JLPT 문제 형식명. 본 문항은 자체 제작이며 공식 기출이 아님.",
    ),
    "text_grammar": (
        "grammar", "글의 문법", "文章の文法", 1,
        "공식 JLPT 문제 형식명. 본 문항은 자체 제작이며 공식 기출이 아님.",
    ),
}

feedback = {
    1: dict(
        ko="수업 종료 벨이 울리자마자 학생들은 교실을 뛰쳐나갔다.",
        rule="Vる＋か＋Vない＋かのうちに: 앞 동작이 일어나는 것과 거의 동시에 뒤 동작이 이어집니다.",
        trap="鳴ったかぎり는 이 문맥의 ‘울리자마자’를 만들지 못합니다. かぎり는 조건·범위가 유지되는 동안을 나타냅니다.",
        diff="〜たとたん도 직후지만, 〜か〜ないかのうちに는 했는지 안 했는지 모를 정도의 밀착된 동시성을 강조합니다.",
        ex="電車が止まるか止まらないかのうちに、乗客が立ち上がった。 → 전철이 멈추자마자 승객이 일어섰다.",
        procedure="앞뒤 사건이 ‘거의 동시에’인지 먼저 확인하고, 반복되는 VるかVないか 형태를 찾으세요.",
        check="‘~하자마자’인가, ‘~하는 한’인가?",
    ),
    2: dict(
        ko="매일 발음을 연습한 보람이 있어서 전보다 자연스럽게 말할 수 있게 되었다.",
        rule="Vた／Nの＋かいがある: 노력이나 행위의 결과로 보람 있는 성과가 나타났음을 말합니다.",
        trap="かけ는 시작했지만 끝내지 않은 상태입니다. 뒤에 실제 향상이라는 좋은 결과가 있으므로 かいがあって가 맞습니다.",
        diff="〜かいもなく은 노력했지만 보람이 없었을 때, 〜かけ는 동작이 미완료일 때 씁니다.",
        ex="毎日勉強したかいがあって、試験に合格した。 → 매일 공부한 보람이 있어 시험에 합격했다.",
        procedure="앞에 노력, 뒤에 좋은 결과가 있는지 찾은 뒤 ‘보람’ 문형을 고르세요.",
        check="노력→성과인가, 시작→미완료인가?",
    ),
    3: dict(
        ko="몸이 건강한 한 이 일을 계속하고 싶다고 생각한다.",
        rule="普通形＋かぎり: 앞의 상태·조건이 유지되는 범위에서는 뒤 내용도 계속 성립합니다. な형용사는 元気なかぎり입니다.",
        trap="かけ는 동작 미완료라서 元気なかけで와 연결할 수 없습니다.",
        diff="〜うちは 변화 전의 기간에, 〜かぎり는 조건이 유효한 범위에 초점이 있습니다.",
        ex="力があるかぎり、困っている人を助けたい。 → 힘이 있는 한 곤란한 사람을 돕고 싶다.",
        procedure="뒤 내용이 앞 조건이 유지되는 동안 계속되는지 확인하세요.",
        check="앞말이 조건·범위인가? な형용사＋なかぎり인가?",
    ),
    4: dict(
        ko="본인이 동의하지 않는 한 이 계획을 진행할 수 없다.",
        rule="Vない＋かぎり: 앞의 필수 조건이 충족되지 않으면 뒤 내용도 성립하지 않습니다.",
        trap="かというとは 판단을 질문처럼 제시한 뒤 そうではない 등으로 답할 때 씁니다. 여기서는 진행 불가능의 전제 조건이 필요합니다.",
        diff="〜なければ도 조건이지만, 〜ないかぎり는 그 조건이 핵심 전제임을 강하게 나타냅니다.",
        ex="許可を得ないかぎり、ここには入れない。 → 허가를 받지 않는 한 여기에 들어갈 수 없다.",
        procedure="뒤에 できない가 보이면 앞에 필요한 조건이 충족되지 않았는지 확인하세요.",
        check="‘~하지 않는 한, 불가능’ 구조인가?",
    ),
    5: dict(
        ko="책상 위에 읽다 만 책이 놓여 있다.",
        rule="Vます語幹＋かけの＋N: 시작했으나 아직 끝내지 않은 상태의 명사를 수식합니다.",
        trap="読むかぎりの本은 이 문맥에서 자연스럽지 않고 ‘읽다 만 책’이라는 미완료 상태도 나타내지 못합니다.",
        diff="〜途中の는 단순히 도중임을, 〜かけ는 시작했으나 완성되지 않은 흔적이 남아 있음을 강조합니다.",
        ex="食べかけのパンを袋に入れた。 → 먹다 만 빵을 봉지에 넣었다.",
        procedure="명사 앞에서 ‘하다 만’의 의미가 필요한지 보고 ます어간＋かけの를 만드세요.",
        check="読みます→読み＋かけの 형태인가?",
    ),
    6: dict(
        ko="오랫동안 지지해 준 친구의 친절은 나에게 잊기 어렵다.",
        rule="Vます語幹＋がたい: 감정·판단상 받아들이거나 실행하기 매우 어려움을 나타냅니다.",
        trap="忘れないかぎりだ는 ‘잊지 않는 한이다’가 되어 문장이 완결되지 않고 의도한 ‘잊기 어렵다’도 아닙니다.",
        diff="〜にくい는 물리적·기능적 어려움에도 널리 쓰고, 〜がたい는 심리적·추상적 판단에 자주 씁니다.",
        ex="その光景は今でも信じがたい。 → 그 광경은 지금도 믿기 어렵다.",
        procedure="능력 문제가 아니라 감정적으로 하기 어려운지 확인한 뒤 ます어간＋がたい를 고르세요.",
        check="忘れます→忘れ＋がたい인가?",
    ),
    7: dict(
        ko="요즘은 바빠서 아침을 거르는 일이 많다.",
        rule="Vます語幹／N＋がちだ: 바람직하지 않은 상태나 행동이 자주 발생하는 경향을 나타냅니다.",
        trap="抜きかけている는 한 번의 동작이 미완료인 뜻에 가까워 最近의 반복 경향과 맞지 않습니다.",
        diff="〜気味는 약간 그런 상태라는 느낌, 〜がちは 실제로 그런 일이 자주 생기는 경향입니다.",
        ex="忙しいと、連絡を忘れがちだ。 → 바쁘면 연락을 자주 잊는 편이다.",
        procedure="最近・よく 같은 반복 신호를 찾고 ‘나쁜 경향’이면 がち를 선택하세요.",
        check="한 번 하다 만 것인가, 자주 반복되는가?",
    ),
    8: dict(
        ko="내가 단것을 싫어하느냐 하면 그런 것은 아니다. 다만 매일 먹지 않을 뿐이다.",
        rule="普通形＋かというと／かといえば: 판단을 질문처럼 제시한 뒤 그에 답하거나 일부 부정합니다.",
        trap="かける는 동사 ます어간에 붙는 미완료 문형입니다. 嫌い는 な형용사이며 뒤의 そういうわけではない를 받아야 합니다.",
        diff="〜わけではない는 전면 부정을 직접 나타내고, 〜かというと는 판단을 화제로 꺼내 답하는 흐름을 만듭니다.",
        ex="日本料理が苦手かというと、そうではない。 → 일본 요리를 어려워하느냐 하면 그렇지는 않다.",
        procedure="빈칸 뒤에 そうではない가 있으면 앞 판단을 질문 형태로 꺼내는 문형을 찾으세요.",
        check="‘~냐 하면, 그렇지는 않다’ 구조인가?",
    ),
    9: dict(
        ko="그는 무언가를 말하려다 말고 입을 다물었다.",
        rule="문장 배열은 何かを／言い／かけた／が이며 ★에는 かけた가 들어갑니다. Vます語幹＋かける입니다.",
        trap="★만 보지 말고 네 조각을 모두 사용해 완성해야 합니다. 言い는 두 번째 칸이며 ★가 아닙니다.",
        diff="〜かける는 시작했지만 끝내지 않음, 〜そうになる는 어떤 일이 일어날 뻔함을 나타냅니다.",
        ex="彼女は何か言いかけたが、やめた。 → 그녀는 무언가 말하려다가 그만두었다.",
        procedure="조각을 목적어→동사 어간→문형→접속 조사 순으로 전부 배열한 뒤 ★ 위치만 답하세요.",
        check="완성문 何かを言いかけたが가 자연스러운가? ★는 세 번째 조각인가?",
    ),
    10: dict(
        ko="새 제도로 절차는 편리해졌다. 하지만 문제가 모두 사라졌느냐 하면 그렇지는 않다. 이용자 설명은 아직 충분하지 않기 때문이다.",
        rule="普通形＋かといえば、そうではない: 앞의 판단을 전면 인정하지 않고 제한이나 반례를 덧붙입니다.",
        trap="しかし와 そうではない가 반대 방향을 분명히 표시합니다. 보람·미완료·경향 문형은 이 논리 흐름을 만들지 못합니다.",
        diff="〜とは限らない도 예외를 말하지만, 〜かといえば는 판단을 질문처럼 제시하고 직접 답하는 흐름입니다.",
        ex="高ければ必ず便利かといえば、そうではない。 → 비싸면 반드시 편리하냐 하면 그렇지는 않다.",
        procedure="접속사 しかし와 지시 표현 そうではない를 먼저 연결해 글의 반전 방향을 잡으세요.",
        check="앞 판단을 질문으로 제시한 뒤 부정하는 문형인가?",
    ),
}

trap_hypotheses = {
    1: "직후 관계를 조건·범위의 かぎり로 선택. 시간 관계와 범위 조건을 구별하지 못한 선택 결과.",
    2: "노력→성과 문맥에서 미완료 かけ를 선택. 문형 의미 표지 연결이 고정되지 않은 선택 결과.",
    3: "조건 유지 문맥에서 다시 かけ를 선택. な形容詞＋かぎり 접속을 회상하지 못한 선택 결과.",
    4: "필수 부정 조건을 판단 제시 かというと로 선택. 뒤의 できない와의 조건 관계를 놓친 선택 결과.",
    5: "미완료 명사수식에서 かぎり를 선택. ます어간＋かけの 형태를 회상하지 못한 선택 결과.",
    6: "심리적 난이도 がたい 대신 ないかぎり를 선택. 문장 완결성과 의미를 함께 확인하지 못한 선택 결과.",
    7: "반복 경향 がち 대신 미완료 かけ를 선택. 最近의 반복 신호를 활용하지 못한 선택 결과.",
    8: "判断提示 かというと 대신 존재하지 않는 な形容詞＋かける 형태를 선택. 접속 검토 누락 결과.",
    9: "전체 배열을 완성하지 않고 言い를 ★로 선택. 모든 조각 사용 후 ★ 위치를 찾는 절차가 필요.",
    10: "分からない 선택. 글의 しかし・そうではない가 만드는 부분 부정 구조를 회상하지 못한 결과.",
}

notes = {
    "submitted_result": payload,
    "raw_result": RAW.relative_to(ROOT).as_posix(),
    "classification_note": "Self-made delayed post-lecture check using JLPT-style grammar templates; not official material or a D+1 retention test.",
    "calendar_timing_note": "The user clarified that the lecture was viewed before dawn and the test was taken in the morning of 2026-08-30. Exact clock times and sleep interval are unverified, so submitted '익일' wording is preserved only as raw input.",
    "session_base_seconds": 49 * 60,
    "session_increment_seconds": 425,
    "session_total_seconds": 49 * 60 + 425,
    "session_integer_minutes": 56,
    "session_remainder_seconds": 5,
    "timing_note": "Only the 425-second test timer was added. Lecture duration and explanation time were not inferred.",
    "interpretation_note": "0/10 shows the seven new forms were not retrievable in this cold self-made sample. It does not independently determine official N2 score, mastery, or pass probability.",
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
    with sqlite3.connect(backup_dir / ("before-n2-009-015-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")) as backup:
        con.backup(backup)
    with con:
        session = con.execute("SELECT * FROM study_sessions WHERE session_date='2026-08-30'").fetchone()
        assert session is not None and session["verified_minutes"] == 49
        assert TID not in (session["summary"] or "")
        for item_type_id, values in extra_types.items():
            if con.execute("SELECT 1 FROM item_types WHERE id=?", (item_type_id,)).fetchone() is None:
                con.execute(
                    """INSERT INTO item_types
                       (id,domain,label_ko,label_ja,is_official_type,timing_note)
                       VALUES (?,?,?,?,?,?)""",
                    (item_type_id, *values),
                )
        con.execute(
            """INSERT INTO tests
               (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,
                response_format,total_items,correct_items,unknown_items,unanswered_items,
                elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                TID, payload["test_date"], payload["title"], "self_made", "N2",
                "N2 문형 범위 확인; 공식 난이도 미검증", "delayed_post_lecture_check",
                "multiple_choice", 10, 0, 1, 0, 425, 600, 0.15,
                json.dumps(notes, ensure_ascii=False),
            ),
        )
        for a in attempts:
            cur = con.execute(
                """INSERT INTO question_attempts
                   (test_id,item_no,item_type_id,level_label,response_state,response_seconds,
                    selected_text,correct_text,trap_hypothesis,trap_confidence)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (
                    TID, a["item_no"], a["item_type_id"], "N2", a["state"], None,
                    a["selected_text"], a["correct_text"],
                    trap_hypotheses[a["item_no"]], "medium",
                ),
            )
            for d in payload["review_dates"]:
                con.execute(
                    "INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,?)",
                    (cur.lastrowid, d["date"], d["interval"], "pending"),
                )
        extra = (
            f" [{TID}] N2 문법009~015 지연 확인 0/10, 오답9·모름1, 타이머425초. "
            "기존 Anki49분+시험7분05초=확인 시간56분05초; DB 정수56분, 잔여5초 보존. "
            "강의·해설 시간 미가산. 새복습30건, 기존 결과·일정·합격확률 보존. 오늘 종료 아님."
        )
        con.execute(
            """UPDATE study_sessions SET verified_minutes=56,summary=summary||?,updated_at=CURRENT_TIMESTAMP
               WHERE session_date='2026-08-30'""",
            (extra,),
        )
else:
    assert json.loads(existing["notes"])["submitted_result"] == payload

saved = con.execute("SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no", (TID,)).fetchall()
assert len(saved) == 10
reviews = con.execute(
    """SELECT q.item_no,r.review_date,r.interval_label,r.status
       FROM review_queue r JOIN question_attempts q ON q.id=r.attempt_id
       WHERE q.test_id=? ORDER BY q.item_no,r.review_date""",
    (TID,),
).fetchall()
assert len(reviews) == 30
assert {(r["item_no"], r["review_date"], r["interval_label"]) for r in reviews} == {
    (i, d["date"], d["interval"]) for i in range(1, 11) for d in payload["review_dates"]
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


study = """## 2026-08-30 — N2 문법 009~015 지연 확인시험

- 시험 ID `n2-grammar-009-015-check-20260830`. 사용자 실제 제출, 자체 제작 JLPT식 문법 확인시험. 공식 기출·공식 시험·공식 모의고사와 분리.
- 결과 **0/10(0%)**: 오답 9, `分からない` 1, 미응답 0. 제한 10분 중 **7분05초(425초)**, 시간 초과 없음.
- 유형별: 文の文法1 0/8, 文の文法2 0/1, 文章の文法 0/1. 문장 배열과 글의 문법은 각각 1문항뿐이므로 유형 전체 능력으로 일반화하지 않음.
- 범위: 〜か〜ないかのうちに, 〜かいがある, 〜かぎり／〜ないかぎり, 〜かけの／〜かける, 〜がたい, 〜がち, 〜かというと・〜かといえば.
- 사용자 확인 시간 관계: **새벽에 강의 시청 후 같은 날 아침 시험**. 정확한 시각·경과시간·수면 구간은 미확인. 원본의 ‘익일’ 표기는 제출값으로 보존하지만 공식 D+1 유지율로 처리하지 않음.
- 문항별 시간은 수집되지 않았으므로 타이머 425초만 가산. 오늘 확인 학습시간은 Anki 49분+시험 7분05초=**56분05초**. DB 정수 필드 56분, 잔여 5초는 notes·요약에 보존. 강의·해설 시간 미가산.
- 오답9·모름1 전부 새 D+1 **8/31**, D+3 **9/2**, D+7 **9/6**에 등록: 총 30건. 기존 이후 일정·기존 점수·복습 상태 보존.
- 이번 냉각 표본에서는 7개 문형의 의미와 형태를 선택지에 연결하지 못함. 특히 `かけ`를 2·3·7·8번에서 반복 선택하거나 관련 형태로 혼동했으며, 접속과 문장 전체 방향을 먼저 확인하는 절차가 필요함. 실제 사고 과정은 미확인.
- 자체 제작 10문항 한 번으로 공식 N2 점수·숙달·합격 확률을 직접 변경하지 않음. 오늘 학습 종료 아님.
- 원본: `database/results/n2-grammar-009-015-check-20260830.json`.
"""
append_once("JLPT_STUDY_LOG.md", study)

errors = """## 2026-08-30 — N2 문법 009~015 오답·모름 해설

자체 제작 지연 확인 0/10, 오답9·모름1. 공식 시험 및 D+1 유지율과 분리. **이번에는 답을 외우기보다 접속→문장 관계→의미 순서로 다시 고정하는 것이 우선입니다.**

"""
for a in attempts:
    f = feedback[a["item_no"]]
    choices = "\n".join(f"{i + 1}. {x}" for i, x in enumerate(a["choices"]))
    errors += f"""### {a['item_no']}번 — {a['pattern']}

**카테고리: {a['category']}**

**문제 원문**

{a['question']}

{choices}

**번역**

{f['ko']}

**선택 → 정답**

{a['selected_text']} → **{a['correct_text']}**

**접속·의미**

{f['rule']}

**함정·선택 분석**

{f['trap']} {trap_hypotheses[a['item_no']]} 실제 사고 과정은 확인하지 않음.

**유사 문형 차이**

{f['diff']}

**추가 예문**

{f['ex']}

**다음번 풀이 절차**

{f['procedure']}

**정답 직전 체크**

{f['check']}

**다음 복습일**

D+1 2026-08-31 · D+3 2026-09-02 · D+7 2026-09-06. 새 시도에 연결해 등록, 기존 일정 보존.

문항별 체류시간은 수집되지 않음. 전체 시험 타이머만 425초.

"""
append_once("JLPT_ERROR_NOTE.md", errors)

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
