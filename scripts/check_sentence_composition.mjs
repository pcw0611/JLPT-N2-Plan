import assert from 'node:assert/strict';
import fs from 'node:fs';
import {fresh,makeRun,grade,applyResult,statusOf,validateBackup,day,prioritizeIds,intersectingIds} from '../jlpt-calendar-site/public/exams/composition-core.mjs';
import {validateCompositionResult} from '../jlpt-calendar-site/lib/composition-result.mjs';
import {addStudySeconds,formatStudyTime} from '../jlpt-calendar-site/lib/study-time.mjs';
const qs=JSON.parse(fs.readFileSync(new URL('../jlpt-calendar-site/public/exams/n2-sentence-composition-100.json',import.meta.url))).questions;
assert.equal(qs.length,100);assert.equal(new Set(qs.map(q=>q.full)).size,100);
assert.deepEqual(qs.map(q=>q.id),Array.from({length:100},(_,i)=>i+1));
for(const q of qs){assert.equal(new Set(q.parts).size,4);assert.equal(q.answer,q.star-1);assert.equal(q.full,q.before+q.parts.join('')+q.after);assert(!/[가-힣]/.test(q.before+q.parts.join('')+q.after));assert(q.reviewFull.includes('<ruby>'));}
for(let n=0;n<100;n++){
 const run=makeRun(qs.map(q=>q.id));const positions=[0,0,0,0];
 for(const id of run.order){positions[run.choices[id].indexOf(2)]++;run.answers[id]=2;run.times[id]=1;}
 assert.deepEqual(positions,[25,25,25,25]);run.elapsed=100;
 const result=grade(run,qs,'2026-11-11');assert.equal(result.correctCount,100);assert.equal(validateCompositionResult(result).correctCount,100);
}
const run=makeRun([1,2,3,4]);run.answers={1:2,2:0,3:-1};run.elapsed=12;
const result=grade(run,qs,'2026-11-11');assert.deepEqual([result.correctCount,result.wrongCount,result.unknownCount,result.unansweredCount],[1,1,1,1]);
let state=applyResult(fresh(),result);assert.equal(Object.keys(state.items).length,3);assert(!state.items[4]);assert.deepEqual(state.items[2].reviewDates,['2026-11-12','2026-11-14','2026-11-18']);
assert.equal(statusOf(state.items[2],'2026-11-12'),'due');assert.equal(statusOf(state.items[2],'2026-11-11'),'wrong');
assert.equal(applyResult(state,result).runs.length,1);
const retry=makeRun([2]);retry.answers[2]=2;state=applyResult(state,grade(retry,qs,'2026-11-12'));
assert.deepEqual(state.items[2].reviewDates,['2026-11-14','2026-11-18']);assert.equal(statusOf(state.items[2],'2026-11-12'),'correct');
const week=makeRun([2]);week.answers[2]=2;state=applyResult(state,grade(week,qs,'2026-11-18'));assert.equal(statusOf(state.items[2],'2026-11-18'),'correct');
assert.deepEqual(validateBackup(JSON.parse(JSON.stringify(state))),state);
const active=fresh();active.active=makeRun([1,2]);active.active.answers[1]=-1;assert(validateBackup(JSON.parse(JSON.stringify(active))).active);
assert.throws(()=>validateBackup({version:1,items:{101:{last:{status:'correct'},reviewDates:[]}},runs:[],outbox:[]}));
const tampered=structuredClone(result);tampered.details.attempts[0].status=tampered.details.attempts[0].status==='wrong'?'correct':'wrong';assert.throws(()=>validateCompositionResult(tampered));
const dup=structuredClone(result);dup.details.attempts.push(dup.details.attempts[0]);assert.throws(()=>validateCompositionResult(dup));
assert.equal(day(new Date('2026-11-10T15:01:00Z')),'2026-11-11');
const items={1:{last:{status:'correct',date:'2026-11-01'},reviewDates:['2026-11-03']},2:{last:{status:'wrong',date:'2026-11-01'},reviewDates:['2026-11-02']},3:{last:{status:'wrong',date:'2026-11-10'},reviewDates:['2026-11-12']},4:{last:{status:'unknown',date:'2026-11-10'},reviewDates:['2026-11-12']},100:{last:{status:'correct',date:'2026-11-10'},reviewDates:['2026-11-18']}};
for(let i=0;i<50;i++){
 const batch=prioritizeIds(qs.map(q=>q.id),items,10,'2026-11-11');assert.equal(batch.length,10);assert.deepEqual(batch.slice(0,2),[2,1]);assert(batch.includes(3)&&batch.includes(4));assert(!batch.includes(100));assert.equal(new Set(batch).size,10);
}
assert.deepEqual(prioritizeIds([100,4,1],items,2,'2026-11-11'),[1,4]);
assert.equal(prioritizeIds([2,2,3],items,100,'2026-11-11').length,2);
const cells=[{id:1,left:0,right:10,top:0,bottom:10},{id:2,left:11,right:21,top:0,bottom:10},{id:3,left:0,right:10,top:11,bottom:21}];
assert.deepEqual(intersectingIds(cells,{left:3,right:15,top:3,bottom:15}),[1,2,3]);
assert.deepEqual(intersectingIds(cells,{left:10,right:11,top:0,bottom:10}),[]);
const elapsed=[24,30,108,7,7,47,35,14,20].reduce(addStudySeconds,0);
assert.equal(formatStudyTime(elapsed),'0時間4分52秒');assert.equal(formatStudyTime(addStudySeconds(100,7)),'1時間40分7秒');
console.log('PASS: 100 questions, 100 full shuffled runs, mixed grading, stable choice IDs, resume JSON, D+1/3/7, no false mastery, duplicate run guard, server validation.');
console.log('PASS: oldest-due/error/new/correct priority, filtered limits, drag rectangle intersections, sub-minute session accumulation.');
