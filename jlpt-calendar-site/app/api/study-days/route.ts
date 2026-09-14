import { asc } from 'drizzle-orm';
import { getDb } from '../../../db';
import { dailyReports } from '../../../db/schema';

export async function GET() {
  const rows = await getDb().select().from(dailyReports).orderBy(asc(dailyReports.date));
  return Response.json({
    days: rows.map((row) => JSON.parse(row.payloadJson)),
  }, {
    headers: { 'Cache-Control': 'public, max-age=30, stale-while-revalidate=120' },
  });
}
