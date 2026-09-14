"""Record the second 2026-08-29 due-review submission once."""
from __future__ import annotations
import json, sqlite3, statistics
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'database/jlpt_learning.db'
TID='due-review-20260829-mixed-16'
Q=json.loads((ROOT/'database/question_sets'/TID/'questions.json').read_text(encoding='utf-8'))['questions']

# selected choice index (or unknown), response seconds, audio seconds, decision seconds, play count
SUB=[
 (3,81,None,None,None),(2,112,None,None,None),(1,39,24,2,1),(2,80,29,0,1),
 (1,33,None,None,None),('unknown',41,None,None,None),(1,61,28,2,1),(2,78,None,None,None),
 (2,77,26,13,1),(0,71,28,0,1),(2,53,27,3,1),(2,59,27,0,1),
 (0,35,26,3,1),(1,62,29,0,1),(0,67,40,0,2),(2,36,2,13,1),
]
assert len(Q)==len(SUB)==16
attempts=[]; groups={}
for i,(x,(sel,sec,audio,decision,plays)) in enumerate(zip(Q,SUB),1):
    state='unknown' if sel=='unknown' else ('correct' if sel==x['a'] else 'wrong')
    selected='分からない' if sel=='unknown' else x['c'][sel]
    a=dict(item_no=i,review_queue_id=x['queue'],source_attempt_id=x['source'],due_interval=x['due_interval'],
           item_type_id=x['itemType'],is_official_type=x['isOfficialType'],type=x['type'],category=x['category'],subtype=x['sub'],
           state=state,question=x['q'],choices=x['c'],selected_text=selected,correct_text=x['c'][x['a']],
           response_seconds=sec,audio_seconds=audio,decision_seconds=decision,play_count=plays,audio_error=False,visited=True)
    attempts.append(a)
    g=groups.setdefault(x['type'],dict(correct=0,total=0,excluded=0));g['total']+=1;g['correct']+=state=='correct'

review_dates=[dict(interval='D+1',date='2026-08-30'),dict(interval='D+3',date='2026-09-01'),dict(interval='D+7',date='2026-09-05')]
payload=dict(test_id=TID,test_date='2026-08-29',due_date='2026-08-29',title='만기 복습 2차 — 어휘·독해·청해 16문항',
 source_class='자체 제작',target_level='N3 기반·N2 입문',memory_timing='D+3 8문항·D+1 8문항 변형 재시험',
 total_items=16,correct_items=12,unknown_items=1,unanswered_items=0,valid_items=16,valid_correct_items=12,
 elapsed_seconds=985,time_limit_seconds=1440,timed_out=False,groups=groups,wrong=[1,8,11],unknown=[6],unanswered=[],
 attempts=attempts,review_dates=review_dates,
 mapping_note='2026-08-29 남은 만기 review_queue 16건과 source_attempt_id·due_interval을 1대1 연결한 변형 문제. D+3 8건·D+1 8건. 16번 표현 듣기는 학습용 비공식 유형.',
 timing_note='開始する부터 제출까지 타이머. 청해는 재생시간과 마지막 재생 종료 후 선택시간을 별도 측정. 음성 오류·미응답·중단은 만기 완료 판정에서 제외.')

assert sum(a['response_seconds'] for a in attempts)==985
assert [a['item_no'] for a in attempts if a['state']=='wrong']==[1,8,11]
assert [a['item_no'] for a in attempts if a['state']=='unknown']==[6]
assert sum(a['state']=='correct' for a in attempts if a['due_interval']=='D+3')==5
assert sum(a['state']=='correct' for a in attempts if a['due_interval']=='D+1')==7
assert groups=={
 '言い換え類義':{'correct':0,'total':1,'excluded':0},'短文主張理解':{'correct':1,'total':1,'excluded':0},
 'ポイント理解':{'correct':3,'total':4,'excluded':0},'課題理解':{'correct':6,'total':6,'excluded':0},
 '漢字読み':{'correct':1,'total':1,'excluded':0},'文脈語彙':{'correct':0,'total':1,'excluded':0},
 '短文内容理解':{'correct':0,'total':1,'excluded':0},'表現の聞き取り':{'correct':1,'total':1,'excluded':0}}

traps={
 1:'`準備に時間がかからない`를 선택. 適した를 상황·목적 적합성보다 준비 편의성으로 해석한 선택이며 실제 판단 과정은 미확인.',
 6:'分からない 선택. 改善의 읽기는 맞혔지만 문맥 속 의미·용법 또는 선택지 어휘 중 어디가 막혔는지는 미확인.',
 8:'현재 상태 `にぎやかでした`를 선택. 질문의 以前·본문의 十年前보다 마지막 현재 문장 `今は…にぎやか`에 답을 맞춘 선택과 일치하며 실제 판단 과정은 미확인.',
 11:'`千六百円`을 선택. 성인 할인 후 1000엔과 학생 원가 600엔의 합과 일치하여 학생증 할인 후 400엔을 적용하지 않았을 가능성. 실제 계산 과정은 미확인.',
}
raw=ROOT/'database/results'/f'{TID}.json'
notes=dict(submitted_result=payload,question_definitions=Q,raw_result=raw.relative_to(ROOT).as_posix(),
 source_note='자체 제작 만기 변형 재시험. 공식 시험·공식 모의고사와 분리. 16번 표현 듣기는 학습용 비공식 유형.',
 format_note='1~15번은 공식 JLPT식 선택형 템플릿. 6번은 제출 원문상 공식형 형식이나 기존 전역 item_types의 context_vocabulary 메타데이터(is_official_type=0)는 과거 기록 보존을 위해 변경하지 않음. 16번만 명시적 표현 듣기 비공식 유형.',
 due_split={'D+3':{'correct':5,'total':8},'D+1':{'correct':7,'total':8}},
 timing_note='기존 시험 타이머 894초+이번 985초=정확한 시험 타이머 누적 1879초(31분19초). 사용자 보고 개인 공부 약180분과 합산한 오늘 표시는 약211분19초. 해설·기타 시간 미추정.',
 diagnostic_note='공식 성적·합격 확률·기존 숙달 스냅샷으로 직접 환산하지 않음.')

con=sqlite3.connect(DB);con.row_factory=sqlite3.Row;con.execute('pragma foreign_keys=on')
old_reviews={r['id']:dict(r) for r in con.execute('select * from review_queue')}
protected={t:[tuple(r) for r in con.execute(f'select * from {t} order by id')] for t in ('mastery_snapshots','pass_probability_snapshots','study_intervals','item_types')}
old_tests={r['id']:tuple(r) for r in con.execute('select * from tests where id<>?',(TID,))}
old_attempts={r['id']:tuple(r) for r in con.execute('select * from question_attempts where test_id<>?',(TID,))}
existing=con.execute('select * from tests where id=?',(TID,)).fetchone()
if existing is None:
    bdir=ROOT/'outputs/db_backups';bdir.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(bdir/('before-due-review-mixed16-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.db')) as b: con.backup(b)
    with con:
        con.execute('begin immediate')
        sess=con.execute("select * from study_sessions where session_date='2026-08-29'").fetchone()
        assert sess['verified_minutes']==194 and sess['has_untracked_activity']==1 and TID not in sess['summary']
        assert '[due-review-20260829-grammar-21]' in sess['summary'] and '[personal-study-20260829-user-report]' in sess['summary']
        for a in attempts:
            r=con.execute('''select r.*,q.item_type_id from review_queue r join question_attempts q on q.id=r.attempt_id where r.id=?''',(a['review_queue_id'],)).fetchone()
            assert r and r['attempt_id']==a['source_attempt_id'] and r['review_date']=='2026-08-29'
            assert r['interval_label']==a['due_interval'] and r['status']=='pending' and r['item_type_id']==a['item_type_id']
            assert a['visited'] and not a['audio_error'] and a['state'] in ('correct','wrong','unknown')
        con.execute('''insert into tests(id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
          values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(TID,'2026-08-29',payload['title'],'self_made','N3 기반·N2 입문','만기 D+3·D+1 표적 변형; 공식 난이도 미검증',payload['memory_timing'],'multiple_choice',16,12,1,0,985,1440,.2,json.dumps(notes,ensure_ascii=False)))
        for a in attempts:
            cur=con.execute('''insert into question_attempts(test_id,item_no,item_type_id,level_label,response_state,response_seconds,audio_seconds,decision_seconds,play_count,selected_text,correct_text,trap_hypothesis,trap_confidence)
              values(?,?,?,?,?,?,?,?,?,?,?,?,?)''',(TID,a['item_no'],a['item_type_id'],'N3 기반·N2 입문',a['state'],a['response_seconds'],a['audio_seconds'],a['decision_seconds'],a['play_count'],a['selected_text'],a['correct_text'],traps.get(a['item_no']),'medium' if a['item_no'] in traps else None))
            new_attempt=cur.lastrowid
            changed=con.execute('''update review_queue set status='completed',result_state=?,result_seconds=? where id=? and attempt_id=? and review_date='2026-08-29' and interval_label=? and status='pending' ''',(a['state'],a['response_seconds'],a['review_queue_id'],a['source_attempt_id'],a['due_interval']))
            assert changed.rowcount==1
            if a['state'] in ('wrong','unknown'):
                for d in review_dates: con.execute("insert into review_queue(attempt_id,review_date,interval_label,status) values(?,?,?,'pending')",(new_attempt,d['date'],d['interval']))
        extra=f' [{TID}] 자체 제작 만기2차 12/16, D+3 5/8·D+1 7/8, 타이머985초. 정상응답16건 완료, 오답3·모름1 새복습12건. 16번 표현듣기 비공식 분리. 정확한 시험 타이머 누적31분19초; 개인공부 약180분 포함 오늘 약211분19초. 해설·기타 시간 미가산. 오늘 만기0건, 학습 종료 아님.'
        con.execute("update study_sessions set verified_minutes=211,summary=summary||?,updated_at=current_timestamp where session_date='2026-08-29'",(extra,))
else:
    assert json.loads(existing['notes'])['submitted_result']==payload

saved=list(con.execute('select * from question_attempts where test_id=? order by item_no',(TID,)));assert len(saved)==16
for a,r in zip(attempts,saved):
    assert r['response_state']==a['state']
    for k in ('item_no','item_type_id','response_seconds','audio_seconds','decision_seconds','play_count','selected_text','correct_text'): assert r[k]==a[k],(k,r[k],a[k])
for a in attempts:
    r=con.execute('select * from review_queue where id=?',(a['review_queue_id'],)).fetchone()
    assert r['attempt_id']==a['source_attempt_id'] and r['status']=='completed' and r['interval_label']==a['due_interval']
    assert r['result_state']==a['state'] and r['result_seconds']==a['response_seconds']
new_reviews=list(con.execute('''select q.item_no,r.review_date,r.interval_label from review_queue r join question_attempts q on q.id=r.attempt_id where q.test_id=?''',(TID,)))
expected={(i,d['date'],d['interval']) for i in (1,6,8,11) for d in review_dates}
assert {(r['item_no'],r['review_date'],r['interval_label']) for r in new_reviews}==expected and len(new_reviews)==12
target={a['review_queue_id']:a for a in attempts}
for r in con.execute('select * from review_queue'):
    if r['id'] not in old_reviews: continue
    e=old_reviews[r['id']].copy()
    if r['id'] in target:
        a=target[r['id']];e.update(status='completed',result_state=a['state'],result_seconds=a['response_seconds'])
    assert dict(r)==e,f'unrelated review changed {r["id"]}'
for t,rows in protected.items(): assert [tuple(r) for r in con.execute(f'select * from {t} order by id')]==rows
assert {r['id']:tuple(r) for r in con.execute('select * from tests where id<>?',(TID,))}==old_tests
assert {r['id']:tuple(r) for r in con.execute('select * from question_attempts where test_id<>?',(TID,))}==old_attempts
assert con.execute('pragma integrity_check').fetchone()[0]=='ok' and not con.execute('pragma foreign_key_check').fetchall()
if raw.exists(): assert json.loads(raw.read_text(encoding='utf-8'))==payload
else: raw.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

marker=f'<!-- {TID} -->'
def append_once(name,text):
    p=ROOT/name;old=p.read_text(encoding='utf-8')
    if marker not in old:p.write_text(old.rstrip()+'\n\n'+marker+'\n'+text.strip()+'\n',encoding='utf-8')
    assert p.read_text(encoding='utf-8').count(marker)==1

audio=[a for a in attempts if a['audio_seconds'] is not None]
study=f'''## 2026-08-29 — 만기 복습 2차: 어휘·독해·청해 16문항

- `{TID}` 사용자 제출 실제 결과. 자체 제작 만기 변형 재시험이며 공식 시험·공식 모의고사와 분리.
- 전체 **12/16(75.0%)**, 오답1·8·11, `分からない`6, 미응답·음성 오류·중단0. 제한24분 중 **16분25초(985초)**, 시간 초과 없음.
- 만기별 **D+3 5/8(62.5%)**, **D+1 7/8(87.5%)**. 별도 집계하며 공식 점수·합격 확률로 환산하지 않음.
- 유형: 과제이해6/6, 포인트이해3/4, 유의표현0/1, 한자읽기1/1, 문맥어휘0/1, 단문주장1/1, 단문내용0/1, 표현듣기1/1.
- 16번 표현 듣기1/1은 학습용 비공식 유형으로 과제·포인트이해와 분리. 1~15번은 공식 JLPT식 선택형 템플릿이지만 문제 출처는 자체 제작.
- `review_queue_id`·`source_attempt_id`·`due_interval`·문항 유형 16건 대조. 정상 제출16건만 결과·시간과 함께 완료 처리. 기존 이후 일정·점수·복습 상태 보존.
- 오답1·8·11 및 모름6만 D+1 **8/30**, D+3 **9/1**, D+7 **9/5** 새 복습12건 등록. 처리 후 오늘 만기 대기0건.
- 청해11문항 모두 음성 오류 없음으로 제출. 오디오 합 **{sum(a['audio_seconds'] for a in audio)}초**, 마지막 재생 종료 후 선택 합 **{sum(a['decision_seconds'] for a in audio)}초**, 재생 합 **{sum(a['play_count'] for a in audio)}회**. 소리 품질의 독립 검증은 아님.
- 시간: 기존 시험 타이머14분54초+이번16분25초=정확한 시험 타이머31분19초. 사용자 보고 개인 공부 약180분 포함 오늘 **약3시간31분19초**. DB 정수211분, 잔여19초 보존. 해설·다른 학습시간 미가산. 오늘 종료 아님.
- 원본 `database/results/{TID}.json`. 합격확률·숙달 스냅샷·item_types 전역 메타데이터 미변경.
'''
append_once('JLPT_STUDY_LOG.md',study)

errors=f'''## 2026-08-29 — 만기 복습 2차 오답·모름 4문항

자체 제작 만기 변형 12/16. D+3 5/8, D+1 7/8. 오답1·8·11, 모름6. 공식 시험과 분리하며 기존 점수·복습 상태를 변경하지 않음.

'''
for a,x in zip(attempts,Q):
    if a['state'] not in ('wrong','unknown'):continue
    errors+=f'''### {a['item_no']}번 — {'오답' if a['state']=='wrong' else '分からない'} · {x['sub']} ({a['due_interval']})

**카테고리: {x['category']}**

**원문**

{x['q']}

'''
    if x.get('s'):
        errors+='**청해 대본**\n\n'+'\n\n'.join({'n':'안내','m':'남자','f':'여자'}[r]+': '+t for r,t in x['s'])+'\n\n'
    errors+=f'''**번역·정답 근거**

{x['ko']}

**선택 → 정답**

{a['selected_text']} → **{a['correct_text']}**

**접속·의미**

{x['rule']}

**함정·선택 분석**

{x['trap']} {traps[a['item_no']]}

**유사 표현·유형 차이**

{x['diff']}

**추가 예문**

{x['ex']}

**다음에는 이렇게 풀기**

{x['procedure']}

**정답 직전 체크**

{x['check']}

**다음 복습일**

D+1 2026-08-30 · D+3 2026-09-01 · D+7 2026-09-05. 새 시도에 등록, 기존 이후 일정 보존.

기존 queue `{a['review_queue_id']}` / source attempt `{a['source_attempt_id']}` / due `{a['due_interval']}`. 문항 체류 {a['response_seconds']}초''' + (f", 오디오 {a['audio_seconds']}초, 종료 후 선택 {a['decision_seconds']}초, 재생 {a['play_count']}회" if a['audio_seconds'] is not None else '') + ' (순수 사고시간 아님).\n\n'
append_once('JLPT_ERROR_NOTE.md',errors)

result=dict(test_id=TID,inserted=existing is None,attempts=16,completed_due_reviews=16,due_split={'D+3':'5/8','D+1':'7/8'},new_reviews=12,
 pending_due_today=con.execute("select count(*) from review_queue where status='pending' and review_date<='2026-08-29'").fetchone()[0],
 session_minutes_field=con.execute("select verified_minutes from study_sessions where session_date='2026-08-29'").fetchone()[0],
 display_total='약 3시간31분19초',protected_tables_unchanged=True,integrity='ok')
print(json.dumps(result,ensure_ascii=False));con.close()
