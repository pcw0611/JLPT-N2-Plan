import taxonomy from './report-taxonomy.json';

export type Probability = { low: number; high: number; projected: number };
export type Domain = { key: string; label: string; low: number | null; high: number | null; grade: string | null };
export type Counts = { correct: number; total: number; wrong?: number; unknown?: number; unanswered?: number; excluded?: number; averageSeconds: number | null; timedItems?: number };
export type TypeMetric = Counts & { key: string; label: string; domain: string; cumulative?: Counts; timingBasis?: string; grade: string | null; evaluationSampleCount?: number; evaluationConfidence?: string | null };
export type AnkiStats = {
  scope: string; scopeLabel: string; answeredCards: number; studyMinutes: number; secondsPerCard: number;
  againCount: number; againPct: number; learningCards: number; reviewCards: number; relearningCards: number; filteredCards: number;
  forecast: { periodDays: number; totalReviews: number; dailyAverage: number; tomorrowDue: number; dailyLoad: number };
  history: { periodDays: number; studyDays: number; studyDayPct: number; totalReviews: number; calendarDailyAverage: number; studyDayAverage: number };
  cards: { total: number; new: number; newPct: number; young: number; youngPct: number; mature: number; suspended: number; buried: number };
  medianIntervalDays: number; medianEasePct: number;
  retention: Record<'today' | 'yesterday' | 'lastWeek' | 'lastMonth' | 'lastYear', { pct: number; count: number }>;
  sourceNote?: string;
};
export type AnkiDailySummary = {
  schema: 'daily_summary_v1'; scope: string; scopeLabel: string; answeredCards: number; studyMinutes: number; secondsPerCard: number;
  againCount: number; againPct: number; learningReviews: number; reviewsDone: number;
  ratings: { again: number; hard: number; good: number; easy: number };
  cardsRemaining: { new: number; learning: number; review: number };
  sourceNote?: string;
};
export type DailyReport = {
  schemaVersion?: number; date: string; syncedAt?: string; studyMinutes: number; hasUntrackedActivity: boolean;
  tests: { count: number; correct: number; total: number; wrong: number; unknown: number; unanswered?: number; elapsedSeconds: number; untimedTests?: number; unclassifiedItems?: number; excludedItems?: number };
  testDetails?: { id: string; title: string; sourceClass: string; correct: number; total: number; elapsedSeconds: number | null }[];
  probabilities: Partial<Record<'N3' | 'N2', Probability>>; domains: Domain[]; types: TypeMetric[];
  anki?: AnkiStats | AnkiDailySummary | null;
  nextReview: { date: string; count: number } | null; strengths: string[]; weaknesses: string[]; confidenceNote: string;
};

export const domainLabel = (key: string) => taxonomy.domains.find(d => d.key === key)?.label ?? key;
export function orderedDomains(rows: Domain[]) {
  return taxonomy.domains.map(d => rows.find(row => row.key === d.key) ?? { ...d, low: null, high: null, grade: null });
}
export function orderedTypes(rows: TypeMetric[]): TypeMetric[] {
  const known = new Set(taxonomy.types.map(t => t.key));
  const all: TypeMetric[] = taxonomy.types.map(t => ({ ...(rows.find(row => row.key === t.key) ?? { correct: 0, total: 0, averageSeconds: null, grade: null }), ...t }));
  const extras = rows.filter(r => !known.has(r.key)).sort((a,b) => a.key.localeCompare(b.key));
  return [...all, ...extras].sort((a,b) => {
    const order = (key: string) => { const n = taxonomy.domains.findIndex(d => d.key === key); return n < 0 ? 99 : n; };
    return order(a.domain) - order(b.domain);
  });
}
export const formatAccuracy = (row?: Pick<Counts, 'correct' | 'total'>) => !row?.total ? '未実施' : `${row.correct}/${row.total} (${Math.round(row.correct / row.total * 100)}%)`;
export const formatClock = (seconds: number | null) => seconds === null ? '未計測' : `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
export const formatStudy = (minutes: number) => `${Math.floor(minutes / 60)}時間${Math.floor(minutes % 60)}分`;
export const sourceLabel = (source: string) => ({self_made:'自作',self_made_tts:'自作・TTS',official:'公式',official_mock:'公式模試',textbook:'教材'}[source] ?? source);
