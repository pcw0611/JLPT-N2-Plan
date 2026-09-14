'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { questions, type Question } from './questions';

type Answer = number | 'unknown' | null;
type Phase = 'intro' | 'quiz' | 'result';
type SessionQuestion = Question & { sessionChoices: string[]; sessionAnswer: number };

const TEST_ID = 'n2-grammar-026-035-check-20260831';
const TEST_DATE = '2026-08-31';
const TOTAL = questions.length;
const HALF = Math.ceil(TOTAL / 2);

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
    questions.slice(0, 10),
    questions.slice(10, 11),
    questions.slice(11, 12),
  ];
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

  const submit = () => {
    const unanswered = answers.filter((answer) => answer === null).length;
    if (unanswered && !globalThis.confirm(`未回答が${unanswered}問あります。提出しますか。`)) return;
    bankCurrentTime();
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
  })), [session, answers, questionTimes]);

  const score = evaluated.filter((item) => item.correct).length;
  const wrong = evaluated.filter((item) => item.answer !== null && item.answer !== 'unknown' && !item.correct).length;
  const unknown = evaluated.filter((item) => item.answer === 'unknown').length;
  const unanswered = evaluated.filter((item) => item.answer === null).length;
  const firstHalf = evaluated.slice(0, HALF);
  const secondHalf = evaluated.slice(HALF);
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
      date: TEST_DATE,
      sourceClass: 'self_made_immediate_recognition',
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
        patternNumber: item.question.reviewQueueId,
        responseState: item.answer === null ? 'unanswered' : item.answer === 'unknown' ? 'unknown' : item.correct ? 'correct' : 'wrong',
        selectedText: typeof item.answer === 'number' ? item.question.sessionChoices[item.answer] : item.answer === 'unknown' ? '分からない' : null,
        correctText: item.question.sessionChoices[item.question.sessionAnswer],
        responseSeconds: Math.round(item.seconds * 10) / 10,
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
        <div className="exam-mark">JLPT N2 · GRAMMAR CHECK</div>
        <section className="intro-card">
          <p className="kicker">2026年8月31日</p>
          <h1>文法 026〜035<br /><span>講義直後・確認試験</span></h1>
          <p className="intro-copy">学習順の手掛かりを避けるため、同じ問題形式の中では問題と選択肢がシャッフルされます。</p>
          <div className="intro-grid">
            <div><b>12</b><span>問題</span></div>
            <div><b>1</b><span>連続タイマー</span></div>
            <div><b>10</b><span>文法項目</span></div>
          </div>
          <ol className="sequence">
            <li><span>01</span>文の文法1</li>
            <li><span>02</span>文の文法2</li>
            <li><span>03</span>文章の文法</li>
          </ol>
          <button className="primary large" onClick={start}>開始する</button>
          <p className="fine-print">途中採点なし · 解説は提出後に表示 · 「分からない」を選択可能</p>
        </section>
      </main>
    );
  }

  if (phase === 'quiz') {
    const question = session[current];
    const sectionName = current < 10 ? '文の文法1' : current < 11 ? '文の文法2' : '文章の文法';
    const answeredCount = answers.filter((answer) => answer !== null).length;
    return (
      <main className="shell quiz-shell">
        <header className="quiz-header">
          <div><p>{sectionName}</p><strong>{current + 1}<span> / {TOTAL}</span></strong></div>
          <div className="timer"><small>経過時間</small><b>{formatTime(elapsed)}</b></div>
        </header>
        <div className="progress"><i style={{ width: `${((current + 1) / TOTAL) * 100}%` }} /></div>
        <section className="question-card">
          <div className="question-meta"><span>問題 {current + 1}</span><em>{question.subtype}</em></div>
          <div className="question-instruction"><b>指示</b><span>{instructionFor(question)}</span></div>
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
          <span>{answeredCount} / {TOTAL} 回答済み</span>
          {current < TOTAL - 1 ? <button className="primary" onClick={() => move(current + 1)}>次へ</button> : <button className="submit" onClick={submit}>提出する</button>}
        </nav>
        <div className="question-map">
          {session.map((_, index) => <button key={index} onClick={() => move(index)} className={`${index === current ? 'current' : ''} ${answers[index] !== null ? 'answered' : ''}`}>{index + 1}</button>)}
        </div>
      </main>
    );
  }

  const accuracy = Math.round((score / TOTAL) * 1000) / 10;
  const fatigueDelta = Math.round(((secondScore / secondHalf.length) - (firstScore / firstHalf.length)) * 1000) / 10;
  return (
    <main className="shell result-shell">
      <header className="result-hero">
        <div><p className="kicker">採点完了 · 강의 직후 자체 제작 확인</p><h1>{score}<span> / {TOTAL}</span></h1><strong>{accuracy}%</strong></div>
        <button className="primary" onClick={copyResult}>{copied ? '복사됨' : '결과 기록문 복사'}</button>
      </header>

      <section className="result-grid">
        <article><span>소요시간</span><b>{formatTime(elapsed)}</b><small>연속 타이머</small></article>
        <article><span>오답</span><b>{wrong}</b><small>선택 후 오답</small></article>
        <article><span>모름</span><b>{unknown}</b><small>分からない</small></article>
        <article><span>미응답</span><b>{unanswered}</b><small>선택 없음</small></article>
      </section>

      <section className="stamina-card">
        <div className="section-title"><div><p className="kicker">STAMINA CHECK</p><h2>전반 6문항과 후반 6문항</h2></div><strong className={fatigueDelta < 0 ? 'down' : 'up'}>{fatigueDelta > 0 ? '+' : ''}{fatigueDelta}%p</strong></div>
        <div className="half-grid">
          <div><span>전반</span><b>{firstScore} / {firstHalf.length}</b><small>{formatTime(firstSeconds)} · 문항당 {Math.round(firstSeconds / firstHalf.length)}초</small></div>
          <div><span>후반</span><b>{secondScore} / {secondHalf.length}</b><small>{formatTime(secondSeconds)} · 문항당 {Math.round(secondSeconds / secondHalf.length)}초</small></div>
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
        <div className="section-title"><div><p className="kicker">FULL REVIEW</p><h2>문항별 채점과 해설</h2></div><span>오답·모름은 9월 1일 재복습 대상</span></div>
        <div className="review-list">
          {evaluated.map((item, index) => {
            const selected = typeof item.answer === 'number' ? item.question.sessionChoices[item.answer] : item.answer === 'unknown' ? '分からない' : '선택 없음';
            const correctText = item.question.sessionChoices[item.question.sessionAnswer];
            const label = stateLabel(item.answer, item.correct);
            const nextReview = item.correct ? item.question.nextReview : '2026-09-01';
            return (
              <details key={item.question.id} className={item.correct ? 'correct' : 'needs-review'} open={!item.correct}>
                <summary><b>{index + 1}</b><span>{item.question.prompt.split('\n')[0]}</span><em>{label} · {Math.round(item.seconds)}초</em></summary>
                <div className="explanation">
                  <p className="category">{item.question.category}</p>
                  <div className="answer-pair"><p><span>선택</span>{selected}</p><p><span>정답</span>{correctText}</p></div>
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
      <footer>이 결과는 강의 직후 자체 제작 확인이며 공식 JLPT 점수로 환산하지 않습니다.</footer>
    </main>
  );
}
