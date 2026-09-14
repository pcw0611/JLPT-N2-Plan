PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS study_sessions (
  id INTEGER PRIMARY KEY,
  session_date TEXT NOT NULL UNIQUE,
  verified_minutes INTEGER NOT NULL DEFAULT 0,
  has_untracked_activity INTEGER NOT NULL DEFAULT 0,
  summary TEXT,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS item_types (
  id TEXT PRIMARY KEY,
  domain TEXT NOT NULL,
  label_ko TEXT NOT NULL,
  label_ja TEXT,
  is_official_type INTEGER NOT NULL DEFAULT 1,
  recommended_min_sec INTEGER,
  recommended_max_sec INTEGER,
  timing_note TEXT
);

CREATE TABLE IF NOT EXISTS tests (
  id TEXT PRIMARY KEY,
  test_date TEXT NOT NULL,
  title TEXT NOT NULL,
  source_class TEXT NOT NULL,
  target_level TEXT,
  difficulty_label TEXT,
  memory_timing TEXT,
  response_format TEXT,
  total_items INTEGER NOT NULL,
  correct_items INTEGER NOT NULL,
  unknown_items INTEGER NOT NULL DEFAULT 0,
  unanswered_items INTEGER NOT NULL DEFAULT 0,
  elapsed_seconds INTEGER,
  time_limit_seconds INTEGER,
  diagnostic_weight REAL NOT NULL DEFAULT 0.3,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS question_attempts (
  id INTEGER PRIMARY KEY,
  test_id TEXT NOT NULL REFERENCES tests(id) ON DELETE CASCADE,
  item_no INTEGER NOT NULL,
  item_type_id TEXT NOT NULL REFERENCES item_types(id),
  level_label TEXT,
  response_state TEXT NOT NULL CHECK(response_state IN ('correct','wrong','unknown','unanswered')),
  response_seconds INTEGER,
  audio_seconds INTEGER,
  decision_seconds INTEGER,
  play_count INTEGER,
  selected_text TEXT,
  correct_text TEXT,
  trap_hypothesis TEXT,
  trap_confidence TEXT,
  UNIQUE(test_id, item_no)
);

CREATE TABLE IF NOT EXISTS review_queue (
  id INTEGER PRIMARY KEY,
  attempt_id INTEGER NOT NULL REFERENCES question_attempts(id) ON DELETE CASCADE,
  review_date TEXT NOT NULL,
  interval_label TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  result_state TEXT,
  result_seconds INTEGER,
  UNIQUE(attempt_id, review_date)
);

CREATE TABLE IF NOT EXISTS mastery_snapshots (
  id INTEGER PRIMARY KEY,
  snapshot_date TEXT NOT NULL,
  metric_group TEXT NOT NULL,
  metric_key TEXT NOT NULL,
  low_pct REAL,
  high_pct REAL,
  internal_grade TEXT,
  sample_count INTEGER NOT NULL DEFAULT 0,
  confidence TEXT NOT NULL,
  evidence TEXT,
  UNIQUE(snapshot_date, metric_group, metric_key)
);

CREATE TABLE IF NOT EXISTS pass_probability_snapshots (
  id INTEGER PRIMARY KEY,
  snapshot_date TEXT NOT NULL,
  level TEXT NOT NULL,
  current_low_pct REAL,
  current_high_pct REAL,
  projected_exam_pct REAL,
  daily_change_pp REAL,
  confidence TEXT NOT NULL,
  reason TEXT,
  UNIQUE(snapshot_date, level)
);

CREATE TABLE IF NOT EXISTS anki_daily_stats (
  snapshot_date TEXT PRIMARY KEY,
  scope_label TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  source_filename TEXT NOT NULL,
  captured_at TEXT,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_attempt_type ON question_attempts(item_type_id);
CREATE INDEX IF NOT EXISTS idx_test_date ON tests(test_date);
CREATE INDEX IF NOT EXISTS idx_review_due ON review_queue(review_date, status);

CREATE VIEW IF NOT EXISTS v_type_accuracy AS
SELECT
  qa.item_type_id,
  it.domain,
  it.label_ko,
  COUNT(*) AS attempts,
  SUM(CASE WHEN qa.response_state='correct' THEN 1 ELSE 0 END) AS correct,
  SUM(CASE WHEN qa.response_state='unknown' THEN 1 ELSE 0 END) AS unknown,
  SUM(CASE WHEN qa.response_state='wrong' THEN 1 ELSE 0 END) AS selected_wrong,
  ROUND(100.0 * SUM(CASE WHEN qa.response_state='correct' THEN 1 ELSE 0 END) / COUNT(*), 1) AS accuracy_pct,
  ROUND(AVG(qa.response_seconds), 1) AS avg_total_seconds,
  ROUND(AVG(qa.decision_seconds), 1) AS avg_decision_seconds,
  it.recommended_min_sec,
  it.recommended_max_sec,
  it.timing_note
FROM question_attempts qa
JOIN item_types it ON it.id=qa.item_type_id
GROUP BY qa.item_type_id, it.domain, it.label_ko, it.recommended_min_sec, it.recommended_max_sec, it.timing_note;
