/* Local, per-question freehand pencil. No answer or study-record writes. */
window.addEventListener('DOMContentLoaded', () => {
  const NS='http://www.w3.org/2000/svg';
  const PREFIX='jlpt-n2-pencil-v1:';
  const surfaces=new Map();
  let enabled=false, mode='pencil', drawing=null, swallowClick=false;
  const history=[];
  const tools=document.createElement('div');
  tools.className='pencil-tools';
  tools.innerHTML='<button type="button" id="pencilToggle" aria-pressed="false" title="H：鉛筆 ON / OFF">✎ 鉛筆 OFF <kbd>H</kbd></button><button type="button" id="eraserToggle" aria-pressed="false" title="E：消しゴム ON / OFF">⌫ 消しゴム OFF <kbd>E</kbd></button><button type="button" id="pencilUndo" aria-label="最後の操作を戻す (Ctrl+Z)" title="最後の操作を戻す (Ctrl+Z)">↶</button><span id="pencilSaveState" role="status" aria-live="polite"></span>';
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
    if(drawing?.surface===surface&&drawing.mode==='pencil')surface.svg.appendChild(line(surface,drawing.stroke));
  }
  function point(surface,e) {
    const r=surface.svg.getBoundingClientRect();
    return [Math.max(0,Math.min(1,(e.clientX-r.left)/(r.width||1))),Math.max(0,Math.min(1,(e.clientY-r.top)/(r.height||1)))].map(n=>Math.round(n*100000)/100000);
  }
  function finish(cancel=false) {
    if(!drawing)return;
    const {surface,stroke,pointer,mode:gestureMode,removed}=drawing;
    drawing=null;
    const before=load(surface.key);
    surface.strokes=before;
    if(!cancel){
      surface.strokes=gestureMode==='pencil'?[...before,stroke]:before.filter(s=>!removed.has(JSON.stringify(s)));
      if(JSON.stringify(before)!==JSON.stringify(surface.strokes)){
        history.push({key:surface.key,before,after:surface.strokes});
        if(history.length>100)history.shift();
        save(surface);
      }
    }
    redraw(surface);
    if(surface.svg.hasPointerCapture(pointer))surface.svg.releasePointerCapture(pointer);
  }
  function setTool(value) {
    finish();enabled=!!value;if(value)mode=value;
    document.body.classList.toggle('pencil-on',enabled);
    document.body.classList.toggle('eraser-on',enabled&&mode==='eraser');
    const pencil=enabled&&mode==='pencil',eraser=enabled&&mode==='eraser';
    toggle.setAttribute('aria-pressed',String(pencil));
    toggle.innerHTML=`✎ 鉛筆 ${pencil?'ON':'OFF'} <kbd>H</kbd>`;
    $('eraserToggle').setAttribute('aria-pressed',String(eraser));
    $('eraserToggle').innerHTML=`⌫ 消しゴム ${eraser?'ON':'OFF'} <kbd>E</kbd>`;
    if(notice.dataset.error!=='true')notice.textContent=enabled?(eraser?'触れた線を消す · Ctrl+Zで戻す':'黒鉛筆 · Ctrl+Zで戻す'):'';
  }
  function undo() {
    if(drawing){finish(true);return;}
    const visible=[...surfaces.values()].filter(s=>s.host.isConnected&&s.host.getClientRects().length);
    for(let i=history.length-1;i>=0;i--){
      const action=history[i],surface=visible.find(s=>s.key===action.key);
      if(!surface)continue;
      history.splice(i,1);
      if(JSON.stringify(load(surface.key))!==JSON.stringify(action.after))continue;
      surface.strokes=action.before;save(surface);redraw(surface);return;
    }
    let latest=null;
    for(const surface of surfaces.values()) {
      if(!surface.host.isConnected||!surface.host.getClientRects().length)continue;
      surface.strokes=load(surface.key);
      const last=surface.strokes.at(-1);
      if(last&&(!latest||(last.at||0)>(latest.strokes.at(-1).at||0)))latest=surface;
    }
    if(latest){latest.strokes.pop();save(latest);redraw(latest);}
  }
  toggle.onclick=()=>setTool(enabled&&mode==='pencil'?null:'pencil');
  $('eraserToggle').onclick=()=>setTool(enabled&&mode==='eraser'?null:'eraser');
  $('pencilUndo').onclick=undo;
  document.addEventListener('pointerdown',()=>{if(!drawing)swallowClick=false;},true);
  document.addEventListener('click',e=>{
    if((enabled||swallowClick)&&e.target.closest?.('.pencil-host')){e.preventDefault();e.stopImmediatePropagation();swallowClick=false;}
  },true);
  window.addEventListener('keydown',e=>{
    if(e.isComposing||e.target.closest?.('input,textarea,select,[contenteditable]:not([contenteditable="false"])'))return;
    if(['KeyH','KeyE'].includes(e.code)&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&!e.shiftKey){
      e.preventDefault();e.stopImmediatePropagation();
      const requested=e.code==='KeyH'?'pencil':'eraser';
      if(!e.repeat)setTool(enabled&&mode===requested?null:requested);return;
    }
    if(enabled&&(e.ctrlKey||e.metaKey)&&e.code==='KeyZ'&&!e.shiftKey&&!e.altKey){e.preventDefault();e.stopImmediatePropagation();if(!e.repeat)undo();return;}
    // Writing must not mark an answer or move to a new question accidentally.
    if(enabled&&!$('screenExam').classList.contains('hidden')&&[' ','Enter','1','2','3','4','5','0','ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();e.stopImmediatePropagation();}
  },true);
  window.addEventListener('blur',()=>finish());
  const resize=new ResizeObserver(entries=>{for(const entry of entries){const surface=surfaces.get(entry.target);if(surface)redraw(surface);}});
  function pointSegment(p,a,b){
    const dx=b[0]-a[0],dy=b[1]-a[1];
    const t=Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy||1)));
    return Math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy);
  }
  function segmentDistance(a,b,c,d){
    const cross=(p,q,r)=>(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0]);
    if(cross(a,b,c)*cross(a,b,d)<0&&cross(c,d,a)*cross(c,d,b)<0)return 0;
    return Math.min(pointSegment(a,c,d),pointSegment(b,c,d),pointSegment(c,a,b),pointSegment(d,a,b));
  }
  function eraseAt(surface,from,to){
    const pixels=p=>[p[0]*surface.host.clientWidth,p[1]*surface.host.clientHeight];
    const a=pixels(from),b=pixels(to);
    surface.strokes=surface.strokes.filter(stroke=>{
      const points=stroke.points.map(pixels);
      const hit=points.length===1?pointSegment(points[0],a,b)<=10:points.slice(1).some((p,i)=>segmentDistance(a,b,points[i],p)<=10);
      if(hit)drawing.removed.add(JSON.stringify(stroke));
      return !hit;
    });
  }
  function move(e){
    const surface=drawing.surface,p=point(surface,e);
    if(drawing.mode==='eraser'){eraseAt(surface,drawing.last,p);drawing.last=p;}
    else {
      const prev=drawing.stroke.points.at(-1);
      if(Math.hypot((p[0]-prev[0])*surface.host.clientWidth,(p[1]-prev[1])*surface.host.clientHeight)>.7)drawing.stroke.points.push(p);
    }
  }
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
      const p=point(surface,e);
      surface.strokes=load(surface.key);
      drawing={surface,pointer:e.pointerId,mode,last:p,removed:new Set(),stroke:{points:[p],at:Date.now()}};
      if(mode==='eraser')eraseAt(surface,p,p);
      svg.setPointerCapture(e.pointerId);redraw(surface);
    });
    svg.addEventListener('pointermove',e=>{
      if(!drawing||drawing.surface!==surface||drawing.pointer!==e.pointerId)return;
      e.preventDefault();e.stopPropagation();
      const events=e.getCoalescedEvents?.()||[];
      for(const sample of events.length?events:[e])move(sample);
      redraw(surface);
    });
    svg.addEventListener('pointerup',e=>{if(drawing?.pointer===e.pointerId){e.preventDefault();e.stopPropagation();move(e);finish();}});
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
