import { asc } from 'drizzle-orm';
import { getDb } from '../../../db';
import { dailyReports, examSubmissions } from '../../../db/schema';

export async function GET() {
  const rows = await getDb().select().from(dailyReports).orderBy(asc(dailyReports.date));
  const daysMap = new Map<string, any>();
  for (const row of rows) {
    try {
      daysMap.set(row.date, JSON.parse(row.payloadJson));
    } catch (e) {}
  }

  // Real-time merge of pending online exam submissions from Cloudflare D1
  try {
    const submissions = await getDb().select().from(examSubmissions).orderBy(asc(examSubmissions.id));
    for (const sub of submissions) {
      if (!sub || !sub.date) continue;
      if (sub.title && sub.title.includes('검증 테스트')) continue;

      let day = daysMap.get(sub.date);
      if (!day) {
        day = {
          schemaVersion: 2,
          date: sub.date,
          studyMinutes: 0,
          hasUntrackedActivity: false,
          tests: {
            count: 0,
            correct: 0,
            total: 0,
            wrong: 0,
            unknown: 0,
            elapsedSeconds: 0,
          },
          testDetails: [],
          activityHistory: [],
          domains: [],
          types: [],
          probabilities: {},
          strengths: [],
          weaknesses: [],
        };
        daysMap.set(sub.date, day);
      }

      const subIdStr = `online-sub-${sub.id}`;
      const alreadyMerged = (day.testDetails || []).some((t: any) => t.id === subIdStr || (t.id && String(t.id).includes(subIdStr)));
      if (!alreadyMerged) {
        const sec = Number(sub.elapsedSeconds || 0);
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        const timeStr = m > 0 ? `${m}분 ${s}초` : `${s}초`;
        const addMin = Math.round(sec / 60);

        if (!day.tests) {
          day.tests = { count: 0, correct: 0, total: 0, wrong: 0, unknown: 0, elapsedSeconds: 0 };
        }
        day.tests.count = (day.tests.count || 0) + 1;
        day.tests.total = (day.tests.total || 0) + Number(sub.totalQuestions || 0);
        day.tests.correct = (day.tests.correct || 0) + Number(sub.correctCount || 0);
        day.tests.wrong = (day.tests.wrong || 0) + Number(sub.wrongCount || 0);
        day.tests.elapsedSeconds = (day.tests.elapsedSeconds || 0) + sec;
        day.studyMinutes = (day.studyMinutes || 0) + addMin;

        if (!day.testDetails) day.testDetails = [];
        day.testDetails.push({
          id: subIdStr,
          title: `${sub.title}${sub.course ? ` (${sub.course})` : ''}`,
          sourceClass: '자체 제작',
          correct: Number(sub.correctCount || 0),
          total: Number(sub.totalQuestions || 0),
          elapsedSeconds: sec,
        });

        if (!day.activityHistory) day.activityHistory = [];
        day.activityHistory.push({
          id: `sub-${sub.id}`,
          source: 'quiz',
          durationSeconds: sec,
          timeStr,
          minutes: Math.round((sec / 60) * 10) / 10,
          notes: `[${sub.title}] ${timeStr} (${sub.course || '코스'}, ${sub.correctCount}/${sub.totalQuestions}, 정답률: ${sub.accuracy}%)`,
          startedAt: sub.createdAt,
        });
      }
    }
  } catch (err) {
    console.warn('study-days live merge warning:', err);
  }

  const sortedDays = Array.from(daysMap.values()).sort((a, b) => a.date.localeCompare(b.date));

  return Response.json({
    days: sortedDays,
  }, {
    headers: {
      'Cache-Control': 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0',
      'Pragma': 'no-cache',
    },
  });
}
