import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const html=fs.readFileSync('jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html','utf8');
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(x=>x[1]);
const nodes=new Map();
const node=()=>({insertAdjacentElement(){},setAttribute(){},pause(){},value:'',checked:false,textContent:'',innerHTML:'',parentElement:{},classList:{add(){},remove(){},contains(){return true}},querySelectorAll(){return []}});
const document={createElement:()=>node(),getElementById(id){if(!nodes.has(id))nodes.set(id,node());return nodes.get(id)},querySelectorAll(){return []}};
const memory=new Map(); let writes=0;
const context=vm.createContext({document,window:{addEventListener(){},scrollTo(){}},localStorage:{getItem:k=>memory.get(k),setItem(k,v){writes++;memory.set(k,v)}},Date,Set,Intl,console,setInterval:()=>1,clearInterval(){},confirm:()=>true,alert(){}});
scripts.forEach(s=>vm.runInContext(s,context));
vm.runInContext(fs.readFileSync('jlpt-calendar-site/public/exams/mock-review-filters.js','utf8'),context);
const run=s=>vm.runInContext(s,context);
assert.equal(run('ALL_ERROR_QUESTIONS.length'),139);
assert.equal(run('new Set(ALL_ERROR_QUESTIONS.map(q=>q.id)).size'),139);
assert.equal(run("ALL_ERROR_QUESTIONS.filter(q=>q.id.startsWith('err-202307-')).length"),52);
for (const q of run('ALL_ERROR_QUESTIONS')) {
 assert.ok(q.correct_num>=1&&q.correct_num<=q.choices.length);
 if(q.is_listening)assert.ok(fs.existsSync('jlpt-calendar-site/public/exams/audio_clips/'+q.audio_file),q.id);
}
document.getElementById('scopeExam').value='2023年7月 本試験資料';
assert.equal(run('getFilteredAnkiQuestions().length'),52);
for(const [domain,n] of [['어휘',13],['문법',12],['독해',10],['청해',17]]){document.getElementById('scopeDomain').value=domain;assert.equal(run('getFilteredAnkiQuestions().length'),n)}
document.getElementById('scopeDomain').value='문법';document.getElementById('scopeType').value='文の文法2';
assert.equal(run('getFilteredAnkiQuestions().length'),4);
run("state.ankiSearchQuery='없는문항xyz'");assert.equal(run('getFilteredAnkiQuestions().length'),0);run("state.ankiSearchQuery=''");
run("renderQuestion=()=>{};updateOmrCount=()=>{};state.activeQuestions=getFilteredAnkiQuestions();state.currentIndex=0;state.feedbackMode='instant';selectAnswer(5);selectAnswer(1)");
assert.equal(run('state.userAnswers[state.activeQuestions[0].id]'),5);
run("state.feedbackMode='batch';state.currentAnswered=false;selectAnswer(1)");assert.equal(run('state.currentIndex'),0);
run("initResultControls=()=>{};renderExplanations=()=>{};state.userAnswers={};state.submitted=false;state.startTime=Date.now();state.masteredIds=new Set([state.activeQuestions[0].id]);state.srsData={};finishExam(false)");
assert.match(document.getElementById('resSubtitle').innerHTML,/未回答: 4問/);
assert.equal(document.getElementById('resWrongCount').textContent,0);
assert.equal(run('Object.keys(state.srsData).length'),0);
assert.equal(run('state.masteredIds.size'),1);
const prior=writes;run('finishExam(false)');assert.equal(writes,prior);
memory.clear();run("state.submitted=false;state.startTime=Date.now();state.userAnswers={};state.masteredIds=new Set();state.srsData={};state.activeQuestions.forEach((q,i)=>{if(i===0)state.userAnswers[q.id]=q.correct_num;if(i===1)state.userAnswers[q.id]=q.correct_num===1?2:1;if(i===2)state.userAnswers[q.id]=5});finishExam(false)");
assert.equal(document.getElementById('resWrongCount').textContent,1);
assert.equal(document.getElementById('resUnknownCount').textContent,1);
assert.match(document.getElementById('resSubtitle').innerHTML,/未回答: 1問/);
assert.match(document.getElementById('resFraction').textContent,/1 \/ 4/);
assert.equal(run('Object.keys(state.srsData).length'),3);
console.log('PASS:139 IDs,52 actual errors,all local audio,combined filters,empty search,answer lock,batch navigation,unanswered preservation,duplicate grading');

run("state.ankiFilter='unresolved'");assert.equal(run("getFilteredAnkiQuestions().length"),3);
run("state.ankiFilter='all'");assert.equal(run("getFilteredAnkiQuestions().length"),4);
console.log("PASS unresolved excludes saved correct answers, all retains them");
