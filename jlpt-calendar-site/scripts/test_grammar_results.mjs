import assert from 'node:assert/strict';
import {normalizeGrammarResult,normalizeGrammarRow} from '../lib/grammar-result.mjs';

const attempt=(status,item_no)=>({status,item_no,selected_text:status==='unanswered'?null:'answer',response_seconds:status==='unanswered'?0:2});
function fixture(states=['correct','correct','correct']) {
  const attempts=[...states,...Array(200-states.length).fill('unanswered')].map((s,i)=>attempt(s,i+1));
  return {examType:'grammar-speedrun',course:`종합 · ${states.length}/200문항 응답`,
    totalQuestions:200,answeredQuestions:states.length,correctCount:states.filter(s=>s==='correct').length,
    wrongCount:states.filter(s=>s==='wrong').length,unknownCount:states.filter(s=>s==='unknown').length,
    unansweredCount:200-states.length,elapsedSeconds:22,date:'2026-11-03',
    details:{test_id:'n2-grammar-speedrun-v2',termination_reason:'early',planned_items:200,answered_items:states.length,attempts}};
}
const old=fixture(),n=normalizeGrammarResult(old);
assert.equal(n.totalQuestions,3);assert.equal(n.correctCount,3);assert.equal(n.accuracy,100);
assert.equal(n.unansweredCount,0);assert.equal(n.unattemptedCount,197);assert.equal(n.plannedQuestions,200);
assert.equal(n.details.attempts.length,3);assert.equal(n.details.unattempted_questions.length,197);
assert.equal(n.details.score_correction.previous_total,200);assert.equal(n.details.scoring_version,'answered-v1');
assert.equal(n.elapsedSeconds,old.elapsedSeconds);assert.equal(n.date,old.date);
assert(!n.course.includes('3/200'));assert.equal(normalizeGrammarResult(n),n,'idempotent');
assert.equal(old.totalQuestions,200,'input evidence stays untouched');assert.equal(old.details.attempts.length,200);
const mixed=normalizeGrammarResult(fixture(['correct','wrong','unknown']));
assert.equal(mixed.totalQuestions,3);assert.equal(mixed.correctCount,1);assert.equal(mixed.wrongCount,1);assert.equal(mixed.unknownCount,1);assert.equal(mixed.accuracy,33);
const viewedThird=normalizeGrammarResult(fixture(['correct','wrong']));assert.equal(viewedThird.totalQuestions,2,'Do not count the unselected third question');
for(const original of [
  {...old,examType:'official-mock'},
  {...old,details:{...old.details,termination_reason:'completed'}},
  {...old,answeredQuestions:4},
  {...old,correctCount:4},
  {...old,details:{...old.details,attempts:[]}},
]) assert.equal(normalizeGrammarResult(original),original,'No inference for full exams or inconsistent records');
const row={id:36,title:'practice',date:old.date,elapsedSeconds:22,totalQuestions:200,correctCount:3,wrongCount:0,accuracy:100,payloadJson:JSON.stringify(old)};
const fixed=normalizeGrammarRow(row);assert.equal(fixed.id,row.id);assert.equal(fixed.title,row.title);assert.equal(fixed.elapsedSeconds,row.elapsedSeconds);assert.equal(fixed.totalQuestions,3);
assert.equal(normalizeGrammarRow(fixed),fixed);
const staleColumns={...row,payloadJson:JSON.stringify(n)};assert.equal(normalizeGrammarRow(staleColumns).totalQuestions,3);
assert.equal(normalizeGrammarRow({...row,payloadJson:'invalid'}).totalQuestions,200);
console.log('PASS: partial 3/3 and mixed 1/3; actual responses, excluded pool, immutable evidence, idempotence, stored/read normalization, full-exam protection.');
