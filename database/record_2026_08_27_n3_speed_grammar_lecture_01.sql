PRAGMA foreign_keys = ON;

UPDATE study_sessions
SET
  has_untracked_activity = 1,
  summary = 'Elapsed chat-span estimate from 05:47:42 KST with 2 hours total away-time excluded. Includes adjective correction quiz; recorded quiz durations are not double-counted. N3 스피드 문법 1강 시청 완료(숙달 여부는 D+1에서 확인).',
  updated_at = CURRENT_TIMESTAMP
WHERE session_date = '2026-08-27';
