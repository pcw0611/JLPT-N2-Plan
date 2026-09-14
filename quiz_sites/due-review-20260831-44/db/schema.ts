import { integer, real, sqliteTable, text } from 'drizzle-orm/sqlite-core';

export const studyDays = sqliteTable('study_days', {
  date: text('date').primaryKey(),
  studyMinutes: integer('study_minutes').notNull(),
  studyTimeIsMinimum: integer('study_time_is_minimum', { mode: 'boolean' }).notNull().default(false),
  testCorrect: integer('test_correct').notNull(),
  testTotal: integer('test_total').notNull(),
  testMinutes: integer('test_minutes').notNull(),
  allowedMinutes: integer('allowed_minutes').notNull(),
  wrongCount: integer('wrong_count').notNull(),
  n3CurrentLow: integer('n3_current_low').notNull(),
  n3CurrentHigh: integer('n3_current_high').notNull(),
  n3Projected: integer('n3_projected').notNull(),
  n2CurrentLow: integer('n2_current_low').notNull(),
  n2CurrentHigh: integer('n2_current_high').notNull(),
  n2Projected: integer('n2_projected').notNull(),
  sourceLabel: text('source_label').notNull(),
});

export const skillSnapshots = sqliteTable('skill_snapshots', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  date: text('date').notNull().references(() => studyDays.date),
  skill: text('skill').notNull(),
  stabilityLow: integer('stability_low').notNull(),
  stabilityHigh: integer('stability_high').notNull(),
  grade: text('grade').notNull(),
});

export const typeMetrics = sqliteTable('type_metrics', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  date: text('date').notNull().references(() => studyDays.date),
  category: text('category').notNull(),
  correct: integer('correct').notNull(),
  total: integer('total').notNull(),
  averageSeconds: real('average_seconds').notNull(),
  status: text('status').notNull(),
  includesAudio: integer('includes_audio', { mode: 'boolean' }).notNull().default(false),
});

export const reviewSchedule = sqliteTable('review_schedule', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  sourceDate: text('source_date').notNull().references(() => studyDays.date),
  reviewDate: text('review_date').notNull(),
  interval: text('interval').notNull(),
  category: text('category').notNull(),
  completed: integer('completed', { mode: 'boolean' }).notNull().default(false),
});
