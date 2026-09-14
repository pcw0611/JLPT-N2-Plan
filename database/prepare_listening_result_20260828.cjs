const fs = require('fs');
const vm = require('vm');
const path = require('path');
const source = 'C:/Users/pcw06/.codex/visualizations/2026/08/28/01a046b7-45a7-7323-85da-ef3f6a0f61b0/n3-listening-order-time.html';
const html = fs.readFileSync(source, 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const literal = script.slice(script.indexOf('const data=') + 11, script.indexOf('\n  const synth='));
const questions = vm.runInNewContext(literal.replace(/;\s*$/, ''));
// User-submitted answers and measurements; not a synthetic test run.
const submitted = [
  [1,'correct',1,182,82,0,2,false],
  [2,'wrong',2,83,33,1,1,false],
  [3,'wrong',3,82,34,4,1,false],
  [4,'correct',2,77,36,4,1,false],
  [5,'correct',3,36,32,1,1,false],
  [6,'correct',1,71,57,2,2,false],
  [7,'wrong',3,92,81,0,2,false],
  [8,'wrong',1,60,37,3,1,false]
];
const result = {
  test_id:'n3-listening-order-time-20260828',test_date:'2026-08-28',
  title:'N3 청해 행동 순서·숫자·시간 8문항',source_class:'자체 제작',target_level:'N3',
  memory_timing:'취약 유형 변형 연습',total_items:8,correct_items:4,unknown_items:0,unanswered_items:0,
  elapsed_seconds:683,time_limit_seconds:960,timed_out:false,
  groups:{'課題理解':{correct:2,total:4},'ポイント理解':{correct:2,total:4}},
  wrong:[2,3,7,8],unknown:[],unanswered:[],
  attempts:submitted.map(([item_no,state,selected,response_seconds,audio_seconds,decision_seconds,play_count,audio_error])=>{
    const q=questions[item_no-1];
    return {item_no,type:q.type,subtype:q.sub,state,question:q.q,choices:q.c,selected_text:q.c[selected],correct_text:q.c[q.a],response_seconds,audio_seconds,decision_seconds,play_count,audio_error};
  }),
  review_dates:[{interval:'D+1',date:'2026-08-29'},{interval:'D+3',date:'2026-08-31'},{interval:'D+7',date:'2026-09-04'}],
  timing_note:'전체 타이머는 시작 버튼부터 제출까지의 경과시간. 오디오 시간은 TTS 재생 구간의 누적 경과시간. 결정시간은 마지막 재생 종료부터 최종 답 선택까지이며 선택 유지 시 다음 이동까지. 청취 여부는 사용자 음성 확인에 의존.',
  provenance:{answers:'사용자가 이 대화에서 전달한 실제 결과',questions:'이 대화에서 제작한 퀴즈 원문',source},
  questions
};
const dir=path.join(__dirname,'results');fs.mkdirSync(dir,{recursive:true});
const target=path.join(dir,result.test_id+'.json');
if(fs.existsSync(target)){
  if(fs.readFileSync(target,'utf8')!==JSON.stringify(result,null,2)+'\n')throw new Error('Existing result differs; refusing overwrite.');
}else fs.writeFileSync(target,JSON.stringify(result,null,2)+'\n','utf8');
console.log(target);
