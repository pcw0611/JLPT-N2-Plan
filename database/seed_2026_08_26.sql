INSERT OR REPLACE INTO study_sessions
  (session_date, verified_minutes, has_untracked_activity, summary, updated_at)
VALUES
  ('2026-08-26', 247, 1, 'Anki 만기 복습, 기초 활용 강의, 독해·청해 개요, 즉시·혼합 테스트. 추가 활동 시간 미계시.', CURRENT_TIMESTAMP);

INSERT OR IGNORE INTO item_types
  (id,domain,label_ko,label_ja,is_official_type,recommended_min_sec,recommended_max_sec,timing_note)
VALUES
  ('kanji_reading','vocabulary','한자 읽기','漢字読み',1,20,30,'훈련용 권장치; 공식 문항별 제한시간 아님'),
  ('paraphrase','vocabulary','유의표현','言い換え類義',1,25,40,'훈련용 권장치; 공식 문항별 제한시간 아님'),
  ('adjective_conjugation','grammar','형용사 활용','形容詞活用',0,20,35,'기초 자동화 훈련 기준'),
  ('verb_conjugation','grammar','동사 활용','動詞活用',0,15,30,'기초 자동화 훈련 기준'),
  ('grammar_form','grammar','문법형식 판단','文の文法1',1,30,50,'훈련용 권장치; 공식 문항별 제한시간 아님'),
  ('short_content','reading','단문 내용이해','短文内容理解',1,120,180,'약 200자 단문 기준'),
  ('short_claim','reading','단문 주장 이해','短文主張理解',1,150,240,'문장 길이와 선택지 난도에 따라 조정'),
  ('listening_point','listening','포인트이해','ポイント理解',1,5,15,'오디오 종료 후 결정시간 기준; 오디오 길이는 별도'),
  ('listening_task','listening','과제이해','課題理解',1,5,15,'오디오 종료 후 결정시간 기준; 오디오 길이는 별도');

INSERT OR REPLACE INTO tests
  (id,test_date,title,source_class,target_level,difficulty_label,memory_timing,response_format,total_items,correct_items,unknown_items,unanswered_items,elapsed_seconds,time_limit_seconds,diagnostic_weight,notes)
VALUES
  ('2026-08-26-mixed-10','2026-08-26','JLPT 혼합 미니 테스트','self_made','N3+N2','N3 기반＋N2 입문','same_day','multiple_choice',10,4,0,0,420,1080,0.30,'공식 형식 기반 자체 제작. 공식 모의고사와 분리.'),
  ('2026-08-26-review-12','2026-08-26','선택형 복습 시험','self_made','N3+N2','교정 직후 복습','immediate','multiple_choice',12,12,0,0,NULL,NULL,0.10,'문법·활용 6/6, 청해 유형 2/2, N2 어휘 4/4. 이해 확인용.');

INSERT OR REPLACE INTO question_attempts
  (test_id,item_no,item_type_id,level_label,response_state,response_seconds,selected_text,correct_text,trap_hypothesis,trap_confidence)
VALUES
  ('2026-08-26-mixed-10',1,'kanji_reading','N3','correct',16,NULL,'かくにん',NULL,NULL),
  ('2026-08-26-mixed-10',2,'paraphrase','N2 입문','wrong',33,NULL,'その場や目的に合っている方法','적절을 일반적인 긍정 평가로 넓게 해석했을 가능성','low'),
  ('2026-08-26-mixed-10',3,'adjective_conjugation','N3','wrong',63,NULL,'おいしくなかったです','명사·な형용사의 ではありません을 적용했거나 과거 부정 결합 순서를 혼동했을 가능성','low'),
  ('2026-08-26-mixed-10',4,'verb_conjugation','N3','correct',12,NULL,'書いて',NULL,NULL),
  ('2026-08-26-mixed-10',5,'grammar_form','N3','wrong',36,NULL,'行く','前に 앞의 사전형 접속을 놓치고 て형·과거형을 골랐을 가능성','low'),
  ('2026-08-26-mixed-10',6,'grammar_form','N2 입문','correct',20,NULL,'うちに',NULL,NULL),
  ('2026-08-26-mixed-10',7,'short_content','N3','correct',54,NULL,'受付は1時30分、説明会は2時30分に始まる',NULL,NULL),
  ('2026-08-26-mixed-10',8,'short_claim','N2 입문','wrong',102,NULL,'優先事項を決め、予定に余裕を持たせるべきだ','첫 문단의 일반론을 결론으로 잡고 둘째 문단의 최종 주장을 놓쳤을 가능성','low'),
  ('2026-08-26-mixed-10',9,'listening_point','N3','wrong',38,NULL,'5部','필요 총수·기존 부수·추가 부수를 구분하지 못하고 직접 들린 숫자를 골랐을 가능성','low'),
  ('2026-08-26-mixed-10',10,'listening_task','N2 입문','wrong',48,NULL,'文章だけを取引先に送ります','사진 선택이나 인쇄에 주의가 끌려 先に·すぐ를 놓쳤을 가능성','low');

INSERT OR IGNORE INTO review_queue (attempt_id,review_date,interval_label)
SELECT id,'2026-08-27','D+1' FROM question_attempts WHERE test_id='2026-08-26-mixed-10' AND response_state='wrong';
INSERT OR IGNORE INTO review_queue (attempt_id,review_date,interval_label)
SELECT id,'2026-08-29','D+3' FROM question_attempts WHERE test_id='2026-08-26-mixed-10' AND response_state='wrong';
INSERT OR IGNORE INTO review_queue (attempt_id,review_date,interval_label)
SELECT id,'2026-09-02','D+7' FROM question_attempts WHERE test_id='2026-08-26-mixed-10' AND response_state='wrong';

INSERT OR REPLACE INTO mastery_snapshots
  (snapshot_date,metric_group,metric_key,low_pct,high_pct,internal_grade,sample_count,confidence,evidence)
VALUES
  ('2026-08-26','exam_domain','vocabulary',35,45,'D',2,'low','기존 진단 35%; 혼합시험 1/2'),
  ('2026-08-26','exam_domain','grammar',45,55,'C-',4,'low','혼합시험 2/4; 동사 활용 강점, 형용사·접속 약점'),
  ('2026-08-26','exam_domain','reading',45,60,'C-',2,'low','내용이해 정답, 주장 이해 오답'),
  ('2026-08-26','exam_domain','listening',25,40,'D-',2,'low','포인트·과제이해 0/2'),
  ('2026-08-26','memory','immediate_recognition',75,90,'B+',12,'medium','교정 직후 선택형 12/12; 합격률 가중치 낮음'),
  ('2026-08-26','memory','delayed_free_recall',40,55,'D+~C-',0,'low','힌트 없이 형태 생성 시 재오류');

INSERT OR REPLACE INTO pass_probability_snapshots
  (snapshot_date,level,current_low_pct,current_high_pct,projected_exam_pct,daily_change_pp,confidence,reason)
VALUES
  ('2026-08-26','N3',23,39,82,0,'low','자체 제작 소표본은 확률을 직접 변경하지 않고 약점 진단에만 반영'),
  ('2026-08-26','N2',6,16,48,0,'low','자체 제작 N3 기반＋N2 입문 소표본; 공식 모의고사로 보정 필요');
