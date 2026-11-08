// Generate an auditable compare-and-update SQL plan from a backed-up D1 export.
// This script does not connect to a service or modify any database itself.
import fs from 'node:fs';
import path from 'node:path';
import {normalizeGrammarResult} from '../lib/grammar-result.mjs';
const [input,output]=process.argv.slice(2);
if(!input||!output)throw new Error('Usage: node plan_grammar_result_repair.mjs input.json output.sql');
const data=JSON.parse(fs.readFileSync(input,'utf8').replace(/^\uFEFF/,''));
const rows=Array.isArray(data)?data.flatMap(block=>block.results||[]):data.submissions||[];
const quote=s=>"'"+String(s).replaceAll("'","''")+"'";
const statements=[],audit=[],unresolved=[];
for(const row of rows) {
  const raw=row.payload_json??row.payloadJson;
  let old;try{old=JSON.parse(raw)}catch{continue}
  const normalized=normalizeGrammarResult(old);
  if(normalized===old){
    if(old.examType==='grammar-speedrun'&&old.details?.termination_reason==='early'&&old.totalQuestions!==old.answeredQuestions&&old.details?.scoring_version!=='answered-v1')unresolved.push(row.id);
    continue;
  }
  if(!Number.isInteger(row.id))throw new Error('Non-numeric row ID');
  const serialized=JSON.stringify(normalized);
  // D1 limits statement length. Keep the full original in the backup, then guard
  // the immutable row with its byte length, prefix, count and creation timestamp
  // rather than duplicating an entire 200-question JSON payload in the WHERE.
  const prefix=Array.from(raw).slice(0,512).join('');
  const oldTotal=row.total_questions??row.totalQuestions;
  const created=row.created_at??row.createdAt;
  const guard=`id=${row.id} AND total_questions=${oldTotal} AND length(CAST(payload_json AS BLOB))=${Buffer.byteLength(raw,'utf8')} AND substr(payload_json,1,${Array.from(prefix).length})=${quote(prefix)}${created ? ' AND created_at='+quote(created) : ''}`;
  const statement=`UPDATE exam_submissions SET total_questions=${normalized.totalQuestions}, correct_count=${normalized.correctCount}, wrong_count=${normalized.wrongCount}, accuracy=${normalized.accuracy}, course=${quote(normalized.course??row.course??'')}, payload_json=${quote(serialized)} WHERE ${guard};`;
  if(Buffer.byteLength(statement,'utf8')>99000)throw new Error('Repair exceeds the D1 statement limit; use a JSON patch for row '+row.id);
  statements.push(statement);
  audit.push({id:row.id,date:row.date,before:row.total_questions??row.totalQuestions,after:normalized.totalQuestions,correct:normalized.correctCount,unattempted:normalized.unattemptedCount});
}
if(unresolved.length)throw new Error('Unverifiable partial rows: '+unresolved.join(','));
fs.writeFileSync(output,statements.join('\n')+'\nSELECT id,total_questions,correct_count,accuracy FROM exam_submissions WHERE id IN ('+(audit.map(x=>x.id).join(',')||'NULL')+');\n');
fs.writeFileSync(path.join(path.dirname(output),'repair-audit.json'),JSON.stringify(audit,null,2));
console.log(JSON.stringify({repairs:audit,sql:output}));
