PRAGMA foreign_keys = ON;

UPDATE study_sessions
SET
  verified_minutes = MAX(verified_minutes, 685),
  has_untracked_activity = 0,
  summary = '05:47:42 KST부터의 경과시간에서 외출 2시간을 제외한 추정치. Anki, D+1·당일 복습시험, N3 기초 활용 강의와 N3 스피드 문법 1~3강 완료를 포함하며 시험 시간은 중복 가산하지 않음. 강의 시청 완료와 숙달 판정은 분리하며 D+1에서 유지 여부 확인.',
  updated_at = CURRENT_TIMESTAMP
WHERE session_date = '2026-08-27';
