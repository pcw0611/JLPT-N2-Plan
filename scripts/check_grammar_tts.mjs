// Real quiz + TTS code, mocked speech/DOM only. No audio, network or learning writes.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const html=fs.readFileSync(new URL('../jlpt-calendar-site/public/exams/n2-grammar-speedrun.html',import.meta.url),'utf8');
const code=html.slice(html.indexOf('const ALL_PATTERNS = ['),html.indexOf('class SoundEngine'))+
  html.slice(html.indexOf('const state = {'),html.lastIndexOf('</script>'));
const jp={name:'Japanese local',lang:'ja-JP',localService:true};
const en={name:'English',lang:'en-US'};
function setup(initialVoices=[en,jp], set='tuesday') {
  let voices=initialVoices;const spoken=[],saved=[],nodes=new Map(),events={},timers=new Map(),prefs=new Map();let nextTimer=1,cancels=0;
  const statuses=[{textContent:''},{textContent:''},{textContent:''}];
  const node=id=>{if(!nodes.has(id)){const c=new Set();nodes.set(id,{style:{},dataset:{},textContent:'',innerHTML:'',focus(){},querySelectorAll(){return []},classList:{add(...a){a.forEach(x=>c.add(x))},remove(...a){a.forEach(x=>c.delete(x))},contains(x){return c.has(x)},toggle(x,on){on?c.add(x):c.delete(x)}}});}return nodes.get(id);};
  class Utterance{constructor(text){this.text=text;}}
  const synth={getVoices(){return voices},cancel(){cancels++},addEventListener(name,fn){events[name]=fn},speak(u){spoken.push(u);u.onstart?.();}};
  const recordings=[];
  class AudioMock {
    constructor(url){this.url=url;recordings.push(this);}
    play(){this.onplaying?.();return Promise.resolve();}
    pause(){this.paused=true;}
  }
  const box={Audio:AudioMock,Date,Intl,URL,URLSearchParams,console,location:{search:'?set='+set,href:'https://example.test/quiz'},history:{replaceState(){}},
    document:{getElementById:node,querySelectorAll(selector){return selector==='[data-tts-status]'?statuses:[]},addEventListener(){}},
    window:{speechSynthesis:synth,SpeechSynthesisUtterance:Utterance,addEventListener(name,fn){events[name]=fn},autoSubmitExamResult(p){saved.push(p)}},
    localStorage:{getItem(k){return prefs.get(k)??null},setItem(k,v){prefs.set(k,v)}},
    sounds:{playCorrect(){},playWrong(){},playComboMilestone(){}},setInterval(){return 1},clearInterval(){},
    setTimeout(fn,ms){const id=nextTimer++;timers.set(id,{fn,ms});return id},clearTimeout(id){timers.delete(id)}};
  vm.createContext(box);vm.runInContext(code+'\nglobalThis.api={grammarTts,state,generateQuestions,startSessionWithQuestions,checkAnswer,advanceNext,pauseSession,resumeSession,requestEndSession,cancelEndSession,finishGame};',box);
  const api=box.api;api.grammarTts.init();
  return {api,spoken,recordings,saved,prefs,statuses,events,timers,setVoices(v){voices=v},unsupported(){delete box.window.speechSynthesis},get cancels(){return cancels}};
}
{
  const e=setup(),{api,spoken}=e,t=api.grammarTts;
  t.play(.95,true);assert.equal(spoken.at(-1).text,'これは日本語の音声です。');
  api.state.questions=api.generateQuestions('all',200);api.startSessionWithQuestions();
  let count=spoken.length;t.play();assert.equal(spoken.length,count,'No answer leak before answering');
  const q=api.state.questions[0];api.checkAnswer(q.answer);
  assert.equal(spoken.length,++count);assert.equal(spoken.at(-1).voice,jp);assert.equal(spoken.at(-1).rate,.95);
  assert.equal(spoken.at(-1).text,t.reading(q.item));assert(!/<|>|[가-힣]/.test(spoken.at(-1).text));
  t.play(.72);assert.equal(spoken.at(-1).rate,.72);count++;
  const cancelled=spoken.at(-1);api.advanceNext();cancelled.onend();assert.equal(t.utterance,null);
  t.play();assert.equal(spoken.length,count);
  api.checkAnswer(api.state.questions[1].choices.find(c=>c!==api.state.questions[1].answer));assert.equal(spoken.length,++count);
  api.advanceNext();api.checkAnswer('');assert.equal(spoken.length,++count,'Unknown also gets review audio');
  api.pauseSession();assert.equal(t.utterance,null);t.play();assert.equal(spoken.length,count);api.resumeSession();assert.equal(spoken.length,count);
  t.setAuto(false);assert.equal(e.prefs.get('n2_speedrun_tts_auto'),'false');t.play(.72);assert.equal(spoken.length,++count,'Manual replay remains usable');
  api.advanceNext();api.checkAnswer(api.state.questions[3].answer);assert.equal(spoken.length,count,'Auto OFF persists across questions');
  t.setAuto(true);assert.equal(spoken.length,++count);
  api.requestEndSession();assert.equal(t.utterance,null);api.cancelEndSession();assert.equal(spoken.length,count);
  t.play();assert.equal(spoken.length,++count);api.finishGame('early');assert.equal(t.utterance,null);t.play();assert.equal(spoken.length,count);assert.equal(e.saved.length,1);
  assert.equal(t.reading({sentence_ja_ruby:'<ruby>今日<rt>きょう</rt></ruby>は<ruby>雨<rt>あめ</rt></ruby>です。'}),'きょうはあめです。');
}
{
  const e=setup([]),{api}=e,t=api.grammarTts;
  api.state.questions=api.generateQuestions('all',200);api.startSessionWithQuestions();api.checkAnswer(api.state.questions[0].answer);
  assert(t.pending);api.advanceNext();e.setVoices([jp]);e.events.voiceschanged();assert.equal(e.spoken.length,0,'Late voices must not read previous answer');
  e.setVoices([]);api.checkAnswer(api.state.questions[1].answer);assert(t.pending);e.setVoices([jp]);e.events.voiceschanged();assert.equal(e.spoken.length,1);
  e.spoken[0].onerror({error:'not-allowed'});assert(e.statuses[0].textContent.includes('다시 듣기'));
}
{
  const e=setup([en]),{api}=e;
  api.state.questions=api.generateQuestions('all',200);api.startSessionWithQuestions();api.checkAnswer('');
  const timer=e.timers.get(api.grammarTts.voiceTimer);timer.fn();assert.equal(e.spoken.length,0);assert(e.statuses[0].textContent.includes('일본어 음성을 찾지'));
  e.unsupported();api.grammarTts.play();assert(e.statuses[0].textContent.includes('지원하지'));
}
const e=setup();const banks=JSON.parse(fs.readFileSync(new URL('./n2_grammar_weekly.json',import.meta.url),'utf8')).banks;
for(const b of banks)for(const row of b.items){const s=e.api.grammarTts.reading(row);assert(s.length>0);assert(!/<ruby>|<rt>|[가-힣]/.test(s));}
{
  const {api,spoken,recordings,events}=setup([jp],'sunday');
  const t=api.grammarTts;
  t.sundayRecordings['n2-grammar-001']='001-elio.mp3';
  api.state.questions=api.generateQuestions('all',200).filter(q=>q.item.id==='n2-grammar-001');
  api.startSessionWithQuestions();
  const replay = {code:'KeyR', preventDefault(){}};
  events.keydown(replay);assert.equal(recordings.length,0,'No recorded answer before reveal');
  api.checkAnswer(api.state.questions[0].answer);
  assert.match(recordings.at(-1).url,/sunday-20261103\/001-elio\.mp3$/);
  assert.equal(spoken.length,0,'Prefer the matching recorded sentence');
  events.keydown({...replay,ctrlKey:true});assert.equal(recordings.length,1);
  events.keydown(replay);
  assert.equal(recordings.length,2,'R replays the revealed answer');
  assert(recordings[0].paused,'Replay cancels the earlier clip');
  const last=recordings.at(-1);
  last.onerror();
  assert(last.paused,'Audio failure releases the recorded clip');
  assert.equal(spoken.at(-1).text,t.reading(api.state.questions[0].item));
}
console.log('PASS: post-answer-only TTS; correct/wrong/unknown; sample, replay/slow/auto preference; cancellation, late voices, missing Japanese, blocked audio; 1400 reading texts. No DB writes.');
