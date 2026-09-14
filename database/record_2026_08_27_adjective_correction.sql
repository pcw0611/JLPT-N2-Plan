PRAGMA foreign_keys = ON;

INSERT OR REPLACE INTO tests (
  id, test_date, title, source_class, target_level, difficulty_label,
  memory_timing, response_format, total_items, correct_items, unknown_items,
  unanswered_items, elapsed_seconds, time_limit_seconds, diagnostic_weight, notes
) VALUES (
  '2026-08-27-adjective-correction-10', '2026-08-27',
  'い・な형용사 선택형 교정 시험', 'self_made', 'N3 foundation',
  'N3 기초 형용사 활용', 'same_day', 'multiple_choice',
  10, 5, 1, 0, 267, 480, 0.15,
  '정답률 50%. 오답 2,3,6,9; 모름 4. 자체 제작 N3 기초 교정 시험이며 공식 모의고사와 분리. 전체 소요시간만 기록되어 문항별 속도 진단에서 제외.'
);

DELETE FROM question_attempts WHERE test_id='2026-08-27-adjective-correction-10';

INSERT INTO question_attempts (
  test_id, item_no, item_type_id, level_label, response_state,
  response_seconds, correct_text, trap_hypothesis, trap_confidence
) VALUES
  ('2026-08-27-adjective-correction-10',1,'adjective_conjugation','N3 foundation','correct',NULL,'高かったです',NULL,NULL),
  ('2026-08-27-adjective-correction-10',2,'adjective_conjugation','N3 foundation','wrong',NULL,'静かでした','な형용사 과거형에 い형용사 かった 활용을 적용했을 가능성','low'),
  ('2026-08-27-adjective-correction-10',3,'adjective_conjugation','N3 foundation','wrong',NULL,'高くありませんでした','い형용사 과거 부정의 くありませんでした 결합 순서가 아직 불안정할 가능성','low'),
  ('2026-08-27-adjective-correction-10',4,'adjective_conjugation','N3 foundation','unknown',NULL,'ではありません','な형용사 현재 부정형을 즉시 회상하지 못함','high'),
  ('2026-08-27-adjective-correction-10',5,'adjective_conjugation','N3 foundation','correct',NULL,'有名な',NULL,NULL),
  ('2026-08-27-adjective-correction-10',6,'adjective_conjugation','N3 foundation','wrong',NULL,'ではありませんでした','きれい를 い형용사로 오분류했거나 な형용사 과거 부정형을 혼동했을 가능성','low'),
  ('2026-08-27-adjective-correction-10',7,'adjective_conjugation','N3 foundation','correct',NULL,'よかったです',NULL,NULL),
  ('2026-08-27-adjective-correction-10',8,'adjective_conjugation','N3 foundation','correct',NULL,'よくないです',NULL,NULL),
  ('2026-08-27-adjective-correction-10',9,'adjective_conjugation','N3 foundation','wrong',NULL,'静かだった','な형용사의 과거 명사 수식에서 な를 제거하고 だった를 쓰는 규칙을 놓쳤을 가능성','low'),
  ('2026-08-27-adjective-correction-10',10,'adjective_conjugation','N3 foundation','correct',NULL,'田中さんは有名な人です。',NULL,NULL);

INSERT OR IGNORE INTO review_queue (attempt_id, review_date, interval_label)
SELECT id, '2026-08-28', 'D+1' FROM question_attempts
WHERE test_id='2026-08-27-adjective-correction-10' AND response_state!='correct';
INSERT OR IGNORE INTO review_queue (attempt_id, review_date, interval_label)
SELECT id, '2026-08-30', 'D+3' FROM question_attempts
WHERE test_id='2026-08-27-adjective-correction-10' AND response_state!='correct';
INSERT OR IGNORE INTO review_queue (attempt_id, review_date, interval_label)
SELECT id, '2026-09-03', 'D+7' FROM question_attempts
WHERE test_id='2026-08-27-adjective-correction-10' AND response_state!='correct';

INSERT INTO mastery_snapshots (
  snapshot_date, metric_group, metric_key, low_pct, high_pct,
  internal_grade, sample_count, confidence, evidence
) VALUES (
  '2026-08-27','item_type','adjective_conjugation',43,57,'C-',27,'medium',
  '당일 누적 형용사 활용 14/27. 이번 교정 시험 5/10: いい 예외와 현재 명사 수식은 정답, な형용사 과거·부정·과거 명사 수식에서 반복 오류.'
)
ON CONFLICT(snapshot_date, metric_group, metric_key) DO UPDATE SET
  low_pct=excluded.low_pct,
  high_pct=excluded.high_pct,
  internal_grade=excluded.internal_grade,
  sample_count=excluded.sample_count,
  confidence=excluded.confidence,
  evidence=excluded.evidence;
