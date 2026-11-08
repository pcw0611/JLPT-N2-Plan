"""Integration test against a LOCAL Miniflare database only. Never a hosted endpoint."""
from pathlib import Path
import json
import urllib.error
import urllib.request
import uuid

ROOT=Path(__file__).resolve().parents[1]
ENDPOINT='http://localhost:8766/api/submit-past-exam'
exam=json.loads((ROOT/'database/past_exams/2023_07_exam.json').read_text(encoding='utf-8'))
attempts=[dict(item_no=q['id'],item_type_id=q['itemTypeId'],category=q['category'],status='correct',
               selected_index=q['answer'],correct_index=q['answer'],selected_text=q['choices'][q['answer']],
               correct_text=q['choices'][q['answer']],response_seconds=None if q['section']=='listening' else 1)
          for q in exam['questions']]
payload=dict(examType='past_exam',title='검증 테스트 · isolated local D1',course='검증 테스트',
             submissionId=str(uuid.uuid4()),date='2026-11-08',elapsedSeconds=2604,totalQuestions=101,
             correctCount=101,wrongCount=0,unknownCount=0,unansweredCount=0,
             details=dict(test_id='n2-past-202307',termination_reason='submitted',attempts=attempts))
def post(data):
    request=urllib.request.Request(ENDPOINT,data=json.dumps(data).encode(),headers={
        'Content-Type':'application/json','Origin':'http://localhost:8766'})
    with urllib.request.urlopen(request,timeout=30) as response:
        return json.load(response),response.headers.get('Access-Control-Allow-Origin')

a,origin=post(payload)
b,_=post(payload)
assert a['ok'] and a['id']==b['id']
try:
    post({**payload,'correctCount':99})
    raise AssertionError('Invalid totals accepted')
except urllib.error.HTTPError as error:
    assert error.code==400
request=urllib.request.Request(ENDPOINT,method='OPTIONS',headers={
    'Origin':'http://localhost:8766',
    'Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'Content-Type'})
try:
    urllib.request.urlopen(request,timeout=30)
    raise AssertionError('Unexpected origin allowed')
except urllib.error.HTTPError as error:
    assert error.code==403
print('PASS: local Miniflare D1 submission, idempotent retry, invalid totals400, unknown CORSorigin403. No hosted writes.')
