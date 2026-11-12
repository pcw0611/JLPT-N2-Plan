import { env } from 'cloudflare:workers';
import { validateCompositionResult } from '../../../lib/composition-result.mjs';

function response(request: Request, body: object, status=200) {
  const origin=request.headers.get('origin');
  const allowed=['https://jlpt-study-calendar.pcwww.chatgpt.site','https://jlpt-study-calendar.pcw0611.workers.dev'];
  const headers: Record<string,string>={'Vary':'Origin'};
  if(origin && allowed.includes(origin))headers['Access-Control-Allow-Origin']=origin;
  return Response.json(body,{status,headers});
}

export async function OPTIONS(request: Request) {
  const origin=request.headers.get('origin') || '';
  if(!['https://jlpt-study-calendar.pcwww.chatgpt.site','https://jlpt-study-calendar.pcw0611.workers.dev'].includes(origin))return new Response(null,{status:403});
  return new Response(null,{status:204,headers:{'Access-Control-Allow-Origin':origin,
    'Access-Control-Allow-Methods':'POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type','Vary':'Origin'}});
}

export async function POST(request: Request) {
  let body: any;
  try { body = validateCompositionResult(await request.json()); }
  catch { return response(request,{ok:false,error:'invalid_sentence_composition_submission'},400); }
  try {
    const db=env.DB;
    if (!db) throw Error('Database unavailable');
    // Shares the existing submissions table; duplicate retries use the stable run UUID.
    await db.prepare(`CREATE TABLE IF NOT EXISTS exam_submissions (
      id INTEGER PRIMARY KEY AUTOINCREMENT, exam_type TEXT NOT NULL, title TEXT NOT NULL,
      course TEXT, elapsed_seconds INTEGER NOT NULL, total_questions INTEGER NOT NULL,
      correct_count INTEGER NOT NULL, wrong_count INTEGER NOT NULL, accuracy INTEGER NOT NULL,
      date TEXT NOT NULL, payload_json TEXT NOT NULL, created_at TEXT NOT NULL)`).run();
    await db.prepare(`CREATE UNIQUE INDEX IF NOT EXISTS exam_submissions_composition_run
      ON exam_submissions(json_extract(payload_json,'$.submissionId'))
      WHERE exam_type='sentence_composition'`).run();
    await db.prepare(`INSERT OR IGNORE INTO exam_submissions
      (exam_type,title,course,elapsed_seconds,total_questions,correct_count,wrong_count,accuracy,date,payload_json,created_at)
      VALUES (?,?,?,?,?,?,?,?,?,?,?)`).bind('sentence_composition',body.title,body.course,
        body.elapsedSeconds,body.totalQuestions,body.correctCount,body.wrongCount,
        Math.round(body.correctCount/body.totalQuestions*100),body.date,JSON.stringify(body),new Date().toISOString()).run();
    const row=await db.prepare(`SELECT id FROM exam_submissions WHERE exam_type='sentence_composition'
      AND json_extract(payload_json,'$.submissionId')=?`).bind(body.submissionId).first<{id:number}>();
    return response(request,{ok:true,id:row?.id});
  } catch { return response(request,{ok:false,error:'submission_storage_failed'},500); }
}
