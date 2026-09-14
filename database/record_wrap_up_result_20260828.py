"""Idempotently record the submitted wrap-up; preserve all prior results/queues."""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TID = 'listening-wrap-up-20260828-3'
questions = json.loads((ROOT/'database/question_sets'/TID/'questions.json').read_text(encoding='utf-8'))['questions']
# Actual user submission: selected index, dwell, audio, decision, play count.
submitted = [(3,19,3,1,1),(1,36,27,1,1),(0,29,25,1,1)]
assert len(questions) == len(submitted) == 3
attempts, groups = [], {}
for i,(q,(choice,dwell,audio,decision,plays)) in enumerate(zip(questions,submitted),1):
    assert choice == q['a']
    attempts.append(dict(item_no=i,question_id=q['id'],item_type_id=q['itemType'],is_official_type=q['official'],
        type=q['type'],category=q['category'],state='correct',question=q['q'],choices=q['c'],
        selected_text=q['c'][choice],correct_text=q['c'][q['a']],response_seconds=dwell,
        audio_seconds=audio,decision_seconds=decision,play_count=plays,audio_error=False,visited=True))
    g=groups.setdefault(q['type'],dict(correct=0,total=0,excluded=0))
    g['correct']+=1; g['total']+=1
payload=dict(test_id=TID,test_date='2026-08-28',title='청해 마무리 — 동작 표현·첫 행동 3문항',
    source_class='자체 제작 TTS',target_level='N3 기반·기초 교정',memory_timing='당일 교정 후 추가 연습',
    total_items=3,correct_items=3,unknown_items=0,unanswered_items=0,valid_items=3,valid_correct_items=3,
    excluded_items=[],elapsed_seconds=84,time_limit_seconds=240,timed_out=False,groups=groups,
    wrong=[],unknown=[],unanswered=[],attempts=attempts,
    review_dates=[dict(interval='D+1',date='2026-08-29'),dict(interval='D+3',date='2026-08-31'),dict(interval='D+7',date='2026-09-04')],
    practice_note='당일 교정 후 표현 인식 1문항과 짧은 과제이해 2문항. 첫 1개는 공식 JLPT 문제 유형이 아닌 학습용 표현 듣기이며 과제이해 성적에 합치지 않음. 이전 만기 복습과 별개의 새 교정 연습. 이전 복습 queue를 완료하거나 원래 오답을 정답으로 변경하지 않음. 이미 설명한 표현을 포함하므로 독립 진단이나 지연 유지율로 해석하지 않음.',
    timing_note='시작부터 제출까지. 문항 시간은 화면 체류시간, 결정시간은 마지막 재생 종료부터 최종 선택까지. TTS rate 0.9, 최대2회. 음성 오류와 중단은 유효 성적에서 제외. 해설 읽기 시간은 포함하지 않음.')
assert sum(a['response_seconds'] for a in attempts)==84
assert [a['selected_text'] for a in attempts]==['机を拭く','受付で名前を書く','机を拭く']
assert [a['is_official_type'] for a in attempts]==[False,True,True]
raw=ROOT/'database/results'/(TID+'.json')
if raw.exists(): assert json.loads(raw.read_text(encoding='utf-8'))==payload
quality=dict(user_report='근데 왜 후구가 누구이테로 들리지 원래 그런가',
    status='unverified_pronunciation_concern',affected_items_possible=[1,3],
    observed_input='拭いて was passed as kanji to browser SpeechSynthesisUtterance, rate 0.9; actual selected voice/audio not captured.',
    note='표준 읽기는 ふく→ふいて. 拭う는 별개 동사 ぬぐう→ぬぐって. 누구이테는 표준 활용이 아님. TTS 오독 또는 청취 혼동 중 실제 원인은 미확인. 사용자의 청취 오류로 단정하지 않음. 원본 audio_error=false는 보존하며 오류가 확인되면 해당 문항의 유효 집계를 별도 정정해야 함. 이번 표본으로 음성 인식 숙달을 판정하지 않음.',
    future_audio_policy='후속 문제는 표시 대본과 TTS 읽기용 문자열을 분리하고 拭いて를 ふいて로 명시. 이미 제출된 대본과 결과는 소급 변경하지 않음.',
    sources=['https://www.kanjipedia.jp/kotoba/0003539600','https://www.kanjipedia.jp/kotoba/0003539500'])
notes=dict(submitted_result=payload,question_definitions=questions,raw_result=raw.relative_to(ROOT).as_posix(),
    classification_note='self_made_tts / immediate_correction_practice; phrase recognition 1/1 separate from listening_task 2/2. Official type name does not mean official source. Not D+1 retention.',
    session_base_seconds=16315,session_increment_seconds=84,session_total_seconds=16399,
    session_integer_minutes=273,session_remainder_seconds=19,audio_quality_followup=quality,
    timing_note='Only the submitted 84-second timer added. No explanation, waiting, lecture, or additional study time inferred. Prior total includes estimates.',
    interpretation_note='Submitted 3/3 with one playback per item. Pronunciation concern remains unverified. No mastery, pass probability, or existing review status update.')
con=sqlite3.connect(ROOT/'database/jlpt_learning.db');con.row_factory=sqlite3.Row
con.execute('PRAGMA foreign_keys=ON')
protected={t:[tuple(r) for r in con.execute('SELECT * FROM '+t+' ORDER BY id')] for t in
    ('review_queue','mastery_snapshots','pass_probability_snapshots','study_intervals','item_types')}
old_tests={r['id']:tuple(r) for r in con.execute('SELECT * FROM tests WHERE id<>?',(TID,))}
old_attempts={r['id']:tuple(r) for r in con.execute('SELECT * FROM question_attempts WHERE test_id<>?',(TID,))}
existing=con.execute('SELECT notes FROM tests WHERE id=?',(TID,)).fetchone()
if existing is None:
    backup_dir=ROOT/'outputs/db_backups';backup_dir.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(backup_dir/('before-wrap-up-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.db')) as backup: con.backup(backup)
    with con:
        con.execute('BEGIN IMMEDIATE')
        session=con.execute("SELECT * FROM study_sessions WHERE session_date='2026-08-28'").fetchone()
        assert session['verified_minutes']==271 and TID not in session['summary'], 'Reconcile changed time base.'
        previous=json.loads(con.execute("SELECT notes FROM tests WHERE id='n2-grammar-001-008-check-20260828'").fetchone()[0])
        assert previous['session_total_seconds']==16315
        assert con.execute("SELECT is_official_type FROM item_types WHERE id='listening_phrase_recognition'").fetchone()[0]==0
        con.execute('''INSERT INTO tests (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,
            response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (TID,payload['test_date'],payload['title'],'self_made_tts',payload['target_level'],'기초 교정; 공식 난이도 미검증',
             'immediate_correction_practice','multiple_choice',3,3,0,0,84,240,0.25,json.dumps(notes,ensure_ascii=False)))
        for a in attempts:
            assert a['visited'] and not a['audio_error'] and a['state']=='correct'
            con.execute('''INSERT INTO question_attempts (test_id,item_no,item_type_id,level_label,response_state,response_seconds,
                audio_seconds,decision_seconds,play_count,selected_text,correct_text,trap_hypothesis,trap_confidence)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (TID,a['item_no'],a['item_type_id'],payload['target_level'],a['state'],a['response_seconds'],a['audio_seconds'],
                 a['decision_seconds'],a['play_count'],a['selected_text'],a['correct_text'],None,None))
        # All three responses are correct: intentionally no review_queue inserts or updates.
        extra=f' [{TID}] 청해 마무리 제출3/3: 비공식 표현1/1·과제이해2/2 분리, 모두1회 재생. 타이머84초만 추가: 271분55초→273분19초(4시간33분19초). 새복습0건, 기존 점수·복습 보존. 拭いて 발음 의문은 음성 품질 확인 대기로 기록; 청취 실수·TTS 오류 확정 아님. 해설시간 미가산, 오늘 종료 아님.'
        con.execute("UPDATE study_sessions SET verified_minutes=273,summary=summary || ?,updated_at=CURRENT_TIMESTAMP WHERE session_date='2026-08-28'",(extra,))
else:
    assert json.loads(existing['notes'])['submitted_result']==payload, 'Conflicting submission.'
stored=json.loads(con.execute('SELECT notes FROM tests WHERE id=?',(TID,)).fetchone()[0])
assert all(stored[k]==v for k,v in notes.items())
saved=con.execute('SELECT * FROM question_attempts WHERE test_id=? ORDER BY item_no',(TID,)).fetchall()
assert len(saved)==3
for r,a in zip(saved,attempts):
    assert r['response_state']==a['state']
    for k in ('item_no','item_type_id','response_seconds','audio_seconds','decision_seconds','play_count','selected_text','correct_text'): assert r[k]==a[k]
for t,rows in protected.items(): assert [tuple(r) for r in con.execute('SELECT * FROM '+t+' ORDER BY id')]==rows
assert {r['id']:tuple(r) for r in con.execute('SELECT * FROM tests WHERE id<>?',(TID,))}==old_tests
assert {r['id']:tuple(r) for r in con.execute('SELECT * FROM question_attempts WHERE test_id<>?',(TID,))}==old_attempts
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
if not raw.exists(): raw.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
marker='<!-- '+TID+' -->'
def append_once(name,body):
    p=ROOT/name;old=p.read_text(encoding='utf-8')
    if marker not in old: p.write_text(old.rstrip()+'\n\n'+marker+'\n'+body.strip()+'\n',encoding='utf-8')
    assert p.read_text(encoding='utf-8').count(marker)==1
append_once('JLPT_STUDY_LOG.md','''## 2026-08-28 — 청해 마무리 3문항 실제 결과

- `listening-wrap-up-20260828-3`: 자체 제작 TTS, 당일 교정 후 추가 연습. 공식 시험·D+1 유지율과 분리.
- 제출값 3/3(100%). 표현 듣기(비공식)1/1, 과제이해2/2 별도 기록. 오답·모름·미응답0, audio_error=false, 중단·시간 초과 없음으로 제출됨. 모두1회 재생. 실제 음성 품질은 독립 검증하지 않음.
- 사용자 추가 보고: “근데 왜 후구가 누구이테로 들리지 원래 그런가”. 拭いて가 들어간 1·3번의 TTS 읽기 품질 확인 필요. 표준 ふく→ふいて와 다른 읽기가 실제 출력됐는지는 미확인. 사용자 청취 실수로 확정하지 않으며 원본 결과는 보존. 음성 오류 확인 시 해당 유효 표본을 정정해야 함.
- 문항 체류19·36·29초, 오디오3·27·25초, 최종 재생 종료 후 선택 각1초. 체류시간은 순수 사고시간이 아님.
- 시험 타이머84초(1분24초)만 추가. 16315+84=16399초, **273분19초(4시간33분19초)**. DB 정수273분, 잔여19초는 notes·요약 보존. 기존 누적에는 추정 구간 포함. 해설·대기·기타 학습시간 미가산.
- 전부 정답이므로 새 D+1·D+3·D+7 등록0건. 기존 시험·복습 일정·완료 상태·숙달·합격 확률 모두 보존. 오늘 만기0건, 내일37건 유지.
- 동일 표현을 이미 학습한 당일 추가 연습. 첫 행동과 어휘를 이번 선택에서 맞혔지만 3문항으로 약점 해결이나 독립 진단을 확정하지 않음. 오늘 학습 종료 처리 및 홈페이지 동기화는 하지 않음.
''')
append_once('JLPT_ERROR_NOTE.md','''## 2026-08-28 — 청해 마무리: 새 오답 없음, 발음 확인 메모

자체 제작 TTS·당일 추가 연습, 제출3/3. 표현 듣기1/1과 과제이해2/2는 별도. 새로운 오답·모름은 없으며 기존 오답을 삭제하거나 기존 복습을 완료하지 않음. 신규 복습0건, 기존 D+1 8/29·D+3 8/31·D+7 9/4 일정 보존.

**청해 → 표현 듣기(학습용) → 机·拭く의 소리와 의미**

1번: この机を拭いてください。 — 이 책상을 닦아 주세요. 선택·정답 모두 机を拭く. 표준 읽기 つくえをふいてください. 拭く（ふく）→拭いて（ふいて）, てください는 ~해 주세요. 拭う（ぬぐう）는 별개 동사로 て형은 ぬぐって. 누구이테로 변하는 규칙은 없음. 예문: 布で机を拭きます。 — 천으로 책상을 닦습니다.

사용자 보고 “후구가 누구이테로 들린다”는 발음 확인 의문이며 틀린 답이나 확정된 청취 오류가 아님. 해당 퀴즈는 拭いて를 한자 그대로 TTS에 전달했음. 실제 음성·선택된 음색은 저장하지 않아 오독 여부 미확인. 1·3번과 관련될 수 있으나 정확한 문항 미지정. 원본 audio_error=false 및 제출점수는 보존하고 품질 의문은 별도 메타데이터에 기록. 음성 오류가 확인되면 해당 문항을 유효 집계에서 제외. 향후 TTS는 표시 대본과 읽기용 문자열을 분리하여 ふいて로 명시할 것. 기존 제출 문제의 대본은 변경하지 않음.

**청해 → 과제이해(課題理解) → 선행 조건과 마지막 안내 구별**

2번 핵심: 先にこちらの紙にお名前を書いてください。それからカードをお渡しします。カードを受け取ったら、二階の教室へどうぞ。
번역: 먼저 종이에 이름을 써 주세요. 그다음 카드를 드립니다. 카드를 받으면 2층 교실로 가세요.
선택·정답: 受付で名前を書く. 이름 작성→카드 수령→2층 이동. 마지막 목적지와 첫 절차를 구분한 선택. 受け取る는 받다, 返す는 돌려주다. 예문: 名前を書いてから、教室へ行きます。 — 이름을 쓰고 교실로 갑니다.

**청해 → 과제이해(課題理解) → 지시 수정 후 첫 행동**

3번 핵심: 椅子は後にして、先に机を拭いてください。飲み物は私が買ってきます。
번역: 의자는 나중에 하고 먼저 책상을 닦아 주세요. 음료는 제가 사 오겠습니다.
선택·정답: 机を拭く. 최초 의자 배치를 수정한 뒤 남자의 첫 행동은 책상 닦기, 음료 구매는 여자의 행동. Aは後にして先にB는 순서 수정, 先にAその後B는 A 뒤에 B 추가. 예문: 買い物は後にして、先に掃除をしましょう。 — 장보기는 나중에 하고 먼저 청소합시다.

이번 결과를 D+1 유지율·공식 성적·약점 해결로 해석하지 않음. 해설 읽기 시간 및 완료 여부는 추정하지 않음.
''')
print(json.dumps(dict(test_id=TID,inserted=existing is None,attempts=len(saved),new_reviews=0,
    old_results_and_reviews_unchanged=True,probabilities_unchanged=True,session_total_seconds=16399,
    actual_session_minutes=con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-28'").fetchone()[0],
    pronunciation_concern='unverified',integrity='ok')))
con.close()
