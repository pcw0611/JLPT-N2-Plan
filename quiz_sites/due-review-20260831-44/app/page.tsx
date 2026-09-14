'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { questions, type Question } from './questions';

type Answer = number | 'unknown' | null;
type Phase = 'intro' | 'quiz' | 'result';
type SessionQuestion = Question & { sessionChoices: string[]; sessionAnswer: number };

const TEST_ID = 'due-review-20260901-review-plus-grammar';

function shuffle<T>(values: T[]): T[] {
  const copy = [...values];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const random = new Uint32Array(1);
    globalThis.crypto.getRandomValues(random);
    const j = random[0] % (i + 1);
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function buildSession(): SessionQuestion[] {
  const blocks = [
    questions.filter((question) => question.category.startsWith('어휘')),
    questions.filter((question) => question.category.startsWith('문법') && question.subtype === '文の文法1'),
    questions.filter((question) => question.category.startsWith('문법') && question.subtype === '文の文法2'),
    questions.filter((question) => question.category.startsWith('문법') && question.subtype === '文章の文法'),
    questions.filter((question) => question.category.startsWith('청해')),
  ].filter((block) => block.length > 0);
  return blocks.flatMap((block) => shuffle(block)).map((question) => {
    const choices = shuffle(question.choices.map((text, original) => ({ text, original })));
    return {
      ...question,
      sessionChoices: choices.map((choice) => choice.text),
      sessionAnswer: choices.findIndex((choice) => choice.original === question.answer),
    };
  });
}

function formatTime(seconds: number) {
  const minutes = Math.floor(seconds / 60);
  const rest = seconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(rest).padStart(2, '0')}`;
}

function stateLabel(answer: Answer, correct: boolean) {
  if (answer === null) return '미응답';
  if (answer === 'unknown') return '모름';
  return correct ? '정답' : '오답';
}

function instructionFor(question: SessionQuestion) {
  if (question.audio) {
    return '音声を聞いて、問いに対する最もよい答えを、1・2・3・4から一つ選んでください。';
  }
  if (question.subtype === '言い換え類義') {
    return '文中の「適している」と意味が最も近いものを、1・2・3・4から一つ選んでください。';
  }
  if (question.subtype === '文の文法2') {
    return '文を正しく並べたとき、★に入るものを、1・2・3・4から一つ選んでください。';
  }
  if (question.prompt.includes('（　）')) {
    return '（　）に入る最もよいものを、1・2・3・4から一つ選んでください。';
  }
  return '問いに対する最もよい答えを、1・2・3・4から一つ選んでください。';
}

export default function Home() {
  const [phase, setPhase] = useState<Phase>('intro');
  const [session, setSession] = useState<SessionQuestion[]>([]);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [current, setCurrent] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const [questionTimes, setQuestionTimes] = useState<number[]>([]);
  const [playCounts, setPlayCounts] = useState<number[]>([]);
  const [copied, setCopied] = useState(false);
  const startedAt = useRef(0);
  const enteredAt = useRef(0);
  const timeBank = useRef<number[]>([]);

  useEffect(() => {
    if (phase !== 'quiz') return;
    const timer = globalThis.setInterval(() => {
      setElapsed(Math.floor((performance.now() - startedAt.current) / 1000));
    }, 250);
    return () => globalThis.clearInterval(timer);
  }, [phase]);

  const start = () => {
    const nextSession = buildSession();
    setSession(nextSession);
    setAnswers(Array(nextSession.length).fill(null));
    setPlayCounts(Array(nextSession.length).fill(0));
    timeBank.current = Array(nextSession.length).fill(0);
    setQuestionTimes(Array(nextSession.length).fill(0));
    setCurrent(0);
    setElapsed(0);
    startedAt.current = performance.now();
    enteredAt.current = performance.now();
    setPhase('quiz');
    globalThis.scrollTo({ top: 0, behavior: 'instant' });
  };

  const bankCurrentTime = () => {
    const now = performance.now();
    timeBank.current[current] += (now - enteredAt.current) / 1000;
    enteredAt.current = now;
  };

  const move = (next: number) => {
    bankCurrentTime();
    setCurrent(Math.max(0, Math.min(session.length - 1, next)));
    globalThis.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const choose = (answer: Answer) => {
    setAnswers((previous) => previous.map((value, index) => index === current ? answer : value));
  };

  const playAudio = () => {
    const question = session[current];
    if (!question.audio || playCounts[current] >= 1 || !('speechSynthesis' in globalThis)) return;
    setPlayCounts((previous) => previous.map((value, index) => index === current ? value + 1 : value));
    const voices = globalThis.speechSynthesis.getVoices().filter((voice) => voice.lang.toLowerCase().startsWith('ja'));
    globalThis.speechSynthesis.cancel();
    let line = 0;
    const speakNext = () => {
      if (!question.audio || line >= question.audio.length) return;
      const item = question.audio[line];
      const utterance = new SpeechSynthesisUtterance(item.text);
      utterance.lang = 'ja-JP';
      utterance.rate = 0.92;
      utterance.pitch = item.speaker % 2 === 0 ? 0.92 : 1.08;
      if (voices.length) utterance.voice = voices[item.speaker % voices.length];
      line += 1;
      utterance.onend = speakNext;
      globalThis.speechSynthesis.speak(utterance);
    };
    speakNext();
  };

  const submit = () => {
    const unanswered = answers.filter((answer) => answer === null).length;
    if (unanswered && !globalThis.confirm(`未回答が${unanswered}問あります。提出しますか。`)) return;
    bankCurrentTime();
    globalThis.speechSynthesis?.cancel();
    const finalElapsed = Math.floor((performance.now() - startedAt.current) / 1000);
    setElapsed(finalElapsed);
    setQuestionTimes([...timeBank.current]);
    setPhase('result');
    globalThis.scrollTo({ top: 0, behavior: 'instant' });
  };

  const evaluated = useMemo(() => session.map((question, index) => ({
    question,
    answer: answers[index],
    correct: answers[index] === question.sessionAnswer,
    seconds: questionTimes[index] || 0,
    playCount: playCounts[index] || 0,
  })), [session, answers, questionTimes, playCounts]);

  const score = evaluated.filter((item) => item.correct).length;
  const wrong = evaluated.filter((item) => item.answer !== null && item.answer !== 'unknown' && !item.correct).length;
  const unknown = evaluated.filter((item) => item.answer === 'unknown').length;
  const unanswered = evaluated.filter((item) => item.answer === null).length;
  const splitPoint = Math.ceil(evaluated.length / 2);
  const firstHalf = evaluated.slice(0, splitPoint);
  const secondHalf = evaluated.slice(splitPoint);
  const firstScore = firstHalf.filter((item) => item.correct).length;
  const secondScore = secondHalf.filter((item) => item.correct).length;
  const firstSeconds = Math.round(firstHalf.reduce((sum, item) => sum + item.seconds, 0));
  const secondSeconds = Math.round(secondHalf.reduce((sum, item) => sum + item.seconds, 0));

  const typeStats = useMemo(() => {
    const grouped = new Map<string, { total: number; correct: number; seconds: number }>();
    evaluated.forEach((item) => {
      const key = item.question.subtype;
      const value = grouped.get(key) ?? { total: 0, correct: 0, seconds: 0 };
      value.total += 1;
      value.correct += item.correct ? 1 : 0;
      value.seconds += item.seconds;
      grouped.set(key, value);
    });
    return [...grouped.entries()];
  }, [evaluated]);

  const copyResult = async () => {
    const payload = {
      testId: TEST_ID,
      date: '2026-09-02',
      sourceClass: 'self_made_due_review',
      total: session.length,
      correct: score,
      wrong,
      unknown,
      unanswered,
      elapsedSeconds: elapsed,
      firstHalf: { correct: firstScore, total: firstHalf.length, seconds: firstSeconds },
      secondHalf: { correct: secondScore, total: secondHalf.length, seconds: secondSeconds },
      responses: evaluated.map((item, index) => ({
        itemNo: index + 1,
        reviewQueueId: item.question.reviewQueueId,
        responseState: item.answer === null ? 'unanswered' : item.answer === 'unknown' ? 'unknown' : item.correct ? 'correct' : 'wrong',
        selectedText: typeof item.answer === 'number' ? item.question.sessionChoices[item.answer] : item.answer === 'unknown' ? '分からない' : null,
        correctText: item.question.sessionChoices[item.question.sessionAnswer],
        responseSeconds: Math.round(item.seconds * 10) / 10,
        playCount: item.playCount,
        category: item.question.category,
      })),
    };
    await navigator.clipboard.writeText(JSON.stringify(payload));
    setCopied(true);
    globalThis.setTimeout(() => setCopied(false), 1800);
  };

  if (phase === 'intro') {
    return (
      <main className="shell intro-shell">
        <div className="exam-mark">JLPT N2 · DUE REVIEW</div>
        <section className="intro-card">
          <p className="kicker">2026年9月2日</p>
          <h1>満期復習<br /><span>{questions.length}問・一括試験</span></h1>
          <p className="intro-copy">学習順の手掛かりを避けるため、同じ問題形式の中では問題と選択肢がシャッフルされます。</p>
          <div className="intro-grid">
            <div><b>{questions.length}</b><span>問題</span></div>
            <div><b>1</b><span>連続タイマー</span></div>
            <div><b>1回</b><span>聴解再生</span></div>
          </div>
          <ol className="sequence">
            <li><span>01</span>文字・語彙</li>
            <li><span>02</span>文法形式</li>
            <li><span>03</span>文の組み立て・文章の文法</li>
            <li><span>04</span>聴解</li>
          </ol>
          <button className="primary large" onClick={start}>開始する</button>
          <p className="fine-print">途中採点なし · 解説は提出後に表示 · 「分からない」を選択可能</p>
        </section>
      </main>
    );
  }

  if (phase === 'quiz') {
    const question = session[current];
    const sectionName = question.category.startsWith('어휘')
      ? '文字・語彙'
      : question.category.startsWith('청해')
        ? '聴解'
        : question.subtype === '文の文法2'
          ? '文の組み立て'
          : question.subtype === '文章の文法'
            ? '文章の文法'
            : '文法形式';
    const answeredCount = answers.filter((answer) => answer !== null).length;
    return (
      <main className="shell quiz-shell">
        <header className="quiz-header">
          <div><p>{sectionName}</p><strong>{current + 1}<span> / {session.length}</span></strong></div>
          <div className="timer"><small>経過時間</small><b>{formatTime(elapsed)}</b></div>
        </header>
        <div className="progress"><i style={{ width: `${((current + 1) / session.length) * 100}%` }} /></div>
        <section className="question-card">
          <div className="question-meta"><span>問題 {current + 1}</span><em>{question.subtype}</em></div>
          <div className="question-instruction"><b>指示</b><span>{instructionFor(question)}</span></div>
          {question.audio ? (
            <div className="audio-box">
              <div className="audio-symbol">音</div>
              <div><strong>音声を聞いて答えてください。</strong><small>再生は1回だけです。スクリプトは提出後に表示されます。</small></div>
              <button onClick={playAudio} disabled={playCounts[current] >= 1}>{playCounts[current] ? '再生済み' : '再生する'}</button>
            </div>
          ) : null}
          <h2>{question.prompt.split('\n').map((line, index) => <span key={index}>{line}</span>)}</h2>
          <div className="choices">
            {question.sessionChoices.map((choice, index) => (
              <button key={choice} className={answers[current] === index ? 'selected' : ''} onClick={() => choose(index)}>
                <b>{index + 1}</b><span>{choice}</span>
              </button>
            ))}
            <button className={`unknown-choice ${answers[current] === 'unknown' ? 'selected' : ''}`} onClick={() => choose('unknown')}>
              <b>?</b><span>分からない</span>
            </button>
          </div>
        </section>
        <nav className="quiz-nav">
          <button onClick={() => move(current - 1)} disabled={current === 0}>前へ</button>
          <span>{answeredCount} / {session.length} 回答済み</span>
          {current < session.length - 1 ? <button className="primary" onClick={() => move(current + 1)}>次へ</button> : <button className="submit" onClick={submit}>提出する</button>}
        </nav>
        <div className="question-map">
          {session.map((_, index) => <button key={index} onClick={() => move(index)} className={`${index === current ? 'current' : ''} ${answers[index] !== null ? 'answered' : ''}`}>{index + 1}</button>)}
        </div>
      </main>
    );
  }

  const accuracy = evaluated.length ? Math.round((score / evaluated.length) * 1000) / 10 : 0;
  const firstRate = firstHalf.length ? firstScore / firstHalf.length : 0;
  const secondRate = secondHalf.length ? secondScore / secondHalf.length : 0;
  const fatigueDelta = Math.round((secondRate - firstRate) * 1000) / 10;
  return (
    <main className="shell result-shell">
      <header className="result-hero">
        <div><p className="kicker">採点完了 · 자체 제작 만기 복습</p><h1>{score}<span> / {evaluated.length}</span></h1><strong>{accuracy}%</strong></div>
        <button className="primary" onClick={copyResult}>{copied ? '복사됨' : '결과 기록문 복사'}</button>
      </header>

      <section className="result-grid">
        <article><span>소요시간</span><b>{formatTime(elapsed)}</b><small>연속 타이머</small></article>
        <article><span>오답</span><b>{wrong}</b><small>선택 후 오답</small></article>
        <article><span>모름</span><b>{unknown}</b><small>分からない</small></article>
        <article><span>미응답</span><b>{unanswered}</b><small>선택 없음</small></article>
      </section>

      <section className="stamina-card">
        <div className="section-title"><div><p className="kicker">STAMINA CHECK</p><h2>전반 {firstHalf.length}문항과 후반 {secondHalf.length}문항</h2></div><strong className={fatigueDelta < 0 ? 'down' : 'up'}>{fatigueDelta > 0 ? '+' : ''}{fatigueDelta}%p</strong></div>
        <div className="half-grid">
          <div><span>전반</span><b>{firstScore} / {firstHalf.length}</b><small>{formatTime(firstSeconds)} · 문항당 {firstHalf.length ? Math.round(firstSeconds / firstHalf.length) : 0}초</small></div>
          <div><span>후반</span><b>{secondScore} / {secondHalf.length}</b><small>{formatTime(secondSeconds)} · 문항당 {secondHalf.length ? Math.round(secondSeconds / secondHalf.length) : 0}초</small></div>
        </div>
        <p>{fatigueDelta <= -10 ? '후반 정답률이 10%p 이상 하락했습니다. 청해 진입 전 집중력과 시간 배분을 오답 원인과 함께 확인하세요.' : fatigueDelta < 0 ? '후반 정답률이 소폭 하락했습니다. 큰 붕괴는 아니지만 문항별 시간을 함께 확인하세요.' : '후반에도 정답률이 유지되거나 상승했습니다. 이번 한 세션에서는 뚜렷한 지구력 저하가 보이지 않습니다.'}</p>
      </section>

      <section className="type-card">
        <div className="section-title"><div><p className="kicker">TYPE ANALYSIS</p><h2>유형별 결과</h2></div></div>
        <div className="type-table">
          {typeStats.map(([name, value]) => <div key={name}><span>{name}</span><b>{value.correct} / {value.total}</b><small>평균 {Math.round(value.seconds / value.total)}초</small></div>)}
        </div>
      </section>

      <section className="review-section">
        <div className="section-title"><div><p className="kicker">FULL REVIEW</p><h2>문항별 채점과 해설</h2></div><span>오답·모름은 9월 3일 재복습 대상 · D+7 정답은 졸업</span></div>
        <div className="review-list">
          {evaluated.map((item, index) => {
            const selected = typeof item.answer === 'number' ? item.question.sessionChoices[item.answer] : item.answer === 'unknown' ? '分からない' : '선택 없음';
            const correctText = item.question.sessionChoices[item.question.sessionAnswer];
            const label = stateLabel(item.answer, item.correct);
            const nextReview = item.correct ? item.question.nextReview : '2026-09-03';
            return (
              <details key={`${item.question.reviewQueueId}-${item.question.id}`} className={item.correct ? 'correct' : 'needs-review'} open={!item.correct}>
                <summary><b>{index + 1}</b><span>{item.question.prompt.split('\n')[0]}</span><em>{label} · {Math.round(item.seconds)}초</em></summary>
                <div className="explanation">
                  <p className="category">{item.question.category}</p>
                  <div className="answer-pair"><p><span>선택</span>{selected}</p><p><span>정답</span>{correctText}</p></div>
                  {item.question.audio ? <div className="transcript"><span>대본</span>{item.question.audio.map((line, lineIndex) => <p key={lineIndex}>{line.speaker % 2 === 0 ? 'A' : 'B'}：{line.text}</p>)}</div> : null}
                  <dl>
                    <div><dt>번역</dt><dd>{item.question.translation}</dd></div>
                    <div><dt>접속</dt><dd>{item.question.connection}</dd></div>
                    <div><dt>핵심 의미</dt><dd>{item.question.meaning}</dd></div>
                    <div><dt>함정</dt><dd>{item.question.trap}</dd></div>
                    <div><dt>유사 문형 차이</dt><dd>{item.question.contrast}</dd></div>
                    <div><dt>추가 예문</dt><dd lang="ja">{item.question.example}</dd></div>
                    <div><dt>다음 복습일</dt><dd>{nextReview}</dd></div>
                    <div><dt>다음 풀이 절차</dt><dd>질문의 요구를 먼저 표시하고 → 시간·접속 신호를 찾고 → 선택지의 기능을 한 단어로 비교합니다.</dd></div>
                    <div><dt>제출 전 체크</dt><dd>문형의 앞뒤 접속과 문장 전체 결론이 동시에 맞는지 확인합니다.</dd></div>
                  </dl>
                </div>
              </details>
            );
          })}
        </div>
      </section>
      <footer>이 결과는 자체 제작 만기 복습이며 공식 JLPT 점수로 환산하지 않습니다.</footer>
    </main>
  );
}
