"""Record due-review-20260829-grammar-21 exactly once and verify queue mappings."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "jlpt_learning.db"
TID = "due-review-20260829-grammar-21"


def attempt(no, queue, source, interval, item_type, category, subtype, practice, pattern,
            state, question, choices, selected, correct, seconds):
    return {
        "item_no": no, "review_queue_id": queue, "source_attempt_id": source,
        "due_interval": interval, "item_type_id": item_type, "category": category,
        "subtype": subtype, "practice_type": practice, "pattern": pattern,
        "state": state, "question": question, "choices": choices,
        "selected_text": selected, "correct_text": correct,
        "response_seconds": seconds, "visited": True,
    }


A = [
 attempt(1,41,35,"D+3","adjective_conjugation","문법 → 문법형식 판단 → 형용사 활용·い형용사 과거 긍정","い形容詞・過去肯定","形容詞","い形容詞の過去肯定","correct","昨日見た映画は、とても（　）。",["面白いでした","面白かったです","面白くでした","面白ではありました"],"面白かったです","面白かったです",38),
 attempt(2,44,38,"D+3","adjective_conjugation","문법 → 문법형식 판단 → 형용사 활용·な형용사 과거 긍정","な形容詞・過去肯定","形容詞","な形容詞の過去肯定","correct","先週の図書館は、とても（　）。",["静かかったです","静かでした","静かいでした","静かなでした"],"静かでした","静かでした",144),
 attempt(3,23,17,"D+3","adjective_conjugation","문법 → 문법형식 판단 → 형용사 활용·い형용사 과거 부정","い形容詞・過去否定","形容詞","い形容詞の過去否定","correct","先月の家賃は、今月ほど（　）。",["高いではありませんでした","高くありません","高くありませんでした","高かったではありません"],"高くありませんでした","高くありませんでした",49),
 attempt(4,26,19,"D+3","adjective_conjugation","문법 → 문법형식 판단 → 형용사 활용·な형용사 현재 부정","な形容詞・現在否定","形容詞","な形容詞の現在否定","correct","この部屋は駅に近いですが、あまり静か（　）。",["くありません","ではありません","ではありませんでした","ないですでした"],"ではありません","ではありません",24),
 attempt(5,29,20,"D+3","adjective_conjugation","문법 → 문법형식 판단 → 형용사 활용·な형용사 과거 긍정","な形容詞・過去肯定","形容詞","な形容詞の過去肯定","correct","子どものころ、この町はもっと（　）。",["にぎやかでした","にぎやかかったです","にぎやかなでした","にぎやかくでした"],"にぎやかでした","にぎやかでした",62),
 attempt(6,8,3,"D+3","adjective_conjugation","문법 → 문법형식 판단 → 형용사 활용·い형용사 과거 부정","い形容詞・過去否定","形容詞","い形容詞の過去否定","correct","昨日食べたケーキは、あまり（　）。",["おいしいではありませんでした","おいしくありませんでした","おいしくないでした","おいしかったではありません"],"おいしくありませんでした","おいしくありませんでした",135),
 attempt(7,9,5,"D+3","grammar_form","문법 → 문법형식 판단 → 前に·동작 전의 사전형 접속","前に・사전형 접속","文法","Vる＋前に","wrong","日本へ（　）前に、日本語を少し勉強しました。",["行って","行った","行く","行き"],"行き","行く",28),
 attempt(8,94,103,"D+1","grammar_form","문법 → 문법형식 판단 → ところ·동작 진행 시점","ところ・진행 중","文法","Vている＋ところ","wrong","今、昼ご飯を（　）ところです。後で電話します。",["食べる","食べている","食べた","食べない"],"食べる","食べている",23),
 attempt(9,97,106,"D+1","grammar_form","문법 → 문법형식 판단 → 最中·한창 진행 중","最中・한창","文法","Nの／Vている＋最中","wrong","会議の（　）に、携帯電話が鳴ってしまった。",["一方","最中","ところで","うえ"],"うえ","最中",33),
 attempt(10,100,108,"D+1","grammar_form","문법 → 문법형식 판단 → にくい·행동의 어려움","にくい・하기 어렵다","文法","Vます語幹＋にくい","wrong","この説明は言葉が難しくて、少し（　）。",["分かるにくいです","分かりにくいです","分かってにくいです","分からないにくいです"],"分かってにくいです","分かりにくいです",41),
 attempt(11,103,109,"D+1","grammar_form","문법 → 문법형식 판단 → にしたがって·동조 변화","にしたがって・동조 변화","文法","N／Vる＋にしたがって","correct","気温が上がる（　）、アイスの売り上げも増えている。",["に対して","にとって","にしたがって","について"],"にしたがって","にしたがって",42),
 attempt(12,106,110,"D+1","grammar_form","문법 → 문법형식 판단 → に対して·행동과 태도의 대상","に対して・행동 대상","文法","N＋に対して","correct","店員は客（　）、丁寧に説明しました。",["にとって","に対して","にしたがって","のおかげで"],"に対して","に対して",23),
 attempt(13,109,112,"D+1","grammar_form","문법 → 문법형식 판단 → はずがない·근거상 불가능","はずがない・근거상 불가능","文法","普通形＋はずがない","correct","田中さんは今、海外にいる。ここに（　）。",["いるはずです","いるはずがありません","いたところです","いる一方です"],"いるはずがありません","いるはずがありません",39),
 attempt(14,112,115,"D+1","grammar_form","문법 → 문법형식 판단 → 사역형·시키다","사역형","文法","Vさせる","wrong","先生は学生に作文を（　）。",["書かれました","書かせました","書かせられました","書きました"],"書かせられました","書かせました",18),
 attempt(15,139,140,"D+1","adjective_conjugation","문법 → 문법형식 판단 → 형용사 활용·な형용사 과거 명사 수식","な形容詞・과거 명사 수식","形容詞","な形容詞普通形過去＋名詞","wrong","以前は（　）駅前も、今は店が増えてにぎやかです。",["静かな","静かでした","静かだった","静かかった"],"静かかった","静かだった",31),
 attempt(16,127,126,"D+1","grammar_form","문법 → 문법형식 판단 → 경어·존경어·상대의 말하기","존경어·말하다","敬語","言う→おっしゃる","correct","部長は会議が中止になったと（　）。",["申しました","おっしゃいました","拝見しました","伺いました"],"おっしゃいました","おっしゃいました",13),
 attempt(17,130,129,"D+1","grammar_form","문법 → 문법형식 판단 → 경어·겸양어·상대 방문하기","겸양어·방문하다","敬語","行く・訪ねる→伺う","wrong","来週、私が先生の研究室へ（　）。",["いらっしゃいます","ご覧になります","伺います","おっしゃいます"],"いらっしゃいます","伺います",21),
 attempt(18,133,131,"D+1","grammar_form","문법 → 문법형식 판단 → 경어·정중어의 기능 구별","정중어만 구별","敬語","丁寧語だけ","wrong","尊敬語や謙譲語の特別な動詞を使わず、丁寧語だけの文はどれですか。",["先生がお帰りになります。","私は資料を拝見します。","明日は雨が降ります。","社長が召し上がります。"],"先生がお帰りになります。","明日は雨が降ります。",66),
 attempt(19,136,132,"D+1","grammar_form","문법 → 문법형식 판단 → 경어·존경어·상대의 행동","존경어·하다","敬語","する→なさる","correct","先生は午後、研究の発表を（　）。",["いたします","なさいます","申します","拝見します"],"なさいます","なさいます",21),
 attempt(20,154,149,"D+1","grammar_form","문법 → 문법형식 판단 → あげく·과정 끝의 결과","あげく·과정 끝 결과","N2文法","Vた／Nの＋あげく","correct","何度も店を回ったあげく、結局何も買わなかった。意味に最も近いものはどれですか。",["何も買わずに、これから店を回る。","何度も店を回った末に、何も買わなかった。","最初の店ですぐ商品を買った。","何かを買ってから店を回った。"],"何度も店を回った末に、何も買わなかった。","何度も店を回った末に、何も買わなかった。",30),
 attempt(21,157,153,"D+1","grammar_form","문법 → 문법형식 판단 → うえに·성질의 추가","うえに·성질 추가","N2文法","普通形＋うえに","correct","このホテルは駅に近い（　）、部屋も広い。",["うえに","うえで","うえは","あげく"],"うえに","うえに",11),
]

REVIEW_DATES = [
    {"interval": "D+1", "date": "2026-08-30"},
    {"interval": "D+3", "date": "2026-09-01"},
    {"interval": "D+7", "date": "2026-09-05"},
]

GROUPS = {}
for a in A:
    g = GROUPS.setdefault(a["practice_type"], {"correct": 0, "total": 0})
    g["total"] += 1
    g["correct"] += a["state"] == "correct"

PAYLOAD = {
    "test_id": TID, "test_date": "2026-08-29", "due_date": "2026-08-29",
    "title": "만기 복습 1차 — 문법·형용사·경어 21문항",
    "source_class": "자체 제작", "target_level": "N3 기반·N2 입문",
    "memory_timing": "D+3 7문항·D+1 14문항 변형 재시험",
    "total_items": 21, "correct_items": 13, "unknown_items": 0,
    "unanswered_items": 0, "elapsed_seconds": 894, "time_limit_seconds": 1500,
    "timed_out": False, "groups": GROUPS, "wrong": [7,8,9,10,14,15,17,18],
    "unknown": [], "unanswered": [], "attempts": A, "review_dates": REVIEW_DATES,
    "mapping_note": "2026-08-29 만기 review_queue 21건과 source_attempt_id를 1대1 대조한 변형 문제. D+3 7건과 D+1 14건을 포함. 공식 시험과 분리.",
    "timing_note": "開始する부터 제출까지의 타이머만 기록. 문항 시간은 화면 체류시간이며 순수 사고시간 아님. 미응답·중단 항목은 만기 완료 처리하지 않음.",
}

DETAILS = {
7: {"translation":"일본에 가기 전에 일본어를 조금 공부했습니다.","full":"日本へ行く前に、日本語を少し勉強しました。","rule":"앞 행동이 아직 일어나지 않은 시점이므로 `Vる＋前に`를 쓴다. 과거 문장이어도 前に 앞은 사전형이다.","trap":"`行き`는 ます형 어간이지만 단독으로 前に를 수식할 수 없다.","diff":"`Vた後で`는 행동 완료 뒤, `Vる前に`는 행동 실행 전이다.","example":"寝る前に、歯を磨きます。 — 자기 전에 이를 닦습니다."},
8: {"translation":"지금 점심을 먹고 있는 중입니다. 나중에 전화하겠습니다.","full":"今、昼ご飯を食べているところです。後で電話します。","rule":"`Vている＋ところだ`는 바로 지금 진행 중인 동작을 나타낸다.","trap":"`食べるところ`는 아직 먹기 전, 막 먹으려는 참이라는 뜻이다.","diff":"`Vるところ` 직전, `Vているところ` 진행 중, `Vたところ` 막 끝난 직후이다.","example":"今、資料を読んでいるところです。 — 지금 자료를 읽고 있는 중입니다."},
9: {"translation":"회의가 한창 진행 중일 때 휴대전화가 울리고 말았습니다.","full":"会議の最中に、携帯電話が鳴ってしまった。","rule":"`Nの／Vている＋最中に`는 어떤 일이 한창 진행 중인 바로 그때를 강조한다.","trap":"`うえ`는 위·측면 또는 다른 N2 문형의 일부이며 ‘한창 도중’이 아니다.","diff":"`ところ`는 동작의 시점을 중립적으로, `最中`는 방해받기 쉬운 한창인 상황을 강하게 나타낸다.","example":"食事の最中に電話が来ました。 — 식사 도중 한창일 때 전화가 왔습니다."},
10:{"translation":"이 설명은 말이 어려워서 조금 이해하기 어렵습니다.","full":"この説明は言葉が難しくて、少し分かりにくいです。","rule":"`Vます형 어간＋にくい`; 分かります에서 ます를 뺀 `分かり＋にくい`가 된다.","trap":"て형 `分かって` 뒤에는 にくい를 붙이지 않는다.","diff":"`〜にくい`는 하기 어렵다, `〜づらい`는 심리적·육체적 부담 때문에 하기 괴롭다는 뉘앙스가 강하다.","example":"この字は小さくて読みにくいです。 — 이 글자는 작아서 읽기 어렵습니다."},
14:{"translation":"선생님은 학생에게 작문을 쓰게 했습니다.","full":"先生は学生に作文を書かせました。","rule":"`書く→書かせる`; 사역형은 주체가 다른 사람에게 행동을 시키거나 허락함을 나타낸다.","trap":"선택한 `先生は学生に作文を書かせられました`는 사역수동이어서 ‘선생님이 학생에게 억지로 작문을 쓰게 되었다’가 되어 의도한 인물 관계가 뒤집힌다.","diff":"`先生は学生に書かせた`는 선생님이 학생에게 쓰게 함, `学生は先生に書かせられた`는 학생이 선생님에게 강제로 쓰게 됨이다.","example":"母は子どもに野菜を食べさせました。 — 어머니는 아이에게 채소를 먹게 했습니다."},
15:{"translation":"예전에는 조용했던 역 앞도 지금은 가게가 늘어 번화합니다.","full":"以前は静かだった駅前も、今は店が増えてにぎやかです。","rule":"な형용사 보통형 과거는 `静かだった`; 명사 앞에서도 그대로 `静かだった＋名詞`를 쓴다.","trap":"`〜かった`는 い형용사의 과거형이므로 静か에 붙일 수 없다.","diff":"현재 수식은 `静かな町`, 과거 수식은 `静かだった町`, 정중 종결은 `静かでした`이다.","example":"昔有名だった店が閉まりました。 — 예전에 유명했던 가게가 문을 닫았습니다."},
17:{"translation":"다음 주에 제가 선생님의 연구실을 찾아뵙겠습니다.","full":"来週、私が先生の研究室へ伺います。","rule":"내가 윗사람의 장소로 가거나 찾아갈 때 `行く・訪ねる`의 겸양어 `伺う`를 쓴다.","trap":"`いらっしゃる`는 상대방의 行く・来る・いる를 높이는 존경어라서 `私が`와 맞지 않는다.","diff":"상대의 이동은 `先生がいらっしゃいます`, 나의 방문은 `私が先生の所へ伺います`이다.","example":"明日の午後、会社へ伺います。 — 내일 오후 회사로 찾아뵙겠습니다."},
18:{"translation":"존경어나 겸양어의 특별한 동사를 쓰지 않고 정중어만 사용한 문장은 어느 것입니까?","full":"明日は雨が降ります。","rule":"정중어는 보통 동사에 `です・ます`를 붙여 듣는 사람에게 공손하게 말하며 인물의 행동을 특별히 높이거나 낮추지 않는다.","trap":"`お帰りになります`는 `お＋ます형 어간＋になる` 존경어라서 단순 정중어가 아니다.","diff":"`召し上がる・お〜になる`는 존경어, `拝見する`는 겸양어, `降ります`는 단순한 ます형 정중어이다.","example":"電車は九時に着きます。 — 전철은 9시에 도착합니다."},
}

assert len(A) == 21 and sum(a["response_seconds"] for a in A) == 892
assert [a["item_no"] for a in A if a["state"] == "wrong"] == PAYLOAD["wrong"]
assert GROUPS == {"形容詞":{"correct":6,"total":7},"文法":{"correct":3,"total":8},"敬語":{"correct":2,"total":4},"N2文法":{"correct":2,"total":2}}
assert sum(a["state"] == "correct" for a in A if a["due_interval"] == "D+3") == 6
assert sum(a["state"] == "correct" for a in A if a["due_interval"] == "D+1") == 7

raw = ROOT / "database" / "results" / f"{TID}.json"
notes = {
    "submitted_result": PAYLOAD,
    "raw_result": raw.relative_to(ROOT).as_posix(),
    "source_note": "자체 제작 만기 변형 재시험. 공식 시험·공식 모의고사와 분리.",
    "timing_note": "2026-08-29 신규 세션. 제출 타이머 894초만 기록; 문항 체류 합은 892초이며 차이 2초의 원인은 추정하지 않음. 해설 읽기·다른 학습시간 미추정.",
    "due_split": {"D+3":{"correct":6,"total":7},"D+1":{"correct":7,"total":14}},
    "diagnostic_note": "합격 확률·기존 점수·숙달 스냅샷에 직접 환산하지 않음.",
    "format_note": "18번은 경어 용어를 직접 분류하는 학습용 개념 확인 문항으로 공식 JLPT 형식의 성취 근거에서 제외. 이후 문제는 공식 JLPT 형식 템플릿을 기본으로 제작.",
}

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys=ON")
old_reviews = {r["id"]: dict(r) for r in con.execute("SELECT * FROM review_queue")}
protected = {t:[tuple(r) for r in con.execute(f"SELECT * FROM {t} ORDER BY id")]
             for t in ("mastery_snapshots","pass_probability_snapshots","study_intervals")}
old_tests = {r["id"]:tuple(r) for r in con.execute("SELECT * FROM tests WHERE id<>?",(TID,))}
old_attempts = {r["id"]:tuple(r) for r in con.execute("SELECT * FROM question_attempts WHERE test_id<>?",(TID,))}
existing = con.execute("SELECT * FROM tests WHERE id=?",(TID,)).fetchone()

if existing is None:
    backup_dir = ROOT / "outputs" / "db_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / ("before-due-review-20260829-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")
    with sqlite3.connect(backup_path) as backup:
        con.backup(backup)
    with con:
        con.execute("BEGIN IMMEDIATE")
        assert con.execute("SELECT COUNT(*) FROM study_sessions WHERE session_date='2026-08-29'").fetchone()[0] == 0
        for a in A:
            r = con.execute("""SELECT r.*,q.item_type_id FROM review_queue r
                JOIN question_attempts q ON q.id=r.attempt_id WHERE r.id=?""",
                (a["review_queue_id"],)).fetchone()
            assert r and r["attempt_id"] == a["source_attempt_id"]
            assert r["review_date"] == "2026-08-29" and r["interval_label"] == a["due_interval"]
            assert r["status"] == "pending" and r["item_type_id"] == a["item_type_id"]
            assert a["visited"] and a["state"] in ("correct","wrong","unknown")
        con.execute("""INSERT INTO tests
          (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,
           total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
          (TID,"2026-08-29",PAYLOAD["title"],"self_made","N3 기반·N2 입문",
           "만기 D+3·D+1 표적 변형; 공식 난이도 미검증",PAYLOAD["memory_timing"],"multiple_choice",
           21,13,0,0,894,1500,0.2,json.dumps(notes,ensure_ascii=False)))
        for a in A:
            trap = DETAILS.get(a["item_no"],{}).get("trap")
            cur = con.execute("""INSERT INTO question_attempts
              (test_id,item_no,item_type_id,level_label,response_state,response_seconds,selected_text,correct_text,trap_hypothesis,trap_confidence)
              VALUES (?,?,?,?,?,?,?,?,?,?)""",
              (TID,a["item_no"],a["item_type_id"],"N3 기반·N2 입문",a["state"],a["response_seconds"],
               a["selected_text"],a["correct_text"],trap,"medium" if trap else None))
            new_attempt = cur.lastrowid
            changed = con.execute("""UPDATE review_queue SET status='completed',result_state=?,result_seconds=?
                WHERE id=? AND attempt_id=? AND review_date=? AND interval_label=? AND status='pending'""",
                (a["state"],a["response_seconds"],a["review_queue_id"],a["source_attempt_id"],
                 "2026-08-29",a["due_interval"]))
            assert changed.rowcount == 1
            if a["state"] in ("wrong","unknown"):
                for d in REVIEW_DATES:
                    con.execute("INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,'pending')",
                                (new_attempt,d["date"],d["interval"]))
        summary = (f"[{TID}] 자체 제작 만기 변형 13/21, D+3 6/7·D+1 7/14, 타이머 894초. "
                   "정상 제출 21건만 완료, 오답8건 새 복습24건. 공식 시험·합격 확률과 분리. "
                   "해설·기타 학습시간 미가산; 정확한 누적 14분54초(정수 필드14분, 잔여54초). 오늘 학습 종료 아님.")
        con.execute("""INSERT INTO study_sessions
            (session_date,verified_minutes,has_untracked_activity,summary) VALUES ('2026-08-29',14,0,?)""",(summary,))
else:
    assert json.loads(existing["notes"])["submitted_result"] == PAYLOAD, "Existing test differs"
    if json.loads(existing["notes"]) != notes:
        with con:
            con.execute("UPDATE tests SET notes=? WHERE id=?",(json.dumps(notes,ensure_ascii=False),TID))

saved = list(con.execute("SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no",(TID,)))
assert len(saved) == 21
with con:
    for a in A:
        if a["state"] == "wrong":
            con.execute("UPDATE question_attempts SET trap_hypothesis=?,trap_confidence='medium' WHERE test_id=? AND item_no=?",
                        (DETAILS[a["item_no"]]["trap"],TID,a["item_no"]))
saved = list(con.execute("SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no",(TID,)))
for a,r in zip(A,saved):
    for key in ("item_no","item_type_id","response_seconds","selected_text","correct_text"):
        assert r[key] == a[key], (key,r[key],a[key])
    assert r["response_state"] == a["state"]
    if a["state"] == "wrong": assert r["trap_hypothesis"] == DETAILS[a["item_no"]]["trap"]
for a in A:
    r=con.execute("SELECT * FROM review_queue WHERE id=?",(a["review_queue_id"],)).fetchone()
    assert r["attempt_id"] == a["source_attempt_id"] and r["status"] == "completed"
    assert r["interval_label"] == a["due_interval"] and r["result_state"] == a["state"]
    assert r["result_seconds"] == a["response_seconds"]
new_reviews=list(con.execute("""SELECT q.item_no,r.review_date,r.interval_label FROM review_queue r
    JOIN question_attempts q ON q.id=r.attempt_id WHERE q.test_id=?""",(TID,)))
expected={(i,d["date"],d["interval"]) for i in PAYLOAD["wrong"] for d in REVIEW_DATES}
assert {(r["item_no"],r["review_date"],r["interval_label"]) for r in new_reviews} == expected
assert len(new_reviews) == 24
for r in con.execute("SELECT * FROM review_queue"):
    if r["id"] not in old_reviews: continue
    expected_row=old_reviews[r["id"]].copy()
    match=next((a for a in A if a["review_queue_id"]==r["id"]),None)
    if match: expected_row.update(status="completed",result_state=match["state"],result_seconds=match["response_seconds"])
    assert dict(r)==expected_row, f"Unrelated review changed: {r['id']}"
for t,rows in protected.items():
    assert [tuple(r) for r in con.execute(f"SELECT * FROM {t} ORDER BY id")] == rows
assert {r["id"]:tuple(r) for r in con.execute("SELECT * FROM tests WHERE id<>?",(TID,))} == old_tests
assert {r["id"]:tuple(r) for r in con.execute("SELECT * FROM question_attempts WHERE test_id<>?",(TID,))} == old_attempts
assert con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not con.execute("PRAGMA foreign_key_check").fetchall()

raw.parent.mkdir(parents=True,exist_ok=True)
if raw.exists(): assert json.loads(raw.read_text(encoding="utf-8")) == PAYLOAD
else: raw.write_text(json.dumps(PAYLOAD,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

marker=f"<!-- {TID} -->"
def append_once(name,text):
    p=ROOT/name; old=p.read_text(encoding="utf-8")
    if marker not in old: p.write_text(old.rstrip()+"\n\n"+marker+"\n"+text.strip()+"\n",encoding="utf-8")
    assert p.read_text(encoding="utf-8").count(marker)==1

study=f"""## 2026-08-29 — 만기 복습 1차: 문법·형용사·경어 21문항

- 시험 ID `{TID}`. 사용자 제출 실제 결과, 자체 제작 만기 변형 재시험. 공식 시험·공식 모의고사와 분리.
- 전체 **13/21(61.9%)**, 오답 8, 모름·미응답·중단 0. 제한 25분 중 **14분54초(894초)**, 시간 초과 없음.
- 만기별: **D+3 6/7(85.7%)**, **D+1 7/14(50.0%)**. 서로 분리 집계하며 장기 숙달이나 공식 점수로 환산하지 않음.
- 유형별: 형용사 6/7, 문법 3/8, 경어 2/4, N2문법 2/2. 문항 수가 적은 하위 유형은 방향 신호로만 사용.
- `review_queue_id`·`source_attempt_id`·`due_interval`·문항 유형을 21건 모두 대조. 정상 제출된 해당 만기 21건만 결과·시간과 함께 `completed` 처리. 기존 이후 일정·기존 점수·복습 상태 보존.
- 오답 7·8·9·10·14·15·17·18만 새 D+1 **2026-08-30**, D+3 **2026-09-01**, D+7 **2026-09-05**에 등록: 총 24건. 모름은 없음.
- 시간은 오늘 신규 세션에 시험 타이머 894초만 기록: **14분54초**. DB 정수 필드 14분, 잔여54초는 요약·시험 notes에 보존. 해설 읽기·다른 학습시간은 미추정·미가산. 오늘 학습 종료 아님.
- 문항별 체류시간 합은 892초로 전체 타이머보다 2초 짧음. 제출값을 수정하지 않았으며 차이의 원인은 추정하지 않음.
- 원본 응답: `database/results/{TID}.json`. 합격 확률·숙달 스냅샷은 변경하지 않음.
- 형식 주의: 18번은 경어 용어를 직접 분류하는 **학습용 개념 확인**으로 실제 JLPT형 성취 근거에서 제외. 이후 문제는 문맥 빈칸·문장 배열·글의 흐름 등 공식 JLPT 형식 템플릿을 기본으로 사용.
"""
append_once("JLPT_STUDY_LOG.md",study)

err=f"""## 2026-08-29 — 만기 복습 1차 오답 8문항

자체 제작 만기 변형 재시험 13/21. D+3 6/7, D+1 7/14. 공식 시험과 분리하며 기존 점수·복습 상태를 변경하지 않음. 아래 오답만 새 D+1·D+3·D+7에 등록.

"""
for a in A:
    if a["state"] != "wrong": continue
    d=DETAILS[a["item_no"]]
    err += f"""### {a['item_no']}번 — {a['pattern']} ({a['due_interval']})

**카테고리: {a['category']}**

**원문**  
{a['question']}

**번역**  
{d['translation']}

**선택 → 정답**  
{a['selected_text']} → **{a['correct_text']}**

**완성 문장**  
{d['full']}

**접속·의미**  
{d['rule']}

**함정**  
{d['trap']} 선택 사실에 근거한 설명이며 실제 사고 과정은 확인하지 않음.

**유사 문형**  
{d['diff']}

**예문**  
{d['example']}

**다음 복습일**  
D+1 2026-08-30 · D+3 2026-09-01 · D+7 2026-09-05. 새 시도에 등록했으며 기존 이후 일정은 보존.

기존 만기 queue `{a['review_queue_id']}` / source attempt `{a['source_attempt_id']}` / due `{a['due_interval']}`. 문항 체류 {a['response_seconds']}초(순수 사고시간 아님).

"""
append_once("JLPT_ERROR_NOTE.md",err)

result={
 "test_id":TID,"inserted":existing is None,"attempts":len(saved),"completed_due_reviews":21,
 "due_split":{"D+3":"6/7","D+1":"7/14"},"new_reviews":len(new_reviews),
 "pending_due_today":con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date<='2026-08-29'").fetchone()[0],
 "new_D1":con.execute("""SELECT count(*) FROM review_queue r JOIN question_attempts q ON q.id=r.attempt_id WHERE q.test_id=? AND r.review_date='2026-08-30'""",(TID,)).fetchone()[0],
 "session_minutes_field":con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-29'").fetchone()[0],
 "session_exact_seconds":894,"integrity":"ok","protected_tables_unchanged":True,
}
print(json.dumps(result,ensure_ascii=False))
con.close()
