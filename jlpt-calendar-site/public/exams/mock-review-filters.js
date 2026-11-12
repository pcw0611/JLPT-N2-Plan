/* One filter scope for browsing and starting a review. Existing storage IDs stay intact. */
const latestReviewExam = ALL_ERROR_QUESTIONS.at(-1)?.exam_src || '';
function formatReviewPassage(value) {
  const source=String(value||'').replace(/\r\n?/g,'\n');
  // Inline references stay in the text; only a note beginning on its own line is split off.
  const boundary=source.search(/(?:^|\n|<br\s*\/?>)\s*[（(]\s*注\s*[0-9０-９]+\s*[)）]/i);
  const body=(boundary<0?source:source.slice(0,boundary)).trim();
  const notes=boundary<0?'':source.slice(boundary).replace(/^(?:\s|<br\s*\/?>)+/i,'').trim();
  const bodyHtml=/<(?:p|div|table|ul|ol|section)\b/i.test(body)
    ? body
    : body.split(/\n+|(?:<br\s*\/?>\s*){2,}/i).filter(part=>part.trim()).map(part=>`<p>${part}</p>`).join('');
  const rows=notes?notes.split(/\n+|<br\s*\/?>/i).filter(part=>part.trim()):[];
  return `<div class="review-passage-body">${bodyHtml}</div>`+(rows.length
    ? `<aside class="review-passage-notes" aria-label="語句の注釈"><div class="review-notes-heading">注釈</div><div class="review-passage-notes-content">${rows.map(row=>`<div class="review-note">${row}</div>`).join('')}</div></aside>`
    : '');
}
function withoutRuby(value) {
  return String(value || '').replace(/<rt\b[^>]*>[\s\S]*?<\/rt>/gi, '').replace(/<\/?(?:ruby|rp)\b[^>]*>/gi, '');
}
function getScopedQuestions() {
  const exam = document.getElementById('scopeExam')?.value || '';
  const domain = document.getElementById('scopeDomain')?.value || '';
  const type = document.getElementById('scopeType')?.value || '';
  return ALL_ERROR_QUESTIONS.filter(q => (!exam || q.exam_src === exam) && (!domain || reviewDomain(q) === domain) && (!type || q.type_label === type));
}
function reviewDomain(q) {
  if (q.is_listening) return '청해';
  if (q.section.includes('文法')) return '문법';
  if (q.section.includes('読解')) return '독해';
  return '어휘';
}
function syncReviewStorage() {
  // Read-only refresh: never replace saved history with a stale tab snapshot.
  try {
    const ids = JSON.parse(localStorage.getItem(MASTERED_STORAGE_KEY) || 'null');
    const srs = JSON.parse(localStorage.getItem(SRS_STORAGE_KEY) || 'null');
    if (Array.isArray(ids)) state.masteredIds = new Set(ids);
    if (srs && typeof srs === 'object' && !Array.isArray(srs)) state.srsData = srs;
  } catch (_) { /* Keep current state if saved data cannot be read. */ }
}
const baseReviewFilter = getFilteredAnkiQuestions;
getFilteredAnkiQuestions = function() {
  const qs = baseReviewFilter();
  if (state.ankiFilter === 'unresolved') return qs.filter(q => !state.masteredIds.has(q.id));
  if (state.ankiFilter === 'learning') return qs.filter(q=>getQuestionSrsStatus(q).status==='learning');
  return qs;
};
const baseReviewFinish = finishExam;
finishExam = function(partial = false) {
  if (state.submitted) return;
  syncReviewStorage();
  baseReviewFinish(partial);
  let stored = false;
  try {
    const saved = JSON.parse(localStorage.getItem(SRS_STORAGE_KEY) || '{}');
    stored = state.evalQuestions.filter(q=>state.userAnswers[q.id]!==undefined).every(q=>JSON.stringify(saved[q.id])===JSON.stringify(state.srsData[q.id]));
  } catch (_) {}
  let notice = document.getElementById('reviewSaveNotice');
  if (!notice) { notice=document.createElement('p');notice.id='reviewSaveNotice';notice.setAttribute('role','status');$('resSubtitle').insertAdjacentElement('afterend',notice); }
  notice.textContent=stored ? '✓ 이 브라우저에 복습 상태를 저장했습니다. 목록으로 돌아가면 맞힌 문항은 기본 출제에서 제외됩니다.' : '⚠ 브라우저에 복습 상태를 저장하지 못했습니다. 결과 화면을 유지하고 결과를 복사해 주세요.';
};
window.addEventListener('DOMContentLoaded', () => {
  const panel = document.createElement('section');
  panel.id = 'reviewScope';
  panel.innerHTML = `<h2>어떤 오답을 복습할까요?</h2>
    <p>시험과 유형을 선택하면 아래 목록과 출제 범위가 함께 바뀝니다.</p>
    <div class="scope-grid">
      <label>시험<select id="scopeExam"><option value="">모든 시험 · ${ALL_ERROR_QUESTIONS.length}문항</option></select></label>
      <label>영역<select id="scopeDomain"><option value="">모든 영역</option><option>어휘</option><option>문법</option><option>독해</option><option>청해</option></select></label>
      <label>세부 유형<select id="scopeType"><option value="">모든 유형</option></select></label>
      <label>복습 상태<select id="scopeStatus"><option value="unresolved">아직 맞히지 못한 문항</option><option value="all">모든 문항 (맞힌 문제 포함)</option><option value="new">신규</option><option value="due">복습일 도래</option><option value="lapsed">오답·모름 재도전</option><option value="mastered">맞힌 문항</option><option value="learning">복습 대기</option></select></label>
    </div>
    <div class="scope-actions"><button id="scopeLatest">최근 시험 오답 ${ALL_ERROR_QUESTIONS.filter(q=>q.exam_src===latestReviewExam).length}문항</button><button id="scopeReset">필터 초기화</button><button id="scopeBrowse">문항 목록 보기 ↓</button><strong id="scopeSummary" role="status" aria-live="polite"></strong></div>
    <p class="scope-note">맞힌 문제는 삭제하지 않고 기본 출제에서 제외합니다. 원 시험의 선택 답·오답 날짜는 역사 기록으로 유지됩니다. 복습 상태는 이 브라우저에 저장되며 기기 간 자동 공유되지 않습니다.</p>`;
  const style = document.createElement('style');
  style.textContent = `#reviewScope{padding:24px;background:#fff;border:1px solid #cbd5ce;border-radius:16px;color:#172d25;font:15px/1.7 system-ui,sans-serif}#reviewScope h2{font-size:22px;font-weight:750;margin:0 0 8px}#reviewScope p{margin:6px 0 18px}.scope-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.scope-grid label{font-weight:650}.scope-grid select{display:block;width:100%;padding:11px;margin-top:6px;border:1px solid #aebdb4;border-radius:8px;background:#fff;color:#172d25;font:inherit}.scope-actions{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:18px}.scope-actions button{border:1px solid #b9c8bf;background:#edf4ee;color:#174932;padding:9px 13px;border-radius:8px;cursor:pointer}.scope-actions button:first-child{background:#21583e;color:#fff}.scope-note{font-size:12px;color:#53665b}#courseList,.anki-filter-pill{display:none!important}#ankiQuestionList{max-height:580px}.dark-theme #reviewScope{background:#17251e;color:#eef5ef}.dark-theme #reviewScope p{color:#c5d6ca}@media(max-width:520px){.scope-grid{grid-template-columns:1fr}#reviewScope{padding:18px}}`;
  document.head.appendChild(style);
  const lobby = $('screenLobby');
  const header = lobby.querySelector('.jlpt-header-box');
  header.insertAdjacentElement('afterend', panel);
  header.querySelector('h1').textContent = '모의고사 오답 복습';
  header.querySelector('p').textContent = `${new Set(ALL_ERROR_QUESTIONS.map(q=>q.exam_src)).size}개 시험 · ${ALL_ERROR_QUESTIONS.length}문항. 범위를 고르고, 문항을 살펴보거나 바로 복습하세요.`;
  // Old course presets are replaced with the shared scope. Their engine remains compatible.
  $('courseList').parentElement.style.display = 'none';
  const exclude = $('chkExcludeMastered');
  if (exclude) { exclude.checked = false; exclude.closest('label').style.display = 'none'; }
  state.course = 'all';
  state.ankiFilter = 'unresolved';
  syncReviewStorage();
  for (const src of [...new Set(ALL_ERROR_QUESTIONS.map(q=>q.exam_src))]) {
    const count = ALL_ERROR_QUESTIONS.filter(q=>q.exam_src===src).length;
    $('scopeExam').add(new Option(`${src} · ${count}문항`,src));
  }
  function types() {
    $('scopeType').value = '';
    const qs = getScopedQuestions();
    $('scopeType').replaceChildren(new Option('모든 유형',''));
    for (const type of [...new Set(qs.map(q=>q.type_label))]) $('scopeType').add(new Option(`${type} · ${qs.filter(q=>q.type_label===type).length}`,type));
  }
  const originalUpdate = updateAnkiDeckUI;
  updateAnkiDeckUI = function() {
    originalUpdate();
    const count = getFilteredAnkiQuestions().length;
    const total = getScopedQuestions().length;
    const correct = getScopedQuestions().filter(q=>state.masteredIds.has(q.id)).length;
    $('scopeSummary').textContent = `전체 ${total} · 맞힘 ${correct} · 남음 ${total-correct} / 출제 ${count}문항`;
    $('btnStartFilteredBatch').disabled = !count;
    $('btnStartExam').disabled = !count;
  };
  function refresh() { updateLobbyMasteredUI(); updateAnkiDeckUI(); }
  $('scopeExam').onchange = $('scopeDomain').onchange = () => { types(); refresh(); };
  $('scopeType').onchange = refresh;
  $('scopeStatus').onchange = () => { state.ankiFilter=$('scopeStatus').value; refresh(); };
  $('scopeLatest').onclick = () => { $('scopeExam').value=latestReviewExam; $('scopeDomain').value=''; $('scopeStatus').value='unresolved';state.ankiFilter='unresolved';state.ankiSearchQuery='';$('ankiSearchInput').value='';syncReviewStorage();types();refresh(); };
  $('scopeReset').onclick = () => { $('scopeExam').value='';$('scopeDomain').value='';$('scopeStatus').value='unresolved';state.ankiFilter='unresolved';state.ankiSearchQuery='';$('ankiSearchInput').value='';types();refresh(); };
  $('scopeBrowse').onclick = () => $('ankiPoolSection').scrollIntoView({behavior:'smooth'});
  function startSelected() {
    let qs=getFilteredAnkiQuestions();
    if(state.qLimit!=='all') qs=qs.slice(0,Number(state.qLimit));
    if(!qs.length) return;
    state.feedbackMode=document.querySelector('input[name="feedbackMode"]:checked').value;
    startSessionWithPool(qs);
  }
  $('btnStartExam').onclick=$('btnStartFilteredBatch').onclick=startSelected;
  $('btnStartExam').textContent='선택한 범위로 복습 시작 →';
  $('ankiPoolSection').querySelector('h2').textContent='선택한 범위의 문항 목록';
  // initResultControls rewires this button after grading, so wrap that setup too.
  const resultControls=initResultControls;
  initResultControls=function(){resultControls();const back=$('btnRestartLobby').onclick;$('btnRestartLobby').onclick=()=>{syncReviewStorage();state.ankiFilter='unresolved';$('scopeStatus').value='unresolved';back();refresh();};};
  function refreshSaved(){if(!lobby.classList.contains('hidden')){syncReviewStorage();refresh();}}
  window.addEventListener('focus',refreshSaved);
  window.addEventListener('storage',event=>{if([MASTERED_STORAGE_KEY,SRS_STORAGE_KEY].includes(event.key))refreshSaved();});
  types(); refresh();
});
