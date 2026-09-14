"""Persist the user's N2 001-008 result once without re-counting the lecture."""
import json
import sqlite3
import statistics
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TID='n2-grammar-001-008-check-20260828'
questions=json.loads((ROOT/'database/question_sets'/TID/'questions.json').read_text(encoding='utf-8'))['questions']
# Exact submitted zero-based choices and measured dwell seconds.
submitted=[(0,61),(0,44),(2,14),(1,84),(1,42),(3,57),(0,19),(1,29)]
assert len(questions)==len(submitted)==8
attempts=[]
groups={}
for i,(q,(selected,seconds)) in enumerate(zip(questions,submitted),1):
    state='correct' if selected==q['a'] else 'wrong'
    attempts.append(dict(item_no=i,question_id=q['id'],item_type_id='grammar_form',category=q['category'],
        practice_type=q['type'],pattern=q['pattern'],state=state,question=q['q'],choices=q['c'],
        selected_text=q['c'][selected],correct_text=q['c'][q['a']],response_seconds=seconds,visited=True))
    g=groups.setdefault(q['type'],dict(correct=0,total=0));g['total']+=1;g['correct']+=state=='correct'
payload=dict(test_id=TID,test_date='2026-08-28',title='N2 문법 001~008 강의 후 확인 8문항',source_class='자체 제작',
    target_level='N2 입문',memory_timing='강의 직후 선택형 재인',total_items=8,correct_items=6,unknown_items=0,
    unanswered_items=0,elapsed_seconds=350,time_limit_seconds=480,timed_out=False,groups=groups,wrong=[1,5],
    unknown=[],unanswered=[],attempts=attempts,
    review_dates=[dict(interval='D+1',date='2026-08-29'),dict(interval='D+3',date='2026-08-31'),dict(interval='D+7',date='2026-09-04')],
    source_note='기록된 강의 문형 001~008을 대상으로 만든 자체 제작 확인 문제. 교재 원문·강의 문제를 복제한 시험이나 공식 N2 진단 아님. 文法形式/意味確認은 이번 연습의 하위 구분으로 모두 grammar_form에 연결.',
    timing_note='開始する부터 제출까지. 문항 시간은 화면 체류시간이며 순수 사고시간 아님. 미방문 문항은 null. 강의 시청시간은 이 타이머에 포함되지 않으며 별도 사용자 확인 없이는 추정하지 않음.')
assert [a['item_no'] for a in attempts if a['state']=='wrong']==[1,5]
assert sum(a['state']=='correct' for a in attempts)==6
assert sum(a['response_seconds'] for a in attempts)==350
assert groups=={'意味確認':{'correct':3,'total':5},'文法形式':{'correct':3,'total':3}}
assert [a['selected_text'] for a in attempts]==['旅行をあきらめてから、何日も悩んだ。','あまり','一方だ','内容を確認する → 署名する','親切なら、説明が分かりやすくなる。','引き受けたからには、最後までやり通すつもりだ。','うちに','正午（12時）']
raw=ROOT/'database/results'/(TID+'.json')
if raw.exists():assert json.loads(raw.read_text(encoding='utf-8'))==payload,'Conflicting result; do not overwrite.'
lecture_path=ROOT/'database/results/n2-grammar-001-008-lecture-completed-20260828.json'
lecture_bytes=lecture_path.read_bytes()
lecture=json.loads(lecture_bytes)
assert lecture['duration_seconds']==1260 and lecture['session_total_seconds']==15965
traps={1:'原文の悩む→あきらめるに対し、あきらめてから悩む選択肢を選択。선택한 답에서 과정과 결과의 순서가 뒤집힌 사실 확인. あげく의 관계 해석 또는 선택지 어휘·접속 해석 중 실제 원인은 미확인. 이전 청해 오답과 동일 원인으로 확정하지 않음.',
       5:'추가 관계 うえに를 조건 관계 なら로 바꾼 선택지를 선택. 원문에 있는 두 장점을 조건·변화로 읽은 결과. うえに의 의미 또는 선택지의 なら・なる 해석 중 실제 원인은 미확인.'}
notes=dict(submitted_result=payload,question_definitions=questions,raw_result=raw.relative_to(ROOT).as_posix(),
    classification_note='Self-made, same-day recognition after a lecture. Not an official exam or D+1 retention test.',
    session_base_seconds=15965,session_increment_seconds=350,session_total_seconds=16315,
    session_integer_minutes=271,session_remainder_seconds=55,
    lecture_minutes_already_recorded=21,lecture_added_again=False,
    timing_note='Add only 350 exam seconds to the existing 15965 seconds. No inferred explanation or lecture time.',
    interpretation_note='Form selection 3/3; meaning recognition 3/5. Small immediate sample; no mastery or pass-probability update.')

con=sqlite3.connect(ROOT/'database/jlpt_learning.db')
con.row_factory=sqlite3.Row
con.execute('PRAGMA foreign_keys=ON')
protected={t:[tuple(r) for r in con.execute('SELECT * FROM '+t+' ORDER BY id')]
    for t in ('mastery_snapshots','pass_probability_snapshots','study_intervals','item_types')}
old_tests={r['id']:tuple(r) for r in con.execute('SELECT * FROM tests WHERE id<>?',(TID,))}
old_attempts={r['id']:tuple(r) for r in con.execute('SELECT * FROM question_attempts WHERE test_id<>?',(TID,))}
old_reviews={r['id']:tuple(r) for r in con.execute('SELECT * FROM review_queue')}
existing=con.execute('SELECT notes FROM tests WHERE id=?',(TID,)).fetchone()
if existing is None:
    backup_dir=ROOT/'outputs/db_backups'
    backup_dir.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(backup_dir/('before-n2-check-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.db')) as backup:
        con.backup(backup)
    with con:
        con.execute('BEGIN IMMEDIATE')
        session=con.execute("SELECT * FROM study_sessions WHERE session_date='2026-08-28'").fetchone()
        assert session['verified_minutes']==266 and TID not in session['summary']
        assert lecture['activity_id'] in session['summary']
        con.execute('''INSERT INTO tests (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,
            response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (TID,payload['test_date'],payload['title'],'self_made','N2 입문','입문 문형 확인; 공식 난이도 미검증',
             'same_day_recognition','multiple_choice',8,6,0,0,350,480,0.25,json.dumps(notes,ensure_ascii=False)))
        for a in attempts:
            cur=con.execute('''INSERT INTO question_attempts (test_id,item_no,item_type_id,level_label,response_state,
                response_seconds,selected_text,correct_text,trap_hypothesis,trap_confidence) VALUES (?,?,?,?,?,?,?,?,?,?)''',
                (TID,a['item_no'],'grammar_form','N2 입문',a['state'],a['response_seconds'],a['selected_text'],a['correct_text'],
                 traps.get(a['item_no']),'medium' if a['item_no'] in traps else None))
            if a['state'] in ('wrong','unknown'):
                for d in payload['review_dates']:
                    con.execute('INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,?)',
                        (cur.lastrowid,d['date'],d['interval'],'pending'))
        extra=f' [{TID}] N2 문법001~008 강의 직후 확인 6/8. 오답1·5, 모름·미응답 없음. 기존266분05초+시험350초=271분55초(4시간31분55초). 강의21분은 이미 반영되어 재가산하지 않음. 해설시간 미가산. 새복습6건, 기존 결과·복습 상태 보존. 오늘 종료 아님.'
        con.execute("UPDATE study_sessions SET verified_minutes=271,summary=summary || ?,updated_at=CURRENT_TIMESTAMP WHERE session_date='2026-08-28'",(extra,))
else:
    assert json.loads(existing['notes'])['submitted_result']==payload,'Existing result differs.'

saved=con.execute('SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no',(TID,)).fetchall()
assert len(saved)==8
for row,a in zip(saved,attempts):
    assert row['response_state']==a['state']
    for k in ('item_no','item_type_id','response_seconds','selected_text','correct_text'):
        assert row[k]==a[k]
reviews=con.execute('''SELECT q.item_no,r.review_date,r.interval_label FROM review_queue r
    JOIN question_attempts q ON q.id=r.attempt_id WHERE q.test_id=?''',(TID,)).fetchall()
assert len(reviews)==6
assert {(r['item_no'],r['review_date'],r['interval_label']) for r in reviews}=={(i,d['date'],d['interval']) for i in (1,5) for d in payload['review_dates']}
for t,rows in protected.items():
    assert [tuple(r) for r in con.execute('SELECT * FROM '+t+' ORDER BY id')]==rows
assert {r['id']:tuple(r) for r in con.execute('SELECT * FROM tests WHERE id<>?',(TID,))}==old_tests
assert {r['id']:tuple(r) for r in con.execute('SELECT * FROM question_attempts WHERE test_id<>?',(TID,))}==old_attempts
for r in con.execute('SELECT * FROM review_queue'):
    if r['id'] in old_reviews:assert tuple(r)==old_reviews[r['id']]
stored=json.loads(con.execute('SELECT notes FROM tests WHERE id=?',(TID,)).fetchone()[0])
assert all(stored[k]==v for k,v in notes.items())
assert lecture_path.read_bytes()==lecture_bytes
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
if not raw.exists():raw.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

marker='<!-- '+TID+' -->'
def append_once(filename,text):
    path=ROOT/filename
    old=path.read_text(encoding='utf-8')
    if marker not in old:path.write_text(old.rstrip()+'\n\n'+marker+'\n'+text.strip()+'\n',encoding='utf-8')
    assert path.read_text(encoding='utf-8').count(marker)==1

summary='''## 2026-08-28 — N2 문법001~008 강의 후 확인시험

- 시험 ID: `n2-grammar-001-008-check-20260828`. 사용자 제출 실제 결과, 자체 제작·강의 직후 선택형 재인(`same_day_recognition`). 교재 원문 시험·공식 시험·공식 모의고사·D+1 유지율과 구분.
- 결과 **6/8(75%)**, 오답1·5, 모름0, 미응답0. 제한8분 중 **5분50초(350초)** 사용, 시간 초과 없음.
- 문법형식 선택3/3(100%)과 의미 확인3/5(60%)는 이번 연습의 하위 구분. DB 유형은 모두 grammar_form이며 공식 별도 문제 유형으로 신설하지 않음.

| 연습 구분 | 정답 | 체류 평균 | 체류 중앙 |
|---|---:|---:|---:|
'''
for group,g in groups.items():
    seconds=[a['response_seconds'] for a in attempts if a['practice_type']==group]
    summary+=f"| {group} | {g['correct']}/{g['total']} | {statistics.mean(seconds):.1f}초 | {statistics.median(seconds):g}초 |\n"
summary+='''
- 오답1번: 고민→포기의 순서를 포기→고민으로 뒤집은 답 선택. 오답5번: 추가를 조건으로 바꾼 답 선택. 문형·선택지 어휘·접속 중 실제 혼동 원인은 미확인. 청해의 순서 오답과 같은 원인으로 단정하지 않음.
- 맞힌 문형: あまり・一方だ・たうえで・うえは・ないうちに・おきに. 특히4번은 확인→서명 순서를 정답으로 선택했으므로 모든 순서 관계를 이해하지 못한다고 일반화하지 않음.
- 4번84초는 이번8문항 중 가장 긴 체류시간. 체류시간만으로 어휘 부족이나 순수 사고시간을 확정하지 않음. 전체 문항 시간 합350초, 평균43.75초, 중앙43초. 별도 권장시간을 소급 적용하지 않음.
- 문형당1문항, 강의 직후 재인 표본. 정답6개를 장기 숙달 완료로 처리하지 않으며 합격 확률·내부 등급을 변경하지 않음.
- 시간: 기존266분05초+시험350초=**271분55초(4시간31분55초)**. DB 정수271분, 잔여55초는 notes·요약에 보존. 사용자 확인 강의21분은 기존 누적에 이미 포함되어 추가 가산하지 않음. 해설·대기·추가 학습시간 미가산. 기존 누적에는 추정 구간 포함. 오늘 종료 아님.
- 오답1·5 각각 D+1 **2026-08-29**, D+3 **2026-08-31**, D+7 **2026-09-04**: 새복습6건 등록. 기존 시험·응답·복습 상태 및 강의 활동 원본 보존. 등록 직후 오늘 만기0건, 내일37건(기존35+새2).
- 전체 제출값: `database/results/n2-grammar-001-008-check-20260828.json`. 문제·선택지·정답·선택답·제작 해설은 tests.notes에도 보존. 홈페이지 동기화·알림 자동화는 실행하지 않음.
'''
append_once('JLPT_STUDY_LOG.md',summary)

errors='''## 2026-08-28 — N2 문법001~008 오답 해설

자체 제작 강의 직후 재인 6/8(75%), 5분50초. 오답1·5, 모름·미응답 없음. 공식 시험 및 D+1 유지율과 분리. 해설 제공과 해설 학습 완료는 별개이며 해설시간 미가산.

'''
for a,q in zip(attempts,questions):
    if a['state']=='correct':continue
    errors+=f"### {a['item_no']}번 — {a['pattern']}\n\n**카테고리: {a['category']}**\n\n**문제 원문**\n\n{q['q']}\n\n"
    errors+='\n'.join(f'{i+1}. {choice}' for i,choice in enumerate(q['c']))+'\n\n'
    errors+=f"**번역**\n\n{q['ko']}\n\n**선택 → 정답**\n\n{a['selected_text']} → **{a['correct_text']}**\n\n완성 문장: {q['full']}\n\n"
    errors+=f"**접속·의미**\n\n{q['rule']}\n\n**함정**\n\n{q['trap']}\n\n**선택 결과에 따른 원인 추정**\n\n{traps[a['item_no']]}\n\n"
    errors+=f"**유사 문형 차이**\n\n{q['diff']}\n\n**추가 예문**\n\n{q['ex']}\n\n**다음 복습일**\n\nD+1 2026-08-29 · D+3 2026-08-31 · D+7 2026-09-04. 새 시도에 연결해 등록, 기존 일정 보존.\n\n문항 체류시간 {a['response_seconds']}초(순수 사고시간 아님).\n\n"
append_once('JLPT_ERROR_NOTE.md',errors)
print(json.dumps(dict(test_id=TID,inserted=existing is None,attempts=len(saved),new_reviews=len(reviews),
    old_records_preserved=True,lecture_not_counted_twice=True,integrity='ok',
    session_minutes=con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-28'").fetchone()[0],
    due_pending=con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date<='2026-08-28'").fetchone()[0],
    tomorrow_pending=con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date='2026-08-29'").fetchone()[0])))
con.close()
