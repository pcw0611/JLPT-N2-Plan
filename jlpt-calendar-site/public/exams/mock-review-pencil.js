/* Local, per-question freehand pencil. No answer or study-record writes. */
window.addEventListener('DOMContentLoaded', () => {
  const NS='http://www.w3.org/2000/svg';
  const PREFIX='jlpt-n2-pencil-v1:';
  const surfaces=new Map();
  let enabled=false, drawing=null, swallowClick=false;
  const tools=document.createElement('div');
  tools.className='pencil-tools';
  tools.innerHTML='<button type="button" id="pencilToggle" aria-pressed="false" title="H：鉛筆 ON / OFF">✎ 鉛筆 OFF <kbd>H</kbd></button><button type="button" id="pencilUndo" aria-label="最後の線を戻す (Ctrl+Z)" title="最後の線を戻す (Ctrl+Z)">↶</button><span id="pencilSaveState" role="status" aria-live="polite"></span>';
  document.body.appendChild(tools);
  const toggle=$('pencilToggle'),notice=$('pencilSaveState');
  function load(key) {
    try {
      const value=JSON.parse(localStorage.getItem(key)||'{"strokes":[]}');
      if(!Array.isArray(value.strokes))return [];
      return value.strokes.filter(s=>Array.isArray(s.points)&&s.points.length&&s.points.every(p=>Array.isArray(p)&&p.length===2&&p.every(n=>Number.isFinite(n)&&n>=0&&n<=1)));
    } catch {return [];}
  }
  function save(surface) {
    try {
      localStorage.setItem(surface.key,JSON.stringify({version:1,strokes:surface.strokes}));
      notice.textContent='保存済み';
      notice.dataset.error='false';
    } catch {
      notice.textContent='保存できません';
      notice.dataset.error='true';
    }
  }
  function line(surface,stroke) {
    const shape=document.createElementNS(NS,stroke.points.length===1?'circle':'polyline');
    const w=surface.host.clientWidth,h=surface.host.clientHeight;
    if(stroke.points.length===1){shape.setAttribute('cx',stroke.points[0][0]*w);shape.setAttribute('cy',stroke.points[0][1]*h);shape.setAttribute('r','0.9');shape.setAttribute('fill','#151515');}
    else {shape.setAttribute('points',stroke.points.map(p=>`${p[0]*w},${p[1]*h}`).join(' '));shape.setAttribute('fill','none');shape.setAttribute('stroke','#151515');shape.setAttribute('stroke-width','1.8');shape.setAttribute('stroke-linecap','round');shape.setAttribute('stroke-linejoin','round');shape.setAttribute('vector-effect','non-scaling-stroke');}
    return shape;
  }
  function redraw(surface) {
    surface.svg.setAttribute('viewBox',`0 0 ${surface.host.clientWidth||1} ${surface.host.clientHeight||1}`);
    surface.svg.replaceChildren(...surface.strokes.map(s=>line(surface,s)));
    if(drawing?.surface===surface)surface.svg.appendChild(line(surface,drawing.stroke));
  }
  function point(surface,e) {
    const r=surface.svg.getBoundingClientRect();
    return [Math.max(0,Math.min(1,(e.clientX-r.left)/(r.width||1))),Math.max(0,Math.min(1,(e.clientY-r.top)/(r.height||1)))].map(n=>Math.round(n*100000)/100000);
  }
  function finish(cancel=false) {
    if(!drawing)return;
    const {surface,stroke,pointer}=drawing;
    drawing=null;
    if(!cancel){surface.strokes=load(surface.key);surface.strokes.push(stroke);save(surface);}
    redraw(surface);
    if(surface.svg.hasPointerCapture(pointer))surface.svg.releasePointerCapture(pointer);
  }
  function setEnabled(value) {
    finish();enabled=value;
    document.body.classList.toggle('pencil-on',value);
    toggle.setAttribute('aria-pressed',String(value));
    toggle.innerHTML=`✎ 鉛筆 ${value?'ON':'OFF'} <kbd>H</kbd>`;
    if(notice.dataset.error!=='true')notice.textContent=value?'黒鉛筆 · Ctrl+Zで戻す':'';
  }
  function undo() {
    if(drawing){finish(true);return;}
    let latest=null;
    for(const surface of surfaces.values()) {
      if(!surface.host.isConnected||!surface.host.getClientRects().length)continue;
      surface.strokes=load(surface.key);
      const last=surface.strokes.at(-1);
      if(last&&(!latest||(last.at||0)>(latest.strokes.at(-1).at||0)))latest=surface;
    }
    if(latest){latest.strokes.pop();save(latest);redraw(latest);}
  }
  toggle.onclick=()=>setEnabled(!enabled);
  $('pencilUndo').onclick=undo;
  document.addEventListener('pointerdown',()=>{if(!drawing)swallowClick=false;},true);
  document.addEventListener('click',e=>{
    if((enabled||swallowClick)&&e.target.closest?.('.pencil-host')){e.preventDefault();e.stopImmediatePropagation();swallowClick=false;}
  },true);
  window.addEventListener('keydown',e=>{
    if(e.isComposing||e.target.closest?.('input,textarea,select,[contenteditable]:not([contenteditable="false"])'))return;
    if(e.code==='KeyH'&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&!e.shiftKey){e.preventDefault();e.stopImmediatePropagation();if(!e.repeat)setEnabled(!enabled);return;}
    if(enabled&&(e.ctrlKey||e.metaKey)&&e.code==='KeyZ'&&!e.shiftKey&&!e.altKey){e.preventDefault();e.stopImmediatePropagation();if(!e.repeat)undo();return;}
    // Writing must not mark an answer or move to a new question accidentally.
    if(enabled&&!$('screenExam').classList.contains('hidden')&&[' ','Enter','1','2','3','4','5','0','ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();e.stopImmediatePropagation();}
  },true);
  window.addEventListener('blur',()=>finish());
  const resize=new ResizeObserver(entries=>{for(const entry of entries){const surface=surfaces.get(entry.target);if(surface)redraw(surface);}});
  function attach(host,qid,region) {
    if(!host)return;
    const old=surfaces.get(host);
    if(drawing?.surface===old)finish();
    if(old){old.svg.remove();resize.unobserve(host);}
    for(const [node] of surfaces)if(!node.isConnected){resize.unobserve(node);surfaces.delete(node);}
    host.classList.add('pencil-host');
    const svg=document.createElementNS(NS,'svg');
    svg.classList.add('pencil-layer');svg.setAttribute('aria-hidden','true');svg.setAttribute('preserveAspectRatio','none');
    const surface={host,svg,key:PREFIX+qid+':'+region,strokes:[]};
    surface.strokes=load(surface.key);
    host.appendChild(svg);surfaces.set(host,surface);resize.observe(host);redraw(surface);
    svg.addEventListener('pointerdown',e=>{
      if(!enabled||e.button!==0)return;
      e.preventDefault();e.stopPropagation();swallowClick=true;
      drawing={surface,pointer:e.pointerId,stroke:{points:[point(surface,e)],at:Date.now()}};
      svg.setPointerCapture(e.pointerId);redraw(surface);
    });
    svg.addEventListener('pointermove',e=>{
      if(!drawing||drawing.surface!==surface||drawing.pointer!==e.pointerId)return;
      e.preventDefault();e.stopPropagation();
      const events=e.getCoalescedEvents?.()||[];
      for(const sample of events.length?events:[e]) {
        const p=point(surface,sample),prev=drawing.stroke.points.at(-1);
        if(Math.hypot((p[0]-prev[0])*host.clientWidth,(p[1]-prev[1])*host.clientHeight)>.7)drawing.stroke.points.push(p);
      }
      redraw(surface);
    });
    svg.addEventListener('pointerup',e=>{if(drawing?.pointer===e.pointerId){e.preventDefault();e.stopPropagation();finish();}});
    svg.addEventListener('pointercancel',()=>finish(true));
    svg.addEventListener('lostpointercapture',()=>{if(drawing?.surface===surface)finish();});
  }
  const baseRender=renderQuestion;
  renderQuestion=function(){
    finish();baseRender();
    const q=state.activeQuestions[state.currentIndex];if(!q)return;
    attach($('qInstructionBox'),q.id,'instruction');
    attach($('qQuestionSentence'),q.id,'question');
    const passage=$('qPassageBox');
    if(!passage.classList.contains('hidden')) {
      const content=document.createElement('div');
      while(passage.firstChild)content.appendChild(passage.firstChild);
      passage.appendChild(content);attach(content,q.id,'passage');
    }
    [...$('choicesContainer').children].forEach((choice,i)=>attach(choice,q.id,'choice-'+(i+1)));
    if(!$('instantFeedbackBox').classList.contains('hidden'))attach($('instantExplanationContent'),q.id,'exam-explanation');
  };
  window.addEventListener('jlpt-review-detail',e=>{
    const qid=e.detail.questionId;
    const card=$('ankiQuestionList').firstElementChild;if(!card)return;
    attach(card.children[1],qid,'preview-question');
    const explanation=document.getElementById('cardExp-'+qid)?.querySelector('.overflow-x-auto');
    if(explanation){
      const content=document.createElement('div');
      while(explanation.firstChild)content.appendChild(explanation.firstChild);
      explanation.appendChild(content);attach(content,qid,'preview-explanation');
    }
  });
  const baseExplanations=renderExplanations;
  renderExplanations=function(){
    finish();baseExplanations();
    for(const card of $('explanationsList').querySelectorAll('[data-pencil-question]'))attach(card.querySelector('.explanation-box'),card.dataset.pencilQuestion,'result-explanation');
  };
  window.addEventListener('storage',e=>{
    if(!e.key?.startsWith(PREFIX))return;
    for(const surface of surfaces.values())if(surface.key===e.key&&drawing?.surface!==surface){surface.strokes=load(e.key);redraw(surface);}
  });
});
