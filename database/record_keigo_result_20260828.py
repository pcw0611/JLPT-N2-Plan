"""Record the submitted keigo attempt, preserving full questions and exact choices."""
import json
import sqlite3
import statistics
from datetime import datetime, date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TID = 'keigo-basics-check-20260828'
source = ROOT / 'database/question_sets' / TID / 'questions.json'
definition = json.loads(source.read_text(encoding='utf-8'))
questions = definition['questions']
# User-submitted zero-based selections, states and measured dwell times.
submitted = [(0,'wrong',31),(0,'correct',23),(3,'correct',50),(3,'wrong',22),
             (0,'correct',7),(None,'unknown',22),(1,'wrong',13),(1,'correct',30)]
groups = {}
attempts = []
for i, (q, (selected, state, seconds)) in enumerate(zip(questions, submitted), 1):
    assert state == ('unknown' if selected is None else 'correct' if selected == q['answer'] else 'wrong')
    g = groups.setdefault(q['group'], dict(correct=0, total=0))
    g['total'] += 1
    g['correct'] += state == 'correct'
    attempts.append(dict(item_no=i, question_id=q['id'], item_type_id='grammar_form',
        category=['문법','문법형식 판단','경어',q['group'],q['sub']], question=q['q'], context=q['context'],
        choices=q['choices'], selected_index=selected, selected_text='分からない' if selected is None else q['choices'][selected],
        correct_index=q['answer'], correct_text=q['choices'][q['answer']], response_state=state, response_seconds=seconds))
payload = dict(test_id=TID, test_date='2026-08-28', title='경어 기초 선택형 확인 8문항',
    source_class='self_made', target_level='N3 기반·경어 입문', memory_timing='same_day_recognition',
    total_items=8, correct_items=4, unknown_items=1, unanswered_items=0, elapsed_seconds=199,
    time_limit_seconds=600, timed_out=False, groups=groups, wrong=[1,4,7], unknown=[6], unanswered=[], attempts=attempts,
    review_dates=[dict(interval='D+'+str(n), date=(date(2026,8,28)+timedelta(days=n)).isoformat()) for n in (1,3,7)],
    timing_note='시작 버튼부터 제출까지 경과시간. 문항별 시간은 해당 문항 화면 체류시간을 재방문 포함 합산한 값으로 순수 사고시간이 아님. 반올림 때문에 합계가 전체 시간과 다를 수 있음.')
assert len(questions) == len(attempts) == 8
assert [a['item_no'] for a in attempts if a['response_state']=='wrong'] == payload['wrong']
assert [a['item_no'] for a in attempts if a['response_state']=='unknown'] == payload['unknown']
assert sum(a['response_state']=='correct' for a in attempts)==4
assert sum(a['response_seconds'] for a in attempts)==198
assert [a['selected_text'] for a in attempts] == ['申しました','拝見しました','召し上がりました','ご覧になります','申します','分からない','いたします','A ご覧になりました ／ B 拝見しました']

traps = {
 1:'선생님의 말하기에 申しました를 선택. 言う 계열의 의미는 맞지만 자기 쪽을 낮추는 申す와 상대를 높이는 おっしゃる의 방향을 혼동했을 가능성.',
 4:'방문 문장에 ご覧になります를 선택. ご覧になる는 見る의 존경어이므로 방문이라는 동작 의미와 私라는 주어에 모두 맞지 않음. 단어 의미와 높임 방향을 함께 재확인할 필요가 있으나 실제 원인은 미확인.',
 6:'分からない를 명시. 丁寧語だけ라는 조건 또는 丁寧語와 존경·겸양 동사의 관계가 불확실했을 가능성. 특정 오답을 선택했다고 간주하지 않음.',
 7:'선생님의 する에 いたします를 선택. する 계열이라는 의미는 맞지만 자기 쪽을 낮추는 いたす와 상대를 높이는 なさる의 방향을 혼동했을 가능성.'}
raw = ROOT / 'database/results' / (TID+'.json')
notes = dict(source='자체 제작 당일 선택형 재인 확인시험; 공식 시험·공식 모의고사 아님',
    submitted_result=payload, question_definitions=questions, raw_result=raw.relative_to(ROOT).as_posix(),
    diagnostic_weight_note='기존 자체 제작 당일 문법 시험과 같은 0.25 참고값. 합격 확률 및 숙달 등급 변경에 사용하지 않음.',
    session_base_seconds=11543, session_increment_seconds=199, session_total_seconds=11742,
    session_integer_minutes=195, session_remainder_seconds=42,
    timing_caution='문항 체류시간 합 198초, 전체 199초. 반올림 차이 1초를 임의 배분하지 않음. 시작·종료 시각은 전달되지 않아 추정하지 않음.')

con = sqlite3.connect(ROOT / 'database/jlpt_learning.db')
con.row_factory = sqlite3.Row
con.execute('PRAGMA foreign_keys=ON')
protected = {t:[tuple(r) for r in con.execute('SELECT * FROM '+t+' ORDER BY id')] for t in ('mastery_snapshots','pass_probability_snapshots','study_intervals')}
old_reviews = {r['id']:tuple(r) for r in con.execute('SELECT * FROM review_queue')}
existing = con.execute('SELECT * FROM tests WHERE id=?',(TID,)).fetchone()
if existing is None:
    backup_dir=ROOT/'outputs/db_backups'
    backup_dir.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(backup_dir/('before-keigo-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.db')) as backup:
        con.backup(backup)
    with con:
        # Acquire the write lock before validating the time base.
        con.execute('BEGIN IMMEDIATE')
        session=con.execute('SELECT * FROM study_sessions WHERE session_date=?',(payload['test_date'],)).fetchone()
        assert session and session['verified_minutes']==192, 'Session timing changed; reconcile before adding.'
        previous=json.loads(con.execute("SELECT notes FROM tests WHERE id='n3-listening-order-time-20260828'").fetchone()[0])
        assert previous['session_total_seconds']==11543
        con.execute('''INSERT INTO tests (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,
          response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
          (TID,payload['test_date'],payload['title'],'self_made',payload['target_level'],'경어 기초·당일 재인; 공식 난이도 미검증',
           'same_day_recognition','multiple_choice',8,4,1,0,199,600,0.25,json.dumps(notes,ensure_ascii=False)))
        for a in attempts:
            cur=con.execute('''INSERT INTO question_attempts (test_id,item_no,item_type_id,level_label,response_state,
              response_seconds,selected_text,correct_text,trap_hypothesis,trap_confidence) VALUES (?,?,?,?,?,?,?,?,?,?)''',
              (TID,a['item_no'],'grammar_form',payload['target_level'],a['response_state'],a['response_seconds'],
               a['selected_text'],a['correct_text'],traps.get(a['item_no']),'low' if a['item_no']==6 else 'medium' if a['item_no'] in traps else None))
            if a['response_state'] in ('wrong','unknown'):
                for d in payload['review_dates']:
                    con.execute('INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,?)',
                        (cur.lastrowid,d['date'],d['interval'],'pending'))
        extra=f' [경어 결과 {TID}] 실제 결과 4/8, 오답 1·4·7, 모름 6. 기존 기록 192분 23초에 시험 타이머 199초만 추가하여 누적 195분 42초(3시간 15분 42초). 정수 분 필드 195, 잔여 42초는 tests.notes와 요약에 보존. 기존 시간에는 추정 구간이 포함됨. 해설 읽기·추가 학습·대기 시간 미가산. 오늘 학습 종료 아님.'
        con.execute('UPDATE study_sessions SET verified_minutes=195,summary=summary || ?,updated_at=CURRENT_TIMESTAMP WHERE session_date=?',(extra,payload['test_date']))
else:
    stored_notes=json.loads(existing['notes'])
    assert stored_notes['submitted_result']==payload, 'Existing result differs; refusing overwrite.'

# Re-read persisted DB content; retry must neither duplicate results nor reset review completion.
stored=json.loads(con.execute('SELECT notes FROM tests WHERE id=?',(TID,)).fetchone()[0])
assert stored['submitted_result']==payload and stored['question_definitions']==questions
saved=con.execute('SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no',(TID,)).fetchall()
assert len(saved)==8
for row,a in zip(saved,attempts):
    assert all(row[k]==a[k] for k in ('item_no','item_type_id','response_state','response_seconds','selected_text','correct_text'))
reviews=con.execute('''SELECT q.item_no,r.review_date,r.interval_label,r.status FROM review_queue r JOIN question_attempts q
  ON q.id=r.attempt_id WHERE q.test_id=? ORDER BY q.item_no,r.review_date''',(TID,)).fetchall()
assert len(reviews)==12
assert {(r['item_no'],r['review_date'],r['interval_label']) for r in reviews} == {(i,d['date'],d['interval']) for i in (1,4,6,7) for d in payload['review_dates']}
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
for t,before in protected.items():
    assert [tuple(r) for r in con.execute('SELECT * FROM '+t+' ORDER BY id')]==before
for r in con.execute('SELECT * FROM review_queue'):
    if r['id'] in old_reviews: assert tuple(r)==old_reviews[r['id']]

raw.parent.mkdir(parents=True,exist_ok=True)
if raw.exists(): assert json.loads(raw.read_text(encoding='utf-8'))==payload
else: raw.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

marker='<!-- '+TID+' -->'
def append_once(filename,text):
    path=ROOT/filename
    old=path.read_text(encoding='utf-8')
    if marker not in old: path.write_text(old.rstrip()+'\n\n'+marker+'\n'+text.strip()+'\n',encoding='utf-8')
    assert path.read_text(encoding='utf-8').count(marker)==1

summary='''## 2026-08-28 — 경어 기초 선택형 확인 8문항

- 시험 ID: `keigo-basics-check-20260828`. 사용자 제출 실제 결과, 자체 제작·당일 선택형 재인(`same_day_recognition`). N3 기반 경어 입문이며 공식 시험·공식 모의고사와 구분; 공식 N3 난이도 검증 자료 아님.
- 결과 4/8(50%): 오답 1·4·7, 모름 6, 미응답 0. 10분 제한 중 3분 19초 사용, 시간 초과 없음.
- 8문항의 상황·원문·선택지·정답·선택한 답·문항별 카테고리·시간을 DB `tests.notes.submitted_result` 및 `database/results/keigo-basics-check-20260828.json`에 보존. 제작 당시 전체 해설도 DB `tests.notes.question_definitions`에 보존. 응답 8건은 `question_attempts`에 저장.
- 시간: 기존 누적 기록 192분 23초 + 이번 타이머 199초 = 195분 42초(3시간 15분 42초). DB 정수 분 195, 잔여 42초는 notes·요약 보존. 기존 누적에는 추정 구간이 포함됨. 해설 확인·대기·추가 강의 시간을 추정하지 않았으며 오늘 학습 종료 아님.

| 영역 → 문제 유형 → 세부 유형 | 정답 | 오답 | 모름 | 정답률 | 문항 체류 평균 / 중앙 |
|---|---:|---:|---:|---:|---|
'''
for group,g in groups.items():
    subset=[a for a in attempts if a['category'][3]==group]
    times=[a['response_seconds'] for a in subset]
    summary+=f"| 문법 → 문법형식 판단 → 경어·{group} | {g['correct']}/{g['total']} | {sum(a['response_state']=='wrong' for a in subset)} | {sum(a['response_state']=='unknown' for a in subset)} | {100*g['correct']/g['total']:.1f}% | {statistics.mean(times):.1f}초 / {statistics.median(times):g}초 |\n"
summary+='''
- 강점 신호: 見る의 拝見する / ご覧になる 구별(2·8번), 식사의 召し上がる(3번), 자기소개 申します(5번). 맞혔다고 장기 숙달 완료로 간주하지 않음. 3번은 50초이지만 체류시간만으로 원인이나 자동화 정도를 확정하지 않음.
- 우선 약점: 1·7번은 동작 의미는 맞고 상대를 높이는 방향이 뒤집힘. 4번은 방문 대신 ご覧になる(보다)를 골라 동사 의미와 주체를 함께 재확인. 6번은 丁寧語だけ의 기능 구별을 모름으로 분리. 실제 오답 원인은 추정임.
- 각 경어 세부 유형은 1~3문항, 이전의 동일 조건 경어 기준선과 지연 복습 결과가 없음. 상승·하락·숙달 등급 및 D+1/3/7 유지율은 아직 판정하지 않음. 총 모름률 12.5%, 전체 대비 선택 후 오답률 37.5%(모름 제외 실제 선택 7개 중 오답 3개, 42.9%).
- 문항 체류시간 합 198초, 전체 타이머 199초: 반올림 차이 1초를 임의 보정하지 않음. 평균 24.75초, 중앙 22.5초; 정답 문항 평균 27.5초·중앙 26.5초, 오답 평균 22초·중앙 22초, 모름 22초. 이번 경어 입문에 별도 문항별 권장시간을 소급 적용하지 않음. 제한시간 미소진만으로 성급한 응답이라고 단정하지 않음.
- 5번 申す는 넓은 분류에서 겸양어이며 세부적으로 丁重語(謙譲語Ⅱ). です・ます의 丁寧語와 구분.
- 오답 1·4·7 + 모름 6 × D+1 2026-08-29 / D+3 2026-08-31 / D+7 2026-09-04 = 복습 12건 등록. 기존 복습 상태 유지, 알림 자동화는 생성하지 않음.
- 합격 확률과 내부 숙달 스냅샷은 변경하지 않음. 당일 소표본 정답률을 공식 점수나 합격 확률로 직접 환산하지 않음.
- 이번 요청의 DB·학습 기록·오답노트 반영 완료. 홈페이지 동기화는 이번 작업에서 실행하지 않음.
'''
append_once('JLPT_STUDY_LOG.md',summary)
errors='''## 2026-08-28 — 경어 기초 확인시험

자체 제작·당일 선택형 재인, 4/8(50%), 3분 19초. 오답 1·4·7, 모름 6, 미응답 없음. 공식 시험과 구분하며 합격 확률 변경 없음.
복습: 4문항 × D+1 2026-08-29 · D+3 2026-08-31 · D+7 2026-09-04, 총 12건 등록.

'''
for a,q in zip(attempts,questions):
    if a['response_state']=='correct': continue
    errors+=f"### {a['item_no']}번 — {'모름' if a['response_state']=='unknown' else '오답'}\n\n**카테고리: {' → '.join(a['category'])}**\n\n**문제 원문**\n\n{q['context']}\n\n{q['q']}\n\n"
    errors+='\n'.join(f'{j+1}. {c}' for j,c in enumerate(q['choices']))+'\n\n'
    errors+=f"**번역**\n\n{q['translation']}\n\n**선택 답 → 정답**\n\n{a['selected_text']} → **{a['correct_text']}**\n\n완성 문장: {q['completed']}\n\n**접속·의미**\n\n{q['rule']}\n\n**선택한 답에 따른 해석**\n\n{traps[a['item_no']]}\n\n**함정**\n\n{q['trap']}\n\n**유사 표현 차이**\n\n{q['difference']}\n\n**추가 예문**\n\n{q['example']}\n\n**다음 복습일**\n\nD+1 2026-08-29 · D+3 2026-08-31 · D+7 2026-09-04. 등록 완료; 완료 여부는 review_queue를 기준으로 확인.\n\n문항 체류시간 {a['response_seconds']}초(순수 사고시간 아님).\n\n"
append_once('JLPT_ERROR_NOTE.md',errors)
append_once('JLPT_DATABASE.md','''## 경어 확인시험 원문 보존 (2026-08-28)

`keigo-basics-check-20260828`부터 이 시험의 전체 제출 결과를 `tests.notes`의 JSON `submitted_result`에 저장했다. 문항 원문·상황·선택지·선택한 답·정답·카테고리를 포함한다. 제작 해설은 같은 JSON의 `question_definitions`에 보존한다. 독립 문제은행 테이블을 신설하거나 과거 시험의 누락 원문을 복구한 것은 아니다.
별도 원본 결과 파일: `database/results/keigo-basics-check-20260828.json`. 제작 당시 자료: `database/question_sets/keigo-basics-check-20260828/`. 제작 당시 `prepared_unattempted` 표시는 출제 시점 상태이며 실제 응시 여부의 기준은 `tests`다.
''')
print(json.dumps(dict(test_id=TID,inserted=existing is None,attempts=len(saved),reviews=len(reviews),
    review_statuses=sorted(set(r['status'] for r in reviews)),integrity='ok',protected_tables_unchanged=True,
    original_reviews_unchanged=True,full_content_verified=True,session_minutes=con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-28'").fetchone()[0]),ensure_ascii=False))
con.close()
