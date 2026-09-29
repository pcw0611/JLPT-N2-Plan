'use client';

import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import Link from 'next/link';
import { SONGS, type Song, type SongLine } from './songs';

interface UserRecord {
  bestCpm: number;
  bestAccuracy: number;
  playCount: number;
}

interface UserStats {
  records: Record<string, UserRecord>;
  totalPlays: number;
  totalKeystrokes: number;
  totalTimeSeconds: number;
}

export default function MygoTypingPage() {
  const [selectedSongId, setSelectedSongId] = useState<string>(SONGS[0].id);
  const [categoryFilter, setCategoryFilter] = useState<'all' | 'original' | 'cover'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Feature: Toggle Korean Lyrics Translation
  const [showKorean, setShowKorean] = useState<boolean>(true);

  // Typing Game State
  const [currentLineIndex, setCurrentLineIndex] = useState(0);
  const [currentCharIndex, setCurrentCharIndex] = useState(0);
  const [typedHistory, setTypedHistory] = useState<string>('');
  const [missCount, setMissCount] = useState(0);
  const [totalKeystrokes, setTotalKeystrokes] = useState(0);
  const [correctKeystrokes, setCorrectKeystrokes] = useState(0);
  const [isShaking, setIsShaking] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);

  // Slide Animation State: Outgoing line for smooth slide-up exit
  const [outgoingLine, setOutgoingLine] = useState<SongLine | null>(null);

  // Time & Speed Tracking
  const [isPlaying, setIsPlaying] = useState(false);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [currentCpm, setCurrentCpm] = useState(0);
  const [peakCpm, setPeakCpm] = useState(0);
  const startTimeRef = useRef<number | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // Local Storage Stats
  const [userStats, setUserStats] = useState<UserStats>({
    records: {},
    totalPlays: 0,
    totalKeystrokes: 0,
    totalTimeSeconds: 0,
  });

  const song = useMemo(() => SONGS.find(s => s.id === selectedSongId) || SONGS[0], [selectedSongId]);

  // Load stats & preferences from localStorage
  useEffect(() => {
    try {
      const savedStats = localStorage.getItem('mygo_typing_stats');
      if (savedStats) {
        setUserStats(JSON.parse(savedStats));
      }
      const savedShowKo = localStorage.getItem('mygo_typing_show_ko');
      if (savedShowKo !== null) {
        setShowKorean(savedShowKo === 'true');
      }
    } catch {
      // ignore
    }
  }, []);

  // Save Korean lyrics toggle preference
  const toggleKorean = useCallback(() => {
    setShowKorean(prev => {
      const next = !prev;
      try {
        localStorage.setItem('mygo_typing_show_ko', String(next));
      } catch {
        // ignore
      }
      return next;
    });
  }, []);

  // Save stats to localStorage
  const saveStats = useCallback((songId: string, finalCpm: number, accuracy: number, timeSec: number, keys: number) => {
    setUserStats(prev => {
      const prevRecord = prev.records[songId] || { bestCpm: 0, bestAccuracy: 0, playCount: 0 };
      const updatedRecords = {
        ...prev.records,
        [songId]: {
          bestCpm: Math.max(prevRecord.bestCpm, finalCpm),
          bestAccuracy: Math.max(prevRecord.bestAccuracy, accuracy),
          playCount: prevRecord.playCount + 1,
        }
      };
      const updated: UserStats = {
        records: updatedRecords,
        totalPlays: prev.totalPlays + 1,
        totalKeystrokes: prev.totalKeystrokes + keys,
        totalTimeSeconds: prev.totalTimeSeconds + timeSec,
      };
      try {
        localStorage.setItem('mygo_typing_stats', JSON.stringify(updated));
      } catch {
        // ignore
      }
      return updated;
    });
  }, []);

  // Reset / Change Song
  const resetGame = useCallback((targetSongId?: string) => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (targetSongId) setSelectedSongId(targetSongId);
    setCurrentLineIndex(0);
    setCurrentCharIndex(0);
    setOutgoingLine(null);
    setTypedHistory('');
    setMissCount(0);
    setTotalKeystrokes(0);
    setCorrectKeystrokes(0);
    setIsPlaying(false);
    setIsCompleted(false);
    setElapsedSeconds(0);
    setCurrentCpm(0);
    setPeakCpm(0);
    startTimeRef.current = null;
  }, []);

  // Timer Effect
  useEffect(() => {
    if (isPlaying && !isCompleted) {
      timerRef.current = setInterval(() => {
        if (!startTimeRef.current) return;
        const now = Date.now();
        const sec = Math.max(1, Math.floor((now - startTimeRef.current) / 1000));
        setElapsedSeconds(sec);

        // Real-time CPM calculation
        const cpm = Math.round((correctKeystrokes / sec) * 60);
        setCurrentCpm(cpm);
        setPeakCpm(prev => Math.max(prev, cpm));
      }, 500);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, isCompleted, correctKeystrokes]);

  // Active Line & Romaji
  const currentLine: SongLine | undefined = song.lines[currentLineIndex];
  const targetRomaji = useMemo(() => {
    if (!currentLine) return '';
    return currentLine.romaji.toLowerCase();
  }, [currentLine]);

  // Key Event Listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (isCompleted) return;
      if (e.ctrlKey || e.altKey || e.metaKey) return;
      if (e.key === 'Tab') return;

      // Handle Backspace
      if (e.key === 'Backspace') {
        e.preventDefault();
        if (currentCharIndex > 0) {
          setCurrentCharIndex(prev => prev - 1);
          setTypedHistory(prev => prev.slice(0, -1));
        }
        return;
      }

      // Ignore special non-printable keys
      if (e.key.length > 1) return;

      e.preventDefault();
      const pressedChar = e.key.toLowerCase();

      // Start timer on first keypress
      if (!isPlaying) {
        setIsPlaying(true);
        startTimeRef.current = Date.now();
      }

      if (!targetRomaji) return;

      const expectedChar = targetRomaji[currentCharIndex];

      // Check if match
      if (pressedChar === expectedChar) {
        // Correct Keypress
        const nextIndex = currentCharIndex + 1;
        setCorrectKeystrokes(prev => prev + 1);
        setTotalKeystrokes(prev => prev + 1);
        setTypedHistory(prev => prev + pressedChar);
        setCurrentCharIndex(nextIndex);

        // Check if line finished
        if (nextIndex >= targetRomaji.length) {
          if (currentLineIndex + 1 < song.lines.length) {
            // Trigger smooth slide-up transition
            setOutgoingLine(currentLine);
            setTimeout(() => {
              setOutgoingLine(null);
            }, 260);

            setCurrentLineIndex(prev => prev + 1);
            setCurrentCharIndex(0);
            setTypedHistory('');
          } else {
            // Completed Song!
            const now = Date.now();
            const timeSec = startTimeRef.current ? Math.max(1, Math.round((now - startTimeRef.current) / 1000)) : 1;
            const finalCorrect = correctKeystrokes + 1;
            const finalTotal = totalKeystrokes + 1;
            const finalCpm = Math.round((finalCorrect / timeSec) * 60);
            const accuracy = Math.round((finalCorrect / finalTotal) * 100);

            setIsPlaying(false);
            setIsCompleted(true);
            saveStats(song.id, finalCpm, accuracy, timeSec, finalTotal);
          }
        }
      } else {
        // Miss / Typo
        setMissCount(prev => prev + 1);
        setTotalKeystrokes(prev => prev + 1);
        setIsShaking(true);
        setTimeout(() => setIsShaking(false), 200);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [
    isCompleted,
    isPlaying,
    currentCharIndex,
    currentLineIndex,
    targetRomaji,
    song,
    currentLine,
    correctKeystrokes,
    totalKeystrokes,
    saveStats,
  ]);

  // Metrics
  const accuracy = totalKeystrokes > 0
    ? Math.round((correctKeystrokes / totalKeystrokes) * 100)
    : 100;

  const progressPct = song.lines.length > 0
    ? Math.round(((currentLineIndex + (currentCharIndex / (targetRomaji.length || 1))) / song.lines.length) * 100)
    : 0;

  const careerAvgCpm = useMemo(() => {
    if (userStats.totalTimeSeconds <= 0) return 0;
    return Math.round((userStats.totalKeystrokes / userStats.totalTimeSeconds) * 60);
  }, [userStats]);

  // Precise Per-Character Glow Sync Mapping
  const jaCharRanges = useMemo(() => {
    if (!currentLine) return [];
    const chars = currentLine.ja.split('');
    const ranges: { char: string; start: number; end: number }[] = [];
    let offset = 0;

    if (currentLine.charRomaji && currentLine.charRomaji.length === chars.length) {
      for (let i = 0; i < chars.length; i++) {
        const ro = currentLine.charRomaji[i];
        const start = offset;
        const end = offset + ro.length;
        ranges.push({ char: chars[i], start, end });
        offset = end;
      }
    } else {
      // Proportional fallback
      const totalLen = targetRomaji.length || 1;
      for (let i = 0; i < chars.length; i++) {
        const start = Math.floor((i / chars.length) * totalLen);
        const end = Math.floor(((i + 1) / chars.length) * totalLen);
        ranges.push({ char: chars[i], start, end });
      }
    }
    return ranges;
  }, [currentLine, targetRomaji]);

  // Filtered Song List (Only All, Original, Cover)
  const filteredSongs = useMemo(() => {
    return SONGS.filter(s => {
      if (categoryFilter === 'original' && s.category !== 'original') return false;
      if (categoryFilter === 'cover' && s.category !== 'cover') return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        return s.title.toLowerCase().includes(q) || s.reading.toLowerCase().includes(q) || s.album.toLowerCase().includes(q);
      }
      return true;
    });
  }, [categoryFilter, searchQuery]);

  // Grade calculation
  const getRank = (cpm: number, acc: number) => {
    if (acc < 80) return { rank: 'C', label: '見習い (Novice)', color: '#94a3b8' };
    if (cpm >= 380) return { rank: 'S', label: '迷子の神域 (Master)', color: '#38bdf8' };
    if (cpm >= 280) return { rank: 'A', label: '達人 (Expert)', color: '#34d399' };
    if (cpm >= 180) return { rank: 'B', label: '快速 (Advanced)', color: '#fbbf24' };
    return { rank: 'C', label: '標準 (Standard)', color: '#cbd5e1' };
  };

  const currentRank = getRank(currentCpm, accuracy);

  return (
    <div className="typing-page-container">
      {/* Top Navigation */}
      <header className="typing-topbar">
        <div className="typing-nav-left">
          <Link href="/" className="typing-back-btn">
            ← 学習カレンダー
          </Link>
          <div className="typing-title-group">
            <span className="typing-badge">MyGO!!!!! 歌詞タイピング</span>
            <h1 className="typing-title">{song.title} <small>({song.reading})</small></h1>
          </div>
        </div>

        {/* Korean Translation Toggle Switch */}
        <div className="typing-toggle-wrapper">
          <label className="korean-toggle-label">
            <input
              type="checkbox"
              checked={showKorean}
              onChange={toggleKorean}
              className="korean-toggle-checkbox"
            />
            <span className="korean-toggle-switch"></span>
            <span className="korean-toggle-text">한국어 가사 번역</span>
          </label>
        </div>
      </header>

      {/* Main Layout Grid */}
      <div className="typing-layout-grid">
        {/* Left Column: Player & Game Arena */}
        <section className="typing-arena-column">
          {/* Dashboard HUD */}
          <div className="typing-hud">
            <div className="hud-card cpm-card">
              <span className="hud-label">リアルタイム打鍵速度</span>
              <div className="hud-value-row">
                <span className="hud-number">{currentCpm}</span>
                <span className="hud-unit">CPM</span>
              </div>
              <span className="hud-sub">最高: {peakCpm} CPM</span>
            </div>

            <div className="hud-card acc-card">
              <span className="hud-label">正確率 (Accuracy)</span>
              <div className="hud-value-row">
                <span className="hud-number">{accuracy}%</span>
              </div>
              <span className="hud-sub">ミス: {missCount}回</span>
            </div>

            <div className="hud-card time-card">
              <span className="hud-label">経過時間</span>
              <div className="hud-value-row">
                <span className="hud-number">
                  {Math.floor(elapsedSeconds / 60)}:{(elapsedSeconds % 60).toString().padStart(2, '0')}
                </span>
              </div>
              <span className="hud-sub">{isPlaying ? '🔥 演奏中' : '準備完了'}</span>
            </div>

            <div className="hud-card prog-card">
              <span className="hud-label">進行状況</span>
              <div className="hud-value-row">
                <span className="hud-number">{progressPct}%</span>
              </div>
              <div className="progress-bar-bg">
                <div className="progress-bar-fill" style={{ width: `${progressPct}%` }} />
              </div>
            </div>
          </div>

          {/* YouTube MV / Audio Player */}
          {song.youtubeId && (
            <div className="typing-video-wrapper">
              <iframe
                src={`https://www.youtube-nocookie.com/embed/${song.youtubeId}?loop=1&playlist=${song.youtubeId}&enablejsapi=1&rel=0&modestbranding=1`}
                title={`${song.title} - Video (Loop)`}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="typing-youtube-frame"
              />
            </div>
          )}

          {/* Lyrics Typing Display Area with Slide Up Animation */}
          <div className={`typing-display-box ${isShaking ? 'shake-animation' : ''}`}>
            {/* Outgoing Line (Sliding Out Upwards) */}
            {outgoingLine && (
              <div className="typing-line-active slide-out-up">
                <div className="lyrics-ja-container">
                  {outgoingLine.ja.split('').map((char, i) => (
                    <span key={i} className="ja-char completed">{char}</span>
                  ))}
                </div>
                {showKorean && outgoingLine.ko && (
                  <div className="lyrics-ko-text">{outgoingLine.ko}</div>
                )}
                <div className="lyrics-romaji-track">
                  {outgoingLine.romaji.split('').map((char, idx) => (
                    <span key={idx} className="romaji-char completed">{char}</span>
                  ))}
                </div>
              </div>
            )}

            {/* Current Active Line (Sliding In From Bottom) */}
            {currentLine ? (
              <div key={currentLineIndex} className="typing-line-active slide-in-up">
                {/* Japanese Characters with 100% Precise Glow Sync */}
                <div className="lyrics-ja-container">
                  {jaCharRanges.map((r, i) => {
                    let statusClass = 'ja-char pending';
                    if (currentCharIndex >= r.end && r.end > 0) {
                      statusClass = 'ja-char completed';
                    } else if (currentCharIndex >= r.start) {
                      statusClass = 'ja-char current';
                    }

                    return (
                      <span key={i} className={statusClass}>
                        {r.char}
                      </span>
                    );
                  })}
                </div>

                {/* Optional Korean Translation */}
                {showKorean && currentLine.ko && (
                  <div className="lyrics-ko-text">
                    {currentLine.ko}
                  </div>
                )}

                {/* Romaji Letters Track */}
                <div className="lyrics-romaji-track">
                  {targetRomaji.split('').map((char, idx) => {
                    let charStatus = 'pending';
                    if (idx < currentCharIndex) charStatus = 'completed';
                    else if (idx === currentCharIndex) charStatus = 'current';

                    return (
                      <span
                        key={idx}
                        className={`romaji-char ${charStatus}`}
                      >
                        {char === ' ' ? '␣' : char}
                      </span>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="typing-line-active">
                <p className="text-muted">準備完了。キーを押してスタート！</p>
              </div>
            )}
          </div>
        </section>

        {/* Right Column: Song Selector */}
        <aside className="typing-song-sidebar">
          <div className="sidebar-header">
            <h3>曲を選択 ({filteredSongs.length}曲)</h3>
            <input
              type="text"
              placeholder="曲名・よみがな検索..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              className="song-search-input"
            />
          </div>

          {/* Category Tabs: All / Original / Cover */}
          <div className="song-tabs">
            <button
              type="button"
              className={`song-tab ${categoryFilter === 'all' ? 'active' : ''}`}
              onClick={() => setCategoryFilter('all')}
            >
              全曲
            </button>
            <button
              type="button"
              className={`song-tab ${categoryFilter === 'original' ? 'active' : ''}`}
              onClick={() => setCategoryFilter('original')}
            >
              オリジナル
            </button>
            <button
              type="button"
              className={`song-tab ${categoryFilter === 'cover' ? 'active' : ''}`}
              onClick={() => setCategoryFilter('cover')}
            >
              カバー
            </button>
          </div>

          {/* Song Card List */}
          <div className="song-list-scroll">
            {filteredSongs.map(s => {
              const isSelected = s.id === song.id;
              const record = userStats.records[s.id];

              return (
                <div
                  key={s.id}
                  onClick={() => resetGame(s.id)}
                  className={`song-card ${isSelected ? 'selected' : ''}`}
                >
                  <div className="song-card-header">
                    <span className="song-name">{s.title}</span>
                    <span className="category-badge">{s.category === 'original' ? 'オリジナル' : 'カバー'}</span>
                  </div>
                  <div className="song-card-sub">
                    <span className="song-reading">{s.reading}</span>
                    <span className="song-album">{s.album}</span>
                  </div>
                  {record && record.bestCpm > 0 && (
                    <div className="song-card-record">
                      <span>最高: <strong>{record.bestCpm} CPM</strong></span>
                      <span>正答率: {record.bestAccuracy}%</span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </aside>
      </div>

      {/* Completion Result Modal */}
      {isCompleted && (
        <div className="result-modal-backdrop">
          <div className="result-modal-card">
            <div className="modal-header">
              <span className="celebration-badge">🎉 FINISHED!</span>
              <h2>{song.title} 完奏！</h2>
              <p className="song-album-desc">{song.album}</p>
            </div>

            <div className="rank-display" style={{ borderColor: currentRank.color }}>
              <span className="rank-letter" style={{ color: currentRank.color }}>
                {currentRank.rank}
              </span>
              <span className="rank-name">{currentRank.label}</span>
            </div>

            <div className="result-grid">
              <div className="result-stat-box">
                <span className="label">平均打鍵速度</span>
                <strong className="val cyan">{currentCpm} <small>CPM</small></strong>
              </div>
              <div className="result-stat-box">
                <span className="label">最高瞬間速度</span>
                <strong className="val white">{peakCpm} <small>CPM</small></strong>
              </div>
              <div className="result-stat-box">
                <span className="label">正確率 (Accuracy)</span>
                <strong className="val green">{accuracy}%</strong>
              </div>
              <div className="result-stat-box">
                <span className="label">ミス誤打数</span>
                <strong className="val rose">{missCount} <small>回</small></strong>
              </div>
              <div className="result-stat-box">
                <span className="label">所要時間</span>
                <strong className="val amber">
                  {Math.floor(elapsedSeconds / 60)}分{elapsedSeconds % 60}秒
                </strong>
              </div>
              <div className="result-stat-box">
                <span className="label">生涯平均打鍵</span>
                <strong className="val purple">{careerAvgCpm} <small>CPM</small></strong>
              </div>
            </div>

            <div className="modal-actions">
              <button
                type="button"
                className="modal-btn-retry"
                onClick={() => resetGame()}
              >
                もう一度挑戦
              </button>
              <button
                type="button"
                className="modal-btn-next"
                onClick={() => {
                  const currentIndex = SONGS.findIndex(s => s.id === song.id);
                  const nextSong = SONGS[(currentIndex + 1) % SONGS.length];
                  resetGame(nextSong.id);
                }}
              >
                次の曲へ →
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
