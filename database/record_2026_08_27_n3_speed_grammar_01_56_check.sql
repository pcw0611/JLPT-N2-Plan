PRAGMA foreign_keys = ON;

INSERT OR REPLACE INTO tests
  (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
VALUES
  ('2026-08-27-n3-speed-grammar-01-56-check','2026-08-27','N3 스피드 문법 01~56 당일 선택형 확인시험','self_made','N3','N3 스피드 문법 01~56','same_day','multiple_choice',10,6,0,0,149,420,0.20,'다락원 N3 스피드 문법 PDF 01~56에 기반한 자체 제작 당일 재인형 시험. 공식 모의고사와 분리. 오답 선택지 문구와 문항별 시간은 전달되지 않음.');

INSERT OR REPLACE INTO question_attempts
  (test_id,item_no,item_type_id,level_label,response_state,response_seconds,selected_text,correct_text,trap_hypothesis,trap_confidence)
VALUES
  ('2026-08-27-n3-speed-grammar-01-56-check',1,'grammar_form','N3','wrong',NULL,NULL,'間','계속되는 기간의 間와 기간 중 한 시점의 間に를 구분하지 못했을 가능성','low'),
  ('2026-08-27-n3-speed-grammar-01-56-check',2,'grammar_form','N3','correct',NULL,NULL,'うちに',NULL,NULL),
  ('2026-08-27-n3-speed-grammar-01-56-check',3,'grammar_form','N3','correct',NULL,NULL,'ようとした',NULL,NULL),
  ('2026-08-27-n3-speed-grammar-01-56-check',4,'grammar_form','N3','correct',NULL,NULL,'ことから',NULL,NULL),
  ('2026-08-27-n3-speed-grammar-01-56-check',5,'grammar_form','N3','wrong',NULL,NULL,'ことにした','자기 결정의 ことにする와 외부 결정·결과의 ことになる를 혼동했을 가능성','low'),
  ('2026-08-27-n3-speed-grammar-01-56-check',6,'grammar_form','N3','wrong',NULL,NULL,'ずに','동작을 하지 않은 채의 ずに와 원인·이유의 なくて를 혼동했을 가능성','low'),
  ('2026-08-27-n3-speed-grammar-01-56-check',7,'grammar_form','N3','correct',NULL,NULL,'そうだ',NULL,NULL),
  ('2026-08-27-n3-speed-grammar-01-56-check',8,'grammar_form','N3','correct',NULL,NULL,'ところ',NULL,NULL),
  ('2026-08-27-n3-speed-grammar-01-56-check',9,'grammar_form','N3','wrong',NULL,NULL,'てあります','의도적으로 준비해 둔 결과의 てある와 자연 상태·진행의 ている를 혼동했을 가능성','low'),
  ('2026-08-27-n3-speed-grammar-01-56-check',10,'grammar_form','N3','correct',NULL,NULL,'ても仕方がない',NULL,NULL);

INSERT OR IGNORE INTO review_queue (attempt_id,review_date,interval_label)
SELECT id,'2026-08-28','D+1' FROM question_attempts
WHERE test_id='2026-08-27-n3-speed-grammar-01-56-check' AND response_state='wrong';
INSERT OR IGNORE INTO review_queue (attempt_id,review_date,interval_label)
SELECT id,'2026-08-30','D+3' FROM question_attempts
WHERE test_id='2026-08-27-n3-speed-grammar-01-56-check' AND response_state='wrong';
INSERT OR IGNORE INTO review_queue (attempt_id,review_date,interval_label)
SELECT id,'2026-09-03','D+7' FROM question_attempts
WHERE test_id='2026-08-27-n3-speed-grammar-01-56-check' AND response_state='wrong';

INSERT OR REPLACE INTO mastery_snapshots
  (snapshot_date,metric_group,metric_key,low_pct,high_pct,internal_grade,sample_count,confidence,evidence)
VALUES
  ('2026-08-27','exam_domain','grammar',47,59,'C-',44,'medium','기초 동사 활용은 안정적이나 형용사와 신규 N3 문형이 불안정. 스피드 문법 01~56 당일 선택형 6/10.'),
  ('2026-08-27','item_type','grammar_form',52,68,'C+',13,'medium','누적 문법형식 판단 8/13. 신규 문형에서 間/間に, ことにする/なる, ずに, てある 오답.');

INSERT OR REPLACE INTO pass_probability_snapshots
  (snapshot_date,level,current_low_pct,current_high_pct,projected_exam_pct,daily_change_pp,confidence,reason)
VALUES
  ('2026-08-27','N3',23,39,82,0,'low','N3 신규 문형 01~56 당일 자체 시험 6/10으로 약점 진단은 갱신했으나 합격률을 직접 조정할 공식 근거는 아님.'),
  ('2026-08-27','N2',6,16,48,0,'low','N3 문형 당일 자체 시험이므로 N2 합격률 직접 조정 근거에서 제외.');

UPDATE study_sessions
SET
  has_untracked_activity = 1,
  summary = '기존 최소 추정 학습시간 685분. 추가 식사 휴식 길이는 미확인. Anki, N3 기초 활용 강의, N3 스피드 문법 1~6강(01~56)과 당일 선택형 확인시험 6/10 완료. 시험시간은 누적시간에 중복 가산하지 않음.',
  updated_at = CURRENT_TIMESTAMP
WHERE session_date='2026-08-27';
