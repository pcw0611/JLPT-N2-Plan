"""Record the user's approximate three hours of personal study once."""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'database/jlpt_learning.db'
RID='personal-study-20260829-user-report'
payload={
    'record_id':RID,'study_date':'2026-08-29','reported_minutes':180,
    'precision':'approximate','source':'user_reported',
    'details':'개인적으로 약 3시간 공부. 과목·시작·종료·세부 활동은 미확인.',
    'timing_note':'기존 만기 복습 타이머 894초와 중복되지 않는 추가 공부로 사용자 요청에 따라 반영.',
}
raw=ROOT/'database/results'/f'{RID}.json'
con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
session=con.execute("select * from study_sessions where session_date='2026-08-29'").fetchone()
assert session is not None
marker=f'[{RID}]'
inserted=marker not in (session['summary'] or '')
if inserted:
    backup_dir=ROOT/'outputs/db_backups'; backup_dir.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(backup_dir/('before-personal-study-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.db')) as backup:
        con.backup(backup)
    with con:
        changed=con.execute("""update study_sessions set verified_minutes=verified_minutes+180,
          has_untracked_activity=1,summary=summary||?,updated_at=current_timestamp
          where session_date='2026-08-29' and instr(summary,?)=0""",
          (f' {marker} 사용자 보고 개인 공부 약180분 추가. 과목·시작·종료·세부 활동 미확인; 임의 배분 없음. 기존 시험 타이머와 합계 약194분54초.',marker))
        assert changed.rowcount==1
session=con.execute("select * from study_sessions where session_date='2026-08-29'").fetchone()
assert session['verified_minutes']==194 and session['has_untracked_activity']==1 and marker in session['summary']
if raw.exists(): assert json.loads(raw.read_text(encoding='utf-8'))==payload
else: raw.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

log_marker=f'<!-- {RID} -->'
p=ROOT/'JLPT_STUDY_LOG.md'; old=p.read_text(encoding='utf-8')
entry='''## 2026-08-29 — 개인 공부 시간 추가

- 사용자 보고: 오늘 개인적으로 **약 3시간(180분)** 공부.
- 과목·시작·종료·세부 활동은 확인되지 않아 임의로 배분하거나 추정하지 않음. `has_untracked_activity=1`로 표시.
- 기존 만기 복습 타이머 14분54초와 중복되지 않는 추가 시간으로 반영. 오늘 누적 **약 3시간14분54초**; DB 정수 필드 194분, 잔여54초는 요약에 보존.
- 오늘 학습 종료로 처리하지 않음. 원본: `database/results/personal-study-20260829-user-report.json`.
'''
if log_marker not in old: p.write_text(old.rstrip()+'\n\n'+log_marker+'\n'+entry,encoding='utf-8')
assert p.read_text(encoding='utf-8').count(log_marker)==1
assert con.execute('pragma integrity_check').fetchone()[0]=='ok'
print(json.dumps({'inserted':inserted,'verified_minutes':session['verified_minutes'],'exact_known_seconds':894,
                  'reported_approximate_minutes':180,'display_total':'약 3시간14분54초','integrity':'ok'},ensure_ascii=False))
con.close()
