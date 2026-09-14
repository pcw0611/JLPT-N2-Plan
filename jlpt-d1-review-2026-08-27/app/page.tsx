'use client';

import { useEffect, useMemo, useRef, useState } from 'react';

type Question = {
  id: number; category: string; prompt: string; instruction?: string; choices?: string[];
  answers: string[]; explanation: string; audio?: { speaker: 'A' | 'B'; text: string }[];
};

const questions: Question[] = [
  { id: 1, category: '形容詞の活用', prompt: '「高い」の丁寧体・過去肯定として正しいものはどれですか。', choices: ['高いでした', '高かったです', '高くでした', '高かったでした'], answers: ['高かったです'], explanation: 'い형용사는 끝의 い를 빼고 かったです를 붙입니다. 高い → 高かったです.' },
  { id: 2, category: '形容詞の活用', prompt: '「静かだ」の丁寧体・過去肯定として正しいものはどれですか。', choices: ['静かなでした', '静かかったです', '静かでした', '静かだでした'], answers: ['静かでした'], explanation: 'な형용사의 정중한 과거 긍정형은 でした입니다. 따라서 静かでした가 정답입니다.' },
  { id: 3, category: '形容詞の活用', prompt: '昨日のホテルはあまり（　）。', choices: ['高いでした', '高かったです', '高くありませんでした', '高くないでした'], answers: ['高くありませんでした'], explanation: '昨日은 과거, あまり는 부정형과 함께 쓰입니다. 高い의 정중한 과거 부정형은 高くありませんでした입니다.' },
  { id: 4, category: '形容詞の活用', prompt: '「よい」の丁寧体・過去肯定として正しいものはどれですか。', choices: ['よいでした', 'よくでした', 'よかったです', 'よかったでした'], answers: ['よかったです'], explanation: 'よい의 과거형은 예외적으로 よかった가 됩니다. 정중형은 よかったです입니다.' },
  { id: 5, category: '形容詞の活用', prompt: 'この町は昔、とても（　）。', choices: ['静かでした', '静かなでした', '静かかったです', '静かではありません'], answers: ['静かでした'], explanation: '昔가 있으므로 과거형이 필요합니다. な형용사 静かだ의 과거 긍정형은 静かでした입니다.' },
  { id: 6, category: '形容詞の活用', prompt: '田中さんは会社で（　）人です。', choices: ['有名', '有名に', '有名な', '有名だ'], answers: ['有名な'], explanation: 'な형용사가 명사를 수식할 때는 な를 붙입니다. 따라서 有名な人입니다.' },
  { id: 7, category: '文法形式の判断', prompt: '日本へ行ったら、温泉に（　）みたいです。', choices: ['入って', '入り', '入る', '入った'], answers: ['入って'], explanation: '～てみたい는 ‘시험 삼아 ~해 보고 싶다’라는 뜻입니다. 入る의 て형은 入って이므로 入ってみたい가 됩니다.' },
  { id: 8, category: '言い換え類義', prompt: '「状況を改善する」と最も近い意味はどれですか。', choices: ['状況を詳しく説明する', '状況をよりよくする', '状況をそのままにする', '状況について質問する'], answers: ['状況をよりよくする'], explanation: '改善する는 나쁜 점을 고쳐 더 좋은 상태로 만든다는 뜻이므로 状況をよりよくする와 가장 가깝습니다.' },
  { id: 9, category: '漢字の読み', prompt: 'この料金には朝食も「含まれています」。', choices: ['つつまれています', 'ふくまれています', 'たたまれています', 'くるまれています'], answers: ['ふくまれています'], explanation: '含む는 ふくむ로 읽습니다. 수동형 含まれる의 읽기는 ふくまれる입니다.' },
  { id: 10, category: '文脈語彙', prompt: '事故を防ぐためには、（　）な方法を選ぶ必要があります。', choices: ['適切', '直接', '正直', '確実そう'], answers: ['適切'], explanation: '목적이나 상황에 알맞은 방법이라는 뜻에는 適切な方法가 자연스럽습니다.' },
  { id: 11, category: '短文主張理解', prompt: '筆者が最も言いたいことは何ですか。\n\n外国語の単語は、一度にたくさん覚えるより、何日かに分けて何度も思い出すほうが忘れにくい。覚えた直後だけでなく、翌日にも確認することが大切だ。', choices: ['単語は一日ですべて覚えるべきだ', '覚えた直後の確認だけで十分だ', '日を空けて思い出す練習が大切だ', '外国語の単語は覚えなくてもよい'], answers: ['日を空けて思い出す練習が大切だ'], explanation: '필자의 결론은 마지막 문장에 있습니다. 외운 직후뿐 아니라 다음 날에도 확인해야 한다는 것이 핵심입니다.' },
  { id: 12, category: '短文内容理解', prompt: '山田さんは何時までに受付へ行けばいいですか。\n\n【健康診断のお知らせ】予約時間は10時です。検査の準備がありますので、予約時間の15分前までに2階受付へお越しください。', choices: ['9時30分', '9時45分', '10時', '10時15分'], answers: ['9時45分'], explanation: '예약 시간은 10시이고 15분 전까지 오라고 했으므로 정답은 9시 45분입니다.' },
  { id: 13, category: 'ポイント理解', prompt: '女の人は、どこで男の人と会いますか。', instruction: '音声は1回だけ再生できます。', choices: ['駅の改札', '駅前の本屋', '喫茶店の中', '会社の受付'], answers: ['駅前の本屋'], explanation: '처음 언급된 개찰구나 카페가 아니라 변경된 약속 장소인 駅前の本屋가 정답입니다.', audio: [
    { speaker: 'A', text: 'もしもし、駅の改札に着きました。どこにいますか。' },
    { speaker: 'B', text: 'ごめんなさい。喫茶店が混んでいるので、駅前の本屋にいます。そこで会いましょう。' },
    { speaker: 'A', text: '分かりました。すぐ行きます。' },
  ] },
  { id: 14, category: '課題理解', prompt: '女の人は、このあとまず何をしますか。', instruction: '音声は1回だけ再生できます。', choices: ['写真を選ぶ', '文章だけを取引先へ送る', '部長にメールする', 'パンフレットを印刷する'], answers: ['文章だけを取引先へ送る'], explanation: '사진은 내일 오전에 고릅니다. 여자가 지금 바로 해야 하는 일은 거래처에 글만 먼저 보내는 것입니다.', audio: [
    { speaker: 'A', text: 'パンフレットの案、今日中に取引先へ送れそうですか。' },
    { speaker: 'B', text: '文章はできましたが、使う写真がまだ決まっていません。' },
    { speaker: 'A', text: 'では、先方には文章だけ先に送ってください。写真は明日の午前中に私と選びましょう。' },
    { speaker: 'B', text: '分かりました。すぐメールします。' },
  ] },
  { id: 15, category: '課題理解', prompt: '男の人は、このあとまず何をしますか。', instruction: '音声は1回だけ再生できます。', choices: ['資料を30部コピーする', '会議室へ資料を運ぶ', '資料の間違いを直す', '課長に電話する'], answers: ['資料の間違いを直す'], explanation: '복사하기 전에 3페이지의 잘못된 숫자를 고치라는 지시를 받았습니다. 따라서 가장 먼저 할 일은 자료 수정입니다.', audio: [
    { speaker: 'A', text: '午後の会議の資料、もうコピーしましたか。' },
    { speaker: 'B', text: '今から30部コピーするところです。' },
    { speaker: 'A', text: 'その前に、3ページの数字が違っているので直してください。コピーしたら会議室へ運んでください。' },
    { speaker: 'B', text: 'はい、先に3ページを確認します。' },
  ] },
];

const normalize = (value: string) => value.replace(/[\s。、・]/g, '').trim();

export default function Home() {
  const [started, setStarted] = useState(false);
  const [finished, setFinished] = useState(false);
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [remaining, setRemaining] = useState(18 * 60);
  const [plays, setPlays] = useState<Record<number, number>>({});
  const [copied, setCopied] = useState(false);
  const startedAt = useRef<number>(0);

  useEffect(() => {
    if (!started || finished) return;
    const timer = window.setInterval(() => setRemaining((value) => {
      if (value <= 1) { window.clearInterval(timer); setFinished(true); return 0; }
      return value - 1;
    }), 1000);
    return () => window.clearInterval(timer);
  }, [started, finished]);

  const current = questions[index];
  const elapsed = 18 * 60 - remaining;
  const result = useMemo(() => {
    const correct = questions.filter((q) => q.answers.some((answer) => normalize(answer) === normalize(answers[q.id] ?? ''))).length;
    const unknown = questions.filter((q) => answers[q.id] === '__unknown__').length;
    const byCategory = questions.reduce<Record<string, { correct: number; total: number }>>((acc, q) => {
      acc[q.category] ??= { correct: 0, total: 0 }; acc[q.category].total += 1;
      if (q.answers.some((answer) => normalize(answer) === normalize(answers[q.id] ?? ''))) acc[q.category].correct += 1;
      return acc;
    }, {});
    const unanswered = questions.filter((q) => answers[q.id] === undefined).length;
    return { correct, unknown, unanswered, wrong: 15 - correct - unknown - unanswered, byCategory };
  }, [answers]);

  const start = () => { startedAt.current = Date.now(); setStarted(true); };
  const finish = () => { setRemaining(Math.max(0, 18 * 60 - Math.round((Date.now() - startedAt.current) / 1000))); setFinished(true); speechSynthesis.cancel(); };
  const choose = (value: string) => setAnswers((prev) => ({ ...prev, [current.id]: value }));
  const playAudio = () => {
    if (!current.audio || plays[current.id]) return;
    setPlays((prev) => ({ ...prev, [current.id]: 1 }));
    speechSynthesis.cancel();
    const voices = speechSynthesis.getVoices().filter((v) => v.lang.startsWith('ja'));
    let line = 0;
    const next = () => {
      if (!current.audio || line >= current.audio.length) return;
      const item = current.audio[line++];
      const utterance = new SpeechSynthesisUtterance(item.text);
      utterance.lang = 'ja-JP'; utterance.rate = item.speaker === 'A' ? 0.9 : 0.98; utterance.pitch = item.speaker === 'A' ? 0.82 : 1.18;
      if (voices.length) utterance.voice = voices[item.speaker === 'A' ? 0 : Math.min(1, voices.length - 1)];
      utterance.onend = next; speechSynthesis.speak(utterance);
    };
    next();
  };

  const reportText = `8月27日 D+1復習テスト結果：${result.correct}/15、所要時間 ${Math.floor(elapsed / 60)}:${String(elapsed % 60).padStart(2, '0')}、不明 ${result.unknown}、誤答 ${result.wrong}、未回答 ${result.unanswered}。自作D+1選択式復習として記録してください。`;
  const copyReport = async () => { await navigator.clipboard.writeText(reportText); setCopied(true); };

  if (!started) return <main className="quiz-shell intro"><section className="intro-card"><p className="eyebrow">JLPT N3 FOUNDATION · D+1</p><h1>翌日想起テスト</h1><p className="lead">昨日の誤答と「不明」を、翌日も正しく識別できるか確認します。</p><div className="intro-grid"><div><b>15</b><span>問題</span></div><div><b>18:00</b><span>制限時間</span></div><div><b>80%</b><span>合格目標</span></div></div><ul><li>全15問・選択式</li><li>聴解3問は各1回のみ再生</li><li>分からない場合は「分からない」を選択</li></ul><button className="primary" onClick={start}>テストを始める</button></section></main>;

  if (finished) return <main className="quiz-shell"><header className="quiz-top"><div><p className="eyebrow">RESULT</p><h1>D+1 復習結果</h1></div><div className="timer done">{Math.floor(elapsed / 60)}:{String(elapsed % 60).padStart(2, '0')}</div></header><section className="score-card"><div className="score"><strong>{result.correct}</strong><span>/ 15</span></div><div><p>正答率</p><b>{Math.round(result.correct / 15 * 100)}%</b></div><div><p>不明</p><b>{result.unknown}</b></div><div><p>誤答</p><b>{result.wrong}</b></div><div><p>未回答</p><b>{result.unanswered}</b></div></section><section className="result-grid"><div className="panel"><h2>分野別</h2>{Object.entries(result.byCategory).map(([name, value]) => <div className="category-row" key={name}><span>{name}</span><b>{value.correct}/{value.total}</b></div>)}</div><div className="panel"><h2>記録用</h2><p className="report-copy">{reportText}</p><button className="secondary" onClick={copyReport}>{copied ? 'コピーしました' : '結果をコピー'}</button></div></section><section className="review-list"><h2>全問解説</h2>{questions.map((q) => { const ok = q.answers.some((answer) => normalize(answer) === normalize(answers[q.id] ?? '')); return <article key={q.id} className={ok ? 'review-item correct' : 'review-item wrong'}><div><b>{q.id}</b><span>{q.category}</span><em>{ok ? '正解' : answers[q.id] === '__unknown__' ? '不明' : answers[q.id] === undefined ? '未回答' : '誤答'}</em></div><h3>{q.prompt}</h3><p>あなたの答え：{answers[q.id] === '__unknown__' ? '分からない' : answers[q.id] || '未回答'}</p><p>正解：<strong>{q.answers[0]}</strong></p><small lang="ko">{q.explanation}</small></article>})}</section></main>;

  return <main className="quiz-shell"><header className="quiz-top"><div><p className="eyebrow">D+1 DELAYED RECALL</p><h1>翌日想起テスト</h1></div><div className={`timer ${remaining < 180 ? 'urgent' : ''}`}>{Math.floor(remaining / 60)}:{String(remaining % 60).padStart(2, '0')}</div></header><div className="progress"><i style={{ width: `${(index + 1) / 15 * 100}%` }} /></div><section className="question-card"><div className="question-meta"><span>{current.category}</span><b>{index + 1} / 15</b></div><h2>{current.prompt}</h2>{current.instruction && <p className="instruction">{current.instruction}</p>}{current.audio && <button className="audio-button" disabled={Boolean(plays[current.id])} onClick={playAudio}>{plays[current.id] ? '再生済み' : '▶ 音声を再生'}</button>}{current.choices ? <div className="choices">{current.choices.map((choice, choiceIndex) => <button className={answers[current.id] === choice ? 'selected' : ''} onClick={() => choose(choice)} key={choice}><i>{choiceIndex + 1}</i>{choice}</button>)}</div> : <input autoFocus value={answers[current.id] === '__unknown__' ? '' : answers[current.id] ?? ''} onChange={(e) => choose(e.target.value)} placeholder="答えを入力してください" /> }<button className={`unknown ${answers[current.id] === '__unknown__' ? 'selected' : ''}`} onClick={() => choose('__unknown__')}>分からない</button></section><nav><button className="secondary" disabled={index === 0} onClick={() => setIndex(index - 1)}>戻る</button>{index < 14 ? <button className="primary" onClick={() => setIndex(index + 1)}>次へ</button> : <button className="primary finish" onClick={finish}>採点する</button>}</nav></main>;
}
