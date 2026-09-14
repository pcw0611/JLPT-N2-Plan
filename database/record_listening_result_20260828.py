"""Record the user-submitted result once; preserve existing tests and review states."""
import json
import sqlite3
import statistics
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'database/results/n3-listening-order-time-20260828.json'
p = json.loads(RAW.read_text(encoding='utf-8'))
tid = p['test_id']
attempts = p['attempts']
assert len(attempts) == p['total_items'] == 8
assert sum(a['state'] == 'correct' for a in attempts) == p['correct_items'] == 4
assert sum(a['response_seconds'] for a in attempts) == p['elapsed_seconds'] == 683
assert [a['item_no'] for a in attempts if a['state'] == 'wrong'] == p['wrong']
assert not any(a['audio_error'] for a in attempts), 'Audio errors require separate exclusion handling; refusing normal insertion.'
for a,q in zip(attempts,p['questions']):
    assert a['correct_text'] == q['c'][q['a']]
    assert (a['selected_text'] == a['correct_text']) == (a['state'] == 'correct')

traps = {
  2:'선택한 店のドアを開ける는 레지 확인 이후의 행동. その後で를 첫 행동과 구분하지 못했을 가능성. 어떤 표현을 못 들었는지는 미확인.',
  3:'선택한 新しいカードを受け取る는 신청서 작성과 학생증 제시 이후의 결과. 최종 목적과 먼저 해야 할 행동을 혼동했을 가능성.',
  7:'선택한 千八百円는 1200+600의 할인 전 합계. 성인 200엔 할인과 학생증 제시 후 중학생 400엔 가격을 최종 계산에 반영하지 못했을 가능성.',
  8:'선택한 今週の金曜日の午後六時는 반환 기한의 화요일과 별개인 금요일 영업 예외를 혼합한 답. 오후 6시는 맞지만 주·요일 조건을 잘못 연결했을 가능성.'
}
notes = {
 'source':'자체 제작 일본어 TTS 선택형; 공식 시험·공식 모의고사 아님',
 'raw_result':str(RAW.relative_to(ROOT)),
 'audio_error_items':[], 'audio_error_flags':{str(a['item_no']):a['audio_error'] for a in attempts},
 'timing_note':p['timing_note'],
 'timing_caution':'0초는 반올림된 선택 이벤트 시각이며 즉시 이해·성급한 답변의 증거가 아님. 오디오 시간은 반복 재생 포함 누적값이고 원본 음원 길이가 아님.',
 'replay_note':'1·6·7번은 2회 재생. 1회 집단 2/5, 2회 집단 2/3은 서로 다른 문항이므로 재생 효과나 첫 청취 정확도로 해석하지 않음.',
 'source_weight_note':'diagnostic_weight 0.3은 기존 자체 제작 기본값이며 확률 환산에 사용하지 않음.',
 'session_increment_seconds':683,
 'review_dates':p['review_dates']
}
con = sqlite3.connect(ROOT / 'database/jlpt_learning.db')
con.row_factory = sqlite3.Row
con.execute('PRAGMA foreign_keys=ON')
existing = con.execute('SELECT * FROM tests WHERE id=?',(tid,)).fetchone()
if existing is None:
    backup_dir = ROOT / 'outputs/db_backups'
    backup_dir.mkdir(parents=True,exist_ok=True)
    backup_path = backup_dir / ('before-listening-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.db')
    with sqlite3.connect(backup_path) as backup:
        con.backup(backup)
    with con:
        con.execute('''INSERT INTO tests
          (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
          (tid,p['test_date'],p['title'],'self_made_tts','N3','취약 유형 변형 연습','targeted_variant_practice','multiple_choice',8,4,0,0,683,960,0.3,json.dumps(notes,ensure_ascii=False)))
        for a in attempts:
            type_id = 'listening_task' if a['type']=='課題理解' else 'listening_point'
            cur=con.execute('''INSERT INTO question_attempts
              (test_id,item_no,item_type_id,level_label,response_state,response_seconds,audio_seconds,decision_seconds,play_count,selected_text,correct_text,trap_hypothesis,trap_confidence)
              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
              (tid,a['item_no'],type_id,'N3',a['state'],a['response_seconds'],a['audio_seconds'],a['decision_seconds'],a['play_count'],a['selected_text'],a['correct_text'],traps.get(a['item_no']),'medium' if a['state']=='wrong' else None))
            if a['state'] in ('wrong','unknown'):
                for d in p['review_dates']:
                    con.execute('INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,?)',(cur.lastrowid,d['date'],d['interval'],'pending'))
        session=con.execute('SELECT * FROM study_sessions WHERE session_date=?',(p['test_date'],)).fetchone()
        assert session is not None and session['verified_minutes']==181, 'Reconcile session timing before adding; base changed.'
        notes['session_base_minutes']=181
        notes['session_total_seconds']=181*60+683
        notes['session_integer_minutes']=192
        notes['session_remainder_seconds']=23
        con.execute('UPDATE tests SET notes=? WHERE id=?',(json.dumps(notes,ensure_ascii=False),tid))
        extra=' [청해 결과 '+tid+'] 사용자 전달 결과 4/8, 11분 23초 완료. 기존 기록 181분에 이번 시험 경과시간만 추가: 192분 23초. 정수 verified_minutes에는 192분, 잔여 23초는 이 요약과 시험 notes에 보존. 경어 학습·추가 해설 읽기·대기 시간은 완료 및 소요시간 미확인으로 미가산. 오늘 학습 종료 아님.'
        con.execute('UPDATE study_sessions SET verified_minutes=192,summary=summary || ?,updated_at=CURRENT_TIMESTAMP WHERE session_date=?',(extra,p['test_date']))
else:
    assert existing['correct_items']==4 and existing['elapsed_seconds']==683
    for a in attempts:
        stored=con.execute('SELECT * FROM question_attempts WHERE test_id=? AND item_no=?',(tid,a['item_no'])).fetchone()
        assert stored and all(stored[k]==a[k] for k in ('selected_text','correct_text','response_seconds','audio_seconds','decision_seconds','play_count'))
        assert stored['response_state']==a['state']

assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('SELECT count(*) FROM question_attempts WHERE test_id=?',(tid,)).fetchone()[0]==8
assert con.execute('SELECT count(*) FROM review_queue r JOIN question_attempts q ON q.id=r.attempt_id WHERE q.test_id=?',(tid,)).fetchone()[0]==12

type_stats=[]
for key in ('listening_task','listening_point'):
    current=[a for a in attempts if ('listening_task' if a['type']=='課題理解' else 'listening_point')==key]
    history=con.execute('''SELECT q.*,t.test_date FROM question_attempts q JOIN tests t ON t.id=q.test_id WHERE q.item_type_id=? ORDER BY t.test_date DESC,q.id DESC''',(key,)).fetchall()
    recent=history[:10]
    type_stats.append(dict(type=key,current_correct=2,current_total=4,mean=statistics.mean(a['response_seconds'] for a in current),median=statistics.median(a['response_seconds'] for a in current),audio=sum(a['audio_seconds'] for a in current),decision_mean=statistics.mean(a['decision_seconds'] for a in current),cumulative_correct=sum(a['response_state']=='correct' for a in history),cumulative_n=len(history),recent_correct=sum(a['response_state']=='correct' for a in recent),recent_n=len(recent)))

marker='<!-- '+tid+' -->'
def append_once(name,text):
    path=ROOT/name
    old=path.read_text(encoding='utf-8')
    if marker not in old:
        path.write_text(old.rstrip()+'\n\n'+marker+'\n'+text.strip()+'\n',encoding='utf-8')

summary='''## 2026-08-28 — N3 청해 행동 순서·숫자·시간 8문항

- 시험 ID: `n3-listening-order-time-20260828`
- 사용자 전달 실제 결과. 자체 제작 일본어 TTS 선택형·취약 유형 변형 연습. 공식 시험·공식 모의고사와 분리.
- 4/8 (50%), 오답 2·3·7·8, 모름 0, 미응답 0. 제한 16분 중 11분 23초 사용; 4분 37초 남음.
- `audio_error=false` 8문항: 보고된 음성 오류 없음. 별도 제외 문항 없음. 실제 소리 품질을 독립적으로 검증한 것은 아님.
- 원본: `database/results/n3-listening-order-time-20260828.json` (사용자 응답·측정값, 제작 문제의 선택지·대본·해설 보존).
- 오늘 누적: 기존 기록 181분 + 이번 시험 11분 23초 = 192분 23초(3시간 12분 23초). DB 정수 분 필드는 192, 잔여 23초는 요약과 시험 notes 보존. 추가 경어·해설 완료 또는 시간을 추정하지 않음. 오늘 종료 아님.

### 유형별 결과

| 유형 | 이번 | 문항 평균 / 중앙 | 누적 오디오 | 종료 후 선택 평균 | 기존 기록 포함 누적 | 최근 최대 10문항 |
|---|---|---|---|---|---|---|
'''
for s in type_stats:
    label='과제이해' if s['type']=='listening_task' else '포인트이해'
    summary+=f"| {label} | 2/4 (50%) | {s['mean']:g}초 / {s['median']:g}초 | {s['audio']}초 | {s['decision_mean']:g}초 | {s['cumulative_correct']}/{s['cumulative_n']} ({100*s['cumulative_correct']/s['cumulative_n']:.1f}%) | {s['recent_correct']}/{s['recent_n']} |\n"
summary+='''
- 이번 각 유형은 4문항으로 방향 신호에 불과함. 누적·최근 값에는 즉시 복습, 지연 복습, 재생 횟수와 수준이 다른 시험, 과거 미응답이 섞임. 직접적인 숙달 점수나 공식 점수로 해석하지 않음.
- 맞힌 항목: 1 행동 순서(2회 재생), 4 변경 후 행동(1회), 5 추가 부수(1회), 6 최종 약속 시간(2회). 숫자 조건을 전혀 못 듣는 것은 아님. 특히 5번은 추가량을 한 번 듣고 정답.
- 반복 약점: 2·3번에서 후속 행동/목적을 첫 행동으로 선택. 7번은 할인 전 합계 1800엔 선택. 8번은 금요일을 기한으로 선택해 요일 예외를 혼합했을 가능성.
- 재생 1회 집단 2/5, 2회 집단 2/3. 다른 문항 집단이므로 재생 효과를 비교하거나 첫 청취 점수로 계산하지 않음.
- 문항 시간 합 683초, 누적 오디오 392초(6분 32초), 재생 총 11회. 나머지 시간에는 읽기·이동·대기 등이 섞여 모두 사고시간이라고 단정할 수 없음.
- 종료 후 선택 시간은 0~4초. 0초는 반올림과 선택 이벤트 측정의 결과여서 즉시 이해 또는 성급한 답변을 뜻하지 않음. 기존 5~15초 권장치는 공식 제한이 아니며 이번 이벤트 측정과 단순 비교하지 않음.
- 8/26 최초 혼합 청해 0/2와 이번 4/8은 개선의 방향 신호이나 표본·조건이 달라 성장 폭 확정 불가. 숙달 등급·합격 가능성 수치는 이번 결과로 환산하거나 변경하지 않음.
- 이번 시험은 과거 오답의 동일 항목 D+1 이행으로 연결하지 않음. 기존 대기 복습은 그대로 유지.

### 복습

- 2·3·7·8번 각각 D+1 2026-08-29, D+3 2026-08-31, D+7 2026-09-04: 총 12건 등록.
- 인물·수량·요일을 바꾼 일본어 선택형 청해로 재시험. 첫 행동과 후속 행동, 할인 전·후 가격, 기한 요일과 예외 영업일을 따로 메모.
- 다음 학습은 오답 해설 확인 → 경어 기초 확인 → N2 입문. 청해 20~30분 계획 전체를 완료했다고 추정하지 않음.
- 홈페이지는 이번 요청에서 동기화하지 않음. `HANDOFF.md`의 청해 미완료·누적 181분 표기는 이 기록보다 오래된 상태.
'''
append_once('JLPT_STUDY_LOG.md',summary)

translations={
2:['안내: 빵집에서 점장과 여자가 이야기합니다. 여자는 이후 먼저 무엇을 합니까?','남: 10분 뒤에 개점이네요. 빵을 봉투에 넣는 작업은 끝났나요?','여: 네. 다음에는 테이블을 닦겠습니다.','남: 그건 제가 할게요. 계산대 돈이 충분한지 먼저 확인해 주세요.','여: 네. 그 뒤에 문을 열면 될까요?','남: 네, 부탁합니다.'],
3:['안내: 도서관 접수처에서 남자와 직원이 이야기합니다. 남자는 먼저 무엇을 해야 합니까?','남: 처음 왔는데 책을 빌리고 싶습니다. 학생증은 가지고 있습니다.','여: 그러면 이 신청서에 이름과 주소를 써 주세요. 학생증은 다 쓴 뒤 보여 주세요.','남: 그러면 카드를 받을 수 있는 거군요.','여: 네. 카드를 받으면 2층에서 책을 골라 주세요.'],
7:['안내: 미술관 접수처에서 남자가 입장료를 묻습니다. 두 사람의 입장료는 합해서 얼마입니까?','남: 성인 한 명과 중학생 한 명입니다. 얼마인가요?','여: 성인은 1,200엔, 중학생은 600엔입니다. 오늘은 성인만 200엔 할인됩니다.','남: 중학생도 학생증으로 할인되나요?','여: 네. 학생증이 있으면 400엔입니다.','남: 가지고 있습니다. 여기 있습니다.','여: 감사합니다. 그러면 할인된 요금으로 부탁합니다.'],
8:['안내: 도서관에서 남자가 책 반환에 대해 묻습니다. 남자는 언제까지 책을 반납해야 합니까?','남: 이 책 반납일은 다음 주 월요일이지요?','여: 보통은 그렇지만, 다음 주 월요일은 휴관일이라 화요일까지면 괜찮습니다.','남: 밤 8시까지 여나요?','여: 아니요. 8시까지 여는 건 금요일뿐입니다. 화요일은 오후 6시까지입니다. 반납함이 없으니 문을 연 시간에 창구로 와 주세요.']
}
complete={2:'女の人は、まずレジのお金を確認します。',3:'男の人は、まず申込書に名前と住所を書かなければなりません。',7:'二人の入場料は、合わせて千四百円です。',8:'男の人は、来週の火曜日の午後六時までに本を返さなければなりません。'}
error_text='''## 2026-08-28 — N3 청해 행동 순서·숫자·시간

자체 제작 일본어 TTS, 4/8 (50%), 11분 23초. 실제 선택 답 수신. 음성 오류 보고 없음. 오답 2·3·7·8, 모름·미응답 없음. 공식 시험과 분리; 합격 확률 변경 없음.
복습 12건 등록: 오답 4개 × D+1 2026-08-29 · D+3 2026-08-31 · D+7 2026-09-04.

'''
for a in attempts:
    if a['state']!='wrong':continue
    i=a['item_no'];q=p['questions'][i-1]
    category='과제이해(課題理解)' if a['type']=='課題理解' else '포인트이해(ポイント理解)'
    error_text+=f"### {i}번 — {a['subtype']}\n\n**카테고리: 청해 → {category} → {a['subtype']}**\n\n**문제 원문**\n\n{a['question']}\n\n"
    for role,line in q['s']:
        error_text+='> '+{'n':'案内','m':'男','f':'女'}[role]+': '+line+'  \n'
    error_text+='\n'+ '\n'.join(f"{j+1}. {c}" for j,c in enumerate(a['choices']))+'\n\n'
    error_text+='**한국어 번역**\n\n'+'  \n'.join(translations[i])+'\n\n'
    error_text+=f"**선택 답 → 정답**\n\n{a['selected_text']} → **{a['correct_text']}**\n\n완성 문장: {complete[i]}\n\n"
    error_text+=f"**접속·의미**\n\n{q['rule']}\n\n**선택 답의 함정**\n\n{traps[i]} 듣지 못한 표현과 실제 원인은 아직 미확인.\n\n**유사 표현 차이**\n\n{q['diff']}\n\n**추가 예문**\n\n{q['ex']}\n\n"
    error_text+=f"**다음 복습일**\n\nD+1 2026-08-29 · D+3 2026-08-31 · D+7 2026-09-04. 모두 pending.\n\n측정: 문항 {a['response_seconds']}초 / 누적 오디오 {a['audio_seconds']}초 / 종료 후 선택 {a['decision_seconds']}초 / 재생 {a['play_count']}회. 0초 선택시간은 이해 속도로 해석하지 않음.\n\n"
append_once('JLPT_ERROR_NOTE.md',error_text)

for name in ('JLPT_STUDY_LOG.md','JLPT_ERROR_NOTE.md'):
    assert (ROOT/name).read_text(encoding='utf-8').count(marker)==1
print(json.dumps({'test_id':tid,'inserted':existing is None,'items':8,'review_rows':12,'integrity':'ok','type_stats':type_stats,'session':dict(con.execute('SELECT verified_minutes,summary FROM study_sessions WHERE session_date=?',(p['test_date'],)).fetchone())},ensure_ascii=False,indent=2))
con.close()
