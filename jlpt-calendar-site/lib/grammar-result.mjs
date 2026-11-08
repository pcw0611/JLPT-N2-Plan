/** Score a stopped practice session from actual responses, never its unused pool.
 * Formal exams, completed sessions and unverifiable legacy records are unchanged.
 */
export function normalizeGrammarResult(payload) {
  const d = payload?.details;
  if (payload?.examType !== 'grammar-speedrun' || d?.test_id !== 'n2-grammar-speedrun-v2' || d.termination_reason !== 'early') return payload;
  if (!Array.isArray(d.attempts) || !d.attempts.length) return payload;
  if (d.attempts.some(a=>!a || typeof a!=='object')) return payload;
  const answered = d.attempts.filter(a => ['correct','wrong','unknown'].includes(a.status));
  const notAttempted = d.attempts.filter(a => a.status === 'unanswered');
  if (answered.length + notAttempted.length !== d.attempts.length || !answered.length) return payload;
  const declared = payload.answeredQuestions ?? d.answered_items;
  if (declared != null && declared !== answered.length) return payload;
  const planned = payload.plannedQuestions ?? d.planned_items ?? payload.totalQuestions;
  if (!Number.isInteger(planned) || planned <= answered.length) return payload;
  const correct = answered.filter(a=>a.status==='correct').length;
  const wrong = answered.filter(a=>a.status==='wrong').length;
  const unknown = answered.filter(a=>a.status==='unknown').length;
  if (payload.correctCount !== correct || (payload.wrongCount != null && payload.wrongCount !== wrong) || (payload.unknownCount != null && payload.unknownCount !== unknown)) return payload;
  const unattempted = planned-answered.length;
  const accuracy = Math.round(correct/answered.length*100);
  if (payload.totalQuestions===answered.length && payload.unansweredCount===0 && d.scoring_version==='answered-v1' && payload.accuracy===accuracy && notAttempted.length===0) return payload;
  return {
    ...payload, totalQuestions:answered.length, answeredQuestions:answered.length,
    ...(typeof payload.course==='string' ? {course:payload.course.replace(/\d+\/\d+문항 응답/,`${answered.length}문항 풀이 (예정 ${planned})`)} : {}),
    plannedQuestions:planned, unattemptedCount:unattempted,
    correctCount:correct, wrongCount:wrong, unknownCount:unknown, unansweredCount:0, accuracy,
    details:{...d, scoring_version:'answered-v1', planned_items:planned, answered_items:answered.length,
      unattempted_items:unattempted, unanswered_items:0, accuracy_denominator:'answered_items',
      attempts:answered,
      unattempted_questions:d.unattempted_questions ?? notAttempted.map(a=>({...a,status:'unattempted'})),
      ...(payload.totalQuestions!==answered.length ? {score_correction:d.score_correction ?? {
        reason:'exclude-unattempted-from-score', previous_total:payload.totalQuestions,
        previous_unanswered:payload.unansweredCount ?? d.unanswered_items ?? 0,
      }} : {}),
    },
  };
}

/** Pure read-time protection for rows written by a stale client. */
export function normalizeGrammarRow(row) {
  let payload;
  try { payload=JSON.parse(row.payloadJson); } catch (_) { return row; }
  const normalized=normalizeGrammarResult(payload);
  if (normalized===payload && !(payload?.details?.scoring_version==='answered-v1' && payload?.details?.termination_reason==='early' && row.totalQuestions!==payload.totalQuestions)) return row;
  return {...row,totalQuestions:normalized.totalQuestions,correctCount:normalized.correctCount,
    course:normalized.course ?? row.course,wrongCount:normalized.wrongCount,accuracy:normalized.accuracy,payloadJson:JSON.stringify(normalized)};
}
