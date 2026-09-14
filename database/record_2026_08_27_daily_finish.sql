PRAGMA foreign_keys = ON;

INSERT INTO study_sessions
  (session_date, verified_minutes, has_untracked_activity, summary, updated_at)
VALUES
  ('2026-08-27', 23, 1, 'Anki 만기 복습과 새 카드, D+1 복습, 동사의 ない형·의지형/청유형 강의, 마무리 혼합시험까지 완료. 강의와 일부 복습 시간은 미계시.', CURRENT_TIMESTAMP)
ON CONFLICT(session_date) DO UPDATE SET
  verified_minutes = MAX(study_sessions.verified_minutes, excluded.verified_minutes),
  has_untracked_activity = 1,
  summary = excluded.summary,
  updated_at = CURRENT_TIMESTAMP;

INSERT OR REPLACE INTO tests
  (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
VALUES
  ('2026-08-27-daily-mixed-12','2026-08-27','마무리 혼합 선택형 시험','self_made','N3 foundation','N3 기초 당일 종합 확인','same_day','multiple_choice',12,9,0,0,313,720,0.25,'정답률 75%. ない형 4/4, 의지형·청유 3/3, 형용사 0/1, 문맥어휘 1/1, 단문내용 1/1, 포인트이해 0/1, 과제이해 0/1. 자체 제작 시험이며 공식 모의고사와 분리. 문항별 시간은 UI 타이머 재렌더링 문제로 과소 측정되어 속도 진단에서 제외.');

INSERT OR REPLACE INTO question_attempts
  (test_id,item_no,item_type_id,level_label,response_state,response_seconds,play_count,selected_text,correct_text,trap_hypothesis,trap_confidence)
VALUES
  ('2026-08-27-daily-mixed-12',1,'verb_conjugation','N3 foundation','correct',1,NULL,NULL,'書かない',NULL,NULL),
  ('2026-08-27-daily-mixed-12',2,'verb_conjugation','N3 foundation','correct',1,NULL,NULL,'帰らない',NULL,NULL),
  ('2026-08-27-daily-mixed-12',3,'verb_conjugation','N3 foundation','correct',2,NULL,NULL,'起きない',NULL,NULL),
  ('2026-08-27-daily-mixed-12',4,'verb_conjugation','N3 foundation','correct',1,NULL,NULL,'ない',NULL,NULL),
  ('2026-08-27-daily-mixed-12',5,'verb_conjugation','N3 foundation','correct',1,NULL,NULL,'書こう',NULL,NULL),
  ('2026-08-27-daily-mixed-12',6,'verb_conjugation','N3 foundation','correct',3,NULL,NULL,'食べよう',NULL,NULL),
  ('2026-08-27-daily-mixed-12',7,'verb_conjugation','N3 foundation','correct',1,NULL,NULL,'休みましょう',NULL,NULL),
  ('2026-08-27-daily-mixed-12',8,'adjective_conjugation','N3 foundation','wrong',6,NULL,NULL,'静かではありませんでした','な형용사의 과거 부정을 い형용사 활용과 혼동했을 가능성','low'),
  ('2026-08-27-daily-mixed-12',9,'context_vocabulary','N3 foundation','correct',2,NULL,NULL,'適切',NULL,NULL),
  ('2026-08-27-daily-mixed-12',10,'short_content','N3 foundation','correct',1,NULL,NULL,'午後1時40分',NULL,NULL),
  ('2026-08-27-daily-mixed-12',11,'listening_point','N3 foundation','wrong',1,1,NULL,'資料を十部印刷する','이미 완료된 내용 작성과 이후 지시인 10부 인쇄의 순서를 혼동했을 가능성','low'),
  ('2026-08-27-daily-mixed-12',12,'listening_task','N3 foundation','wrong',3,1,NULL,'明日の一時ごろ','12시 회의와 변경 후 약속 시각인 1시를 혼동했을 가능성','low');

INSERT OR IGNORE INTO review_queue (attempt_id,review_date,interval_label)
SELECT id,'2026-08-28','D+1' FROM question_attempts
WHERE test_id='2026-08-27-daily-mixed-12' AND response_state='wrong';
INSERT OR IGNORE INTO review_queue (attempt_id,review_date,interval_label)
SELECT id,'2026-08-30','D+3' FROM question_attempts
WHERE test_id='2026-08-27-daily-mixed-12' AND response_state='wrong';
INSERT OR IGNORE INTO review_queue (attempt_id,review_date,interval_label)
SELECT id,'2026-09-03','D+7' FROM question_attempts
WHERE test_id='2026-08-27-daily-mixed-12' AND response_state='wrong';

INSERT OR REPLACE INTO mastery_snapshots
  (snapshot_date,metric_group,metric_key,low_pct,high_pct,internal_grade,sample_count,confidence,evidence)
VALUES
  ('2026-08-27','exam_domain','vocabulary',37,48,'D+',6,'low','당일 마무리 문맥어휘 1/1; 자체 제작 소표본'),
  ('2026-08-27','exam_domain','grammar',48,60,'C',34,'low','당일 마무리 7/8; 동사 활용 7/7, 형용사 활용 0/1'),
  ('2026-08-27','exam_domain','reading',46,62,'C-',9,'low','당일 단문 내용이해 1/1; 짧은 자체 지문'),
  ('2026-08-27','exam_domain','listening',27,42,'D-',11,'low','재생 1회 포인트·과제이해 0/2; 청해 행동·시각 조건 취약'),
  ('2026-08-27','item_type','verb_conjugation',85,95,'B+',15,'medium','당일 ない형·의지형·청유 표현 7/7; 기초 활용 안정'),
  ('2026-08-27','item_type','adjective_conjugation',45,60,'C-',17,'medium','누적 자체문제 9/17 추정; D+1 5/6 뒤 문맥 적용 0/1로 재오류'),
  ('2026-08-27','item_type','context_vocabulary',70,88,'B',6,'low','당일 適切 문맥 판단 1/1; 자체 제작 소표본'),
  ('2026-08-27','item_type','short_content',68,84,'B',6,'low','당일 시간 조건 계산 단문 1/1'),
  ('2026-08-27','item_type','short_claim',45,70,'C+',3,'low','오늘 추가 표본 없음; 전일 값 유지'),
  ('2026-08-27','item_type','listening_point',45,65,'C-',4,'low','D+1 1/1 뒤 당일 재생 1회 적용 0/1; 안정성 미확인'),
  ('2026-08-27','item_type','listening_task',20,40,'D',5,'medium','시간초과 미응답에 이어 당일 재생 1회 적용도 0/1; 반복 약점');

INSERT OR REPLACE INTO pass_probability_snapshots
  (snapshot_date,level,current_low_pct,current_high_pct,projected_exam_pct,daily_change_pp,confidence,reason)
VALUES
  ('2026-08-27','N3',23,39,82,0,'low','당일 자체 제작 시험은 합격률을 직접 변경하지 않음. 동사 활용 강점과 청해 반복 약점의 진단 신뢰도만 상승.'),
  ('2026-08-27','N2',6,16,48,0,'low','N3 기초 당일 자체 시험이므로 N2 합격률 직접 조정 근거에서 제외. 공식 모의고사로 보정 필요.');
