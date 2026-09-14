"""Record this user's submitted due-review result once, preserving older queues."""
import json
import sqlite3
import statistics
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TID = 'due-review-20260828-11'
questions = json.loads((ROOT/'database/question_sets'/TID/'questions.json').read_text(encoding='utf-8'))['questions']
# Exact user-submitted selections (zero based), response times, audio times and decision times.
submitted = [(1,19,None,None),(3,53,None,None),(0,54,None,None),(2,34,None,None),
             (1,38,None,None),(3,37,None,None),(1,41,None,None),(2,78,33,5),
             (1,86,36,5),(0,34,29,2),(1,39,33,2)]
expected_mappings = [(49,48),(58,69),(67,75),(68,76),(69,77),(70,79),(71,82),(52,60),(55,61),(59,72),(60,73)]
assert [(q['queue'],q['source']) for q in questions] == expected_mappings
assert len(questions) == len(submitted) == 11
attempts=[]
groups={}
for i,(q,(selected,seconds,audio,decision)) in enumerate(zip(questions,submitted),1):
    state='correct' if selected==q['a'] else 'wrong'
    attempts.append(dict(item_no=i,review_queue_id=q['queue'],source_attempt_id=q['source'],
        item_type_id=q['itemType'],type=q['type'],category=q['category'],subtype=q['sub'],state=state,
        question=q['q'],form_hint=q.get('hint'),choices=q['c'],selected_text=q['c'][selected],
        correct_text=q['c'][q['a']],response_seconds=seconds,audio_seconds=audio,decision_seconds=decision,
        play_count=1 if audio is not None else None,audio_error=False,visited=True))
    g=groups.setdefault(q['type'],dict(correct=0,total=0,excluded=0))
    g['total']+=1
    g['correct']+=state=='correct'
payload=dict(test_id=TID,test_date='2026-08-28',due_date='2026-08-28',title='만기 D+1 복습 — 형용사 7·청해 4',
    source_class='자체 제작',target_level='N3 기반',memory_timing='D+1 변형 재시험',total_items=11,
    correct_items=7,unknown_items=0,unanswered_items=0,valid_items=11,valid_correct_items=7,
    excluded_items=[],elapsed_seconds=513,time_limit_seconds=960,timed_out=False,groups=groups,
    wrong=[7,8,9,10],unknown=[],unanswered=[],attempts=attempts,
    review_dates=[dict(interval='D+1',date='2026-08-29'),dict(interval='D+3',date='2026-08-31'),dict(interval='D+7',date='2026-09-04')],
    mapping_note='기존 review_queue 항목별 1대1 변형 문제. 원문을 확인할 수 없는 과제이해 2개는 동일 문제 유형의 새로운 문항이며 동일 원문 재시험은 아님.',
    timing_note='시작 버튼부터 제출까지 경과시간. 문항 시간은 화면 체류시간이며 순수 사고시간이 아님. 청해는 마지막 재생 종료부터 최종 답 선택까지 별도 측정. 미방문 문항 시간은 null. 음성 오류·중단은 정상 청해 표본 및 만기 완료 판정에서 제외.')
assert [a['item_no'] for a in attempts if a['state']=='wrong']==[7,8,9,10]
assert sum(a['state']=='correct' for a in attempts)==7
assert sum(a['response_seconds'] for a in attempts)==513
assert [a['selected_text'] for a in attempts]==['静かな','静かではありませんでした','便利でした','長くありませんでした','ではありません','ではありませんでした','静かかった','コーヒーを入れる','三階へ行く','十二部','明日の四時半ごろ']

traps={
    7:'静かかった를 선택. な형용사의 보통형 과거를 い형용사의 かった로 만든 형태 혼동 가능성. 정답은 静かだった이며 실제 판단 과정은 미확인.',
    8:'コーヒーを入れる를 선택. 손님이 온 뒤의 후속 행동을 지금 첫 행동으로 선택한 사실을 확인. 先に와 来てから의 시간 관계를 놓쳤을 가능성.',
    9:'三階へ行く를 선택. 최종 목적지를 우선 행동으로 선택한 사실을 확인. その前に 및 작성→결제→카드 수령→이동의 순서 유지가 어려웠을 가능성.',
    10:'十二部를 선택. 총 필요량 12를 추가량으로 선택. 이미 인쇄한 8부를 빼는 조건 또는 あと何部의 의미를 놓쳤을 가능성.'}
raw=ROOT/'database/results'/(TID+'.json')
if raw.exists():
    assert json.loads(raw.read_text(encoding='utf-8'))==payload,'Different existing result: do not overwrite.'
notes=dict(submitted_result=payload,question_definitions=questions,raw_result=raw.relative_to(ROOT).as_posix(),
    source_note='자체 제작 일본어 선택형·청해 TTS D+1 변형 재시험. 공식 시험·공식 모의고사와 분리.',
    mapping_note='이번 8·9번은 기존 원문 미확인. 각각 queue 52/source 60, queue 55/source 61과 연결한 동일 과제이해 유형의 새 변형 문항. 동일 원문 유지율로 해석하지 않음.',
    session_base_seconds=13983,session_increment_seconds=513,session_total_seconds=14496,
    session_integer_minutes=241,session_remainder_seconds=36,
    timing_note='기존 233분03초+이번 타이머 513초=241분36초. 기존 누적에는 사용자 추정 및 확인된 대화 경과 구간이 포함됨. 시작·종료 시각, 해설 읽기, 추가 학습시간은 추정하지 않음.',
    diagnostic_weight_note='자체 제작 표적 시험 참고값 0.25. 소표본이므로 공식 점수·합격 확률·숙달 등급으로 환산하지 않음.')

con=sqlite3.connect(ROOT/'database/jlpt_learning.db')
con.row_factory=sqlite3.Row
con.execute('PRAGMA foreign_keys=ON')
old_reviews={r['id']:dict(r) for r in con.execute('SELECT * FROM review_queue')}
protected={t:[tuple(r) for r in con.execute('SELECT * FROM '+t+' ORDER BY id')]
           for t in ('mastery_snapshots','pass_probability_snapshots','study_intervals')}
old_tests={r['id']:tuple(r) for r in con.execute('SELECT * FROM tests WHERE id<>?',(TID,))}
old_attempts={r['id']:tuple(r) for r in con.execute('SELECT * FROM question_attempts WHERE test_id<>?',(TID,))}
existing=con.execute('SELECT * FROM tests WHERE id=?',(TID,)).fetchone()
if existing is None:
    backup_dir=ROOT/'outputs/db_backups'
    backup_dir.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(backup_dir/('before-due-review-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.db')) as backup:
        con.backup(backup)
    with con:
        con.execute('BEGIN IMMEDIATE')
        session=con.execute("SELECT * FROM study_sessions WHERE session_date='2026-08-28'").fetchone()
        assert session['verified_minutes']==233 and TID not in session['summary'],'Time base changed; reconcile first.'
        previous=json.loads(con.execute("SELECT notes FROM tests WHERE id='keigo-basics-check-20260828'").fetchone()[0])
        lecture=con.execute("SELECT duration_seconds FROM study_intervals WHERE source='chat_confirmed' AND session_date='2026-08-28' AND started_at='2026-08-28T15:35:07+09:00'").fetchall()
        assert len(lecture)==1 and previous['session_total_seconds']+lecture[0][0]==13983
        for a in attempts:
            r=con.execute('SELECT r.*,q.item_type_id FROM review_queue r JOIN question_attempts q ON q.id=r.attempt_id WHERE r.id=?',(a['review_queue_id'],)).fetchone()
            assert r and r['attempt_id']==a['source_attempt_id'] and r['item_type_id']==a['item_type_id']
            assert r['review_date']==payload['due_date'] and r['interval_label']=='D+1' and r['status']=='pending'
            assert a['visited'] and not a['audio_error'] and a['state'] in ('correct','wrong','unknown')
        con.execute('''INSERT INTO tests (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,
            response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(TID,payload['test_date'],payload['title'],'self_made','N3 기반',
            '기초 형용사·청해 표적 변형; 공식 난이도 미검증','D+1_variant','multiple_choice',11,7,0,0,513,960,0.25,json.dumps(notes,ensure_ascii=False)))
        for a in attempts:
            cur=con.execute('''INSERT INTO question_attempts (test_id,item_no,item_type_id,level_label,response_state,
                response_seconds,audio_seconds,decision_seconds,play_count,selected_text,correct_text,trap_hypothesis,trap_confidence)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',(TID,a['item_no'],a['item_type_id'],'N3 기반',a['state'],a['response_seconds'],
                a['audio_seconds'],a['decision_seconds'],a['play_count'],a['selected_text'],a['correct_text'],traps.get(a['item_no']),
                'medium' if a['item_no'] in traps else None))
            new_id=cur.lastrowid
            changed=con.execute("UPDATE review_queue SET status='completed',result_state=?,result_seconds=? WHERE id=? AND attempt_id=? AND status='pending'",
                (a['state'],a['response_seconds'],a['review_queue_id'],a['source_attempt_id']))
            assert changed.rowcount==1
            if a['state'] in ('wrong','unknown'):
                for d in payload['review_dates']:
                    con.execute('INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,?)',(new_id,d['date'],d['interval'],'pending'))
        extra=f' [{TID}] 실제 만기 D+1 변형 복습 7/11, 513초. 이전 경어 이후 N2 영상 2241초는 study_intervals의 chat_confirmed 및 학습 로그에서 무휴식 시청 확인 완료: 기존 기록 233분03초. 이번 타이머만 가산하여 241분36초(4시간1분36초), 정수 241분·잔여36초. 기존 누적에는 추정 구간 포함. 해설·추가 학습시간 미가산. 만기11건 완료, 오답4개 새 복습12건, 기존 미래 일정 보존. 오늘 학습 종료 아님.'
        con.execute("UPDATE study_sessions SET verified_minutes=241,summary=summary || ?,updated_at=CURRENT_TIMESTAMP WHERE session_date='2026-08-28'",(extra,))
else:
    assert json.loads(existing['notes'])['submitted_result']==payload,'Existing test differs: refusing overwrite.'

saved=con.execute('SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no',(TID,)).fetchall()
assert len(saved)==11
for a,r in zip(attempts,saved):
    assert r['response_state']==a['state']
    for k in ('item_no','item_type_id','response_seconds','audio_seconds','decision_seconds','play_count','selected_text','correct_text'):
        assert r[k]==a[k],(k,r[k],a[k])
for a in attempts:
    r=con.execute('SELECT * FROM review_queue WHERE id=?',(a['review_queue_id'],)).fetchone()
    assert r['attempt_id']==a['source_attempt_id'] and r['status']=='completed'
    assert r['result_state']==a['state'] and r['result_seconds']==a['response_seconds']
reviews=con.execute('''SELECT q.item_no,r.review_date,r.interval_label FROM review_queue r JOIN question_attempts q
    ON q.id=r.attempt_id WHERE q.test_id=?''',(TID,)).fetchall()
assert {(r['item_no'],r['review_date'],r['interval_label']) for r in reviews}=={(i,d['date'],d['interval']) for i in (7,8,9,10) for d in payload['review_dates']}
assert len(reviews)==12
changed_ids={a['review_queue_id']:a for a in attempts}
for r in con.execute('SELECT * FROM review_queue'):
    if r['id'] not in old_reviews: continue
    expected=old_reviews[r['id']].copy()
    if r['id'] in changed_ids:
        a=changed_ids[r['id']]
        expected.update(status='completed',result_state=a['state'],result_seconds=a['response_seconds'])
    assert dict(r)==expected,'Unrelated review changed'
for t,rows in protected.items():
    assert [tuple(r) for r in con.execute('SELECT * FROM '+t+' ORDER BY id')]==rows
assert {r['id']:tuple(r) for r in con.execute('SELECT * FROM tests WHERE id<>?',(TID,))}==old_tests
assert {r['id']:tuple(r) for r in con.execute('SELECT * FROM question_attempts WHERE test_id<>?',(TID,))}==old_attempts
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert json.loads(con.execute('SELECT notes FROM tests WHERE id=?',(TID,)).fetchone()[0])==notes
raw.parent.mkdir(parents=True,exist_ok=True)
if not raw.exists(): raw.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

marker='<!-- '+TID+' -->'
def append_once(filename,text):
    p=ROOT/filename
    old=p.read_text(encoding='utf-8')
    if marker not in old: p.write_text(old.rstrip()+'\n\n'+marker+'\n'+text.strip()+'\n',encoding='utf-8')
    assert p.read_text(encoding='utf-8').count(marker)==1

summary='''## 2026-08-28 — 만기 D+1 복습: 형용사 7·청해 4

- 시험 ID: `due-review-20260828-11`. 사용자 제출 실제 결과, 자체 제작 D+1 변형 선택형 재시험(청해 일본어 TTS). 공식 시험·공식 모의고사와 분리.
- 결과 **7/11(63.6%)**, 오답 7·8·9·10, 모름·미응답·음성 오류·중단 없음. 제한 16분 중 **8분33초(513초)**, 시간 초과 없음. 음성 오류 없음은 사용자 제출값이며 소리 품질의 독립 검증을 뜻하지 않음.
- `review_queue_id`/`source_attempt_id` 및 문항 유형 대조 완료. 정상 제출한 만기 11건만 `completed`와 문항별 결과·시간으로 갱신. 완료는 이번 복습 이행이며 숙달·졸업을 뜻하지 않음.
- 8·9번(52/60, 55/61)은 기존 원문이 없는 과제이해 2개와 연결한 **동일 유형의 새 변형 문항**. 동일 원문 재시험이나 동일 문항 유지율로 표현하지 않음. 이전의 미응답을 이번 응답으로 덮어쓰지 않고 새 시도로 저장.
- 원본 응답: `database/results/due-review-20260828-11.json`. 전체 제출값·제작 문제·대본·해설·복습 연결은 DB `tests.notes`에 보존.
- 시간: 기존 기록 233분03초 + 타이머 513초 = **241분36초(4시간1분36초)**. 정수 분 필드 241, 잔여36초는 notes·요약에 보존. 이전 누적에는 추정 구간이 포함됨. 해설 읽기·추가 학습·대기·작업 시간 미가산. 오늘 학습 종료 아님.

| 유형 | 이번 정답 | 정답률 | 문항 체류 평균 / 중앙 | 오디오 합계 | 종료 후 선택 평균 |
|---|---:|---:|---|---|---|
'''
for key,g in groups.items():
    subset=[a for a in attempts if a['type']==key]
    times=[a['response_seconds'] for a in subset]
    audio=[a['audio_seconds'] for a in subset if a['audio_seconds'] is not None]
    decision=[a['decision_seconds'] for a in subset if a['decision_seconds'] is not None]
    label={'文法':'형용사 활용','課題理解':'과제이해','ポイント理解':'포인트이해'}[key]
    summary+=f"| {label} | {g['correct']}/{g['total']} | {100*g['correct']/g['total']:.1f}% | {statistics.mean(times):.1f}초 / {statistics.median(times):g}초 | {str(sum(audio))+'초' if audio else '해당 없음'} | {str(round(statistics.mean(decision),1))+'초' if decision else '해당 없음'} |\n"
summary+='''
- 청해 전체 1/4(25%), 모두 1회 재생. 문항 체류 합 513초, 청해 오디오 131초, 종료 후 선택 합 14초. 체류시간에는 읽기·대기·이동이 섞이며 순수 사고시간이 아님. 시간 제한 미소진만으로 성급한 응답이라고 판단하지 않음.
- 형용사 활용은 표적 복습 6/7 회복 신호. 静か／便利／安全／きれい의 정중형 구별은 이번 문항에서 정답, な형용사 보통형 과거 수식 `静かだった町`는 반복 약점. 이번 문항에 맞혔다고 장기 숙달로 간주하지 않음.
- 청해 8·9번은 후속 행동·최종 목적지를 첫 행동으로, 10번은 총량을 추가량으로 선택. 11번은 변경 후 방문 시각 정답. 과제이해 3개·포인트이해 1개는 방향 신호이며 이전 다른 문제와 직접 성장 폭 비교하지 않음.
- 오답 7·8·9·10 각각 D+1 **8/29**, D+3 **8/31**, D+7 **9/4**: 새 복습 **12건** 등록. 기존 이후 일정은 모두 보존. 등록 직후 오늘까지 만기 대기 **0건**, 내일 대기 **34건**(기존30+새4).
- 합격 확률·내부 숙달 스냅샷은 변경하지 않음. 별도 알림 자동화나 홈페이지 동기화는 실행하지 않음.
'''
append_once('JLPT_STUDY_LOG.md',summary)
errors='''## 2026-08-28 — 만기 D+1 변형 복습 오답

자체 제작 7/11(63.6%), 8분33초. 오답 7·8·9·10, 모름·미응답·음성 오류 없음. 8·9번은 이전 원문이 없는 동일 과제이해 유형의 새 변형 문제. 공식 시험 및 동일 원문 유지율과 구분. 아래 해설을 제공했지만 해설 학습 완료·시간은 미확인.

'''
for a,q in zip(attempts,questions):
    if a['state']=='correct': continue
    errors+=f"### {a['item_no']}번 — 오답\n\n**카테고리: {a['category']}**\n\n**문제 원문**\n\n{q['q']}\n\n"
    if q.get('hint'): errors+=q['hint']+'\n\n'
    errors+='\n'.join(f'{j+1}. {v}' for j,v in enumerate(q['c']))+'\n\n'
    if q.get('s'):
        errors+='**청해 대본**\n\n'+'\n\n'.join({'n':'안내','f':'여자','m':'남자'}[role]+': '+text for role,text in q['s'])+'\n\n'
    errors+=f"**번역**\n\n{q['ko']}\n\n**선택 → 정답·완성 문장**\n\n{a['selected_text']} → **{a['correct_text']}**\n\n{q['full']}\n\n**접속·의미**\n\n{q['rule']}\n\n**함정**\n\n{q['trap']}\n\n**선택한 답에 따른 원인 추정**\n\n{traps[a['item_no']]} 실제 사고 과정은 확인하지 않음.\n\n**유사 표현 차이**\n\n{q['diff']}\n\n**추가 예문**\n\n{q['ex']}\n\n**다음 복습일**\n\nD+1 2026-08-29 · D+3 2026-08-31 · D+7 2026-09-04. 이번 새 시도에 연결해 등록했으며 기존 미래 일정 보존.\n\n"
    errors+=f"기존 만기 queue {a['review_queue_id']} / source attempt {a['source_attempt_id']}. 문항 체류 {a['response_seconds']}초"
    if a['audio_seconds'] is not None: errors+=f", 오디오 {a['audio_seconds']}초, 종료 후 선택 {a['decision_seconds']}초, 재생 {a['play_count']}회"
    errors+=' (순수 사고시간 아님).\n\n'
append_once('JLPT_ERROR_NOTE.md',errors)
print(json.dumps(dict(test_id=TID,inserted=existing is None,attempts=len(saved),completed_due_reviews=11,
    new_reviews=len(reviews),due_pending=con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date<='2026-08-28'").fetchone()[0],
    tomorrow_pending=con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date='2026-08-29'").fetchone()[0],
    session_minutes=con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-28'").fetchone()[0],
    original_future_reviews_unchanged=True,protected_tables_unchanged=True,integrity='ok'),ensure_ascii=True))
con.close()
