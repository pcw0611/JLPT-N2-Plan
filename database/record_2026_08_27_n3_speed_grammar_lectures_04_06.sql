PRAGMA foreign_keys = ON;

UPDATE study_sessions
SET
  has_untracked_activity = 1,
  summary = '05:47:42 KST부터의 경과시간에서 기존 외출 2시간을 제외한 최소 추정치. 추가 식사 휴식은 길이가 확인되지 않아 아직 차감·갱신하지 않음. Anki, D+1·당일 복습시험, N3 기초 활용 강의와 N3 스피드 문법 1~6강(문형 01~56) 시청 완료. 강의 완료와 숙달 판정은 분리하며 선택형 확인시험과 D+1로 검증.',
  updated_at = CURRENT_TIMESTAMP
WHERE session_date = '2026-08-27';
