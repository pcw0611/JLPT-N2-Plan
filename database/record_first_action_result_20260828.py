"""Record the submitted four-item correction practice once; keep prior results intact."""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TID='listening-first-action-20260828-4'
questions=json.loads((ROOT/'database/question_sets'/TID/'questions.json').read_text(encoding='utf-8'))['questions']
# User-submitted selection index, dwell seconds, audio seconds, decision seconds, play count.
submitted=[(1,77,5,8,2),(0,18,4,5,1),(3,56,47,0,2),(1,58,43,1,2)]
attempts=[]
groups={}
assert len(questions)==len(submitted)==4
for i,(q,(selection,seconds,audio,decision,plays)) in enumerate(zip(questions,submitted),1):
    state='correct' if selection==q['a'] else 'wrong'
    attempts.append(dict(item_no=i,question_id=q['id'],item_type_id=q['itemType'],is_official_type=q['official'],
        type=q['type'],category=q['category'],state=state,question=q['q'],choices=q['c'],selected_text=q['c'][selection],
        correct_text=q['c'][q['a']],response_seconds=seconds,audio_seconds=audio,decision_seconds=decision,
        play_count=plays,audio_error=False,visited=True))
    g=groups.setdefault(q['type'],dict(correct=0,total=0,excluded=0))
    g['total']+=1
    g['correct']+=state=='correct'
payload=dict(test_id=TID,test_date='2026-08-28',title='청해 표현 인식·첫 행동 교정 4문항',source_class='자체 제작 TTS',
    target_level='N3 기반·기초 교정',memory_timing='설명 직후 교정 연습',total_items=4,correct_items=3,unknown_items=0,
    unanswered_items=0,valid_items=4,valid_correct_items=3,excluded_items=[],elapsed_seconds=209,time_limit_seconds=360,
    timed_out=False,groups=groups,wrong=[1],unknown=[],unanswered=[],attempts=attempts,
    review_dates=[dict(interval='D+1',date='2026-08-29'),dict(interval='D+3',date='2026-08-31'),dict(interval='D+7',date='2026-09-04')],
    practice_note='설명 직후 표현 인식 2문항과 짧은 과제이해 2문항. 처음 2개는 공식 JLPT 문제 유형이 아닌 학습용 표현 듣기이며 과제이해 성적에 합치지 않음. 이전 만기 복습과 별개의 새 교정 연습. 이전 복습 queue를 완료하거나 원래 오답을 정답으로 변경하지 않음. 이미 설명한 표현을 포함하므로 독립 진단이나 지연 유지율로 해석하지 않음.',
    timing_note='시작부터 제출까지. 문항 시간은 화면 체류시간, 결정시간은 마지막 재생 종료부터 최종 선택까지. TTS rate 0.9, 최대2회. 음성 오류와 중단은 유효 성적에서 제외. 해설 읽기 시간은 포함하지 않음.')
assert [a['item_no'] for a in attempts if a['state']=='wrong']==[1]
assert sum(a['state']=='correct' for a in attempts)==3
assert sum(a['response_seconds'] for a in attempts)==209
assert [a['selected_text'] for a in attempts]==['机を並べる','カードを受け取る → 部屋に入る','窓を閉める','床を拭く']
assert [a['item_type_id'] for a in attempts]==['listening_phrase_recognition']*2+['listening_task']*2
raw=ROOT/'database/results'/(TID+'.json')
if raw.exists(): assert json.loads(raw.read_text(encoding='utf-8'))==payload,'Conflicting saved result.'
trap='机を拭いてください에 대해 机を並べる를 선택. ふいて→拭く의 활용·음성·표기·의미 연결 중 어디서 혼동했는지는 미확인. 단어가 잘 안 들렸다는 이전 자기보고와 함께 확인할 대상. 같은 拭く를 포함한 4번은 정답이므로 전혀 모르는 단어라고 단정하지 않음.'
notes=dict(submitted_result=payload,question_definitions=questions,raw_result=raw.relative_to(ROOT).as_posix(),
    classification_note='self_made_tts / immediate_correction_practice. 표현 인식 1·2번은 학습용 비공식 listening_phrase_recognition, 3·4번은 listening_task. 과제이해는 공식 유형명일 뿐 이 문항의 출처가 공식이라는 뜻은 아님. D+1 유지율 아님.',
    session_base_seconds=14496,session_increment_seconds=209,session_total_seconds=14705,
    session_integer_minutes=245,session_remainder_seconds=5,
    interpretation_note='표현 듣기 1/2, 과제이해 2/2. 각 2문항, 설명 직후, TTS 0.9, 과제이해 모두2회 재생. 독립 진단·첫 청취 정답률·지연 유지율·약점 해결·합격 확률로 환산하지 않음. 1번77초는 화면 체류시간이며 순수 사고시간 아님. 3번 결정0초는 반올림·최종 선택 이벤트 측정으로 즉시 이해를 입증하지 않음.',
    timing_note='기존 기록 241분36초+타이머209초=245분05초(4시간05분05초). 기존 누적에는 사용자 추정 구간 포함. 해설·대기·추가 학습시간 가산하지 않음. 시작·종료 시각 추정하지 않음.')

con=sqlite3.connect(ROOT/'database/jlpt_learning.db')
con.row_factory=sqlite3.Row
con.execute('PRAGMA foreign_keys=ON')
protected={t:[tuple(r) for r in con.execute('SELECT * FROM '+t+' ORDER BY id')]
    for t in ('mastery_snapshots','pass_probability_snapshots','study_intervals')}
old_tests={r['id']:tuple(r) for r in con.execute('SELECT * FROM tests WHERE id<>?',(TID,))}
old_attempts={r['id']:tuple(r) for r in con.execute('SELECT * FROM question_attempts WHERE test_id<>?',(TID,))}
old_reviews={r['id']:tuple(r) for r in con.execute('SELECT * FROM review_queue')}
old_types={r['id']:tuple(r) for r in con.execute('SELECT * FROM item_types')}
existing=con.execute('SELECT notes FROM tests WHERE id=?',(TID,)).fetchone()
if existing is None:
    backup_dir=ROOT/'outputs/db_backups'
    backup_dir.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(backup_dir/('before-first-action-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.db')) as backup:
        con.backup(backup)
    with con:
        con.execute('BEGIN IMMEDIATE')
        session=con.execute("SELECT * FROM study_sessions WHERE session_date='2026-08-28'").fetchone()
        assert session['verified_minutes']==241 and TID not in session['summary'],'Timing base changed; reconcile first.'
        previous=json.loads(con.execute("SELECT notes FROM tests WHERE id='due-review-20260828-11'").fetchone()[0])
        assert previous['session_total_seconds']==14496
        it=con.execute("SELECT * FROM item_types WHERE id='listening_phrase_recognition'").fetchone()
        if it is None:
            con.execute('''INSERT INTO item_types (id,domain,label_ko,label_ja,is_official_type,recommended_min_sec,recommended_max_sec,timing_note)
                VALUES (?,?,?,?,?,?,?,?)''',('listening_phrase_recognition','listening','표현 듣기(학습용)','表現の聞き取り',0,None,None,
                '공식 JLPT 유형 아님. 짧은 표현의 음성·어휘·순서 확인용. 과제이해와 분리. 오디오·최종 재생 종료 후 선택 시간 별도 기록; 권장시간 미설정.'))
        else:
            assert it['domain']=='listening' and it['is_official_type']==0
        con.execute('''INSERT INTO tests (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,
            response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(TID,payload['test_date'],payload['title'],'self_made_tts',payload['target_level'],
            '기초 표현·단순 첫 행동 교정; 공식 난이도 미검증','immediate_correction_practice','multiple_choice',4,3,0,0,209,360,0.25,
            json.dumps(notes,ensure_ascii=False)))
        for a in attempts:
            assert a['visited'] and not a['audio_error']
            cur=con.execute('''INSERT INTO question_attempts (test_id,item_no,item_type_id,level_label,response_state,response_seconds,
                audio_seconds,decision_seconds,play_count,selected_text,correct_text,trap_hypothesis,trap_confidence)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',(TID,a['item_no'],a['item_type_id'],payload['target_level'],a['state'],
                a['response_seconds'],a['audio_seconds'],a['decision_seconds'],a['play_count'],a['selected_text'],a['correct_text'],
                trap if a['item_no']==1 else None,'low' if a['item_no']==1 else None))
            if a['state'] in ('wrong','unknown'):
                for d in payload['review_dates']:
                    con.execute('INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,?)',
                        (cur.lastrowid,d['date'],d['interval'],'pending'))
        extra=f' [{TID}] 설명 직후 청해 교정 3/4. 학습용 표현 듣기1/2·과제이해2/2 분리. 타이머209초만 추가: 기존241분36초→245분05초(4시간05분05초), 정수245분·잔여5초. 기존 누적에는 추정 구간 포함. 해설·추가 시간 미가산. 1번 오답만 새복습3건; 기존 결과·복습 상태 유지. 오늘 종료 아님.'
        con.execute("UPDATE study_sessions SET verified_minutes=245,summary=summary || ?,updated_at=CURRENT_TIMESTAMP WHERE session_date='2026-08-28'",(extra,))
else:
    assert json.loads(existing['notes'])['submitted_result']==payload,'Existing test differs; no overwrite.'

# Verify persisted results and that no past scores, queues, or probability estimates changed.
stored=json.loads(con.execute('SELECT notes FROM tests WHERE id=?',(TID,)).fetchone()[0])
assert all(stored[k]==v for k,v in notes.items())
saved=con.execute('SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no',(TID,)).fetchall()
assert len(saved)==4
for r,a in zip(saved,attempts):
    assert r['response_state']==a['state']
    for k in ('item_no','item_type_id','response_seconds','audio_seconds','decision_seconds','play_count','selected_text','correct_text'):
        assert r[k]==a[k]
reviews=con.execute('''SELECT q.item_no,r.review_date,r.interval_label FROM review_queue r JOIN question_attempts q
    ON q.id=r.attempt_id WHERE q.test_id=?''',(TID,)).fetchall()
assert len(reviews)==3
assert {(r['item_no'],r['review_date'],r['interval_label']) for r in reviews}=={(1,d['date'],d['interval']) for d in payload['review_dates']}
for t,rows in protected.items():assert [tuple(r) for r in con.execute('SELECT * FROM '+t+' ORDER BY id')]==rows
assert {r['id']:tuple(r) for r in con.execute('SELECT * FROM tests WHERE id<>?',(TID,))}==old_tests
assert {r['id']:tuple(r) for r in con.execute('SELECT * FROM question_attempts WHERE test_id<>?',(TID,))}==old_attempts
for r in con.execute('SELECT * FROM review_queue'):
    if r['id'] in old_reviews:assert tuple(r)==old_reviews[r['id']]
for r in con.execute('SELECT * FROM item_types'):
    if r['id'] in old_types:assert tuple(r)==old_types[r['id']]
assert con.execute("SELECT is_official_type FROM item_types WHERE id='listening_phrase_recognition'").fetchone()[0]==0
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
if not raw.exists():raw.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

marker='<!-- '+TID+' -->'
def append_once(filename,text):
    p=ROOT/filename
    old=p.read_text(encoding='utf-8')
    if marker not in old:p.write_text(old.rstrip()+'\n\n'+marker+'\n'+text.strip()+'\n',encoding='utf-8')
    assert p.read_text(encoding='utf-8').count(marker)==1

append_once('JLPT_STUDY_LOG.md','''## 2026-08-28 — 청해 표현 인식·첫 행동 교정 4문항

- 시험 ID `listening-first-action-20260828-4`. 사용자 제출 실제 결과. 자체 제작 TTS·설명 직후 교정 연습, 공식 시험 및 D+1 유지율과 분리.
- 총 3/4(75%), 오답1번, 모름·미응답·보고된 음성 오류·중단 없음. 제한6분 중 3분29초(209초), 시간 초과 없음. 실제 소리 품질은 독립 검증하지 않음.
- 표현 듣기 1·2번은 `listening_phrase_recognition`(학습용, is_official_type=0)으로 등록. 3·4번 `listening_task`와 분리. 후자의 공식 유형명은 문항 출처가 공식이라는 뜻이 아님.

| 유형 | 정답 | 정답률 | 문항 체류 평균/중앙 | 오디오 합 | 종료 후 선택 평균/중앙 | 재생 |
|---|---:|---:|---|---|---|---|
| 표현 듣기(학습용) | 1/2 | 50% | 47.5초 / 47.5초 | 9초 | 6.5초 / 6.5초 | 2회·1회 |
| 과제이해 | 2/2 | 100% | 57초 / 57초 | 90초 | 0.5초 / 0.5초 | 2회·2회 |

- 문항 체류 합209초, 오디오 합99초, 최종 재생 종료 후 선택 합14초. 체류시간은 순수 사고시간이 아님. 3번 결정시간0초는 반올림된 최종 선택 이벤트 측정이며 즉시 이해의 증거가 아님. 별도 권장시간을 소급 적용하지 않음.
- 1번 `机を拭いてください`를 듣고 `机を並べる` 선택. 음성 ふいて·기본형 拭く·뜻 닦다의 연결을 확인할 필요. 청취·활용·한자 읽기·뜻 중 실제 원인은 미확인. 같은 拭く가 나온 4번은 정답이어서 전혀 모르는 단어라고 단정하지 않음.
- 2번은 수령→입장, 3번은 후속 행동에 흔들리지 않고 창문 닫기, 4번은 수정된 첫 행동인 바닥 닦기를 정답으로 선택. 방향 신호이나 설명 직후·짧은 대화·모두2회 재생한 과제이해2문항으로 반복 약점 해결이나 첫 청취 능력 확정 불가. 독립 진단·지연 유지율·합격 확률로 환산하지 않음.
- 시간: 기존241분36초+이번 타이머209초=245분05초(4시간05분05초). DB 정수245분, 잔여5초는 notes·요약 보존. 기존 누적에는 사용자 추정 구간 포함. 해설·대기·다른 학습시간 미가산, 오늘 종료 아님.
- 1번 오답에만 D+1 2026-08-29 / D+3 2026-08-31 / D+7 2026-09-04 새복습3건 등록. 기존 모든 시험·응답·복습 상태 보존. 등록 직후 오늘 만기0건, 내일35건(기존34+새1).
- 원본 응답 `database/results/listening-first-action-20260828-4.json`; 전체 문제·대본·제작 해설 및 제출값은 tests.notes에도 보존. 합격 확률·숙달 스냅샷 미변경. 홈페이지 동기화·알림 자동화는 실행하지 않음.
''')
append_once('JLPT_ERROR_NOTE.md','''## 2026-08-28 — 청해 표현 인식·첫 행동 교정: 1번 오답

**카테고리: 청해 → 표현 듣기(학습용 비공식 유형) → 동작 어휘·음성 대응**

**문제 원문**

聞こえた動作を選んでください。 — 들린 동작을 고르세요.

1. 机を運ぶ
2. 机を並べる
3. 机を拭く
4. 机を買う

**청해 대본·번역**

机を拭いてください。（つくえを ふいてください。） — 책상을 닦아 주세요.

**선택 → 정답·완성 문장**

② 机を並べる(つくえを ならべる, 책상을 늘어놓다) → ③ 机を拭く(つくえを ふく, 책상을 닦다).

완성 문장: 机を拭いてください。

**접속·의미**

拭く（ふく）→ 拭いて（ふいて）→ 拭いてください（ふいてください）. 拭く는 く가 いて로 바뀌는 て형을 사용하고, 〜てください는 ~해 주세요라는 요청이다. 음성 ふいて를 기본형 ふく 및 표기 拭く·뜻 닦다와 연결해야 한다.

**함정·원인 추정**

2회 재생 후 並べる 선택. 문장에 행동은 하나이므로 이번 문항 자체에는 마지막 행동과 첫 행동의 순서 함정이 없다. 음성·활용·표기·뜻 연결을 확인해야 하지만 어느 단계가 원인인지는 미확인. 77초는 체류시간으로 원인·성급함·순수 사고시간을 단정할 수 없다. 같은 拭く를 포함한 4번은 정답이므로 문맥 도움 가능성 등을 열어 두고 단어를 전혀 모른다고 확정하지 않는다.

**유사 표현 차이**

- 拭く（ふく）→ 拭いて（ふいて）: 닦다 → 닦아 주세요에 쓰는 형태.
- 並べる（ならべる）→ 並べて（ならべて）: 늘어놓다 → 늘어놓아 주세요에 쓰는 형태.
- 運ぶ（はこぶ）→ 運んで（はこんで）: 나르다.
- 買う（かう）→ 買って（かって）: 사다.

ふいて와 ならべて는 다른 동사의 소리이다. 책상을 닦는 행동과 책상을 배치하는 행동을 구분한다.

**추가 예문**

ぬれた床を拭いてください。（ぬれた ゆかを ふいてください。） — 젖은 바닥을 닦아 주세요.

椅子を並べてください。（いすを ならべてください。） — 의자를 늘어놓아 주세요.

**다음 복습일**

D+1 2026-08-29 · D+3 2026-08-31 · D+7 2026-09-04: 새 시도1번에만 3건 등록. 기존 복습 상태는 보존. 이번은 설명 직후 교정이며 D+1 유지율 아님.

문항 체류77초 / 오디오5초 / 최종 재생 종료 후 선택8초 / 재생2회. 해설 읽기 시간 및 완료 여부는 미확인.
''')
append_once('JLPT_DATABASE.md','''## 학습용 표현 듣기 분리 (2026-08-28)

`listening_phrase_recognition`: domain=listening, is_official_type=0, label_ko=표현 듣기(학습용). 짧은 표현의 소리·어휘·순서를 확인하는 비공식 학습 분류이며 과제이해(listening_task)에 합치지 않는다. `listening-first-action-20260828-4`의 1·2번이 해당한다. 이 시험은 self_made_tts / immediate_correction_practice로 저장하여 공식 시험·D+1 지연 유지율과 분리한다. 원본 제출값과 문제 정의는 tests.notes에 보존하며 기존 유형·시험 기록은 변경하지 않는다. 사이트 표시 체계 변경·동기화는 별도이며 이번 작업에서 하지 않았다.
''')
print(json.dumps(dict(test_id=TID,inserted=existing is None,attempts=len(saved),new_reviews=len(reviews),
    old_results_and_reviews_unchanged=True,probabilities_unchanged=True,types_separated=True,
    session_minutes=con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-28'").fetchone()[0],
    due_pending=con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date<='2026-08-28'").fetchone()[0],
    tomorrow_pending=con.execute("SELECT count(*) FROM review_queue WHERE status='pending' AND review_date='2026-08-29'").fetchone()[0],integrity='ok')))
con.close()
