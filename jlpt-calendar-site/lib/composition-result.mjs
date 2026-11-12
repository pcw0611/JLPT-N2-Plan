import key from './composition-key.mjs';
export function validateCompositionResult(body){
  const fail=()=>{throw Error('Invalid composition submission');};
  if(body?.examType!=='sentence_composition'||body.details?.test_id!=='n2-sentence-composition-100'||body.details.termination_reason!=='submitted')fail();
  if(typeof body.submissionId!=='string'||!/^[\da-f]{8}-[\da-f]{4}-4[\da-f]{3}-[89ab][\da-f]{3}-[\da-f]{12}$/i.test(body.submissionId))fail();
  if(!/^\d{4}-\d{2}-\d{2}$/.test(body.date)||Number.isNaN(Date.parse(body.date+'T00:00:00Z')))fail();
  if(!Number.isInteger(body.elapsedSeconds)||body.elapsedSeconds<0||body.elapsedSeconds>604800)fail();
  const input=body.details.attempts;if(!Array.isArray(input)||!input.length||input.length>100||new Set(input.map(a=>a.item_no)).size!==input.length)fail();
  const attempts=input.map(a=>{
    const q=key[a.item_no];if(!q||!Number.isInteger(a.item_no)||![null,-1,0,1,2,3].includes(a.selected_id)||!Number.isInteger(a.response_seconds)||a.response_seconds<0||a.response_seconds>604800)fail();
    if(!Array.isArray(a.display_order)||[...a.display_order].sort().join()!=='0,1,2,3')fail();
    const status=a.selected_id===null?'unanswered':a.selected_id===-1?'unknown':a.selected_id===q.answer?'correct':'wrong';
    if(a.status!==status)fail();
    return {...a,item_type_id:'sentence_composition',status,selected_text:a.selected_id===null?null:a.selected_id===-1?'分からない':q.parts[a.selected_id],correct_text:q.parts[q.answer]};
  });
  const count=s=>attempts.filter(a=>a.status===s).length;
  return {...body,title:'N2 文の組み立て 100',course:'自主制作・文の組み立て',totalQuestions:attempts.length,
    correctCount:count('correct'),wrongCount:count('wrong'),unknownCount:count('unknown'),unansweredCount:count('unanswered'),
    accuracy:Math.round(count('correct')/attempts.length*100),details:{...body.details,attempts}};
}
