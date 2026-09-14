"""Record due-review-20260830-part1-14 exactly once."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
TID = "due-review-20260830-part1-14"
REVIEW_DATES = [
    {"interval": "D+1", "date": "2026-08-31"},
    {"interval": "D+3", "date": "2026-09-02"},
    {"interval": "D+7", "date": "2026-09-06"},
]


def a(no, queue, source, interval, item_type, kind, category, state, question,
      choices, selected, correct, seconds):
    return {
        "item_no": no, "review_queue_id": queue, "source_attempt_id": source,
        "due_interval": interval, "item_type_id": item_type,
        "is_official_type": True, "type": kind, "category": category,
        "state": state, "question": question, "choices": choices,
        "selected_text": selected, "correct_text": correct,
        "response_seconds": seconds, "visited": True,
    }


A = [
    a(1,160,166,"D+1","grammar_form","文の文法1","문법 → 문법형식 판단 → 前に·사전형 접속","correct",
      "旅行に（　）前に、ホテルを予約しました。",["行く","行った","行き","行って"],"行く","行く",4),
    a(2,163,167,"D+1","grammar_form","文の文法1","문법 → 문법형식 판단 → ところ·진행 중","wrong",
      "今、報告書を（　）ところです。",["書く","書いている","書いた","書き"],"書いた","書いている",1),
    a(3,166,168,"D+1","grammar_form","文の文法1","문법 → 문법형식 판단 → 最中·한창","correct",
      "会議の（　）に、宅配便が届きました。",["最中","うえ","かぎり","ところ"],"最中","最中",1),
    a(4,169,169,"D+1","grammar_form","文の文法1","문법 → 문법형식 판단 → にくい·행동의 어려움","correct",
      "このペンは字が細すぎて、少し（　）。",["書きにくいです","書くにくいです","書いてにくいです","書かないにくいです"],"書きにくいです","書きにくいです",2),
    a(5,172,173,"D+1","grammar_form","文の文法1","문법 → 문법형식 판단 → 사역형","correct",
      "母は子どもに野菜を（　）。",["食べさせました","食べられました","食べさせられました","食べました"],"食べさせました","食べさせました",1),
    a(6,175,174,"D+1","adjective_conjugation","文の文法1","문법 → 문법형식 판단 → な형용사 과거 명사 수식","correct",
      "以前は（　）公園も、今は多くの人でにぎやかです。",["静かな","静かでした","静かだった","静かかった"],"静かだった","静かだった",8),
    a(7,178,176,"D+1","grammar_form","文の文法1","문법 → 문법형식 판단 → 겸양어·방문","correct",
      "明日、私が社長の事務所へ（　）。",["伺います","いらっしゃいます","おっしゃいます","ご覧になります"],"伺います","伺います",1),
    a(8,181,177,"D+1","grammar_form","文の文法1","문법 → 문법형식 판단 → 정중어·일반 현상","wrong",
      "天気予報では、明日は雪が（　）。",["降ります","お降りになります","いたします","召し上がります"],"お降りになります","降ります",14),
    a(9,184,181,"D+1","paraphrase","言い換え類義","어휘 → 유의표현 → 適した","wrong",
      "この仕事に適した人を探しています。\n「適した」と意味が最も近いものはどれですか。",
      ["条件や目的に合っている","準備に時間がかからない","経験がまったくない","費用が最も高い"],"準備に時間がかからない","条件や目的に合っている",3),
    a(10,187,186,"D+1","context_vocabulary","文脈規定","어휘 → 문맥규정 → 改善","wrong",
      "利用者の意見を聞き、会社はサービスの（　）を進めています。",["改善","延期","観察","到着"],"延期","改善",1),
    a(11,190,188,"D+1","short_content","短文内容理解","독해 → 단문 → 과거 상태","correct",
      "五年前、この駅前には小さな店が一軒あるだけで、夜になると歩く人もほとんどいませんでした。今は大きな店が増え、夜遅くまで多くの人が利用しています。\n\n五年前の駅前について最もよいものはどれですか。",
      ["人が少なく、静かだった","今よりにぎやかだった","大きな店が多かった","夜遅くまで人が多かった"],"人が少なく、静かだった","人が少なく、静かだった",1),
    a(12,50,48,"D+3","adjective_conjugation","文の文法1","문법 → 문법형식 판단 → な형용사 명사 수식","correct",
      "田中さんは、とても（　）人です。\n「親切だ」を使ってください。",["親切な","親切の","親切く","親切い"],"親切な","親切な",2),
    a(13,61,69,"D+3","adjective_conjugation","文の文法1","문법 → 문법형식 판단 → な형용사 과거 부정","correct",
      "先週泊まったホテルは、あまり便利（　）。",["ではありませんでした","くありませんでした","ではありません","かったです"],"ではありませんでした","ではありませんでした",12),
    a(14,72,75,"D+3","adjective_conjugation","文の文法1","문법 → 문법형식 판단 → な형용사 과거 긍정","wrong",
      "昨日の祭りは、人が多くてとても（　）。\n「にぎやかだ」を使ってください。",["にぎやかでした","にぎやかかったです","にぎやかなでした","にぎやかくでした"],"にぎやかかったです","にぎやかでした",2),
]

WRONG = [2, 8, 9, 10, 14]
PAYLOAD = {
    "test_id": TID, "test_date": "2026-08-30", "due_date": "2026-08-30",
    "title": "만기 복습 1차 — 문법·형용사·어휘·단문 14문항",
    "source_class": "자체 제작", "target_level": "N3 기반·N2 입문",
    "memory_timing": "D+1 11문항·D+3 3문항 변형 재시험",
    "total_items": 14, "correct_items": 9, "unknown_items": 0,
    "unanswered_items": 0, "elapsed_seconds": 595, "time_limit_seconds": 900,
    "timed_out": False, "started_at": "2026-08-30T04:15:40.282Z",
    "groups": {"文の文法1":{"correct":8,"total":11},"言い換え類義":{"correct":0,"total":1},
               "文脈規定":{"correct":0,"total":1},"短文内容理解":{"correct":1,"total":1}},
    "attempts": A, "review_dates": REVIEW_DATES,
    "mapping_note": "2026-08-30 만기 queue 중 비청해 1차 14건을 source_attempt_id·due_interval과 1대1 연결. D+1 11건·D+3 3건.",
    "timing_note": "開始する부터 제출까지 타이머. 문항 시간은 화면 체류시간이며 순수 사고시간이 아님. 미응답·중단은 만기 완료 처리하지 않음.",
}

TRAPS = {
    2: "今과 ところ의 시점 구별에서 완료형 書いた를 선택. 선택 결과만으로 실제 사고 과정은 확정하지 않음.",
    8: "자연현상인 雪에 사람의 행동을 높이는 お〜になる를 적용. 실제 사고 과정은 미확인.",
    9: "適した를 목적·조건에 맞음이 아니라 준비시간이 짧음으로 선택. 실제 사고 과정은 미확인.",
    10: "의견을 받아 서비스를 개선하는 문맥에서 延期(연기)를 선택. 실제 사고 과정은 미확인.",
    14: "な형용사 にぎやかだ에 い형용사의 과거형 かった를 적용. 반복 오답이며 실제 사고 과정은 미확인.",
}

assert len(A) == 14 and [x["item_no"] for x in A] == list(range(1, 15))
assert [x["item_no"] for x in A if x["state"] == "wrong"] == WRONG
assert sum(x["state"] == "correct" for x in A) == 9
assert sum(x["due_interval"] == "D+1" for x in A) == 11
assert sum(x["due_interval"] == "D+3" for x in A) == 3

raw = ROOT / "database" / "results" / f"{TID}.json"
raw.parent.mkdir(parents=True, exist_ok=True)
if raw.exists():
    assert json.loads(raw.read_text(encoding="utf-8")) == PAYLOAD
else:
    raw.write_text(json.dumps(PAYLOAD, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
existing = con.execute("SELECT notes FROM tests WHERE id=?", (TID,)).fetchone()
inserted = existing is None

notes = {
    "submitted_result": PAYLOAD,
    "raw_result": raw.relative_to(ROOT).as_posix(),
    "classification_note": "Self-made due-review variant using JLPT-style multiple-choice templates; separate from official tests.",
    "due_interval_scores": {"D+1":{"correct":7,"total":11},"D+3":{"correct":2,"total":3}},
    "review_dates": REVIEW_DATES,
    "session_base_seconds": 57 * 60 + 14,
    "session_increment_seconds": 595,
    "session_total_seconds": 67 * 60 + 9,
    "session_integer_minutes": 67,
    "session_remainder_seconds": 9,
    "timing_note": "Only the 595-second test timer was added; explanation and other study time were not inferred.",
}

if inserted:
    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / ("before-due-review-20260830-part1-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")
    with sqlite3.connect(backup_path) as backup:
        con.backup(backup)
    with con:
        session = con.execute("SELECT * FROM study_sessions WHERE session_date='2026-08-30'").fetchone()
        assert session and session["verified_minutes"] == 57 and TID not in (session["summary"] or "")
        for x in A:
            row = con.execute(
                """SELECT r.*,q.item_type_id FROM review_queue r
                   JOIN question_attempts q ON q.id=r.attempt_id WHERE r.id=?""",
                (x["review_queue_id"],),
            ).fetchone()
            assert row and row["attempt_id"] == x["source_attempt_id"]
            assert row["review_date"] == "2026-08-30" and row["interval_label"] == x["due_interval"]
            assert row["status"] == "pending" and row["item_type_id"] == x["item_type_id"]
            assert x["visited"] and x["state"] in ("correct", "wrong", "unknown")
        con.execute(
            """INSERT INTO tests
               (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,
                total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (TID,"2026-08-30",PAYLOAD["title"],"self_made","N3 기반·N2 입문",
             "만기 D+1·D+3 표적 변형; 공식 난이도 미검증",PAYLOAD["memory_timing"],"multiple_choice",
             14,9,0,0,595,900,0.2,json.dumps(notes,ensure_ascii=False)),
        )
        for x in A:
            cur = con.execute(
                """INSERT INTO question_attempts
                   (test_id,item_no,item_type_id,level_label,response_state,response_seconds,
                    selected_text,correct_text,trap_hypothesis,trap_confidence)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (TID,x["item_no"],x["item_type_id"],"N3 기반·N2 입문",x["state"],x["response_seconds"],
                 x["selected_text"],x["correct_text"],TRAPS.get(x["item_no"]),"medium" if x["item_no"] in TRAPS else None),
            )
            changed = con.execute(
                """UPDATE review_queue SET status='completed',result_state=?,result_seconds=?
                   WHERE id=? AND attempt_id=? AND review_date='2026-08-30' AND interval_label=? AND status='pending'""",
                (x["state"],x["response_seconds"],x["review_queue_id"],x["source_attempt_id"],x["due_interval"]),
            )
            assert changed.rowcount == 1
            if x["state"] in ("wrong", "unknown"):
                for d in REVIEW_DATES:
                    con.execute(
                        "INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,'pending')",
                        (cur.lastrowid,d["date"],d["interval"]),
                    )
        extra = (
            f" [{TID}] 자체 제작 만기 변형 9/14, D+1 7/11·D+3 2/3, 타이머595초. "
            "정상 제출14건 완료, 오답5건 새복습15건. 공식 시험·합격확률과 분리. "
            "오늘 정확한 확인시간67분09초; DB정수67분, 잔여9초 보존. 해설·기타시간 미가산. 오늘 종료 아님."
        )
        con.execute(
            "UPDATE study_sessions SET verified_minutes=67,summary=summary||?,updated_at=CURRENT_TIMESTAMP WHERE session_date='2026-08-30'",
            (extra,),
        )
else:
    assert json.loads(existing["notes"])["submitted_result"] == PAYLOAD

saved = con.execute("SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no", (TID,)).fetchall()
assert len(saved) == 14
for x, row in zip(A, saved):
    assert row["item_no"] == x["item_no"] and row["item_type_id"] == x["item_type_id"]
    assert row["response_state"] == x["state"] and row["response_seconds"] == x["response_seconds"]
    assert row["selected_text"] == x["selected_text"] and row["correct_text"] == x["correct_text"]
for x in A:
    row = con.execute("SELECT * FROM review_queue WHERE id=?", (x["review_queue_id"],)).fetchone()
    assert row["attempt_id"] == x["source_attempt_id"] and row["interval_label"] == x["due_interval"]
    assert row["status"] == "completed" and row["result_state"] == x["state"]
    assert row["result_seconds"] == x["response_seconds"]
new_reviews = con.execute(
    """SELECT q.item_no,r.review_date,r.interval_label,r.status FROM review_queue r
       JOIN question_attempts q ON q.id=r.attempt_id WHERE q.test_id=?""", (TID,)
).fetchall()
expected = {(i,d["date"],d["interval"]) for i in WRONG for d in REVIEW_DATES}
assert {(r["item_no"],r["review_date"],r["interval_label"]) for r in new_reviews} == expected
assert len(new_reviews) == 15 and all(r["status"] == "pending" for r in new_reviews)
assert con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-30'").fetchone()[0] == 67
assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()

marker = f"<!-- {TID} -->"


def append_once(filename: str, text: str) -> None:
    path = ROOT / filename
    old = path.read_text(encoding="utf-8")
    if marker not in old:
        path.write_text(old.rstrip() + "\n\n" + marker + "\n" + text.strip() + "\n", encoding="utf-8")
    assert path.read_text(encoding="utf-8").count(marker) == 1


study = """## 2026-08-30 — 만기 복습 1차: 문법·형용사·어휘·단문 14문항

- `due-review-20260830-part1-14` 사용자 실제 제출. 자체 제작 만기 변형 재시험이며 공식 시험·공식 모의고사와 분리.
- 전체 **9/14(64.3%)**, 오답 5, `分からない`·미응답·중단 0. 제한 15분 중 **9분55초(595초)**, 시간 초과 없음.
- 만기별 **D+1 7/11(63.6%)**, **D+3 2/3(66.7%)**. 별도 집계하며 공식 점수·합격 확률로 환산하지 않음.
- 유형별: 文の文法1 8/11, 言い換え類義 0/1, 文脈規定 0/1, 短文内容理解 1/1. 소표본이므로 유형 전체 능력으로 확정하지 않음.
- `review_queue_id`·`source_attempt_id`·`due_interval`·문항 유형 14건을 1대1 대조. 정상 제출 14건만 결과·시간과 함께 완료 처리. 기존 이후 일정·점수·복습 상태 보존.
- 오답 2·8·9·10·14만 D+1 **8/31**, D+3 **9/2**, D+7 **9/6**에 새 복습 15건 등록. 모름 없음.
- 타이머 595초만 가산: 기존 57분14초에서 오늘 **67분09초**. DB 정수 67분, 잔여 9초 보존. 해설·다른 학습시간 미가산. 오늘 종료 아님.
- 원본: `database/results/due-review-20260830-part1-14.json`. 숙달 스냅샷·합격 확률은 변경하지 않음.
"""
append_once("JLPT_STUDY_LOG.md", study)

error = """## 2026-08-30 — 만기 복습 1차 오답

### 2번 — 〜ところ: 진행 중

**카테고리: 문법 → 문법형식 판단 → ところ·진행 중**

**원문·번역**  今、報告書を（　）ところです。 → 지금 보고서를 쓰고 있는 중입니다.

**선택 → 정답·완성문**  書いた → **書いている** / 今、報告書を書いているところです。

**접속·의미**  `Vている＋ところ`는 바로 지금 진행 중, `Vる＋ところ`는 막 시작 직전, `Vた＋ところ`는 막 끝난 직후입니다.

**함정**  `書いたところ`는 “막 쓴 참”이라 완료입니다. 문두의 `今`과 진행 중이라는 문맥을 먼저 잡아야 합니다. 1초 선택이므로 실제 사고 과정은 확정하지 않습니다.

**유사 문형**  `Vている最中`도 한창 진행 중이지만, `最中`은 동작 한가운데임을 더 강조합니다.

**예문**  今、資料を確認しているところです。 → 지금 자료를 확인하는 중입니다.

**다음 복습일**  D+1 8/31 · D+3 9/2 · D+7 9/6.

**다음번 풀이 절차**  ① 시간 단서 `今` 확인 → ② 시작 전/진행/완료 중 하나 결정 → ③ 진행이면 `ているところ` 선택.

**정답 직전 체크**  지금 하는 중인가, 이미 끝난 직후인가?

### 8번 — 자연현상과 정중어

**카테고리: 문법 → 문법형식 판단 → 정중어·일반 현상**

**원문·번역**  天気予報では、明日は雪が（　）。 → 일기예보에 따르면 내일은 눈이 옵니다.

**선택 → 정답·완성문**  お降りになります → **降ります** / 天気予報では、明日は雪が降ります。

**접속·의미**  `降ります`는 `降る`의 정중한 `ます`형입니다. 눈은 높임의 대상이 아니므로 존경어를 쓰지 않습니다.

**함정**  `お＋동사ます어간＋になる`는 사람의 행동을 높이는 존경 표현입니다. `雪がお降りになる`는 자연현상에 존경어를 잘못 붙인 형태입니다.

**유사 표현**  `社長がお帰りになります`는 사람의 행동이라 존경어가 가능하고, `私がいたします`는 자기 행동을 낮추는 겸양어입니다.

**예문**  明日は雨が降ります。 → 내일은 비가 옵니다.

**다음 복습일**  D+1 8/31 · D+3 9/2 · D+7 9/6.

**다음번 풀이 절차**  ① 주어 확인 → ② 사람의 행동인지 자연현상인지 구별 → ③ 자연현상이면 보통 `です／ます`형 선택.

**정답 직전 체크**  지금 높여야 할 사람이 실제로 있는가?

### 9번 — 適した

**카테고리: 어휘 → 유의표현(言い換え類義) → 適した**

**원문·번역**  この仕事に適した人を探しています。 → 이 일에 적합한 사람을 찾고 있습니다.

**선택 → 정답**  準備に時間がかからない → **条件や目的に合っている**.

**접속·의미**  `Nに適した`는 “N의 조건·목적·상황에 잘 맞는”입니다. `この仕事に適した人`은 이 일에 알맞은 사람입니다.

**함정**  준비가 빠르다는 것은 적합성의 가능한 한 조건일 수는 있어도 `適した`의 뜻 자체가 아닙니다.

**유사 어휘**  `適切な`는 처리·판단이 적절함, `向いている`는 사람의 성향·능력이 어떤 일에 잘 맞음을 자주 나타냅니다.

**예문**  目的に適した方法を選びます。 → 목적에 맞는 방법을 고릅니다.

**다음 복습일**  D+1 8/31 · D+3 9/2 · D+7 9/6.

**다음번 풀이 절차**  ① 밑줄 어휘를 짧게 한국어로 바꿈 → ② 선택지가 그 뜻 전체를 바꾸어 말하는지 확인 → ③ 주변 상황에서 추측한 부수 조건은 제외.

**정답 직전 체크**  이 선택지는 “알맞다”의 뜻인가, 단지 편리한 특징 하나인가?

### 10번 — 改善

**카테고리: 어휘 → 문맥규정(文脈規定) → 改善**

**원문·번역**  利用者の意見を聞き、会社はサービスの（　）を進めています。 → 이용자의 의견을 듣고 회사는 서비스의 개선을 추진하고 있습니다.

**선택 → 정답·완성문**  延期 → **改善** / 会社はサービスの改善を進めています。

**접속·의미**  `改善する／改善を進める`는 나쁜 점을 고쳐 더 좋게 만드는 것입니다.

**함정**  `延期`는 예정된 일을 뒤로 미루는 “연기”입니다. 이용자 의견을 듣고 서비스를 더 좋게 한다는 방향과 맞지 않습니다.

**유사 어휘**  `改良`은 제품·기술을 고쳐 성능을 좋게 한다는 뜻에 자주 쓰고, `改善`은 서비스·환경·상황·문제에도 넓게 씁니다.

**예문**  働く環境を改善する必要があります。 → 근무 환경을 개선할 필요가 있습니다.

**다음 복습일**  D+1 8/31 · D+3 9/2 · D+7 9/6.

**다음번 풀이 절차**  ① 앞뒤의 원인과 결과를 연결 → ② `意見を聞く` 뒤의 방향이 향상인지 지연인지 판단 → ③ 자연스러운 결합 `サービスの改善を進める` 확인.

**정답 직전 체크**  서비스가 더 좋아지는가, 일정만 뒤로 미뤄지는가?

### 14번 — な형용사 과거 긍정

**카테고리: 문법 → 문법형식 판단 → な형용사 과거 긍정**

**원문·번역**  昨日の祭りは、人が多くてとても（　）。 → 어제 축제는 사람이 많아서 매우 붐볐습니다.

**선택 → 정답·완성문**  にぎやかかったです → **にぎやかでした** / 昨日の祭りは、人が多くてとてもにぎやかでした。

**접속·의미**  `にぎやかだ`는 な형용사입니다. 정중 과거 긍정은 어간＋`でした`: `にぎやかでした`.

**함정**  `〜かったです`는 `楽しい→楽しかったです`처럼 い형용사에 씁니다. `にぎやか`에 かった를 붙이지 않습니다.

**유사 활용**  현재 `にぎやかです`, 과거 `にぎやかでした`, 현재 부정 `にぎやかではありません`, 과거 부정 `にぎやかではありませんでした`.

**예문**  先週の駅前は静かでした。 → 지난주 역 앞은 조용했습니다.

**다음 복습일**  D+1 8/31 · D+3 9/2 · D+7 9/6.

**다음번 풀이 절차**  ① 기본형을 `にぎやかだ`로 복원 → ② な형용사임을 확정 → ③ 과거·정중 단서 `昨日`에 맞춰 `でした` 선택.

**정답 직전 체크**  기본형 끝이 `い`형용사인가, `だ`가 붙는 な형용사인가?
"""
append_once("JLPT_ERROR_NOTE.md", error)

result = {
    "test_id": TID, "inserted": inserted, "attempts": len(saved),
    "completed_due_reviews": 14, "new_reviews": len(new_reviews),
    "session_minutes_field": 67, "session_remainder_seconds": 9,
    "pending_due_today": con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date<='2026-08-30'").fetchone()[0],
    "pending_2026_08_31": con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date='2026-08-31'").fetchone()[0],
    "integrity": "ok",
}
print(json.dumps(result, ensure_ascii=False))
con.close()
