import {fresh,day,makeRun,grade,applyResult,statusOf,validateBackup,prioritizeIds,intersectingIds} from './composition-core.mjs';

const app=document.querySelector('#app');
const preview=new URLSearchParams(location.search).get('preview')==='1';
const KEY='jlpt-n2-composition-100-v1'+(preview?'-preview':'');
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const names={new:'未学習',correct:'正解',wrong:'不正解',unknown:'分からない',unanswered:'未解答',due:'復習日'};
let state=fresh(),data,filter='all',selected=new Set(),size=10,paused=true,lastTick=0,view='lobby',result=null,confirmSubmit=false,storageError='',syncText='';
let drag=null,suppressClick=false,spaceHeld=false;
let clockTimer;
try{const raw=localStorage.getItem(KEY);if(raw)state=validateBackup(JSON.parse(raw));}
catch{storageError='保存データを読み込めませんでした。元のデータは上書きしません。ページを再読み込みしてください。';}

function save(){
  if(storageError)return false;
  try{localStorage.setItem(KEY,JSON.stringify(state));return true;}
  catch{storageError='保存できません。空き容量とブラウザーの設定を確認してください。';return false;}
}
function clock(s){s=Math.max(0,Math.floor(s));return `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`;}
function header(){return `${preview?'<div id="preview">動作確認モード・学習記録には送信されません</div>':''}<div class="row between"><a href="/">← 学習カレンダー</a><span class="eyebrow">N2 / 文法 / 自主制作問題</span></div>`;}
function note(){return storageError?`<p class="notice error" role="alert">${esc(storageError)}</p>`:'';}
function pool(){return data.questions.filter(q=>filter==='all'||statusOf(state.items[q.id])===filter||(filter==='mistakes'&&['wrong','unknown'].includes(state.items[q.id]?.last.status))).map(q=>q.id);}
function start(ids){
  if(!ids.length||storageError)return;
  if(state.active){syncText='中断した学習があります。「中断した学習を再開する」から続けてください。';lobby();return;}
  state.active=makeRun(ids);selected.clear();confirmSubmit=false;save();paused=false;lastTick=performance.now();quiz();window.scrollTo({top:0});
}
function startPriority(){start(prioritizeIds(pool(),state.items,size));}
function startSelected(){start([...selected]);}
function nextPool(r){const done=new Set(r.details.attempts.filter(a=>a.status!=='unanswered').map(a=>a.item_no));return prioritizeIds(data.questions.map(q=>q.id).filter(id=>!done.has(id)),state.items,size);}
function lobby(){
  view='lobby';paused=true;
  const counts={};data.questions.forEach(q=>{const s=statusOf(state.items[q.id]);counts[s]=(counts[s]||0)+1;});
  const learned=Object.keys(state.items).length,ids=pool();
  app.innerHTML=header()+`<div id="reviewGarden"><div class="garden-heading"><div><span class="garden-eyebrow">SENTENCE GARDEN</span><h1>N2 文の組み立て 100</h1><p>つながる二つを見つけて、文全体を組み立てる。</p></div><span>${learned} / 100 学習済み</span></div>${note()}
  <section class="card hero"><div class="row between"><div><h2>${filter==='due'?'今日の復習':'文の組み立てを、得点源に。'}</h2><p class="muted">四つの選択肢を並べ、★に入るものを選んでください。</p></div><div class="row"><label>問題数 <select id="size">${[1,10,20,100].map(n=>`<option value="${n}" ${size===n?'selected':''}>${n===100?'すべて':n+'問'}</option>`).join('')}</select></label><button class="primary" id="start" ${!ids.length||storageError?'disabled':''}>優先順で ${Math.min(size,ids.length)}問を開始</button></div></div>
  <p class="muted">自動選択：復習日（古い順）→ 不正解・分からない → 未学習 → 正解。範囲内から問題数に合わせて選びます。</p>
  <p class="muted">終了後にまとめて採点・韓国語の解説を表示します。出題順と選択肢は毎回変わります。</p>${state.active?'<button id="resume" class="primary">中断した学習を再開する</button>':''}</section>
  <div class="row filters">${[['all','すべて',100],['new','未学習',counts.new||0],['due','復習日',counts.due||0],['mistakes','不正解・不明',Object.values(state.items).filter(i=>['wrong','unknown'].includes(i.last.status)).length]].map(([f,n,c])=>`<button data-filter="${f}" aria-pressed="${filter===f}">${n} ${c}</button>`).join('')}</div>
  <section class="card"><div class="row between"><h2>学習マップ</h2><span class="muted">クリック・ドラッグで複数選択</span></div><div class="garden-progress"><div style="width:${learned}%"></div></div>
  <div class="row"><button id="selectedStart" class="primary" ${!selected.size||storageError?'disabled':''}>選択した ${selected.size}問を開始</button><button id="clearSelection" ${!selected.size?'disabled':''}>選択を解除</button><span id="selectionCount" class="muted" role="status">${selected.size}問選択中</span></div>
  <div class="tiles" id="selectionBoard">${data.questions.map(q=>{const s=statusOf(state.items[q.id]),eligible=ids.includes(q.id);return `<button data-item="${q.id}" class="state-${s} ${selected.has(q.id)?'selected':''} ${!eligible?'faded':''}" ${!eligible?'disabled':''} title="${q.id} · ${names[s]}" aria-label="問題 ${q.id} ${names[s]}" aria-pressed="${selected.has(q.id)}">${q.id}</button>`;}).join('')}</div>
  <div class="row muted">${['new','correct','wrong','unknown','due'].map(s=>`<span><i class="swatch state-${s}"></i>${names[s]}</span>`).join('')}</div>
  <p class="muted">選択した問題は専用ボタン、または Space でまとめて開始。上の「優先順で開始」は選択に関係なく自動で選びます。Shift / Ctrl / ⌘ を押しながらドラッグすると追加できます。</p>
  <p class="muted">不正解・分からないは翌日・3日後・7日後に復習。正解しても将来の復習日は残ります。同じ問題の正解は定着の証明とは区別します。</p></section>
  <div class="row between"><span class="muted">進み具合・中断位置は自動保存。終了・採点すると学習時間も記録します。</span>${state.runs.length?'<button id="last">前回の結果を見る</button>':''}</div><p id="sync" class="sr-status" role="status">${esc(syncText)}</p></div>`;
  bindLobby();
}
function bindLobby(){
  app.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{filter=b.dataset.filter;selected.clear();lobby();});
  app.querySelectorAll('[data-item]').forEach(b=>b.onclick=e=>{if(suppressClick){suppressClick=false;return;}const id=+b.dataset.item;selected.has(id)?selected.delete(id):selected.add(id);paintSelection();});
  document.querySelector('#size').onchange=e=>{size=+e.target.value;lobby();};
  document.querySelector('#start').onclick=startPriority;
  document.querySelector('#selectedStart').onclick=startSelected;
  document.querySelector('#clearSelection').onclick=()=>{selected.clear();paintSelection();};
  document.querySelector('#selectionBoard').onpointerdown=e=>{
    if(e.button!==0||e.pointerType==='touch')return;
    suppressClick=false;drag={pointerId:e.pointerId,x:e.clientX,y:e.clientY,before:new Set(selected),add:e.ctrlKey||e.metaKey||e.shiftKey,active:false};e.preventDefault();
  };
  document.querySelector('#resume')?.addEventListener('click',()=>{paused=false;lastTick=performance.now();quiz();});
  document.querySelector('#last')?.addEventListener('click',()=>showResult(state.runs.at(-1)));
}
function paintSelection(){
  for(const b of app.querySelectorAll('[data-item]')){b.classList.toggle('selected',selected.has(+b.dataset.item));b.setAttribute('aria-pressed',String(selected.has(+b.dataset.item)));}
  const count=document.querySelector('#selectionCount'),startButton=document.querySelector('#selectedStart'),clear=document.querySelector('#clearSelection');
  if(count)count.textContent=`${selected.size}問選択中`;
  if(startButton){startButton.textContent=`選択した ${selected.size}問を開始`;startButton.disabled=!selected.size||!!storageError;}
  if(clear)clear.disabled=!selected.size;
}
const marquee=document.createElement('div');marquee.className='garden-marquee';marquee.hidden=true;document.body.appendChild(marquee);
window.addEventListener('pointermove',e=>{
  if(!drag||drag.pointerId!==e.pointerId)return;
  if(!drag.active&&Math.hypot(e.clientX-drag.x,e.clientY-drag.y)<6)return;
  drag.active=true;
  const rect={left:Math.min(drag.x,e.clientX),right:Math.max(drag.x,e.clientX),top:Math.min(drag.y,e.clientY),bottom:Math.max(drag.y,e.clientY)};
  const cells=[...app.querySelectorAll('[data-item]:not(:disabled)')].map(b=>({id:+b.dataset.item,...Object.fromEntries(['left','right','top','bottom'].map(k=>[k,b.getBoundingClientRect()[k]]))}));
  selected=new Set([...(drag.add?drag.before:[]),...intersectingIds(cells,rect)]);
  marquee.hidden=false;Object.assign(marquee.style,{left:rect.left+'px',top:rect.top+'px',width:rect.right-rect.left+'px',height:rect.bottom-rect.top+'px'});paintSelection();
});
window.addEventListener('pointerup',e=>{if(drag?.pointerId===e.pointerId){suppressClick=drag.active;drag=null;marquee.hidden=true;}});
window.addEventListener('pointercancel',()=>{if(drag){selected=drag.before;drag=null;marquee.hidden=true;paintSelection();}});
function tick(){
  if(view!=='quiz'||paused||!state.active)return;
  const now=performance.now(),delta=Math.max(0,(now-lastTick)/1000);lastTick=now;
  const r=state.active,id=r.order[r.index];r.elapsed+=delta;r.times[id]=(r.times[id]||0)+delta;
}
function choose(id,toggle=true){
  if(view!=='quiz'||paused||!state.active)return;
  tick();const r=state.active,qid=r.order[r.index];
  if(toggle&&r.answers[qid]===id)delete r.answers[qid];else r.answers[qid]=id;
  confirmSubmit=false;save();quiz();
}
function move(index){
  const r=state.active;if(!r||index<0||index>=r.order.length)return;
  tick();r.index=index;confirmSubmit=false;save();quiz();
}
function requestSubmit(){
  const r=state.active;if(!r)return;
  if(r.order.some(id=>r.answers[id]===undefined)){tick();confirmSubmit=true;quiz();}else finish();
}
function advance(){const r=state.active;if(!r||paused)return;if(r.index<r.order.length-1)move(r.index+1);else requestSubmit();}
function quiz(){
  view='quiz';const r=state.active,q=data.questions.find(q=>q.id===r.order[r.index]);
  app.innerHTML=header()+note()+`<div class="row between card"><strong>${r.index+1} / ${r.order.length} <span class="muted">問題 ${q.id}</span></strong><span id="clock" class="clock">${clock(r.elapsed)}</span><div class="row"><button id="pause">${paused?'再開する':'一時停止'}</button><button id="home">保存して戻る</button></div></div>
  ${paused?'<div class="card"><h2>一時停止中</h2><p>再開するまで時間は計測しません。</p></div>':`<section class="card paper"><p class="muted">★に入る最もよいものを、1・2・3・4から一つ選んでください。</p><p>${esc(q.before)}${[1,2,3,4].map(n=>`<span class="blank">${n===q.star?'★':'　'}</span>`).join('')}${esc(q.after)}</p><div class="answers">${r.choices[q.id].map((id,i)=>`<button data-answer="${id}" aria-pressed="${r.answers[q.id]===id}">${i+1}　${esc(q.parts[id])}</button>`).join('')}<button data-answer="-1" aria-pressed="${r.answers[q.id]===-1}">分からない</button></div></section>`}
  <p class="muted shortcut-hint">1〜4：選択 ／ 5・0：分からない ／ Space：次へ ／ ←：前へ</p>
  <div class="row between quiz-controls"><button id="prev" ${r.index===0||paused?'disabled':''}>← 前へ</button><span class="muted">${Object.keys(r.answers).length} / ${r.order.length} 解答済み</span><button id="next" class="primary" ${paused?'disabled':''}>${r.index===r.order.length-1?'終了して採点 →':'次の問題へ →'} <kbd>Space</kbd></button></div>
  <div class="navigator">${r.order.map((id,i)=>`<button data-nav="${i}" title="問題 ${id}" class="${r.answers[id]!==undefined?'answered':''}" aria-current="${i===r.index}">${i+1}</button>`).join('')}</div>
  ${confirmSubmit?`<p class="notice">未解答が ${r.order.filter(id=>r.answers[id]===undefined).length} 問あります。未解答は未学習のまま残します。</p><button id="confirm" class="primary">この内容で終了・採点する</button><button id="cancel">続ける</button>`:'<button id="submit" class="primary">終了して採点する</button>'}`;
  app.querySelectorAll('[data-answer]').forEach(b=>b.onclick=()=>choose(+b.dataset.answer));
  document.querySelector('#prev').onclick=()=>move(r.index-1);document.querySelector('#next').onclick=advance;
  app.querySelectorAll('[data-nav]').forEach(b=>b.onclick=()=>move(+b.dataset.nav));
  document.querySelector('#pause').onclick=()=>{tick();paused=!paused;lastTick=performance.now();save();quiz();};
  document.querySelector('#home').onclick=()=>{tick();paused=true;save();lobby();};
  document.querySelector('#submit')?.addEventListener('click',requestSubmit);
  document.querySelector('#confirm')?.addEventListener('click',finish);
  document.querySelector('#cancel')?.addEventListener('click',()=>{confirmSubmit=false;quiz();});
}
function finish(){
  if(!state.active)return;tick();paused=true;
  result=grade(state.active,data.questions);state=applyResult(state,result);save();confirmSubmit=false;showResult(result);sync();
}
function showResult(r){
  view='result';result=r;paused=true;
  const types={};for(const a of r.details.attempts){const k=a.subtype;types[k]??={n:0,c:0};types[k].n++;types[k].c+=a.status==='correct'?1:0;}
  const half=Math.ceil(r.totalQuestions/2),halfInfo=xs=>`${xs.filter(a=>a.status==='correct').length}/${xs.length} · 平均 ${clock(xs.reduce((s,a)=>s+a.response_seconds,0)/Math.max(1,xs.length))}`;
  app.innerHTML=header()+note()+`<section class="card"><p class="eyebrow">学習結果 / 自主制作・公式換算点ではありません</p><h1 class="result-summary">${r.correctCount} / ${r.totalQuestions} · ${r.accuracy}%</h1><p>正解 ${r.correctCount} · 不正解 ${r.wrongCount} · 分からない ${r.unknownCount} · 未解答 ${r.unansweredCount}</p><p>学習時間 ${clock(r.elapsedSeconds)} · ${esc(r.date)}</p><p class="muted">前半 ${halfInfo(r.details.attempts.slice(0,half))} ／ 後半 ${halfInfo(r.details.attempts.slice(half))}</p><div class="row"><button id="continue" class="primary" ${!nextPool(r).length?'disabled':''}>次の ${nextPool(r).length}問を開始 <kbd>Space</kbd></button><button id="garden">学習マップへ戻る</button></div><p id="sync" class="sr-status" role="status">${esc(syncText)}</p></section>
  <section class="card explain" lang="ko"><h2>유형별 결과</h2><table class="table"><thead><tr><th>세부 유형</th><th>정답</th><th>정답률</th></tr></thead><tbody>${Object.entries(types).map(([k,v])=>`<tr><td>${esc(k)}</td><td>${v.c}/${v.n}</td><td>${Math.round(v.c/v.n*100)}%</td></tr>`).join('')}</tbody></table></section>
  <section class="card explain" lang="ko"><h2>문항별 해설</h2><p>붙는 조각 → 전체 배열 → ★ 확인 순서로 복습하세요. 오답·모름은 실제 응시일 기준 D+1·D+3·D+7에 다시 표시됩니다.</p>${r.details.attempts.map(a=>explanation(a,r)).join('')}</section>`;
  document.querySelector('#garden').onclick=lobby;document.querySelector('#continue').onclick=()=>start(nextPool(r));
}
function explanation(a,r){
  const q=data.questions.find(q=>q.id===a.item_no),order=[0,1,2,3].map(id=>a.display_order.indexOf(id)+1);
  const dates=state.items[q.id]?.reviewDates||[];
  return `<details><summary><span class="badge state-${a.status==='unanswered'?'new':a.status}">${esc(names[a.status])}</span> ${q.id}번 · ${a.response_seconds}초</summary><p class="muted">언어지식 → 문장배열(文の組み立て) → ${esc(q.subtype)} (학습용 세부 분류)</p>
    <h3>원문 · 번역</h3><p class="japanese" lang="ja">${q.reviewPrompt}</p><p>${a.display_order.map((id,i)=>`${i+1}. ${q.reviewParts[id]}`).join(' ／ ')}</p><p class="japanese" lang="ja">${q.reviewFull}</p><p>${esc(q.translation)}</p>
    <h3>선택한 답 · 정답</h3><p>선택: ${esc(a.selected_text??'미응답')} / 정답: ${q.reviewParts[q.answer]}<br>전체 배열: ${order.join(' → ')} / ★는 세 번째 칸: ${order[q.star-1]}번</p>
    <h3>접속·의미와 풀이</h3><p>${esc(q.reason)}</p><p>${q.reviewParts.map((p,i)=>`${i===2?'★ ':''}${p}`).join(' → ')}</p>
    <h3>함정 · 유사 표현 차이</h3><p>${esc(q.trap)}</p><p>${esc(q.contrast)}</p>
    <h3>추가 예문</h3><p class="japanese" lang="ja">${q.reviewExample}</p><p>${esc(q.exampleKo)}</p>
    <h3>다음 복습</h3><p>${dates.length?dates.map(esc).join(' · '):a.status==='unanswered'?'미학습으로 남았습니다.': '새 오답 복습 일정 없음. 기존 미래 복습이 있으면 유지합니다.'}</p>
    <h3>다음 풀이 절차 · 제출 전 체크</h3><p>① 빈칸 앞뒤의 조사·활용을 본다. ② 확실히 이어지는 두 조각을 묶는다. ③ 네 조각을 모두 넣고 의미를 확인한다. ④ 배열의 세 번째 조각과 선택지 표시 번호를 다시 대조한다.</p></details>`;
}
let syncing=false;
async function sync(){
  if(preview){syncText='動作確認モード：学習カレンダーには送信しません。';updateSync();return;}
  if(syncing)return;syncing=true;
  try{for(const payload of [...state.outbox]){
    syncText='学習カレンダーに記録しています…';updateSync();
    const base=location.hostname.endsWith('.chatgpt.site')?'https://jlpt-study-calendar.pcw0611.workers.dev':'';
    const response=await fetch(base+'/api/submit-composition',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),signal:AbortSignal.timeout(15000)});
    if(!response.ok||!(await response.json()).ok)throw Error('send');
    state.outbox=state.outbox.filter(p=>p.submissionId!==payload.submissionId);save();
    try{localStorage.setItem('jlpt-exam-recorded',String(Date.now()));}catch{}
  }syncText='確定した学習結果は記録済みです。進み具合はこのブラウザーに保存されています。';}
  catch{syncText='端末には保存済みです。通信回復後に自動で記録を送信します。';}
  finally{syncing=false;updateSync();}
}
function updateSync(){const node=document.querySelector('#sync');if(node)node.textContent=syncText;}
window.addEventListener('online',()=>{if(state.outbox.length)sync();});
setInterval(()=>{if(!document.hidden&&state.outbox.length)sync();},30000);
window.addEventListener('keydown',e=>{
  if(e.ctrlKey||e.metaKey||e.altKey||e.isComposing||e.target.closest?.('input,select,textarea,a,summary,[contenteditable="true"]'))return;
  const space=e.code==='Space'||e.key===' ';
  if(space){
    e.preventDefault();e.stopImmediatePropagation();
    if(e.repeat||spaceHeld||drag)return;spaceHeld=true;
    if(view==='quiz'&&!paused){if(!confirmSubmit)advance();}
    else if(view==='lobby'){selected.size?startSelected():startPriority();}
    else if(view==='result')start(nextPool(result));
  }else if(view==='quiz'&&!paused&&!confirmSubmit&&!e.repeat){
    if(/^[0-5]$/.test(e.key)){e.preventDefault();const n=+e.key;choose(n===0||n===5?-1:state.active.choices[state.active.order[state.active.index]][n-1],false);}
    else if(e.key==='ArrowLeft'){e.preventDefault();move(state.active.index-1);}
    else if(e.key==='ArrowRight'){e.preventDefault();advance();}
  }
},true);
window.addEventListener('keyup',e=>{if(spaceHeld&&(e.code==='Space'||e.key===' ')){e.preventDefault();e.stopImmediatePropagation();spaceHeld=false;}},true);
window.addEventListener('blur',()=>{spaceHeld=false;});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&view==='quiz'){tick();paused=true;save();quiz();}});
window.addEventListener('pagehide',()=>{tick();save();});
try{
  const response=await fetch('/exams/n2-sentence-composition-100.json');if(!response.ok)throw Error('load');data=await response.json();
  if(data.questions.length!==100)throw Error('count');lobby();
  clockTimer=setInterval(()=>{tick();const node=document.querySelector('#clock');if(node&&state.active)node.textContent=clock(state.active.elapsed);if(view==='quiz')save();},1000);
  if(state.outbox.length)sync();
}catch{app.innerHTML=header()+'<p class="notice error">問題を読み込めませんでした。ページを再読み込みしてください。保存した学習記録は保持されます。</p>';}
