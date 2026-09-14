"""Record the submitted random N2 listening check once."""
import json, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-08-31'
TID = 'n2-listening-random-20260831-8'
RESULT = ROOT / 'database/results' / f'{TID}.json'
payload = {
  'testId': TID, 'date': DATE, 'sourceClass': 'self_made_tts', 'total': 8,
  'correct': 5, 'wrong': 3, 'unknown': 0, 'unanswered': 0, 'elapsedSeconds': 247,
  'firstHalf': {'correct': 2, 'total': 4, 'seconds': 103},
  'secondHalf': {'correct': 3, 'total': 4, 'seconds': 144},
  'responses': [
    {'itemNo':1,'questionId':2,'responseState':'correct','selectedText':'市役所','correctText':'市役所','responseSeconds':19,'playCount':1,'category':'청해 → 課題理解 → N2 랜덤'},
    {'itemNo':2,'questionId':1,'responseState':'correct','selectedText':'机を並べる','correctText':'机を並べる','responseSeconds':28.3,'playCount':1,'category':'청해 → 課題理解 → N2 랜덤'},
    {'itemNo':3,'questionId':3,'responseState':'wrong','selectedText':'印刷する','correctText':'参考文献を確認する','responseSeconds':36.5,'playCount':1,'category':'청해 → 課題理解 → N2 랜덤'},
    {'itemNo':4,'questionId':4,'responseState':'wrong','selectedText':'八部','correctText':'二十部','responseSeconds':19.5,'playCount':1,'category':'청해 → ポイント理解 → N2 랜덤'},
    {'itemNo':5,'questionId':5,'responseState':'correct','selectedText':'千二百円','correctText':'千二百円','responseSeconds':28.9,'playCount':1,'category':'청해 → ポイント理解 → N2 랜덤'},
    {'itemNo':6,'questionId':6,'responseState':'wrong','selectedText':'大学の授業料の説明','correctText':'地域の祭りの日程変更','responseSeconds':48.9,'playCount':1,'category':'청해 → 概要理解 → N2 랜덤'},
    {'itemNo':7,'questionId':8,'responseState':'correct','selectedText':'三時からの予定です。','correctText':'三時からの予定です。','responseSeconds':41,'playCount':1,'category':'청해 → 即時応答 → N2 랜덤'},
    {'itemNo':8,'questionId':7,'responseState':'correct','selectedText':'ええ、この道をまっすぐです。','correctText':'ええ、この道をまっすぐです。','responseSeconds':25.3,'playCount':1,'category':'청해 → 即時応答 → N2 랜덤'},
  ]
}
RESULT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
con = sqlite3.connect(ROOT / 'database/jlpt_learning.db')
con.execute('PRAGMA foreign_keys=ON')
if con.execute('SELECT 1 FROM tests WHERE id=?', (TID,)).fetchone() is None:
    notes = {'source':'자체 제작 일본어 TTS 선택형 청해. 공식 시험·공식 모의고사 아님.',
             'quality_note':'이번 세트는 짧은 형식 확인용으로 실제 N2 대화 길이·정보량보다 낮았음. 난이도 판정에 사용하지 않음.',
             'raw_result':str(RESULT.relative_to(ROOT)), 'review_dates':['2026-09-01','2026-09-03','2026-09-07']}
    con.execute('''INSERT INTO tests (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (TID,DATE,'N2 랜덤 청해 8문항','self_made_tts','N2','짧은 형식 확인용; N2 난도 미검증','immediate_recognition','multiple_choice',8,5,0,0,247,900,0.1,json.dumps(notes,ensure_ascii=False)))
    traps={3:'제출 전에 해야 할 확인과 인쇄 가능하다는 후속 정보를 혼동.',4:'참가자 수 18부를 전체 수량으로 선택하고 예비 2부를 더하지 못함.',6:'세부 정보가 아닌 선택지의 익숙한 대학 소재를 주제로 오인.'}
    for a in payload['responses']:
        subtype=a['category'].split(' → ')[1]
        typ='listening_point' if subtype=='ポイント理解' else 'listening_phrase_recognition' if subtype=='即時応答' else 'listening_task'
        cur=con.execute('''INSERT INTO question_attempts (test_id,item_no,item_type_id,level_label,response_state,response_seconds,audio_seconds,decision_seconds,play_count,selected_text,correct_text,trap_hypothesis,trap_confidence) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (TID,a['itemNo'],typ,'N2',a['responseState'],round(a['responseSeconds']),None,None,a['playCount'],a['selectedText'],a['correctText'],traps.get(a['itemNo']),'medium' if a['responseState']=='wrong' else None))
        if a['responseState'] in ('wrong','unknown'):
            for d,lab in [('2026-09-01','D+1'),('2026-09-03','D+3'),('2026-09-07','D+7')]:
                con.execute('INSERT INTO review_queue (attempt_id,review_date,interval_label,status) VALUES (?,?,?,?)',(cur.lastrowid,d,lab,'pending'))
    s=con.execute('SELECT verified_minutes,summary FROM study_sessions WHERE session_date=?',(DATE,)).fetchone()
    assert s and s[0]==273, f'Unexpected session base: {s}'
    extra=' [청해 결과 '+TID+'] 자체 제작 TTS 랜덤 8문항 5/8, 4분07초. 오답 3개 D+1/D+3/D+7 9건 등록. 기존 273분31.009초에 247초를 더해 277분38.009초; 정수 verified_minutes=277, 잔여 38.009초는 시험 기록에 보존. 이번 세트는 짧은 형식 확인용으로 실제 N2 대화 난도 판정에는 사용하지 않음. 오늘 학습 종료 아님.'
    con.execute('UPDATE study_sessions SET verified_minutes=277,summary=summary||?,updated_at=CURRENT_TIMESTAMP WHERE session_date=?',(extra,DATE))
    con.commit()
else:
    assert con.execute('SELECT correct_items,elapsed_seconds FROM tests WHERE id=?',(TID,)).fetchone()==(5,247)
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
print(json.dumps({'test_id':TID,'score':'5/8','review_rows':con.execute('SELECT count(*) FROM review_queue r JOIN question_attempts q ON q.id=r.attempt_id WHERE q.test_id=?',(TID,)).fetchone()[0],'verified_minutes':con.execute('SELECT verified_minutes FROM study_sessions WHERE session_date=?',(DATE,)).fetchone()[0]},ensure_ascii=False))
con.close()
