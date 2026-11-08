// Older reports use source=quiz for every browser exercise. Prefer the actual
// activity description before falling back to that broad transport category.
export function activityKind(item) {
  const source = item.source || '';
  const text = item.notes || '';
  if (source === 'anki') return 'anki';
  if (source === 'review' || /間違い[\s・]*ノート|오답\s*(?:노트|복습)|오답.*복습|mock-error-pool|machigai-review/i.test(text)) return 'review';
  if (source === 'exam' || /실전\s*모의고사|実戦\s*模擬?試|기출.*모의고사|past_exam|기출.*본시험|공식.*모의고사/i.test(text)) return 'exam';
  if (source === 'typing' || /타이핑|タイピング/.test(text)) return 'typing';
  if (/speed\s*run|스피드\s*(?:런|퀴즈)/i.test(text)) return 'speed';
  if (source === 'quiz') return 'quiz';
  return 'activity';
}
export const activityLabels = {
  anki: 'Anki 복습', review: '오답노트 복습', exam: '실전 모의고사',
  typing: '타이핑 연습', speed: 'SPEED RUN', quiz: '퀴즈', activity: '학습 세션',
};
export const activityIcons = { anki: '🎴', review: '🔁', exam: '📝', typing: '⌨️', speed: '⚡', quiz: '✏️', activity: '📚' };
