"""Add actionable error-prevention feedback without changing scores or queues."""
import json, sqlite3
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'database/jlpt_learning.db'
TID='due-review-20260829-grammar-21'
MARKER='<!-- due-review-20260829-grammar-21-prevention-feedback -->'
feedback={
 "7":{"procedure":"`前に`를 보면 먼저 앞 동작이 아직 안 일어났는지 확인하고 사전형을 만든다: 行きます → 行く → 行く前に.","check":"‘하기 전’ 앞에 사전형을 넣었나?"},
 "8":{"procedure":"시간 표지부터 본다. `今`과 `後で`가 함께 있으므로 지금 진행 중이며 `Vているところ`를 고른다.","check":"지금 직전·진행 중·직후 중 어느 시점인가?"},
 "9":{"procedure":"`Nの（　）に`에서 진행 중 사건에 방해가 끼어들면 `最中に`를 우선 후보로 둔다.","check":"무언가 한창일 때 다른 사건이 끼어들었나?"},
 "10":{"procedure":"`にくい` 앞에서는 동사를 반드시 ます형으로 바꾼 뒤 ます를 뺀다: 分かります → 分かり＋にくい.","check":"て형이 아니라 ます형 어간에 붙였나?"},
 "14":{"procedure":"먼저 `누가 시키고 누가 행동하는가`를 화살표로 잡는다: 先生は → 学生に → 書かせる. 주어가 강제로 당할 때만 사역수동을 쓴다.","check":"주어가 시키는 사람인가, 억지로 하게 된 사람인가?"},
 "15":{"procedure":"활용 전에 형용사 종류부터 판정한다. 静か는 な형용사이므로 과거 보통형 `だった`; 그 뒤에 명사를 바로 붙인다.","check":"이 단어가 い형용사인지 な형용사인지 먼저 확인했나?"},
 "17":{"procedure":"행동 주체를 먼저 찾는다. `私が` 윗사람에게 가므로 나를 낮추는 겸양어 `伺う`; 상대가 이동할 때만 `いらっしゃる`.","check":"지금 높여야 할 사람이 움직이나, 내가 움직이나?"},
 "18":{"procedure":"특별 동사와 `お〜になる`를 먼저 제거한 뒤 평범한 `です／ます` 문장을 찾는다. 다만 이후 채점 문제에서는 이런 용어 분류형을 공식형 성취에서 제외한다.","check":"특별 존경·겸양 표현 없이 단순 です／ます만 썼나?"},
}

con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
row=con.execute('select notes from tests where id=?',(TID,)).fetchone(); assert row
notes=json.loads(row['notes'])
inserted='prevention_feedback' not in notes
if inserted:
    bdir=ROOT/'outputs/db_backups'; bdir.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(bdir/('before-prevention-feedback-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.db')) as b: con.backup(b)
    notes['prevention_feedback']=feedback
    with con: con.execute('update tests set notes=? where id=?',(json.dumps(notes,ensure_ascii=False),TID))
assert json.loads(con.execute('select notes from tests where id=?',(TID,)).fetchone()[0])['prevention_feedback']==feedback
assert con.execute('select correct_items from tests where id=?',(TID,)).fetchone()[0]==13
assert con.execute("select count(*) from review_queue r join question_attempts q on q.id=r.attempt_id where q.test_id=?",(TID,)).fetchone()[0]==24
assert con.execute('pragma integrity_check').fetchone()[0]=='ok' and not con.execute('pragma foreign_key_check').fetchall()

p=ROOT/'JLPT_ERROR_NOTE.md'; old=p.read_text(encoding='utf-8')
text='''## 2026-08-29 — 같은 오답을 막는 다음번 풀이 절차

규칙을 아는 것과 시험장에서 고르는 것은 별개다. 다음 복습부터 아래 확인 절차를 답 선택 전에 적용한다.

| 문항 | 다음번 풀이 절차 | 정답 직전 체크 |
|---:|---|---|
'''
for no,v in feedback.items(): text+=f"| {no} | {v['procedure']} | **{v['check']}** |\n"
text+='''
### 공통 루틴

1. **주어와 행동 주체**를 먼저 찾는다. 특히 경어·사역은 인물 관계를 화살표로 표시한다.
2. `今・前に・最中` 같은 **시간 신호**를 표시한다.
3. 접속 문제는 뜻으로 찍기 전에 **사전형·ている형·ます형 어간·だった** 중 요구 형태를 만든다.
4. 답을 누르기 직전 “이 선택지를 넣으면 문장 전체가 실제로 무슨 뜻인가?”를 한 번 읽는다.

풀이시간을 무조건 늘리라는 뜻은 아니다. 위 네 단계가 자동화되도록 D+1·D+3·D+7에서 반복한다.
'''
if MARKER not in old: p.write_text(old.rstrip()+'\n\n'+MARKER+'\n'+text,encoding='utf-8')
assert p.read_text(encoding='utf-8').count(MARKER)==1
print(json.dumps({'inserted':inserted,'feedback_items':len(feedback),'scores_changed':False,'queues_changed':False,'integrity':'ok'}))
con.close()
