"""Record confirmed viewing; keep chat elapsed time separate from study duration."""
import sqlite3
from pathlib import Path
from datetime import datetime

root = Path(__file__).resolve().parents[1]
key = 'n2-grammar-type-intro-completed-20260828'
note = f' [{key}] 사용자 시청 완료 확인: 다락원 N2 문법 공략편 / 문제 유형 공략하기 / 문제 유형 완전 분석(p.190~193). 강의 안내 응답 완료 2026-08-28 15:35:07 KST부터 사용자 완료 메시지 16:12:28 KST까지 대화 경과 2241초(37분 21초). 실제 재생시간이나 휴식 제외 학습시간을 뜻하지 않음. 해당 구간의 학습시간 확인 전까지 verified_minutes 가산하지 않음. 오늘 학습 종료 아님.'
con = sqlite3.connect(root/'database/jlpt_learning.db')
session = con.execute("SELECT verified_minutes,summary FROM study_sessions WHERE session_date='2026-08-28'").fetchone()
assert session is not None
before = session[0]
increment_seconds = 2241
expected_minutes = 233
expected_remainder = 3
if key not in (session[1] or ''):
    backup_dir = root/'outputs/db_backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(backup_dir/('before-n2-intro-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.db')) as backup:
        con.backup(backup)
    with con:
        con.execute("UPDATE study_sessions SET verified_minutes=?,summary=COALESCE(summary,'') || ?,has_untracked_activity=1,updated_at=CURRENT_TIMESTAMP WHERE session_date='2026-08-28'", (expected_minutes, note))
        con.execute("INSERT INTO study_intervals (session_date,started_at,ended_at,duration_seconds,status,source,notes) VALUES (?,?,?,?,?,?,?)", ('2026-08-28','2026-08-28T15:35:07+09:00','2026-08-28T16:12:28+09:00',increment_seconds,'completed','chat_confirmed','사용자가 쉬지 않고 시청했다고 확인; 실제 영상 재생시간과 구분'))
elif before == 195:
    # The earlier completion marker was written before the user's no-break confirmation.
    with con:
        con.execute("UPDATE study_sessions SET verified_minutes=?,updated_at=CURRENT_TIMESTAMP WHERE session_date='2026-08-28'", (expected_minutes,))
        assert con.execute("SELECT count(*) FROM study_intervals WHERE session_date='2026-08-28' AND source='chat_confirmed' AND duration_seconds=?", (increment_seconds,)).fetchone()[0] == 0
        con.execute("INSERT INTO study_intervals (session_date,started_at,ended_at,duration_seconds,status,source,notes) VALUES (?,?,?,?,?,?,?)", ('2026-08-28','2026-08-28T15:35:07+09:00','2026-08-28T16:12:28+09:00',increment_seconds,'completed','chat_confirmed','사용자가 쉬지 않고 시청했다고 확인; 실제 영상 재생시간과 구분'))
path = root/'JLPT_STUDY_LOG.md'
old = path.read_text(encoding='utf-8')
marker = '<!-- '+key+' -->'
if marker not in old:
    path.write_text(old.rstrip()+'\n\n'+marker+'\n## 2026-08-28 — N2 문법 문제 유형 분석 영상 시청 완료\n\n'+note.strip()+'\n',encoding='utf-8')
assert con.execute("SELECT verified_minutes FROM study_sessions WHERE session_date='2026-08-28'").fetchone()[0] == (expected_minutes if key in con.execute("SELECT summary FROM study_sessions WHERE session_date='2026-08-28'").fetchone()[0] else before)
assert key in con.execute("SELECT summary FROM study_sessions WHERE session_date='2026-08-28'").fetchone()[0]
assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
assert path.read_text(encoding='utf-8').count(marker) == 1
con.close()
print('Viewing completion recorded. Chat elapsed: 2241 seconds. Study minutes unchanged pending confirmation.')
