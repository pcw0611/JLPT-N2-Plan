// Runs the real browser runtime in a deterministic sandbox. Never contacts a live API/DB.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {randomUUID} from 'node:crypto';
import {validatePastExamResult} from '../jlpt-calendar-site/lib/past-exam-result.mjs';
const exam=JSON.parse(fs.readFileSync(new URL('../database/past_exams/2023_07_exam.json',import.meta.url),'utf8'));
const script=fs.readFileSync(new URL('../jlpt-calendar-site/public/exams/past-exam-runtime.js',import.meta.url),'utf8');
const html=fs.readFileSync(new URL('../jlpt-calendar-site/public/exams/n2-past-exam-202307-mock.html',import.meta.url),'utf8');
assert.equal(exam.questions.length,101);
assert.deepEqual(exam.questions.map(q=>q.id),Array.from({length:101},(_,i)=>i+1));
assert.deepEqual(['vocabulary','grammar','reading','listening'].map(s=>exam.questions.filter(q=>q.section===s).length),[30,21,20,30]);
// Q39 is independently solved as 1 (にほかならない); do not inherit a mismatched answer-table number.
const expected=['24413','13424','132','2314432','24123','42113','314241341232','14233','3241','42124','13431324','43','421','23','32223','231313','12444','22331121231','313'].join('');
assert.equal(exam.questions.map(q=>q.answer+1).join(''),expected);
for(const q of exam.questions){assert(q.sourcePages.length);if(q.order)assert.equal(q.order[(q.starSlot||3)-1]-1,q.answer);assert(!/<script|on\w+=|javascript:/i.test(JSON.stringify(q)));}
assert(!html.includes('tailwindcss.min.js'),'Screen hiding must not depend on external CSS');
function sandbox(initial=null,preview=true){
 const nodes=new Map(),events={},windowEvents={},storage=new Map(),timers=[];let now=Date.parse('2026-11-08T03:00:00Z'),posts=0;
 const storageKey=`jlpt-past-${exam.id}-${exam.version}${preview?'-preview':''}`;
 if(initial)storage.set(storageKey,JSON.stringify(initial));
 const node=id=>{if(!nodes.has(id)){const set=new Set();nodes.set(id,{id,innerHTML:'',textContent:'',hidden:false,disabled:false,dataset:{},classList:{add(...xs){xs.forEach(x=>set.add(x));},remove(...xs){xs.forEach(x=>set.delete(x));},toggle(x,on){on?set.add(x):set.delete(x);},contains(x){return set.has(x);}},click(){},addEventListener(){}});}return nodes.get(id);};
 class Audio{constructor(){this.listeners={};this.currentTime=0;this.duration=2588;this.playbackRate=1;this.ended=false;this.src='';}addEventListener(e,f){this.listeners[e]=f;}async play(){this.paused=false;this.listeners.playing?.();}pause(){this.paused=true;this.listeners.pause?.();}}
 const audio=new Audio();nodes.set('exam-audio',audio);node('exam-data').textContent=JSON.stringify(exam);
 class Clock extends Date{constructor(...a){super(...(a.length?a:[now]));}static now(){return now;}}
 const box={Date:Clock,Intl,URL,URLSearchParams,JSON,console,crypto:{randomUUID},Audio,Blob,confirm:()=>true,
 location:{search:preview?'?preview=1':''},document:{getElementById:node,addEventListener(n,f){events[n]=f;},querySelectorAll(){return[];},createElement(){return{click(){}};}},
 localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)},navigator:{clipboard:{async writeText(){}}},
 setInterval:f=>timers.push(f),setTimeout(){},fetch:async()=>{posts++;return{ok:true,json:async()=>({ok:true,id:1})};}};
 box.window={addEventListener(n,f){windowEvents[n]=f;},scrollTo(){}};vm.createContext(box);vm.runInContext(script,box);
 const click=(index,answer)=>events.click({target:{closest:s=>s==='[data-answer]'?{dataset:{answer:`${index}:${answer}`}}:null}});
 return {box,node,audio,click,events,timers,windowEvents,storage,get state(){return JSON.parse(storage.get(storageKey)||'null');},advance:s=>{now+=s*1000;timers.forEach(f=>f());},posts:()=>posts};
}
const p=sandbox(),api=p.box.window.pastExamQA;
let g=api.grade(exam.questions.map(q=>q.answer));assert.equal(g.correct,101);assert.equal(g.unanswered,0);
assert.equal(api.referenceScore(g.bySection).total,180);
g=api.grade(exam.questions.map(()=>null));assert.equal(g.unanswered,101);
assert.equal(api.referenceScore(g.bySection).total,0);
const reference=api.referenceScore({vocabulary:{correct:18,total:30},grammar:{correct:12,total:21},reading:{correct:14,total:20},listening:{correct:21,total:30}});
assert.equal(reference.total,119.3);assert.deepEqual(Array.from(reference.sections,s=>s.points),[35.3,42,42]);
assert.equal(api.referenceScore({}).total,0);
g=api.grade(exam.questions.map(q=>(q.answer+1)%q.choices.length));assert.equal(g.wrong,101);
g=api.grade(exam.questions.map((q,i)=>i%4===0?q.answer:i%4===1?(q.answer+1)%q.choices.length:i%4===2?-1:null));
assert.deepEqual([g.correct,g.wrong,g.unknown,g.unanswered],[26,25,25,25]);
assert.deepEqual(Array.from(api.reviewDates('2026-11-08')),['2026-11-09','2026-11-11','2026-11-15']);
p.node('start').onclick();p.advance(2);p.click(0,0);p.click(0,0);assert.equal(p.state.answers[0],null);p.click(0,-1);assert.equal(p.state.answers[0],-1);
p.node('end-written').onclick();assert.equal(p.state.phase,'written');p.node('confirm-no').onclick();assert.equal(p.state.phase,'written');p.node('end-written').onclick();p.node('confirm-yes').onclick();assert.equal(p.state.phase,'break');p.advance(601);assert.equal(p.state.phase,'listening-ready');await p.node('start-listening').onclick();assert.equal(p.state.phase,'listening');
const before=p.state.answers[0];p.click(0,1);assert.equal(p.state.answers[0],before,'Written answers lock during listening');
await p.node('submit').onclick();assert.equal(p.state.phase,'listening','Cannot submit before audio ends');
p.audio.currentTime=15;p.audio.listeners.timeupdate();p.audio.pause();assert.equal(p.state.interruptions.length,1);await p.node('resume-audio').onclick();
p.audio.currentTime=2500;p.audio.ended=true;p.audio.listeners.ended();p.node('submit').onclick();await p.node('confirm-yes').onclick();assert.equal(p.state.phase,'results');assert.equal(p.posts(),0,'Preview cannot write learning records');
validatePastExamResult(p.state.result);assert.equal(p.state.result.details.attempts.length,101);
assert.equal(p.state.result.details.reference_score.kind,'nonofficial_reference');
assert(p.node('results').innerHTML.includes('비공식 180점 참고점수'));
assert.equal(p.state.result.details.reference_score.total,api.referenceScore(p.state.result.details.by_section).total);
assert.throws(()=>validatePastExamResult({...p.state.result,correctCount:88}));
assert.throws(()=>validatePastExamResult({...p.state.result,totalQuestions:100}));
const frozen=JSON.stringify(p.state.result);p.click(71,1);await p.node('submit').onclick();assert.equal(JSON.stringify(p.state.result),frozen);
const saved=sandbox(p.state);saved.windowEvents.beforeunload();assert.equal(saved.state.phase,'results','An untouched intro must not overwrite a saved exam');saved.node('restore').onclick();assert(!saved.node('results').classList.contains('hidden'));
const timeout=sandbox();timeout.node('start').onclick();timeout.advance(105*60+2);assert.equal(timeout.state.phase,'break');assert.equal(timeout.state.writtenEndReason,'timeout');assert.equal(timeout.state.writtenEnd-timeout.state.writtenStart,105*60000);
const live=sandbox(null,false);if(!exam.ready)assert.equal(live.node('start').disabled,true,'An unresolved source must not allow real testing');
console.log('PASS: 101 IDs; independent answer key; 19 types; four grading patterns; D+1/3/7; toggle; timer timeout; break; audio failure/recovery; lock; result validation; reload preservation; preview writes=0.');
