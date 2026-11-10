// Validate supported completed papers before any persistent learning write.
import { exam202112Key } from './past-exam-202112-key.mjs';
export function validatePastExamResult(body) {
  if (!body || body.examType !== 'past_exam' || !['n2-past-202307','n2-past-202112'].includes(body.details?.test_id)) throw Error('Invalid exam');
  const key=body.details.test_id==='n2-past-202112'?exam202112Key:null;
  if (!/^[a-f0-9-]{36}$/i.test(body.submissionId || '')) throw Error('Invalid submission id');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(body.date || '')) throw Error('Invalid date');
  if (body.totalQuestions !== 101 || body.details.termination_reason !== 'submitted') throw Error('Incomplete exam');
  const attempts=body.details.attempts;
  if (!Array.isArray(attempts) || attempts.length!==101) throw Error('Invalid attempts');
  const counts={correct:0,wrong:0,unknown:0,unanswered:0};
  attempts.forEach((a,i)=>{
    if(key && (a.correct_index!==key[i].answer || a.item_type_id!==key[i].itemTypeId))throw Error('Answer key mismatch');
    if (a.item_no!==i+1 || !Object.hasOwn(counts,a.status)) throw Error('Invalid attempt');
    if (a.status==='unknown' && a.selected_index!==-1) throw Error('Invalid unknown');
    if (a.status==='unanswered' && a.selected_index!==null) throw Error('Invalid unanswered');
    if (['wrong','correct'].includes(a.status) && (!Number.isInteger(a.selected_index)||a.selected_index<0||a.selected_index>3)) throw Error('Invalid choice');
    if (key && ['wrong','correct'].includes(a.status) && a.selected_index>=key[i].choices)throw Error('Choice outside item range');
    if ((a.status==='correct') !== (a.selected_index===a.correct_index)) throw Error('Inconsistent grading');
    counts[a.status]++;
  });
  for(const [s,k]of [['correct','correctCount'],['wrong','wrongCount'],['unknown','unknownCount'],['unanswered','unansweredCount']])if(body[k]!==counts[s])throw Error('Inconsistent totals');
  if(!Number.isInteger(body.elapsedSeconds)||body.elapsedSeconds<0||body.elapsedSeconds>86400)throw Error('Invalid elapsed time');
  return body;
}
