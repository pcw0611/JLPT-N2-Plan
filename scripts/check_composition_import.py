"""Exercise real import queries in memory, never in the user's learning DB."""
import json, sqlite3, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'jlpt-calendar-site/scripts'))
from composition_import import insert_composition_attempts
c=sqlite3.connect(':memory:')
c.executescript((ROOT/'database/schema.sql').read_text(encoding='utf-8'))
print('Schema and in-memory database ready')
source=sqlite3.connect('file:'+str(ROOT/'database/jlpt_learning.db')+'?mode=ro',uri=True)
assert source.execute("SELECT id FROM item_types WHERE id='sentence_composition'").fetchone()
print('Existing ledger supports sentence_composition')
# Minimal test parents use the same production table schema.
for test_id,date in [('test1','2026-11-11'),('test2','2026-11-12'),('test3','2026-11-13')]:
    c.execute("INSERT INTO tests(id,test_date,title,source_class,target_level,response_format,total_items,correct_items,unknown_items,unanswered_items,notes) VALUES (?,?,?,'자체 제작','N2','선택형',1,0,0,0,?)",(test_id,date,'검증 테스트','n2-sentence-composition-100'))
c.execute("INSERT OR IGNORE INTO item_types(id,label_ko,label_ja,domain) VALUES ('sentence_composition','배열','文の組み立て','grammar')")
def payload(status):return {'details':{'attempts':[dict(item_no=1,status=status,response_seconds=12,selected_text='x',correct_text='y')]}}
insert_composition_attempts(c.cursor(),'test1','2026-11-11',payload('wrong'))
assert c.execute("SELECT review_date FROM review_queue ORDER BY review_date").fetchall()==[('2026-11-12',),('2026-11-14',),('2026-11-18',)]
insert_composition_attempts(c.cursor(),'test2','2026-11-12',payload('correct'))
assert c.execute("SELECT COUNT(*) FROM review_queue WHERE status='pending'").fetchone()[0]==2
insert_composition_attempts(c.cursor(),'test3','2026-11-13',payload('unknown'))
assert c.execute("SELECT COUNT(*) FROM review_queue WHERE status='pending'").fetchone()[0]==3
assert c.execute("SELECT COUNT(*) FROM review_queue WHERE status='superseded'").fetchone()[0]==2
print('PASS: actual import SQL, D+1/3/7, correct keeps future dates, repeated error supersedes older queue; no real learning writes.')
