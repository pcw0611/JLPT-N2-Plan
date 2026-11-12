"""Import actual sentence-composition submissions; builders never call this."""
from datetime import date, timedelta
import json

def get_composition_payload(submission):
    try: payload=json.loads(submission.get('payload_json') or '{}')
    except (TypeError,ValueError): return None
    if not isinstance(payload,dict) or payload.get('details',{}).get('test_id')!='n2-sentence-composition-100':return None
    if payload.get('examType')!='sentence_composition' or payload['details'].get('termination_reason')!='submitted':raise ValueError('Unsubmitted composition run')
    return payload

def insert_composition_attempts(cursor,test_id,test_date,payload):
    for a in payload['details']['attempts']:
        if a['status'] not in ('correct','wrong','unknown','unanswered'):raise ValueError('Invalid composition status')
        prior_ids=[r[0] for r in cursor.execute('''SELECT qa.id FROM question_attempts qa
          JOIN tests t ON t.id=qa.test_id WHERE qa.item_type_id='sentence_composition'
          AND qa.item_no=? AND t.notes LIKE '%n2-sentence-composition-100%' ''',(a['item_no'],))]
        for prior_id in prior_ids:
            if a['status'] in ('wrong','unknown'):
                cursor.execute("UPDATE review_queue SET status='superseded' WHERE attempt_id=? AND status='pending'",(prior_id,))
            elif a['status']=='correct':
                cursor.execute("UPDATE review_queue SET status='completed',result_state='correct',result_seconds=? WHERE attempt_id=? AND status='pending' AND review_date<=?",(a['response_seconds'],prior_id,test_date))
        cursor.execute('''INSERT INTO question_attempts
          (test_id,item_no,item_type_id,level_label,response_state,response_seconds,selected_text,correct_text)
          VALUES (?,?,'sentence_composition','N2 자체 제작 문장배열',?,?,?,?)''',
          (test_id,a['item_no'],a['status'],a['response_seconds'],a['selected_text'],a['correct_text']))
        attempt_id=cursor.lastrowid
        if a['status'] in ('wrong','unknown'):
            for days in (1,3,7):
                cursor.execute('''INSERT INTO review_queue(attempt_id,review_date,interval_label,status)
                  VALUES (?,?,?,'pending')''',(attempt_id,(date.fromisoformat(test_date)+timedelta(days=days)).isoformat(),f'D+{days}'))
