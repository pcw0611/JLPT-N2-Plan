/* Presentation only: keep question IDs, grading and browser storage unchanged. */
window.addEventListener('DOMContentLoaded', () => {
  const lobby = $('screenLobby');
  const baseRender = renderAnkiQuestionList;
  const baseUpdate = updateAnkiDeckUI;
  let selectedId = null;
  let batchIds = new Set();
  let drag = null;
  let suppressClick = false;
  const typeNames={'漢字読み':'한자읽기','表記':'한자표기','語形成':'단어형성','文脈規定':'문맥규정','言い換え類義':'유의표현','用法':'용법','文の文法1':'문법형식','文の文法2':'문장배열','文章の文法':'글의 문법','短文読解':'단문','中文読解':'중문','情報検索':'정보검색','統合理解（読解）':'통합이해','主張理解':'주장이해','課題理解':'과제이해','ポイント理解':'포인트이해','概要理解':'개요이해','即時応答':'즉시응답','統合理解（聴解）':'통합이해'};
  const labels = {new:'신규',due:'복습일 도래',lapsed:'재도전',learning:'복습 대기',mastered:'맞힘'};
  for (const child of [...lobby.children]) child.style.display = 'none';
  lobby.classList.add('garden-lobby');
  const garden = document.createElement('div');
  garden.id = 'reviewGarden';
  garden.innerHTML = `
    <header class="garden-heading"><div><span class="garden-eyebrow">JLPT N2 · REVIEW GARDEN</span><h1>오답을 하나씩, 초록으로.</h1><p>작은 칸 하나가 오답 한 문항입니다.</p></div><span class="garden-total">3개 시험 · ${ALL_ERROR_QUESTIONS.length}문항</span></header>
    <section class="garden-hero"><div><span class="garden-eyebrow">오늘의 한 걸음</span><h2 id="gardenHeadline"></h2><p id="gardenSessionInfo"></p></div><div id="gardenStartSlot"></div></section>
    <div class="garden-toolbar"><div class="garden-tabs" aria-label="복습 상태 필터"><button data-garden-filter="unresolved">미해결 <span></span></button><button data-garden-filter="due">복습일 도래 <span></span></button><button data-garden-filter="all">전체 <span></span></button><button data-garden-filter="mastered">맞힘 <span></span></button></div><button id="gardenLatest" class="garden-quiet">최근 시험만 보기</button></div>
    <details class="garden-settings"><summary>범위·분량 설정 <span id="gardenSettingsSummary"></span></summary><div id="gardenScopeSlot"></div><div class="garden-options"><label>한 번에 풀 문항<select id="gardenLimit"><option value="10">10문항</option><option value="20">20문항</option><option value="30">30문항</option><option value="all">전체</option></select></label><label>해설 표시<select id="gardenFeedback"><option value="instant">한 문항씩 즉시 확인</option><option value="batch">모두 푼 뒤 확인</option></select></label></div><div class="garden-search-slot" id="gardenSearchSlot"></div><button class="garden-quiet" id="gardenResetFilters">필터 초기화</button></details>
    <div class="garden-workspace"><section class="garden-map"><div class="garden-map-heading"><h2>나의 오답 잔디밭</h2><span id="gardenProgress"></span></div><div class="garden-progress"><div id="gardenProgressFill"></div></div><p class="garden-hint">드래그로 여러 칸 선택 → Space로 복습 시작. 다시 누르거나 빈 곳을 누르면 해제됩니다.</p><div id="gardenCells"></div><div class="garden-legend">${Object.entries(labels).map(([key,label])=>`<span><i class="garden-swatch garden-${key}"></i>${label}</span>`).join('')}</div><p class="garden-footnote">초록은 이 브라우저에서 맞힌 기록입니다. D+7 졸업 판정과는 별개입니다.</p></section><aside class="garden-detail"><div class="garden-detail-top"><span>선택한 문항</span><button id="gardenCloseDetail" class="garden-quiet" aria-label="문항 상세 닫기">닫기 ×</button></div><div id="gardenDetailSlot"></div><p id="gardenEmptyDetail">궁금한 칸을 선택해 보세요.<br>문제와 복습 기록이 여기에 표시됩니다.</p></aside></div>
    <footer class="garden-footer"><span>복습 상태는 이 브라우저에 저장됩니다. 기기 간 자동 공유되지 않습니다.</span><details><summary>기록 관리</summary><div id="gardenResetSlot"></div></details></footer>`;
  lobby.appendChild(garden);
  $('gardenStartSlot').appendChild($('btnStartExam'));
  $('btnStartExam').className = 'garden-start';
  $('gardenScopeSlot').appendChild($('reviewScope').querySelector('.scope-grid'));
  $('gardenSearchSlot').appendChild($('ankiSearchInput'));
  $('ankiSearchInput').placeholder = '문항 검색 · 단어, Q번호, 시험명';
  $('ankiSearchInput').setAttribute('aria-label','오답 문항 검색');
  $('gardenDetailSlot').appendChild($('ankiQuestionList'));
  $('gardenResetSlot').appendChild($('btnResetMastered'));
  $('btnResetMastered').textContent = '이 브라우저의 맞힘 기록 초기화';
  const startFiltered = $('btnStartExam').onclick;
  $('btnStartExam').onclick = () => {
    if (!batchIds.size) { startFiltered(); return; }
    const pool=getScopedQuestions().filter(q=>batchIds.has(q.id));
    if(!pool.length) return;
    state.feedbackMode=$('gardenFeedback').value;
    batchIds.clear(); paintSelection();
    startSessionWithPool(pool);
  };
  // Consume the whole start keystroke so it cannot become a first-question answer.
  let startSpaceHeld=false;
  window.addEventListener('keydown',e=>{
    if(e.code!=='Space' && e.key!==' ')return;
    if(startSpaceHeld){e.preventDefault();e.stopImmediatePropagation();return;}
    if(e.repeat || e.isComposing || e.ctrlKey || e.metaKey || e.altKey || e.shiftKey || lobby.classList.contains('hidden') || !batchIds.size || drag)return;
    if(e.target.closest?.('input,textarea,select,[contenteditable]:not([contenteditable="false"]),summary,a,button:not(.garden-cell):not(#btnStartExam)'))return;
    e.preventDefault();e.stopImmediatePropagation();startSpaceHeld=true;
    $('btnStartExam').click();
  },true);
  window.addEventListener('keyup',e=>{
    if(!startSpaceHeld || (e.code!=='Space' && e.key!==' '))return;
    e.preventDefault();e.stopImmediatePropagation();startSpaceHeld=false;
  },true);
  window.addEventListener('blur',()=>{startSpaceHeld=false;});
  function paintSelection() {
    for(const cell of garden.querySelectorAll('[data-question-id]')) {
      const selected=batchIds.has(cell.dataset.questionId);
      cell.classList.toggle('garden-selected',selected);
      cell.setAttribute('aria-pressed',String(selected));
    }
    const count=getFilteredAnkiQuestions().length;
    const limit=state.qLimit==='all'?count:Math.min(count,Number(state.qLimit));
    $('btnStartExam').disabled=!batchIds.size && !count;
    $('btnStartExam').textContent=batchIds.size?'선택한 문항 복습 시작 →':count?`복습 시작 · ${limit}문항 →`:'출제할 문항 없음';
    $('gardenSessionInfo').textContent=batchIds.size?'선택한 칸의 문항을 이어서 학습합니다.':count?`이번에 ${limit}문항 · ${state.feedbackMode==='instant'?'한 문항씩 해설 확인':'끝까지 푼 뒤 채점'}`:'다른 상태나 시험을 선택해 보세요.';
  }
  // Rectangle selection is transient UI state, never a change to learning history.
  const board=$('gardenCells');
  const marquee=document.createElement('div');
  marquee.className='garden-marquee'; marquee.hidden=true;
  document.body.appendChild(marquee);
  document.addEventListener('pointerdown',()=>{suppressClick=false;},true);
  garden.querySelector('.garden-map').addEventListener('pointerdown',e=>{
    if(e.button!==0)return;
    suppressClick=false;
    drag={id:e.pointerId,x:e.clientX,y:e.clientY,active:false,before:new Set(batchIds),add:e.shiftKey||e.ctrlKey||e.metaKey};
    if(e.pointerType!=='touch')e.preventDefault();
  });
  window.addEventListener('pointermove',e=>{
    if(!drag || drag.id!==e.pointerId)return;
    if(!drag.active && Math.hypot(e.clientX-drag.x,e.clientY-drag.y)<6)return;
    drag.active=true;
    const rect={left:Math.min(drag.x,e.clientX),right:Math.max(drag.x,e.clientX),top:Math.min(drag.y,e.clientY),bottom:Math.max(drag.y,e.clientY)};
    marquee.hidden=false;
    Object.assign(marquee.style,{left:rect.left+'px',top:rect.top+'px',width:rect.right-rect.left+'px',height:rect.bottom-rect.top+'px'});
    batchIds=drag.add?new Set(drag.before):new Set();
    for(const cell of board.querySelectorAll('[data-question-id]')) {
      const b=cell.getBoundingClientRect();
      if(b.right>rect.left&&b.left<rect.right&&b.bottom>rect.top&&b.top<rect.bottom)batchIds.add(cell.dataset.questionId);
    }
    paintSelection();
  });
  window.addEventListener('pointerup',e=>{
    if(!drag || drag.id!==e.pointerId)return;
    suppressClick=drag.active;drag=null;marquee.hidden=true;
  });
  window.addEventListener('pointercancel',()=>{if(drag){batchIds=drag.before;drag=null;marquee.hidden=true;paintSelection();}});
  document.addEventListener('click',e=>{
    if(lobby.classList.contains('hidden'))return;
    if(suppressClick){suppressClick=false;e.stopPropagation();e.preventDefault();return;}
    // Settings, links, detail actions and the existing start button keep their own behavior.
    if(!e.target.closest('button,input,select,summary,a,.garden-detail,.garden-settings')) {
      batchIds.clear();selectedId=null;detail(null);paintSelection();
    }
  },true);
  // Retain the existing engine's controls and event handlers under the new shell.
  $('gardenLimit').value = state.qLimit;
  $('gardenLimit').onchange = () => {
    document.querySelector(`.q-limit-btn[data-limit="${$('gardenLimit').value}"]`).click();
    updateAnkiDeckUI();
  };
  $('gardenFeedback').value = state.feedbackMode;
  $('gardenFeedback').onchange = () => {
    const radio=document.querySelector(`input[name="feedbackMode"][value="${$('gardenFeedback').value}"]`);
    radio.checked=true; radio.dispatchEvent(new Event('change'));
    updateAnkiDeckUI();
  };
  $('gardenLatest').onclick = () => { $('scopeLatest').click(); };
  $('gardenResetFilters').onclick = () => { $('scopeReset').click(); };
  for (const button of garden.querySelectorAll('[data-garden-filter]')) {
    button.onclick=()=>{ $('scopeStatus').value=button.dataset.gardenFilter; $('scopeStatus').dispatchEvent(new Event('change')); };
  }
  function detail(q) {
    $('gardenEmptyDetail').hidden=!!q;
    $('gardenCloseDetail').hidden=!q;
    if(q) {
      baseRender([q]);
      // A previous correct answer is useful history; it is not proof of D+7 mastery.
      const badge=$('ankiQuestionList').querySelector('.rounded-full');
      if(badge) badge.textContent=labels[getQuestionSrsStatus(q).status];
      window.dispatchEvent(new CustomEvent('jlpt-review-detail',{detail:{questionId:q.id}}));
    } else $('ankiQuestionList').replaceChildren();
  }
  $('gardenCloseDetail').onclick=()=>{
    const previous=selectedId; selectedId=null; detail(null);
    const cell=document.getElementById('garden-cell-'+previous);
    if(cell)cell.focus({preventScroll:true});
  };
  renderAnkiQuestionList = function(filtered) {
    const visible=new Set(filtered.map(q=>q.id));
    const scoped=getScopedQuestions();
    batchIds=new Set([...batchIds].filter(id=>scoped.some(q=>q.id===id)));
    const groups=['어휘','문법','독해','청해'].filter(domain=>scoped.some(q=>reviewDomain(q)===domain));
    const exams=[...new Set(scoped.map(q=>q.exam_src))];
    const examNames={'公式問題集 第2集':'공식 2집','2023年12月 本試験':'2023.12','2023年7月 本試験資料':'2023.07'};
    board.style.setProperty('--garden-exams',exams.length||1);
    $('gardenCells').innerHTML=groups.map(domain=>{
      const qs=scoped.filter(q=>reviewDomain(q)===domain);
      const types=[...new Set(qs.map(q=>q.type_label))];
      return `<section class="garden-group"><h3 class="garden-group-label"><span>${domain}</span><span>${qs.length}문항</span></h3><div class="garden-exam-head"><span>유형</span>${exams.map(src=>`<span title="${escapeHtml(src)}">${escapeHtml(examNames[src]||src)}</span>`).join('')}</div>${types.map(type=>`<div class="garden-type-row"><span class="garden-type-label" title="${escapeHtml(type)}">${escapeHtml(typeNames[type]||type)}</span>${exams.map(src=>`<div class="garden-exam-column" aria-label="${escapeHtml(src)} · ${escapeHtml(typeNames[type]||type)}"><div class="garden-grid">${qs.filter(q=>q.type_label===type&&q.exam_src===src).map(q=>{
        const srs=getQuestionSrsStatus(q);
        const due=!!state.srsData[q.id]?.nextReviewDate && state.srsData[q.id].nextReviewDate<=getTodayStr();
        const text=`${q.exam_src} · ${q.q_num} · ${reviewDomain(q)} · ${typeNames[type]||type} · ${labels[srs.status]}${due?' · 복습일 도래':''}`;
        return `<button type="button" id="garden-cell-${q.id}" class="garden-cell garden-${srs.status}${visible.has(q.id)?'':' garden-dim'}${due?' garden-is-due':''}" data-question-id="${q.id}" title="${escapeHtml(text)}" aria-label="${escapeHtml(text)}" aria-pressed="${batchIds.has(q.id)}"><span>${escapeHtml(q.q_num.replace('Q',''))}</span></button>`;
      }).join('')}</div></div>`).join('')}</div>`).join('')}</section>`;
    }).join('') || '<p class="garden-empty">이 범위에는 문항이 없습니다. 필터를 초기화해 주세요.</p>';
    if(!filtered.length) $('gardenCells').insertAdjacentHTML('afterbegin','<p class="garden-empty" role="status">현재 조건에 맞는 출제 문항이 없습니다. 필터나 검색어를 바꿔 주세요.</p>');
    for(const cell of garden.querySelectorAll('[data-question-id]')) cell.onclick=()=>{
      const id=cell.dataset.questionId;
      if(batchIds.has(id)){batchIds.delete(id);if(selectedId===id)selectedId=null;}
      else {batchIds.add(id);selectedId=id;}
      paintSelection();
      detail(ALL_ERROR_QUESTIONS.find(q=>q.id===selectedId));
    };
    // Each cell remains available for inspection even when dimmed by a filter.
    detail(scoped.find(q=>q.id===selectedId));
    paintSelection();
  };
  updateAnkiDeckUI = function() {
    baseUpdate();
    const scoped=getScopedQuestions();
    const count=getFilteredAnkiQuestions().length;
    const correct=scoped.filter(q=>state.masteredIds.has(q.id)).length;
    const due=scoped.filter(q=>state.srsData[q.id]?.nextReviewDate && state.srsData[q.id].nextReviewDate<=getTodayStr()).length;
    const limit=state.qLimit==='all'?count:Math.min(count,Number(state.qLimit));
    $('gardenHeadline').textContent=count ? `${count}문항이 기다리고 있어요` : '지금 선택한 범위는 비었어요';
    $('gardenSessionInfo').textContent=count ? `이번에 ${limit}문항 · ${state.feedbackMode==='instant'?'한 문항씩 해설 확인':'끝까지 푼 뒤 채점'}` : '다른 상태나 시험을 선택해 보세요.';
    $('btnStartExam').textContent=count?`복습 시작 · ${limit}문항 →`:'출제할 문항 없음';
    $('gardenProgress').textContent=`맞힘 ${correct} / ${scoped.length}`;
    $('gardenProgressFill').style.width=`${scoped.length?correct/scoped.length*100:0}%`;
    $('gardenSettingsSummary').textContent=`${$('scopeExam').value?'선택 시험':'모든 시험'} · ${$('scopeDomain').value||'모든 영역'} · ${state.qLimit==='all'?'전체':state.qLimit+'문항'}`;
    const counts={unresolved:scoped.length-correct,due,all:scoped.length,mastered:scoped.filter(q=>getQuestionSrsStatus(q).status==='mastered').length};
    for(const b of garden.querySelectorAll('[data-garden-filter]')) {
      b.querySelector('span').textContent=counts[b.dataset.gardenFilter];
      b.setAttribute('aria-pressed',String(state.ankiFilter===b.dataset.gardenFilter));
    }
    $('gardenLatest').textContent=$('scopeExam').value==='2023年7月 本試験資料'?'최근 시험 선택됨':'최근 시험만 보기';
    paintSelection();
  };
  updateAnkiDeckUI();
});
