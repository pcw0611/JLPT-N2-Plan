import { env } from 'cloudflare:workers';
import { getDb } from '../../../db';
import { examSubmissions } from '../../../db/schema';
import { desc, gt } from 'drizzle-orm';

let tableEnsured = false;
async function ensureSubmissionsTable() {
  if (tableEnsured) return;
  try {
    if (env.DB) {
      await env.DB.prepare(`
        CREATE TABLE IF NOT EXISTS exam_submissions (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          exam_type TEXT NOT NULL,
          title TEXT NOT NULL,
          course TEXT,
          elapsed_seconds INTEGER NOT NULL,
          total_questions INTEGER NOT NULL,
          correct_count INTEGER NOT NULL,
          wrong_count INTEGER NOT NULL,
          accuracy INTEGER NOT NULL,
          date TEXT NOT NULL,
          payload_json TEXT NOT NULL,
          created_at TEXT NOT NULL
        )
      `).run();
      tableEnsured = true;
    }
  } catch (err) {
    console.error('ensureSubmissionsTable error:', err);
  }
}

export async function POST(request: Request) {
  try {
    await ensureSubmissionsTable();

    const body = await request.json() as Record<string, any>;
    const examType = String(body.examType || 'exam');
    const title = String(body.title || 'JLPT Training');
    const course = body.course ? String(body.course) : null;
    const elapsedSeconds = Number(body.elapsedSeconds || 0);
    const totalQuestions = Number(body.totalQuestions || 0);
    const correctCount = Number(body.correctCount || 0);
    const wrongCount = Number(body.wrongCount ?? Math.max(0, totalQuestions - correctCount));
    const accuracy = Number(body.accuracy ?? (totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0));

    const todaySeoul = new Intl.DateTimeFormat('sv-SE', {
      timeZone: 'Asia/Seoul',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    }).format(new Date());
    const date = (typeof body.date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(body.date)) ? body.date : todaySeoul;
    const createdAt = new Date().toISOString();

    const payloadJson = JSON.stringify(body);

    const inserted = await getDb().insert(examSubmissions).values({
      examType,
      title,
      course,
      elapsedSeconds,
      totalQuestions,
      correctCount,
      wrongCount,
      accuracy,
      date,
      payloadJson,
      createdAt,
    }).returning({ id: examSubmissions.id });

    return Response.json({
      ok: true,
      id: inserted[0]?.id,
      date,
      message: '학습 결과가 정상적으로 자동 기록되었습니다.',
    });
  } catch (err: any) {
    console.error('Submit exam error:', err);
    return Response.json({ ok: false, error: err.message || 'internal_error' }, { status: 500 });
  }
}

export async function GET(request: Request) {
  try {
    await ensureSubmissionsTable();

    const authHeader = request.headers.get('authorization');
    const syncSecret = env.JLPT_SYNC_SECRET;
    const cookieHeader = request.headers.get('cookie') || '';
    const hasPinCookie = /(?:^|;\s*)jlpt_auth=6997(?:;|$)/.test(cookieHeader);
    const hasValidBearer = syncSecret && authHeader === `Bearer ${syncSecret}`;

    if (!hasPinCookie && !hasValidBearer) {
      return Response.json({ ok: false, error: 'unauthorized' }, { status: 401 });
    }

    const url = new URL(request.url);
    const sinceId = Number(url.searchParams.get('since') || 0);
    const limit = Math.min(100, Math.max(1, Number(url.searchParams.get('limit') || 50)));

    let query = getDb().select().from(examSubmissions);
    if (sinceId > 0) {
      query = query.where(gt(examSubmissions.id, sinceId)) as any;
    }
    const rows = await (query.orderBy(desc(examSubmissions.id)).limit(limit) as any);

    return Response.json({
      ok: true,
      submissions: rows,
    });
  } catch (err: any) {
    console.error('Get exam submissions error:', err);
    return Response.json({ ok: false, error: err.message || 'internal_error' }, { status: 500 });
  }
}
