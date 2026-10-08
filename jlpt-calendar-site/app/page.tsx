'use client';

import { useEffect, useMemo, useState } from 'react';
import { type DailyReport, domainLabel, formatAccuracy, formatClock, formatStudy, orderedDomains, orderedTypes, sourceLabel } from '../lib/reports';

const getSeoulDate = () => new Intl.DateTimeFormat('sv-SE', { timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
const getDaysDiff = (targetDate: string) => Math.ceil((Date.parse(targetDate + 'T00:00:00+09:00') - Date.parse(getSeoulDate() + 'T00:00:00+09:00')) / 86400000);
const examDaysLeft = () => Math.max(0, getDaysDiff('2026-12-06'));
const nextMockDaysLeft = () => Math.max(0, getDaysDiff('2026-10-18'));

const dateLabel = (date: string) => {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(date);
  return match ? `${Number(match[2])}月${Number(match[3])}日` : '날짜 없음';
};
const numberLabel = (value: number) => new Intl.NumberFormat('ja-JP').format(value);

interface SpecialDateInfo {
  badge: string;
  type: 'upcoming-mock' | 'official-exam' | 'completed-mock';
  title: string;
  desc: string;
  subDesc?: string;
  linkText?: string;
  linkUrl?: string;
}

const SPECIAL_DATES: Record<string, SpecialDateInfo> = {
  '2026-09-20': {
    badge: '1次完了',
    type: 'completed-mock',
    title: '第1回 N2 実戦模擬試験 (完了)',
    desc: '公式問題集 第2集 全領域完本 107問 · 119/180点 (71/107問, 66.4%) 合格ライン・目標110点突破！'
  },
  '2026-09-30': {
    badge: '2次完了',
    type: 'completed-mock',
    title: '第2回 N2 実戦模擬試験 (完了)',
    desc: '2023年12月 JLPT N2 過去問完本 102問完走 · 92/180点 (51/102問, 50.0%) 全領域足切り0件＆合格ライン突破！'
  },
  '2026-10-18': {
    badge: '3次予定',
    type: 'upcoming-mock',
    title: '第3回 N2 実戦模擬試験 (2023年7月 過去問完本)',
    desc: '言語知識・読解 72問 (105分) ＋ 聴解 32問 (50分) · 計104問 実戦規格',
    subDesc: '10월 단어 전권 완독 및 N2 문법 예문 복습 성과 중간 점검 (목표: 105점+ 돌파)',
    linkUrl: '/exams/past-exams-portal.html',
    linkText: '📋 2023.07 기출 분석 및 출제 경향 확인 ➔'
  },
  '2026-11-01': {
    badge: '4次予定',
    type: 'upcoming-mock',
    title: '第4回 N2 実戦模擬試験 (2022年12月 過去問完本)',
    desc: '言語知識・読解 72問 (105分) ＋ 聴解 32問 (50分) · 計104問 実戦規格',
    subDesc: '고난도 문법 호응 및 청해 즉시응답 방어율 집중 점검 (목표: 110점 안정권)',
    linkUrl: '/exams/past-exams-portal.html',
    linkText: '📋 2022.12 기출 분석 및 출제 경향 확인 ➔'
  },
  '2026-11-15': {
    badge: '5次予定',
    type: 'upcoming-mock',
    title: '第5回 N2 実戦模擬試験 (2022年7月 過去問完本)',
    desc: '言語知識・読解 72問 (105分) ＋ 聴解 32問 (50分) · 計104問 실전규격',
    subDesc: '전 영역 과락 위험 제로 및 110점 방어선 공고화 (목표: 115점+ 고득점 도전)',
    linkUrl: '/exams/past-exams-portal.html',
    linkText: '📋 2022.07 기출 분석 및 출제 경향 확인 ➔'
  },
  '2026-11-29': {
    badge: '最終模試',
    type: 'upcoming-mock',
    title: '第6回 N2 ファイナル実戦リハーサル (D-7)',
    desc: '본시험 1주일 전 최종 실전 리허설 · 실제 시험 시간표 100% 동일 적용 104문항 완본',
    subDesc: '실전 시간 배분, 마킹 루틴, 멘탈 및 컨디션 최종 점검',
    linkUrl: '/exams/past-exams-portal.html',
    linkText: '📋 최종 실전 리허설 가이드 ➔'
  },
  '2026-12-06': {
    badge: '🎯 本番',
    type: 'official-exam',
    title: '2026年 第2回 JLPT N2 本試験',
    desc: '最優先目標: 2026-12-06 JLPT N2 合格および110点以上達成！'
  }
};

export default function Home() {
  const [reports, setReports] = useState<DailyReport[]>([]);
  const [selectedDate, setSelectedDate] = useState(getSeoulDate);
  const [visibleMonth, setVisibleMonth] = useState(() => getSeoulDate().slice(0, 7));
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [daysLeft, setDaysLeft] = useState(examDaysLeft);
  const [mockDays, setMockDays] = useState(nextMockDaysLeft);


  useEffect(() => {
    let mounted = true;
    fetch('/api/study-days', { cache: 'no-store' })
      .then(response => response.ok ? response.json() : Promise.reject(new Error('load failed')))
      .then(data => {
        const payload = data as { days?: unknown };
        if (!Array.isArray(payload?.days)) throw new Error('invalid response');
        const days: DailyReport[] = payload.days
          .filter((day): day is DailyReport => !!day && typeof day === 'object' && typeof (day as DailyReport).date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test((day as DailyReport).date))
          .slice()
          .sort((a: DailyReport, b: DailyReport) => a.date.localeCompare(b.date));
        if (!mounted) return;
        setDaysLeft(examDaysLeft());
        setMockDays(nextMockDaysLeft());
        setReports(days);
        const today = getSeoulDate();
        const initialDate = days.some(r => r.date === today) ? today : days.at(-1)?.date ?? today;
        setSelectedDate(initialDate);
        setVisibleMonth(initialDate.slice(0, 7));
      })
      .catch(() => { if (mounted) setLoadError(true); })
      .finally(() => { if (mounted) setLoading(false); });
    return () => { mounted = false; };
  }, []);

  const latest = reports.at(-1);
  const selected = reports.find(r => r.date === selectedDate);
  const selectedSpecial = SPECIAL_DATES[selectedDate];
  const month = visibleMonth;
  const [year, monthNumber] = month.split('-').map(Number);

  const moveMonth = (offset: number) => {
    const next = new Date(Date.UTC(year, monthNumber - 1 + offset, 1));
    setVisibleMonth(`${next.getUTCFullYear()}-${String(next.getUTCMonth() + 1).padStart(2, '0')}`);
  };

  const cells = useMemo(() => {
    const first = new Date(Date.UTC(year, monthNumber - 1, 1)).getUTCDay();
    const length = new Date(Date.UTC(year, monthNumber, 0)).getUTCDate();
    return [...Array(first).fill(null), ...Array.from({ length }, (_, i) => i + 1)] as (number | null)[];
  }, [year, monthNumber]);

  const recorded = new Set(reports.map(r => r.date));
  const isV2 = selected?.schemaVersion === 2;
  const latestProbability = latest?.probabilities?.N2;
  const types = selected ? orderedTypes(selected.types ?? []) : [];

  return (
    <main className="site-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">JLPT N2 PLAN</p>
          <h1>学習カレンダー</h1>
        </div>
        <div className="topbar-actions">
          <a className="game-button typing-nav-btn" href="/typing" aria-label="MyGO!!!!! 歌詞タイピング練習を開く">
            <span aria-hidden="true">⌨️</span> MyGO!!!!! タイピング <span aria-hidden="true">→</span>
          </a>
          <a className="game-button speedrun-nav-btn" href="/exams/verb-speedrun-100.html" aria-label="動詞活用 SPEED RUN 100 練習を開く">
            <span aria-hidden="true">⚡</span> 動詞活用 SPEED RUN <span aria-hidden="true">→</span>
          </a>
          <a className="game-button adj-speedrun-nav-btn" href="/exams/adj-speedrun-100.html" aria-label="形容詞活用 SPEED RUN 100 練習を開く">
            <span aria-hidden="true">🌟</span> 形容詞活用 SPEED RUN <span aria-hidden="true">→</span>
          </a>
          <a className="game-button grammar-nav-btn" href="/exams/n2-grammar-speedrun.html" aria-label="N2 文法 SPEED RUN 문형 저격 퀴즈를 열기">
            <span aria-hidden="true">🎯</span> N2 文法 SPEED RUN <span aria-hidden="true">→</span>
          </a>
          <a className="game-button puzzle-nav-btn" href="/exams/n2-grammar-puzzle.html" aria-label="N2 文法 接続パズル 블록 조립 퀴즈를 열기">
            <span aria-hidden="true">🧩</span> N2 文法 接続パズル <span aria-hidden="true">→</span>
          </a>
          <a className="game-button error-nav-btn" href="/exams/n2-mock-error-review-pool.html" aria-label="모의고사 間違いノート 복습 마스터 풀 열기">
            <span aria-hidden="true">📑</span> 模試 間違いノート <span aria-hidden="true">→</span>
          </a>
          <a className="game-button mock-nav-btn" href="/exams/past-exams-portal.html" aria-label="実戦模試・過去問アーカイブを開く">
            <span aria-hidden="true">📝</span> 過去問・模試 <span aria-hidden="true">→</span>
          </a>
          <a className="game-button listening-nav-btn" href="/exams/official-vol2-listening-player.html" aria-label="公式聴解音源プレイヤーを開く">
            <span aria-hidden="true">🎧</span> 聴解プレイヤー <span aria-hidden="true">→</span>
          </a>
          <div className="exam-chips-group">
            <button
              type="button"
              className="exam-chip chip-mock"
              onClick={() => { setSelectedDate('2026-10-18'); setVisibleMonth('2026-10'); }}
              title="10月18日(日) 第3回実戦模試 (カレンダーで表示)"
            >
              <span className="chip-dot pulse-amber" />
              <span className="chip-title">10/18 第3回模試</span>
              <strong className="chip-dday">D-{mockDays}</strong>
            </button>
            <button
              type="button"
              className="exam-chip chip-exam"
              onClick={() => { setSelectedDate('2026-12-06'); setVisibleMonth('2026-12'); }}
              title="12月6日(日) JLPT N2本試験 (カレンダーで表示)"
            >
              <span className="chip-dot glow-target" />
              <span className="chip-title">12/6 本試験</span>
              <strong className="chip-dday">D-{daysLeft}</strong>
            </button>
          </div>
        </div>
      </header>

      <section className="hero">
        <div>
          <p className="eyebrow accent">LIVE STUDY LOG</p>
          <h2>今日の学びを<br />合格可能性へ</h2>
          <p>日々の結果と、その日までの記録を分けて確認できます。</p>
        </div>
        <div className="hero-score">
          <span>N2 12月予測・最新記録</span>
          <strong>{latestProbability ? `${latestProbability.projected}%` : '—'}</strong>
          <small>{latestProbability ? `現在の推定 ${latestProbability.low}–${latestProbability.high}%` : '記録を確認中'}</small>
        </div>
      </section>

      {loadError && <p className="load-message" role="alert">記録を読み込めませんでした。再読み込みしてください。過去の仮データは表示していません。</p>}

      <div className="main-grid">
        <section className="calendar-card card">
          <div className="section-head">
            <div>
              <p className="eyebrow">CALENDAR</p>
              <h3>{year}年{monthNumber}月</h3>
            </div>
            <div className="calendar-tools">
              <div className="legend">
                <span className="legend-item"><span className="legend-dot dot-record" /> 学習記録</span>
                <span className="legend-item"><span className="legend-dot dot-mock" /> 実戦模試</span>
                <span className="legend-item"><span className="legend-dot dot-exam" /> 12/6 本試験</span>
              </div>
              <div className="calendar-nav">
                <button type="button" onClick={() => moveMonth(-1)} aria-label="前の月を表示">‹ 前月</button>
                <button type="button" onClick={() => moveMonth(1)} aria-label="次の月を表示">次月 ›</button>
              </div>
            </div>
          </div>
          <div className="weekdays">{['日','月','火','水','木','金','土'].map(d => <span key={d}>{d}</span>)}</div>
          <div className="calendar-grid">{cells.map((day, i) => {
            if (!day) return <span key={`empty-${i}`} className="empty-cell" />;
            const date = `${month}-${String(day).padStart(2, '0')}`;
            const special = SPECIAL_DATES[date];
            const isSelected = selectedDate === date;
            const isRecorded = recorded.has(date);
            const isToday = date === getSeoulDate();

            const classNames = [
              isSelected ? 'selected' : '',
              isRecorded ? 'recorded' : '',
              isToday ? 'today' : '',
              special ? `special-day ${special.type}` : '',
            ].filter(Boolean).join(' ');

            return (
              <button
                key={date}
                type="button"
                className={classNames}
                onClick={() => setSelectedDate(date)}
                aria-label={special ? `${dateLabel(date)}: ${special.title}` : dateLabel(date)}
                aria-pressed={isSelected}
              >
                {special && <span className={`cell-tag ${special.type}`}>{special.badge}</span>}
                <span className="cell-day-num">{day}</span>
                {isRecorded && <i />}
              </button>
            );
          })}</div>

          <div className="exam-milestones">
            <div className="milestones-header">
              <span className="eyebrow accent">EXAM ROADMAP</span>
              <h4>実戦模試・本試験マイルストーン</h4>
            </div>
            <div className="milestones-grid">
              <button
                type="button"
                className={`milestone-item is-completed ${selectedDate === '2026-09-20' ? 'active' : ''}`}
                onClick={() => { setSelectedDate('2026-09-20'); setVisibleMonth('2026-09'); }}
              >
                <div className="ms-badge done">完了</div>
                <div className="ms-date">9/20 (日)</div>
                <div className="ms-info">
                  <strong>第1回 N2 実戦模試</strong>
                  <p>119 / 180点 (公式第2集 71/107問 · 66.4%)</p>
                </div>
              </button>
              <button
                type="button"
                className={`milestone-item is-completed ${selectedDate === '2026-09-30' ? 'active' : ''}`}
                onClick={() => { setSelectedDate('2026-09-30'); setVisibleMonth('2026-09'); }}
              >
                <div className="ms-badge done">完了</div>
                <div className="ms-date">9/30 (水)</div>
                <div className="ms-info">
                  <strong>第2回 N2 実戦模試 (合格)</strong>
                  <p>92 / 180点 (2023.12 51/102問 · 50.0%)</p>
                </div>
              </button>
              <button
                type="button"
                className={`milestone-item is-upcoming ${selectedDate === '2026-10-18' ? 'active' : ''}`}
                onClick={() => { setSelectedDate('2026-10-18'); setVisibleMonth('2026-10'); }}
              >
                <div className="ms-badge upcoming">D-{Math.max(0, getDaysDiff('2026-10-18'))}</div>
                <div className="ms-date">10/18 (日)</div>
                <div className="ms-info">
                  <strong>第3回 N2 実戦模試 (2023.07)</strong>
                  <p>104問 全領域実戦 · 単語/文法成果検証 (目標 105点+)</p>
                </div>
              </button>
              <button
                type="button"
                className={`milestone-item is-upcoming ${selectedDate === '2026-11-01' ? 'active' : ''}`}
                onClick={() => { setSelectedDate('2026-11-01'); setVisibleMonth('2026-11'); }}
              >
                <div className="ms-badge upcoming">D-{Math.max(0, getDaysDiff('2026-11-01'))}</div>
                <div className="ms-date">11/1 (日)</div>
                <div className="ms-info">
                  <strong>第4回 N2 実戦模試 (2022.12)</strong>
                  <p>104問 全領域実戦 · 難関文法/聴解即時応答点検</p>
                </div>
              </button>
              <button
                type="button"
                className={`milestone-item is-upcoming ${selectedDate === '2026-11-15' ? 'active' : ''}`}
                onClick={() => { setSelectedDate('2026-11-15'); setVisibleMonth('2026-11'); }}
              >
                <div className="ms-badge upcoming">D-{Math.max(0, getDaysDiff('2026-11-15'))}</div>
                <div className="ms-date">11/15 (日)</div>
                <div className="ms-info">
                  <strong>第5回 N2 実戦模試 (2022.07)</strong>
                  <p>104問 全領域実戦 · 110点防衛線確立 (目標 115点+)</p>
                </div>
              </button>
              <button
                type="button"
                className={`milestone-item is-upcoming ${selectedDate === '2026-11-29' ? 'active' : ''}`}
                onClick={() => { setSelectedDate('2026-11-29'); setVisibleMonth('2026-11'); }}
              >
                <div className="ms-badge upcoming">D-{Math.max(0, getDaysDiff('2026-11-29'))}</div>
                <div className="ms-date">11/29 (日)</div>
                <div className="ms-info">
                  <strong>第6回 ファイナルリハーサル</strong>
                  <p>本番1週間前 · 時間配分＆実戦メンタル最終点検</p>
                </div>
              </button>
              <button
                type="button"
                className={`milestone-item is-target ${selectedDate === '2026-12-06' ? 'active' : ''}`}
                onClick={() => { setSelectedDate('2026-12-06'); setVisibleMonth('2026-12'); }}
              >
                <div className="ms-badge target">🎯 本番 · D-{daysLeft}</div>
                <div className="ms-date">12/6 (日)</div>
                <div className="ms-info">
                  <strong>2026 JLPT N2 本試験</strong>
                  <p>最優先目標: 110点以上合格達成！</p>
                </div>
              </button>
            </div>
          </div>
        </section>

        <aside className="day-card card">
          <div className="section-head">
            <div>
              <p className="eyebrow">SELECTED DAY</p>
              <h3>{dateLabel(selectedDate)}</h3>
            </div>
            <div className="day-header-badges">
              {selectedSpecial && <span className={`special-day-badge ${selectedSpecial.type}`}>{selectedSpecial.badge}</span>}
              {selected && <span className="done-badge">記録あり</span>}
            </div>
          </div>

          {selectedSpecial && (
            <div className={`special-callout ${selectedSpecial.type}`}>
              <div className="callout-header">
                <span className="callout-icon">{selectedSpecial.type === 'upcoming-mock' ? '🔥' : selectedSpecial.type === 'official-exam' ? '🎯' : '📝'}</span>
                <div>
                  <strong>{selectedSpecial.title}</strong>
                  <p>{selectedSpecial.desc}</p>
                </div>
              </div>
              {selectedSpecial.type === 'completed-mock' && (
                <div className="callout-meta">
                  <span className="meta-highlight">
                    {selectedDate === '2026-09-30'
                      ? '実戦換算得点: 92 / 180点 (合格基準90点突破！全領域足切り0件)'
                      : '実戦換算得点: 119 / 180点 (合格基準90点 & 目標110点突破！)'}
                  </span>
                  <span className="meta-sub">
                    {selectedDate === '2026-09-30'
                      ? '正答 51/102問 (50.0%) · 所要時間 146分28秒 (言語知識 29点 · 読解 37点 · 聴解 26点)'
                      : '正答 71/107問 (66.4%) · 所要時間 115分36秒 (読解 76.2% · 聴解 75.0% 全領域過落なし)'}
                  </span>
                  <div style={{ marginTop: '10px' }}>
                    <a
                      href={selectedDate === '2026-09-30' ? "/exams/n2-past-exam-202312-mock.html" : "/exams/n2-midterm-mock-exam-20260920.html"}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mock-exam-link-btn"
                    >
                      {selectedDate === '2026-09-30' ? "📘 第2回 模試問題・解説 (102問) を開く ➔" : "📘 第1回 模試問題・解説 (107問) を開く ➔"}
                    </a>
                  </div>
                </div>
              )}
              {selectedSpecial.type === 'upcoming-mock' && (
                <div className="callout-meta">
                  <span className="meta-highlight">
                    {getDaysDiff(selectedDate) === 0
                      ? '🔥 本日 実施予定 (今夜！)'
                      : `実施予定 (D-${Math.max(0, getDaysDiff(selectedDate))})`}
                  </span>
                  <span className="meta-sub">
                    {selectedSpecial.subDesc || selectedSpecial.desc}
                  </span>
                  {selectedSpecial.linkUrl && (
                    <div style={{ marginTop: '10px' }}>
                      <a
                        href={selectedSpecial.linkUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="mock-exam-link-btn emerald"
                      >
                        {selectedSpecial.linkText || '🎯 実戦模試の詳細・問題を開く ➔'}
                      </a>
                    </div>
                  )}
                </div>
              )}
              {selectedSpecial.type === 'official-exam' && (
                <div className="callout-meta">
                  <span className="meta-highlight">2026年 12月 6日 (日) 本番 (D-{daysLeft})</span>
                  <span className="meta-sub">合格基準: 90点以上 & 各領域 19点以上 / 目標: 110点以上</span>
                </div>
              )}
            </div>
          )}

          {selected ? <>
            <div className="metric-grid">
              <div><span>記録済み学習時間</span><strong>{formatStudy(selected.studyMinutes)}</strong><small>未計測の活動あり</small></div>
              <div><span>当日のテスト合計</span><strong>{selected.tests.correct} / {selected.tests.total}</strong><small>{selected.tests.count}回・{selected.tests.total ? `正答率${Math.round(selected.tests.correct/selected.tests.total*100)}%` : '未実施'}</small></div>
              <div><span>テスト所要時間</span><strong>{formatClock(selected.tests.elapsedSeconds)}</strong><small>{selected.tests.untimedTests ? `未計測 ${selected.tests.untimedTests}回を除く` : '記録済みテストの合計'}</small></div>
              <div><span>誤答 / 不明 / 未回答</span><strong>{selected.tests.wrong} / {selected.tests.unknown} / {selected.tests.unanswered ?? '—'}</strong><small>それぞれ別に集計</small></div>
            </div>
            <div className="pass-box">{(() => {
              const p = selected.probabilities?.N2;
              return <div><span>N2合格可能性・参考</span><strong>{p ? `${p.low}–${p.high}%` : '未評価'}</strong><small>{p ? `12月予測 ${p.projected}%` : 'この日の評価なし'}</small></div>;
            })()}</div>
            <div className="mini-bars"><h4>分野別の参考評価・当日正答率ではありません</h4>{orderedDomains(selected.domains ?? []).map(domain => <div key={domain.key} className="bar-row"><span>{domain.label}</span><div><i style={{width: domain.low !== null && domain.high !== null ? `${(domain.low+domain.high)/2}%` : '0%'}} /></div><strong>{domain.grade ?? '—'}</strong></div>)}</div>
          </> : <div className="empty-state" role="status"><span>○</span><strong>{loading ? '記録を読み込み中' : loadError ? '読み込みエラー' : 'まだ記録がありません'}</strong><p>{loading ? '最新の学習記録を確認しています。' : '記録が追加されると、この日に表示されます。'}</p></div>}
        </aside>
      </div>

      {selected?.anki && 'cardsRemaining' in selected.anki && <section className="anki-card card">
        <div className="section-head"><div><p className="eyebrow">ANKI · TODAY</p><h3>Anki 当日学習記録</h3></div><span className="scope-badge">{selected.anki.scopeLabel}</span></div>
        <p className="data-note">Ankiの学習日境界（韓国時間4時）を基準にした実測値です。</p>
        <div className="anki-primary">
          <div><span>今日の回答</span><strong>{numberLabel(selected.anki.answeredCards)}</strong><small>{selected.anki.studyMinutes.toFixed(2)}分 · 1回答{selected.anki.secondsPerCard.toFixed(2)}秒</small></div>
          <div><span>「もう一度」</span><strong>{numberLabel(selected.anki.againCount)}</strong><small>{selected.anki.againPct.toFixed(2)}%</small></div>
          <div><span>学習 / 復習</span><strong>{numberLabel(selected.anki.learningReviews)} / {numberLabel(selected.anki.reviewsDone)}</strong><small>当日の回答種別</small></div>
          <div><span>残り</span><strong>{numberLabel(selected.anki.cardsRemaining.learning)}</strong><small>新規 {numberLabel(selected.anki.cardsRemaining.new)} · 復習 {numberLabel(selected.anki.cardsRemaining.review)}</small></div>
        </div>
      </section>}

      {selected?.anki && 'forecast' in selected.anki && <section className="anki-card card">
        <div className="section-head"><div><p className="eyebrow">ANKI · CURRENT DECK</p><h3>Anki 現在デッキ統計</h3></div><span className="scope-badge">{selected.anki.scope}</span></div>
        <p className="data-note">選択日のAnki統計PDF。現在デッキの範囲で、全デッキ統計とは合算していません。</p>
        <div className="anki-primary">
          <div><span>今日の回答</span><strong>{numberLabel(selected.anki.answeredCards)}</strong><small>{selected.anki.studyMinutes.toFixed(2)}分 · 1枚{selected.anki.secondsPerCard.toFixed(2)}秒</small></div>
          <div><span>「もう一度」</span><strong>{numberLabel(selected.anki.againCount)}</strong><small>{selected.anki.againPct.toFixed(2)}%</small></div>
          <div><span>明日の期限</span><strong>{numberLabel(selected.anki.forecast.tomorrowDue)}</strong><small>Daily load {numberLabel(selected.anki.forecast.dailyLoad)}枚/日</small></div>
          <div><span>今日の保持率</span><strong>{selected.anki.retention.today.pct.toFixed(1)}%</strong><small>{numberLabel(selected.anki.retention.today.count)}枚 · 若いカード</small></div>
        </div>
        <div className="anki-secondary">
          <div className="deck-composition"><div className="composition-head"><span>カード構成</span><strong>{numberLabel(selected.anki.cards.total)}枚</strong></div><div className="composition-bar" aria-label={`新規${selected.anki.cards.newPct}%、若いカード${selected.anki.cards.youngPct}%`}><i style={{width:`${selected.anki.cards.newPct}%`}} /><b style={{width:`${selected.anki.cards.youngPct}%`}} /></div><p>新規 {numberLabel(selected.anki.cards.new)}枚 ({selected.anki.cards.newPct}%) · 若いカード {numberLabel(selected.anki.cards.young)}枚 ({selected.anki.cards.youngPct}%) · 成熟 {numberLabel(selected.anki.cards.mature)}枚</p></div>
          <div className="anki-facts"><div><span>1か月予測</span><strong>{numberLabel(selected.anki.forecast.totalReviews)}回</strong></div><div><span>中央値間隔</span><strong>{selected.anki.medianIntervalDays}日</strong></div><div><span>中央値 ease</span><strong>{selected.anki.medianEasePct}%</strong></div><div><span>直近1週の保持率</span><strong>{selected.anki.retention.lastWeek.pct}%</strong><small>{selected.anki.retention.lastWeek.count}枚</small></div></div>
        </div>
      </section>}

      {selected && <>
        <section className="detail-card card">
          <div className="section-head"><div><p className="eyebrow">TYPE ANALYSIS</p><h3>問題形式別の学習記録</h3></div><span className="muted">語彙 → 文法 → 読解 → 聴解</span></div>
          <p className="data-note">当日：{dateLabel(selectedDate)}の結果 ／ 累積：{dateLabel(selectedDate)}まで。未実施は0点ではありません。</p>
          {!isV2 && <p className="data-note" role="status">旧形式の記録です。再集計が完了すると当日・累積を表示します。</p>}
          <div className="table-wrap"><table><thead><tr><th>分野 / 問題形式</th><th>当日正答</th><th>不明 / 未回答</th><th>当日平均時間</th><th>累積正答</th><th>参考評価</th></tr></thead><tbody>{types.map(row => <tr key={row.key}>
            <td><small className="cell-note">{domainLabel(row.domain)}</small>{row.label}</td>
            <td>{isV2 ? formatAccuracy(row) : '再集計待ち'}</td>
            <td>{isV2 && row.total ? `${row.unknown ?? 0} / ${row.unanswered ?? 0}` : '—'}</td>
            <td>{isV2 && row.averageSeconds !== null ? <>{row.averageSeconds}秒<small className="cell-note">{row.timingBasis === 'audio_end_to_answer' ? '音声終了後の選択' : '問題全体'}・{row.timedItems}問</small></> : '—'}</td>
            <td>{isV2 ? formatAccuracy(row.cumulative) : '再集計待ち'}</td>
            <td>{row.grade ?? '未評価'}<small className="cell-note">当日点数とは別</small></td>
          </tr>)}</tbody></table></div>
          <p className="data-note">聴解は音声終了後の選択時間、その他は問題全体の時間です。未計測・計時不具合は平均から除外。聴解の0秒は丸められたイベント時刻で、理解速度を意味しません。</p>
          {!!selected.tests.unclassifiedItems && <p className="data-note">{selected.tests.unclassifiedItems}問は合計点のみ記録されています。形式別の表には含めないため、表の合計と当日合計は一致しません。</p>}
          {!!selected.tests.excludedItems && <p className="data-note">音声エラー {selected.tests.excludedItems}問は形式別の正答率・時間から除外。テスト合計には提出時の記録を保持しています。</p>}
          <details className="test-details"><summary>当日のテスト内訳・出典</summary><div className="table-wrap"><table><thead><tr><th>テスト</th><th>出典</th><th>正答</th><th>時間</th></tr></thead><tbody>{selected.testDetails?.map(test => <tr key={test.id}><td>{test.title}</td><td>{sourceLabel(test.sourceClass)}</td><td>{test.correct}/{test.total}</td><td>{formatClock(test.elapsedSeconds)}</td></tr>)}</tbody></table></div></details>
        </section>

        <section className="bottom-grid">
          <div className="card next-card"><p className="eyebrow">REVIEW PLAN</p><h3>{selected.nextReview ? `${dateLabel(selected.nextReview.date)}の復習予定` : '次回の復習予定'}</h3><p className="data-note">選択日までの問題から登録された予定です。現在の未完了件数ではありません。</p><ol><li><b>01</b><span>登録された復習 {selected.nextReview?.count ?? 0}問<small>誤答と「不明」を優先</small></span></li><li><b>02</b><span>重点弱点の選択式確認<small>少数問題の結果は方向の目安</small></span></li><li><b>03</b><span>通常講義とAnki<small>期限を迎えた復習を優先</small></span></li></ol></div>
          <div className="card insight-card"><p className="eyebrow">SELECTED DAY RESULTS</p><h3>当日の結果から見える傾向</h3><div><span>当日80%以上の形式</span><p>{isV2 ? selected.strengths?.join('・') || '該当なし' : '再集計待ち'}</p></div><div><span>当日80%未満の形式</span><p>{isV2 ? selected.weaknesses?.join('・') || '該当なし' : '再集計待ち'}</p></div><div><span>データの読み方</span><p>{isV2 ? selected.confidenceNote : '集計方法の更新待ちです。'}</p></div></div>
        </section>
      </>}
      <footer>自作テストは公式模擬試験と区別して記録しています。最新記録日: {latest?.date ?? '—'}</footer>
    </main>
  );
}
