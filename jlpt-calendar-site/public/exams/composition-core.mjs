export const VERSION=1;
export const fresh=()=>({version:VERSION,items:{},runs:[],active:null,outbox:[]});
export const day=(now=new Date())=>new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(now);
export function addDays(date,n){const d=new Date(date+'T12:00:00Z');d.setUTCDate(d.getUTCDate()+n);return d.toISOString().slice(0,10);}
export function shuffle(xs,random=Math.random){const a=[...xs];for(let i=a.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
export function makeRun(ids,random=Math.random,uuid=crypto.randomUUID()){
  const order=shuffle(ids,random),positions=shuffle(order.map((_,i)=>i%4),random);
  return {id:uuid,order,choices:Object.fromEntries(order.map((id,i)=>{const p=shuffle([0,1,3],random);p.splice(positions[i],0,2);return [id,p];})),answers:{},times:{},index:0,elapsed:0,date:day()};
}
export function statusOf(item,today=day()){
  if(!item)return 'new';
  if((item.reviewDates||[]).some(d=>d<=today))return 'due';
  return item.last.status;
}
export function grade(run,questions,date=day()){
  const lookup=new Map(questions.map(q=>[q.id,q]));
  const attempts=run.order.map(id=>{const q=lookup.get(id),v=run.answers[id];
    const status=v===undefined?'unanswered':v===-1?'unknown':v===q.answer?'correct':'wrong';
    return {item_no:id,item_type_id:'sentence_composition',subtype:q.subtype,status,selected_id:v??null,
      selected_text:v===undefined?null:v===-1?'分からない':q.parts[v],correct_text:q.parts[q.answer],
      response_seconds:Math.max(0,Math.round(run.times[id]||0)),display_order:run.choices[id]};});
  const counts=Object.fromEntries(['correct','wrong','unknown','unanswered'].map(s=>[s,attempts.filter(a=>a.status===s).length]));
  return {submissionId:run.id,examType:'sentence_composition',title:'N2 文の組み立て 100',course:'自主制作・文の組み立て',date,
    elapsedSeconds:Math.max(0,Math.round(run.elapsed)),totalQuestions:attempts.length,correctCount:counts.correct,
    wrongCount:counts.wrong,unknownCount:counts.unknown,unansweredCount:counts.unanswered,
    accuracy:Math.round(counts.correct/attempts.length*100),details:{test_id:'n2-sentence-composition-100',termination_reason:'submitted',memory_timing:'independent_practice',attempts}};
}
export function applyResult(state,result){
  if(state.runs.some(r=>r.submissionId===result.submissionId))return state;
  const next=structuredClone(state);
  for(const a of result.details.attempts){
    if(a.status==='unanswered')continue; // An unopened question remains unlearned.
    const old=next.items[a.item_no];
    let dates=old?.reviewDates||[];
    if(a.status==='wrong'||a.status==='unknown')dates=[1,3,7].map(n=>addDays(result.date,n));
    else dates=dates.filter(d=>d>result.date); // Keep future intervals. Same-item success is not graduation.
    next.items[a.item_no]={last:{...a,date:result.date},reviewDates:dates,attempts:(old?.attempts||0)+1};
  }
  next.runs.push(result);next.active=null;
  next.outbox.push(result);
  return next;
}
export function validateBackup(s){
  if(!s||s.version!==VERSION||!s.items||typeof s.items!=='object'||!Array.isArray(s.runs)||!Array.isArray(s.outbox))throw Error('Invalid backup');
  for(const [id,v] of Object.entries(s.items)){
    if(!/^\d+$/.test(id)||+id<1||+id>100||!['correct','wrong','unknown'].includes(v?.last?.status)||!Array.isArray(v.reviewDates)||!v.reviewDates.every(d=>/^\d{4}-\d{2}-\d{2}$/.test(d)))throw Error('Invalid item');
  }
  if(s.active){const r=s.active;if(!Array.isArray(r.order)||!r.order.length||new Set(r.order).size!==r.order.length||!r.order.every(i=>Number.isInteger(i)&&i>=1&&i<=100)||!Number.isFinite(r.elapsed)||r.elapsed<0||!Number.isInteger(r.index)||r.index<0||r.index>=r.order.length)throw Error('Invalid run');
    for(const id of r.order){if(!Array.isArray(r.choices?.[id])||[...r.choices[id]].sort().join()!=='0,1,2,3'||![-1,0,1,2,3,undefined].includes(r.answers?.[id]))throw Error('Invalid choices');}}
  return s;
}
