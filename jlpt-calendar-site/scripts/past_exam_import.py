"""Import only an actual submitted past-paper result; never fabricate an attempt."""
from datetime import date, timedelta
import json

def get_past_exam_payload(submission):
    try:
        payload=json.loads(submission.get('payload_json') or '{}')
    except (TypeError,ValueError):
        return None
    details=payload.get('details',{}) if isinstance(payload,dict) else {}
    if details.get('test_id')!='n2-past-202307':return None
    if payload.get('examType')!='past_exam' or details.get('termination_reason')!='submitted':
        raise ValueError('Past exam has not been submitted')
    attempts=details.get('attempts',[])
    if len(attempts)!=101 or [a.get('item_no') for a in attempts]!=list(range(1,102)):
        raise ValueError('Incomplete past-exam attempts')
    return payload

def insert_past_exam_attempts(cursor,test_id,test_date,payload):
    """Called in the existing sync transaction, after its duplicate test-ID guard."""
    date.fromisoformat(test_date)
    valid_types={r[0] for r in cursor.execute('SELECT id FROM item_types')}
    for attempt in payload['details']['attempts']:
        status=attempt.get('status')
        if status not in ('correct','wrong','unknown','unanswered') or attempt.get('item_type_id') not in valid_types:
            raise ValueError('Invalid past-exam attempt')
        cursor.execute('''INSERT INTO question_attempts
            (test_id,item_no,item_type_id,level_label,response_state,response_seconds,selected_text,correct_text)
            VALUES (?,?,?,'N2 기출 자료',?,?,?,?)''',
            (test_id,attempt['item_no'],attempt['item_type_id'],status,
             attempt.get('response_seconds'),attempt.get('selected_text'),attempt.get('correct_text')))
        attempt_id=cursor.lastrowid
        if status in ('wrong','unknown','unanswered'):
            for days in (1,3,7):
                cursor.execute('''INSERT INTO review_queue(attempt_id,review_date,interval_label,status)
                    VALUES (?,?,?,'pending')''',(attempt_id,(date.fromisoformat(test_date)+timedelta(days=days)).isoformat(),f'D+{days}'))
