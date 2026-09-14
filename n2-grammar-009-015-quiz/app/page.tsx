'use client';

import { useEffect, useMemo, useState } from 'react';

type Question = {
  id: string;
  number: number;
  kind: '文の文法1' | '文の文法2' | '文章の文法';
  category: string;
  pattern: string;
  prompt: string;
  choices: string[];
  answer: number;
  translation: string;
  connection: string;
  trap: string;
  similar: string;
  example: string;
};

const questions: Question[] = [
  { id:'n2-009-1',number:1,kind:'文の文法1',category:'문법 → 문법형식 판단 → 직후 발생',pattern:'〜か〜ないかのうちに',prompt:'授業終了のベルが（　）、学生たちは教室を飛び出していった。',choices:['鳴るか鳴らないかのうちに','鳴ったかぎり','鳴りかけのうちに','鳴ったかというと'],answer:0,translation:'수업 종료 벨이 울리자마자 학생들은 교실을 뛰쳐나갔다.',connection:'Vる＋か＋Vない＋かのうちに. 앞일과 거의 동시에 뒷일이 일어남을 나타냅니다.',trap:'단순한 조건이나 진행 중이 아니라, 경계가 분명하지 않을 만큼 즉시 이어지는 상황입니다.',similar:'〜たとたん에도 직후를 나타내지만, 〜か〜ないかのうちに는 「했는지 안 했는지 모를 정도로」 동시성이 강합니다.',example:'家に着くか着かないかのうちに、雨が降り始めた。'},
  { id:'n2-010-2',number:2,kind:'文の文法1',category:'문법 → 문법형식 판단 → 노력의 보람',pattern:'〜かいがある',prompt:'毎日発音を練習した（　）、以前より自然に話せるようになった。',choices:['かいがあって','かぎりで','がちで','かけで'],answer:0,translation:'매일 발음을 연습한 보람이 있어서 전보다 자연스럽게 말할 수 있게 되었다.',connection:'Vた／Nの＋かいがある・かいがあって. 노력한 결과에 보람이 있었음을 나타냅니다.',trap:'좋은 결과가 실제로 나타났으므로 「かいがあって」가 필요합니다.',similar:'〜かいもなく은 노력했지만 기대한 결과가 없었을 때 씁니다.',example:'遠くまで来たかいがあって、美しい景色が見られた。'},
  { id:'n2-011-3',number:3,kind:'文の文法1',category:'문법 → 문법형식 판단 → 범위·조건 유지',pattern:'〜かぎり',prompt:'体が元気な（　）、この仕事を続けたいと思っている。',choices:['かいがある','かけで','かぎり','がたい'],answer:2,translation:'몸이 건강한 한 이 일을 계속하고 싶다고 생각한다.',connection:'普通形＋かぎり. 그 상태나 조건이 계속되는 범위 안에서는 뒷내용도 성립합니다.',trap:'시간의 끝 한 번을 말하는 것이 아니라 조건이 유지되는 전체 기간을 말합니다.',similar:'〜うちは 상태가 변하기 전의 기간에 초점, 〜かぎり는 조건이 유효한 범위에 초점이 있습니다.',example:'日本にいるかぎり、日本語を使う機会は多い。'},
  { id:'n2-011-4',number:4,kind:'文の文法1',category:'문법 → 문법형식 판단 → 필수 전제 조건',pattern:'〜ないかぎり',prompt:'本人が同意しない（　）、この計画を進めることはできない。',choices:['かぎり','かぎりで','かいがなく','かというと'],answer:0,translation:'본인이 동의하지 않는 한 이 계획을 진행할 수 없다.',connection:'Vない＋かぎり. 앞의 조건이 충족되지 않으면 뒤의 일도 성립하지 않음을 나타냅니다.',trap:'「同意しない」라는 부정 조건을 그대로 받아야 합니다. 「同意するまで」와 의미 방향을 혼동하지 마세요.',similar:'〜なければ는 일반 조건, 〜ないかぎり는 그 조건이 핵심 전제라는 강조가 더 강합니다.',example:'実際に見ないかぎり、本当かどうか判断できない。'},
  { id:'n2-012-5',number:5,kind:'文の文法1',category:'문법 → 문법형식 판단 → 미완료 상태',pattern:'〜かけの',prompt:'机の上に（　）本が置いてある。',choices:['読みがたい','読みがちの','読みかけの','読むかぎりの'],answer:2,translation:'책상 위에 읽다 만 책이 놓여 있다.',connection:'Vます語幹＋かけの＋N. 시작했지만 아직 끝나지 않은 상태를 나타냅니다.',trap:'「읽기 어렵다」가 아니라 「읽다가 중간에 멈췄다」입니다.',similar:'〜途中の는 단순히 도중임을 말하고, 〜かけ는 시작했으나 미완성인 상태가 남아 있음을 강조합니다.',example:'飲みかけのコーヒーを冷蔵庫に入れた。'},
  { id:'n2-013-6',number:6,kind:'文の文法1',category:'문법 → 문법형식 판단 → 심리적으로 하기 어려움',pattern:'〜がたい',prompt:'長年支えてくれた友人の親切は、私にとって（　）。',choices:['忘れがたい','忘れかけだ','忘れがちだ','忘れないかぎりだ'],answer:0,translation:'오랫동안 지지해 준 친구의 친절은 나에게 잊기 어렵다.',connection:'Vます語幹＋がたい. 능력 부족보다 감정·판단상 받아들이거나 실행하기 매우 어려움을 나타냅니다.',trap:'자주 잊는 습관(忘れがち)이나 거의 잊을 뻔한 상태(忘れかけ)와 구별합니다.',similar:'〜にくい는 물리적·기능적으로 하기 어려운 경우에도 널리 쓰며, 〜がたい는 심리적·추상적 판단에 자주 쓰입니다.',example:'彼の説明には理解しがたい点がある。'},
  { id:'n2-014-7',number:7,kind:'文の文法1',category:'문법 → 문법형식 판단 → 좋지 않은 경향',pattern:'〜がち',prompt:'最近は忙しくて、朝食を（　）。',choices:['抜きがたい','抜きかけている','抜きがちだ','抜くかいがある'],answer:2,translation:'요즘은 바빠서 아침을 거르는 일이 많다.',connection:'Vます語幹／N＋がちだ. 바람직하지 않은 상태나 행동이 자주 나타나는 경향을 말합니다.',trap:'한 번 하다 만 동작이 아니라 반복되는 경향입니다.',similar:'〜気味는 약간 그런 상태라는 느낌, 〜がちは 실제로 그런 일이 자주 발생한다는 경향입니다.',example:'雨の日は家に閉じこもりがちになる。'},
  { id:'n2-015-8',number:8,kind:'文の文法1',category:'문법 → 문법형식 판단 → 부분 부정·화제 판단',pattern:'〜かというと',prompt:'私は甘い物が嫌い（　）、そういうわけではない。ただ、毎日は食べないだけだ。',choices:['かぎりでは','かというと','かけると','がたいと'],answer:1,translation:'내가 단것을 싫어하느냐 하면 그런 것은 아니다. 다만 매일 먹지 않을 뿐이다.',connection:'普通形＋かというと／かといえば. 어떤 판단이나 질문을 화제로 제시한 뒤 답하거나 일부 부정합니다.',trap:'첫 문장만 보고 「싫어한다」로 확정하면 뒤의 そういうわけではない와 충돌합니다.',similar:'〜わけではない는 전면 부정이 아님을 직접 나타내고, 〜かというと는 판단을 질문 형태로 꺼낸 뒤 설명합니다.',example:'この仕事が簡単かというと、決してそうではない。'},
  { id:'n2-012-9',number:9,kind:'文の文法2',category:'문법 → 문장 배열 → 미완료 동작과 역접',pattern:'〜かける',prompt:'彼は　＿＿＿　＿＿＿　★　＿＿＿、黙ってしまった。',choices:['言い','何かを','が','かけた'],answer:3,translation:'그는 무언가를 말하려다 말고 입을 다물었다.',connection:'자연스러운 배열은 「何かを／言い／かけた／が」이며 ★에는 「かけた」가 들어갑니다.',trap:'공식 배열 문제는 모든 조각을 한 번씩 사용합니다. 목적어→동사 ます어간→かけた→が 순서를 만드세요.',similar:'〜かける는 시작했지만 끝내지 않은 동작, 〜そうになる는 어떤 일이 일어날 뻔한 상태입니다.',example:'彼女は何か言いかけたが、やめた。'},
  { id:'n2-015-10',number:10,kind:'文章の文法',category:'문법 → 글의 흐름 → 판단 제시와 보충',pattern:'〜かといえば',prompt:'新しい制度で手続きは便利になった。しかし、問題がすべてなくなった（　）、そうではない。利用者への説明はまだ十分とは言えないからだ。',choices:['かいがあるので','かといえば','かけなので','がちなので'],answer:1,translation:'새 제도로 절차는 편리해졌다. 하지만 문제가 모두 사라졌느냐 하면 그렇지는 않다. 이용자에 대한 설명은 아직 충분하다고 할 수 없기 때문이다.',connection:'普通形＋かといえば、そうではない. 앞의 평가를 전면적으로 인정하지 않고 제한을 덧붙입니다.',trap:'便利になった만 보고 모든 문제가 해결됐다고 확대 해석하면 안 됩니다. しかし와 そうではない가 반대 방향을 표시합니다.',similar:'〜とは限らない도 예외 가능성을 말하지만, 〜かといえば는 앞의 질문·판단을 직접 받아 대답하는 흐름을 만듭니다.',example:'値段が高ければ品質も高いかといえば、必ずしもそうではない。'},
];

const unknown = '分からない';
const limitSeconds = 600;
const stateOrder: Record<string, number> = { wrong: 0, unknown: 1, unanswered: 2, correct: 3 };

export default function Home() {
  const [started,setStarted]=useState(false);
  const [submitted,setSubmitted]=useState(false);
  const [current,setCurrent]=useState(0);
  const [answers,setAnswers]=useState<Record<string,string>>({});
  const [elapsed,setElapsed]=useState(0);
  const [copied,setCopied]=useState(false);

  useEffect(()=>{
    if(!started||submitted) return;
    const timer=setInterval(()=>setElapsed(v=>v+1),1000);
    return()=>clearInterval(timer);
  },[started,submitted]);
  useEffect(()=>{ if(started&&!submitted&&elapsed>=limitSeconds) setSubmitted(true); },[elapsed,started,submitted]);

  const results=useMemo(()=>questions.map(q=>{
    const selected=answers[q.id];
    const correct=q.choices[q.answer];
    return {...q,selected,correct,state:!selected?'unanswered':selected===unknown?'unknown':selected===correct?'correct':'wrong'};
  }),[answers]);
  const correct=results.filter(r=>r.state==='correct').length;
  const wrong=results.filter(r=>r.state==='wrong').length;
  const unknownCount=results.filter(r=>r.state==='unknown').length;
  const unanswered=results.filter(r=>r.state==='unanswered').length;
  const q=questions[current];
  const time=`${String(Math.floor(elapsed/60)).padStart(2,'0')}:${String(elapsed%60).padStart(2,'0')}`;
  const resultPayload=()=>({test_id:'n2-grammar-009-015-check-20260830',test_date:'2026-08-30',title:'N2 문법 009~015 확인시험',source_class:'자체 제작',target_level:'N2',memory_timing:'강의 후 익일 확인',total_items:10,correct_items:correct,wrong_items:wrong,unknown_items:unknownCount,unanswered_items:unanswered,elapsed_seconds:elapsed,time_limit_seconds:limitSeconds,timed_out:elapsed>=limitSeconds,groups:Object.fromEntries(['文の文法1','文の文法2','文章の文法'].map(k=>{const rows=results.filter(r=>r.kind===k);return[k,{correct:rows.filter(r=>r.state==='correct').length,total:rows.length}]})),attempts:results.map(r=>({item_no:r.number,question_id:r.id,item_type_id:r.kind==='文の文法1'?'grammar_form':r.kind==='文の文法2'?'sentence_composition':'text_grammar',type:r.kind,category:r.category,pattern:r.pattern,state:r.state,question:r.prompt,choices:r.choices,selected_text:r.selected??null,correct_text:r.correct,visited:Boolean(r.selected)})),review_dates:[{interval:'D+1',date:'2026-08-31'},{interval:'D+3',date:'2026-09-02'},{interval:'D+7',date:'2026-09-06'}],practice_note:'문법 009~015 강의 후 자체 제작 확인시험. 실제 JLPT식 문법 형식 템플릿을 사용했으나 공식 기출·공식 모의고사가 아니며 합격 확률로 직접 환산하지 않음.',timing_note:'開始する부터 제출까지의 타이머만 기록. 해설 읽기와 다른 학습시간은 포함하지 않음.'});
  const copyResult=async()=>{await navigator.clipboard.writeText(JSON.stringify(resultPayload(),null,2));setCopied(true);};

  if(!started) return <main className="shell start"><section className="start-card"><p className="kicker">JLPT N2 · 文法 009〜015</p><h1>講義後確認テスト</h1><p className="lead">文の文法・文の組み立て・文章の文法</p><div className="facts"><div><strong>10</strong><span>問題</span></div><div><strong>10:00</strong><span>制限時間</span></div><div><strong>7</strong><span>文型</span></div></div><p className="notice">各問題には「分からない」があります。開始後にタイマーが動きます。</p><button className="primary" onClick={()=>setStarted(true)}>開始する</button></section></main>;

  if(submitted) return <main className="shell results"><header className="result-head"><div><p className="kicker">RESULT</p><h1>{correct} / {questions.length}</h1><p>{time} · 誤答 {wrong} · 分からない {unknownCount} · 未回答 {unanswered}</p></div><button className="secondary" onClick={copyResult}>{copied?'コピーしました':'結果をコピー'}</button></header><section className="score-grid">{['文の文法1','文の文法2','文章の文法'].map(kind=>{const rs=results.filter(r=>r.kind===kind);return <div key={kind}><span>{kind}</span><strong>{rs.filter(r=>r.state==='correct').length}/{rs.length}</strong></div>})}</section><section className="review-list">{[...results].sort((a,b)=>(stateOrder[a.state]??99)-(stateOrder[b.state]??99)).map(r=><article className={`review ${r.state}`} key={r.id}><div className="review-top"><span>問題 {r.number} · {r.kind}</span><b>{r.state==='correct'?'正解':r.state==='wrong'?'誤答':r.state==='unknown'?'分からない':'未回答'}</b></div><p className="category">{r.category}</p><h2>{r.prompt}</h2><dl><dt>번역</dt><dd>{r.translation}</dd><dt>선택 → 정답</dt><dd>{r.selected??'미응답'} → <strong>{r.correct}</strong></dd><dt>접속·의미</dt><dd>{r.connection}</dd><dt>함정</dt><dd>{r.trap}</dd><dt>유사 문형</dt><dd>{r.similar}</dd><dt>예문</dt><dd lang="ja">{r.example}</dd><dt>복습일</dt><dd>D+1 2026-08-31 · D+3 2026-09-02 · D+7 2026-09-06</dd><dt>다음번 풀이 절차</dt><dd>문장 끝의 평가 방향을 먼저 확인하고, 접속 형태를 제거 조건으로 사용한 뒤 남은 문형의 의미를 대입하세요.</dd><dt>정답 직전 체크</dt><dd>접속이 맞는가 → 앞뒤 시간·조건 관계가 맞는가 → 선택지가 문장 전체의 긍정·부정 방향과 맞는가.</dd></dl></article>)}</section></main>;

  return <main className="shell quiz"><header className="quiz-head"><div><p className="kicker">JLPT N2 · 文法 009〜015</p><strong>問題 {current+1} / {questions.length}</strong></div><div className={elapsed>540?'timer danger':'timer'}>{time}</div></header><div className="progress"><i style={{width:`${((current+1)/questions.length)*100}%`}}/></div><section className="question-card"><div className="question-meta"><span>{q.kind}</span><span>問題 {q.number}</span></div><h1>{q.prompt}</h1><div className="choices">{[...q.choices,unknown].map((choice,index)=><button key={choice} className={answers[q.id]===choice?'selected':''} onClick={()=>setAnswers({...answers,[q.id]:choice})}><b>{index<4?index+1:'?'}</b><span>{choice}</span></button>)}</div></section><nav><button className="secondary" disabled={current===0} onClick={()=>setCurrent(v=>v-1)}>前へ</button><div className="dots">{questions.map((item,i)=><button aria-label={`問題 ${i+1}`} key={item.id} className={`${i===current?'active':''} ${answers[item.id]?'answered':''}`} onClick={()=>setCurrent(i)}>{i+1}</button>)}</div>{current<questions.length-1?<button className="primary small" onClick={()=>setCurrent(v=>v+1)}>次へ</button>:<button className="primary small" onClick={()=>setSubmitted(true)}>提出する</button>}</nav></main>;
}
