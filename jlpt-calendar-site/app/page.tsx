'use client';

import { useEffect, useMemo, useState } from 'react';
import { type DailyReport, domainLabel, formatAccuracy, formatClock, formatStudy, orderedDomains, orderedTypes, sourceLabel } from '../lib/reports';

const getSeoulDate = () => new Intl.DateTimeFormat('sv-SE', { timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
const examDaysLeft = () => Math.max(0, Math.ceil((Date.parse('2026-12-06T00:00:00+09:00') - Date.parse(getSeoulDate() + 'T00:00:00+09:00')) / 86400000));
const dateLabel = (date: string) => {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(date);
  return match ? `${Number(match[2])}月${Number(match[3])}日` : '날짜 없음';
};
const numberLabel = (value: number) => new Intl.NumberFormat('ja-JP').format(value);

export default function Home() {
  const [reports, setReports] = useState<DailyReport[]>([]);
  const [selectedDate, setSelectedDate] = useState(getSeoulDate);
  const [visibleMonth, setVisibleMonth] = useState(() => getSeoulDate().slice(0, 7));
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [daysLeft, setDaysLeft] = useState(examDaysLeft);
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
          .sort((a: DailyReport,b: DailyReport) => a.date.localeCompare(b.date));
        if (!mounted) return;
        setDaysLeft(examDaysLeft());
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
  const month = visibleMonth;
  const [year, monthNumber] = month.split('-').map(Number);
  const moveMonth = (offset: number) => {
    const next = new Date(Date.UTC(year, monthNumber - 1 + offset, 1));
    setVisibleMonth(`${next.getUTCFullYear()}-${String(next.getUTCMonth() + 1).padStart(2, '0')}`);
  };
  const cells = useMemo(() => {
    const first = new Date(Date.UTC(year, monthNumber-1, 1)).getUTCDay();
    const length = new Date(Date.UTC(year, monthNumber, 0)).getUTCDate();
    return [...Array(first).fill(null), ...Array.from({length}, (_,i) => i+1)] as (number | null)[];
  }, [year, monthNumber]);
  const recorded = new Set(reports.map(r => r.date));
  const isV2 = selected?.schemaVersion === 2;
  const latestProbability = latest?.probabilities?.N2;
  const types = selected ? orderedTypes(selected.types ?? []) : [];

  return (
    <main className="site-shell">
      <header className="topbar"><div><p className="eyebrow">JLPT N2 PLAN</p><h1>学習カレンダー</h1></div><div className="topbar-actions"><a className="game-button" href="https://slay-the-jlpt.pages.dev/" target="_blank" rel="noopener noreferrer" aria-label="N2単語ゲームを新しいタブで開く"><span aria-hidden="true">🎮</span> N2単語ゲーム <span aria-hidden="true">↗</span></a><div className="exam-chip"><span /> 試験まで{daysLeft}日</div></div></header>
      <section className="hero">
        <div><p className="eyebrow accent">LIVE STUDY LOG</p><h2>今日の学びを<br />合格可能性へ</h2><p>日々の結果と、その日までの記録を分けて確認できます。</p></div>
        <div className="hero-score"><span>N2 12月予測・最新記録</span><strong>{latestProbability ? `${latestProbability.projected}%` : '—'}</strong><small>{latestProbability ? `現在の推定 ${latestProbability.low}–${latestProbability.high}%` : '記録を確認中'}</small></div>
      </section>
      {loadError && <p className="load-message" role="alert">記録を読み込めませんでした。再読み込みしてください。過去の仮データは表示していません。</p>}
      <div className="main-grid">
        <section className="calendar-card card">
          <div className="section-head"><div><p className="eyebrow">CALENDAR</p><h3>{year}年{monthNumber}月</h3></div><div className="calendar-tools"><div className="legend"><span /> 学習記録あり</div><div className="calendar-nav"><button type="button" onClick={() => moveMonth(-1)} aria-label="前の月を表示">‹ 前月</button><button type="button" onClick={() => moveMonth(1)} aria-label="次の月を表示">次月 ›</button></div></div></div>
          <div className="weekdays">{['日','月','火','水','木','金','土'].map(d => <span key={d}>{d}</span>)}</div>
          <div className="calendar-grid">{cells.map((day,i) => {
            const date = day ? `${month}-${String(day).padStart(2,'0')}` : '';
            return day ? <button key={date} className={`${selectedDate === date ? 'selected' : ''} ${recorded.has(date) ? 'recorded' : ''}`} onClick={() => setSelectedDate(date)} aria-label={dateLabel(date)} aria-pressed={selectedDate === date}><span>{day}</span>{recorded.has(date) && <i />}</button> : <span key={`empty-${i}`} />;
          })}</div>
          <div className="calendar-note"><span>初回N2模擬試験</span><strong>9月20日</strong><p>『JLPT 한권으로 끝내기 N2』の未使用練習模試を実施</p></div>
        </section>
        <aside className="day-card card">
          <div className="section-head"><div><p className="eyebrow">SELECTED DAY</p><h3>{dateLabel(selectedDate)}</h3></div>{selected && <span className="done-badge">記録あり</span>}</div>
          {selected ? <>
            <div className="metric-grid">
              <div><span>記録済み学習時間</span><strong>{formatStudy(selected.studyMinutes)}</strong><small>未計測の活動あり</small></div>
              <div><span>当日のテスト合計</span><strong>{selected.tests.correct} / {selected.tests.total}</strong><small>{selected.tests.count}回・{selected.tests.total ? `正答率${Math.round(selected.tests.correct/selected.tests.total*100)}%` : '未実施'}</small></div>
              <div><span>テスト所要時間</span><strong>{formatClock(selected.tests.elapsedSeconds)}</strong><small>{selected.tests.untimedTests ? `未計測 ${selected.tests.untimedTests}回を除く` : '記録済みテストの合計'}</small></div>
              <div><span>誤答 / 不明 / 未回答</span><strong>{selected.tests.wrong} / {selected.tests.unknown} / {selected.tests.unanswered ?? '—'}</strong><small>それぞれ別に集計</small></div>
            </div>
            <div className="pass-box">{(['N3','N2'] as const).map(level => {const p=selected.probabilities?.[level];return <div key={level}><span>{level}合格可能性・参考</span><strong>{p ? `${p.low}–${p.high}%` : '未評価'}</strong><small>{p ? `12月予測 ${p.projected}%` : 'この日の評価なし'}</small></div>;})}</div>
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

