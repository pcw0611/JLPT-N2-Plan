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
  const [categoryFilter, setCategoryFilter] = useState<'all' | 'original' | 'cover' | 'mv'>('all');
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
          // Move to next line
          if (currentLineIndex + 1 < song.lines.length) {
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

  // Progress Ratio of Current Line (for syncing Japanese character color)
  const lineProgressRatio = useMemo(() => {
    if (!targetRomaji || targetRomaji.length === 0) return 0;
    return currentCharIndex / targetRomaji.length;
  }, [currentCharIndex, targetRomaji]);

  // Filtered Song List
  const filteredSongs = useMemo(() => {
    return SONGS.filter(s => {
      if (categoryFilter === 'original' && s.category !== 'original') return false;
      if (categoryFilter === 'cover' && s.category !== 'cover') return false;
      if (categoryFilter === 'mv' && !s.youtubeId) return false;
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

        <div className="typing-nav-right">
          {/* Korean Lyrics Toggle Checkbox */}
          <label className="korean-toggle-label" title="韓国語訳の表示・非表示を切り替えます">
            <input
              type="checkbox"
              checked={showKorean}
              onChange={toggleKorean}
              className="korean-toggle-checkbox"
            />
            <span className="toggle-switch-ui" />
            <span className="toggle-text">🇰🇷 韓国語訳 (한글 가사)</span>
          </label>

          <div className="career-stat-chip">
            <span className="label">生涯平均打鍵:</span>
            <strong className="value">{careerAvgCpm > 0 ? `${careerAvgCpm} CPM` : '未記録'}</strong>
          </div>

          <button
            type="button"
            className="typing-restart-btn"
            onClick={() => resetGame()}
            title="リセットして最初から (Esc)"
          >
            🔄 最初から
          </button>
        </div>
      </header>

      {/* Main Layout: Left Typing & Video / Right Song Selector */}
      <div className="typing-layout-grid">
        {/* Left Column: Game Area */}
        <section className="typing-main-column">
          {/* Real-time HUD Dashboard */}
          <div className="typing-hud">
            <div className="hud-metric">
              <span className="hud-label">リアルタイム打鍵数</span>
              <div className="hud-val-group">
                <strong className="hud-value neon-cyan">{currentCpm}</strong>
                <span className="hud-unit">CPM (打/分)</span>
              </div>
            </div>
            <div className="hud-metric">
              <span className="hud-label">正確性 (Accuracy)</span>
              <div className="hud-val-group">
                <strong className={`hud-value ${accuracy >= 95 ? 'neon-green' : accuracy >= 85 ? 'neon-amber' : 'neon-rose'}`}>
                  {accuracy}%
                </strong>
                <span className="hud-unit">({missCount} 誤打)</span>
              </div>
            </div>
            <div className="hud-metric">
              <span className="hud-label">最高打鍵 / 経過時間</span>
              <div className="hud-val-group">
                <strong className="hud-value text-white">{peakCpm}</strong>
                <span className="hud-unit">最高 | {Math.floor(elapsedSeconds / 60)}:{(elapsedSeconds % 60).toString().padStart(2, '0')}</span>
              </div>
            </div>
            <div className="hud-metric">
              <span className="hud-label">進捗 (Progress)</span>
              <div className="hud-val-group">
                <strong className="hud-value neon-purple">{progressPct}%</strong>
                <span className="hud-unit">{currentLineIndex + 1}/{song.lines.length} 行</span>
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="typing-progress-track">
            <div
              className="typing-progress-fill"
              style={{ width: `${progressPct}%` }}
            />
          </div>

          {/* YouTube Video Section (Always Available & Auto-Looping) */}
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

          {/* Lyrics Typing Display Area */}
          <div className={`typing-display-box ${isShaking ? 'shake-animation' : ''}`}>
            {currentLine ? (
              <div className="typing-line-active">
                {/* Japanese Original Characters with Real-Time Typing Color Sync */}
                <div className="lyrics-ja-container">
                  {(() => {
                    const jaChars = currentLine.ja.split('');
                    const completedJaCount = Math.round(lineProgressRatio * jaChars.length);

                    return jaChars.map((char, i) => {
                      let statusClass = 'ja-char pending';
                      if (i < completedJaCount) {
                        statusClass = 'ja-char completed';
                      } else if (i === completedJaCount && lineProgressRatio > 0 && lineProgressRatio < 1) {
                        statusClass = 'ja-char current';
                      }

                      return (
                        <span key={i} className={statusClass}>
                          {char}
                        </span>
                      );
                    });
                  })()}
                </div>

                {/* Optional Korean Translation */}
                {showKorean && currentLine.ko && (
                  <div className="lyrics-ko-text">
                    {currentLine.ko}
                  </div>
                )}

                {/* Romaji Letters with Active Highlight */}
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

            {/* Next Line Preview */}
            {currentLineIndex + 1 < song.lines.length && (
              <div className="typing-line-preview">
                <div className="preview-content">
                  <span className="preview-label">NEXT:</span>
                  <span className="preview-text">{song.lines[currentLineIndex + 1].ja}</span>
                  {showKorean && song.lines[currentLineIndex + 1].ko && (
                    <span className="preview-ko">({song.lines[currentLineIndex + 1].ko})</span>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* User Guide Hint */}
          <div className="typing-guide-box">
            <p className="guide-text">
              💡 <strong>操作方法:</strong> キーボードでローマ字をタイピングすると、<strong>上の日本語の漢字や仮名もリアルタイムに色が染まっていきます！</strong>
              右上のチェックボックスで<strong>韓国語訳(한글 가사)</strong>の表示も自由に切り替えられます。
            </p>
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

          {/* Category Tabs */}
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
            <button
              type="button"
              className={`song-tab ${categoryFilter === 'mv' ? 'active' : ''}`}
              onClick={() => setCategoryFilter('mv')}
            >
              🎥 動画あり
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
                    {s.youtubeId && <span className="mv-badge">🎥 動画あり</span>}
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
                🔄 もう一度挑戦
              </button>
              {(() => {
                const currentIndex = SONGS.findIndex(s => s.id === song.id);
                const nextSong = SONGS[(currentIndex + 1) % SONGS.length];
                return (
                  <button
                    type="button"
                    className="modal-btn-next"
                    onClick={() => resetGame(nextSong.id)}
                  >
                    次の曲へ ({nextSong.title}) →
                  </button>
                );
              })()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
