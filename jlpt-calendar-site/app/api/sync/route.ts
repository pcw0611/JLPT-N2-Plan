import { env } from 'cloudflare:workers';
import { getDb } from '../../../db';
import { dailyReports } from '../../../db/schema';

export async function POST(request: Request) {
  const expected = env.JLPT_SYNC_SECRET;
  const supplied = request.headers.get('authorization');
  if (!expected || supplied !== `Bearer ${expected}`) {
    return Response.json({ ok: false }, { status: 401 });
  }

  const payload = await request.json() as Record<string, unknown>;
  if (typeof payload.date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(payload.date)) {
    return Response.json({ ok: false, error: 'invalid_date' }, { status: 400 });
  }

  const date = payload.date;
  await getDb().insert(dailyReports).values({
    date,
    payloadJson: JSON.stringify(payload),
    updatedAt: new Date().toISOString(),
  }).onConflictDoUpdate({
    target: dailyReports.date,
    set: {
      payloadJson: JSON.stringify(payload),
      updatedAt: new Date().toISOString(),
    },
  });

  return Response.json({ ok: true, date });
}
