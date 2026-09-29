'use client';

import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import Link from 'next/link';
import { SONGS, type Song, type SongLine, type SongPart } from './songs';

interface UserRecord {
  bestCpm: number;
  bestAccuracy: number;
  playCount: number;
}

interface UserStats {
  records: Record<string, UserRecord>;
  totalPlays: number;
  totalKeystrokes: number;
  totalCorrectKeystrokes?: number;
  totalTimeSeconds: number;
}

export default function MygoTypingPage() {
  const [selectedSongId, setSelectedSongId] = useState<string>(SONGS[0].id);
  const [selectedPartIndex, setSelectedPartIndex] = useState<number>(0);
  const [categoryFilter, setCategoryFilter] = useState<'all' | 'album1' | 'album2' | 'album3' | 'cover'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Feature: Toggle Korean Lyrics Translation
  const [showKorean, setShowKorean] = useState<boolean>(true);

  // Feature: Full Lyrics Modal Viewer
  const [showAllLyricsModal, setShowAllLyricsModal] = useState<boolean>(false);

  // Typing Game State
  const [currentLineIndex, setCurrentLineIndex] = useState(0);
  const [currentCharIndex, setCurrentCharIndex] = useState(0);
  const [typedHistory, setTypedHistory] = useState<string>('');
  const [missCount, setMissCount] = useState(0);
  const [totalKeystrokes, setTotalKeystrokes] = useState(0);
  const [correctKeystrokes, setCorrectKeystrokes] = useState(0);
  const [isShaking, setIsShaking] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);

  // Snappy Line Entrance Animation State (0ms delay)
  const [isLineEntering, setIsLineEntering] = useState(false);

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
  const activePart: SongPart = useMemo(() => {
    return song.parts[selectedPartIndex] || song.parts[0];
  }, [song, selectedPartIndex]);

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
  const saveStats = useCallback((songId: string, partId: string, finalCpm: number, accuracy: number, timeSec: number, keys: number, correctKeys: number) => {
    const recordKey = `${songId}_${partId}`;
    setUserStats(prev => {
      const prevRecord = prev.records[recordKey] || { bestCpm: 0, bestAccuracy: 0, playCount: 0 };
      const updatedRecords = {
        ...prev.records,
        [recordKey]: {
          bestCpm: Math.max(prevRecord.bestCpm, finalCpm),
          bestAccuracy: Math.max(prevRecord.bestAccuracy, accuracy),
          playCount: prevRecord.playCount + 1,
        }
      };
      const prevCorrect = prev.totalCorrectKeystrokes ?? Math.round(prev.totalKeystrokes * 0.95);
      const updated: UserStats = {
        records: updatedRecords,
        totalPlays: prev.totalPlays + 1,
        totalKeystrokes: prev.totalKeystrokes + keys,
        totalCorrectKeystrokes: prevCorrect + correctKeys,
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

  // Reset / Change Song or Part
  const resetGame = useCallback((targetSongId?: string, targetPartIndex: number = 0) => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (targetSongId) setSelectedSongId(targetSongId);
    setSelectedPartIndex(targetPartIndex);
    setCurrentLineIndex(0);
    setCurrentCharIndex(0);
    setIsLineEntering(false);
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
  const currentLine: SongLine | undefined = activePart.lines[currentLineIndex];
  const targetRomaji = useMemo(() => {
    if (!currentLine) return '';
    return currentLine.romaji.toLowerCase();
  }, [currentLine]);

  // Key Event Listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (showAllLyricsModal) {
        if (e.key === 'Escape') setShowAllLyricsModal(false);
        return;
      }
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

      // Reliable Key Extraction (IME Resistant: works even if Korean/Japanese IME is active!)
      let pressedChar = '';
      if (e.code && e.code.startsWith('Key')) {
        pressedChar = e.code.slice(3).toLowerCase(); // 'KeyA' -> 'a'
      } else if (e.code && e.code.startsWith('Digit')) {
        pressedChar = e.code.slice(5);
      } else if (e.code === 'Space') {
        pressedChar = ' ';
      } else if (e.key && e.key.length === 1) {
        pressedChar = e.key.toLowerCase();
      } else {
        return;
      }

      e.preventDefault();

      // Start timer on first keypress
      if (!isPlaying) {
        setIsPlaying(true);
        startTimeRef.current = Date.now();
      }

      if (!targetRomaji) return;

      // Auto-skip any non-alphanumeric characters (spaces, quotes, dashes, etc.)
      let currentPos = currentCharIndex;
      while (currentPos < targetRomaji.length && !/[a-z0-9]/i.test(targetRomaji[currentPos])) {
        currentPos++;
      }

      if (currentPos >= targetRomaji.length) {
        // Line already at end
        return;
      }

      // If user pressed Space, allow skipping to next word/char
      if (pressedChar === ' ') {
        let skipTo = currentPos;
        while (skipTo < targetRomaji.length && /[a-z0-9]/i.test(targetRomaji[skipTo])) {
          skipTo++;
        }
        while (skipTo < targetRomaji.length && !/[a-z0-9]/i.test(targetRomaji[skipTo])) {
          skipTo++;
        }
        if (skipTo > currentPos && skipTo <= targetRomaji.length) {
          setCurrentCharIndex(skipTo);
          return;
        }
      }

      const remaining = targetRomaji.substring(currentPos);
      const expectedChar = remaining[0];

      // Flexible Romaji Matching Logic:
      let matchedLength = 0;

      // 1. Direct Exact Match
      if (pressedChar === expectedChar) {
        matchedLength = 1;
      }
      // 2. 'si' typed when target is 'shi' (skip 'h')
      else if (remaining.startsWith('shi') && pressedChar === 's') {
        matchedLength = 1;
      } else if (remaining.startsWith('hi') && pressedChar === 'i') {
        // user typed 's' then 'i' for 'shi' -> consume both 'h' and 'i'!
        matchedLength = 2;
      }
      // 3. 'shi' typed when target is 'si'
      else if (remaining.startsWith('si') && pressedChar === 's') {
        matchedLength = 1;
      } else if (remaining.startsWith('i') && pressedChar === 'h') {
        // user typed 's' then 'h' for 'si' -> tolerate 'h' without error!
        matchedLength = 0;
        return;
      }
      // 4. 'ti' typed when target is 'chi'
      else if (remaining.startsWith('chi') && pressedChar === 't') {
        matchedLength = 2; // consume 'ch' and expect 'i' next!
      }
      // 5. 'tu' typed when target is 'tsu'
      else if (remaining.startsWith('tsu') && pressedChar === 't') {
        matchedLength = 1;
      } else if (remaining.startsWith('su') && pressedChar === 'u') {
        // user typed 't' then 'u' for 'tsu' -> consume 'su'!
        matchedLength = 2;
      }
      // 6. 'fu' <-> 'hu'
      else if (remaining.startsWith('fu') && pressedChar === 'h') {
        matchedLength = 1;
      } else if (remaining.startsWith('hu') && pressedChar === 'f') {
        matchedLength = 1;
      }
      // 7. 'ji' <-> 'zi'
      else if (remaining.startsWith('ji') && pressedChar === 'z') {
        matchedLength = 1;
      } else if (remaining.startsWith('zi') && pressedChar === 'j') {
        matchedLength = 1;
      }
      // 8. 'o' typed when target is 'wo' (particle を)
      else if (remaining.startsWith('wo') && pressedChar === 'o') {
        matchedLength = 2; // consume both 'w' and 'o'
      }
      // 9. 'wa' <-> 'ha' (particle は)
      else if (remaining.startsWith('ha') && pressedChar === 'w') {
        matchedLength = 1;
      } else if (remaining.startsWith('wa') && pressedChar === 'h') {
        matchedLength = 1;
      }
      // 10. Single 'n' typed for 'nn' when followed by consonant
      else if (remaining.startsWith('nn') && pressedChar === remaining[2] && remaining[2]) {
        // User pressed the next consonant directly, consume 'nn' and 1 char of next!
        matchedLength = 3;
      }


      if (matchedLength > 0) {
        let nextIndex = currentPos + matchedLength;
        // Auto-skip any following spaces or symbols
        while (nextIndex < targetRomaji.length && !/[a-z0-9]/i.test(targetRomaji[nextIndex])) {
          nextIndex++;
        }

        setCorrectKeystrokes(prev => prev + 1);
        setTotalKeystrokes(prev => prev + 1);
        setTypedHistory(prev => prev + pressedChar);
        setCurrentCharIndex(nextIndex);

        // Check if line finished
        if (nextIndex >= targetRomaji.length) {
          if (currentLineIndex + 1 < activePart.lines.length) {
            // Instantly advance to next line with 0ms delay!
            setCurrentLineIndex(prev => prev + 1);
            setCurrentCharIndex(0);
            setTypedHistory('');
            setIsLineEntering(true);
            setTimeout(() => {
              setIsLineEntering(false);
            }, 60);
          } else {
            // Completed Current Part!
            const now = Date.now();
            const timeSec = startTimeRef.current ? Math.max(1, Math.round((now - startTimeRef.current) / 1000)) : 1;
            const finalCorrect = correctKeystrokes + 1;
            const finalTotal = totalKeystrokes + 1;
            const finalCpm = Math.round((finalCorrect / timeSec) * 60);
            const accuracy = Math.round((finalCorrect / finalTotal) * 100);

            setIsPlaying(false);
            setIsCompleted(true);
            saveStats(song.id, activePart.id, finalCpm, accuracy, timeSec, finalTotal, finalCorrect);
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
  }, [
    showAllLyricsModal,
    isCompleted,
    isPlaying,
    currentCharIndex,
    currentLineIndex,
    targetRomaji,
    song,
    activePart,
    currentLine,
    correctKeystrokes,
    totalKeystrokes,
    saveStats,
  ]);

  // Metrics
  const accuracy = totalKeystrokes > 0
    ? Math.round((correctKeystrokes / totalKeystrokes) * 100)
    : 100;

  const progressPct = activePart.lines.length > 0
    ? Math.round(((currentLineIndex + (currentCharIndex / (targetRomaji.length || 1))) / activePart.lines.length) * 100)
    : 0;

  const careerAvgCpm = useMemo(() => {
    if (userStats.totalTimeSeconds <= 0) return 0;
    return Math.round((userStats.totalKeystrokes / userStats.totalTimeSeconds) * 60);
  }, [userStats]);

  const careerAvgAccuracy = useMemo(() => {
    const totalKeys = userStats.totalKeystrokes;
    if (totalKeys <= 0) return accuracy;
    const totalCorrect = userStats.totalCorrectKeystrokes ?? Math.round(totalKeys * 0.95);
    return Math.min(100, Math.max(1, Math.round((totalCorrect / totalKeys) * 100)));
  }, [userStats, accuracy]);

  const displayAvgCpm = useMemo(() => {
    if (isPlaying && elapsedSeconds > 0) {
      return Math.round((correctKeystrokes / elapsedSeconds) * 60);
    }
    return careerAvgCpm > 0 ? careerAvgCpm : currentCpm;
  }, [isPlaying, elapsedSeconds, correctKeystrokes, careerAvgCpm, currentCpm]);

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
      const totalLen = targetRomaji.length || 1;
      for (let i = 0; i < chars.length; i++) {
        const start = Math.floor((i / chars.length) * totalLen);
        const end = Math.floor(((i + 1) / chars.length) * totalLen);
        ranges.push({ char: chars[i], start, end });
      }
    }
    return ranges;
  }, [currentLine, targetRomaji]);

  // Filtered Song List
  const filteredSongs = useMemo(() => {
    return SONGS.filter(s => {
      if (categoryFilter === 'album1' && !s.album.includes('1st Album『迷跡波』')) return false;
      if (categoryFilter === 'album2' && !s.album.includes('2nd Album『跡暖空』')) return false;
      if (categoryFilter === 'album3' && !s.album.includes('3rd Album『致並跡』')) return false;
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
          <a
            href="/"
            className="typing-back-btn"
            onClick={(e) => {
              e.preventDefault();
              window.location.href = '/';
            }}
          >
            ← 学習カレンダー
          </a>
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
          {/* Dashboard HUD: 실시간 타수, 평균 타자, 정확도, 평균 정확도 상시 표시 */}
          <div className="typing-hud">
            {/* 1. 실시간 타수 */}
            <div className="hud-card cpm-card">
              <span className="hud-label">リアルタイム打鍵</span>
              <div className="hud-value-row">
                <span className="hud-number">{currentCpm}</span>
                <span className="hud-unit">CPM</span>
              </div>
              <span className="hud-sub">最高: {peakCpm} CPM</span>
            </div>

            {/* 2. 평균 타자 (상시 표시) */}
            <div className="hud-card avg-cpm-card">
              <span className="hud-label">平均打鍵速度 (常時表示)</span>
              <div className="hud-value-row">
                <span className="hud-number">{displayAvgCpm}</span>
                <span className="hud-unit">CPM</span>
              </div>
              <span className="hud-sub">生涯平均: {careerAvgCpm > 0 ? `${careerAvgCpm} CPM` : '集計中'}</span>
            </div>

            {/* 3. 현재 정확도 */}
            <div className="hud-card acc-card">
              <span className="hud-label">現在正確率</span>
              <div className="hud-value-row">
                <span className="hud-number">{accuracy}%</span>
              </div>
              <span className="hud-sub">ミス: {missCount}回</span>
            </div>

            {/* 4. 평균 정확도 (상시 표시) */}
            <div className="hud-card avg-acc-card">
              <span className="hud-label">平均正確率 (常時表示)</span>
              <div className="hud-value-row">
                <span className="hud-number">{careerAvgAccuracy}%</span>
              </div>
              <span className="hud-sub">通算打鍵: {userStats.totalKeystrokes + totalKeystrokes}打</span>
            </div>

            {/* 5. 진행 상황 & 타이머 */}
            <div className="hud-card prog-card">
              <div className="hud-title-with-time">
                <span className="hud-label">進行 ({activePart.name})</span>
                <span className="hud-time-badge">
                  ⏱️ {Math.floor(elapsedSeconds / 60)}:{(elapsedSeconds % 60).toString().padStart(2, '0')}
                </span>
              </div>
              <div className="hud-value-row">
                <span className="hud-number">{progressPct}%</span>
              </div>
              <div className="progress-bar-bg">
                <div className="progress-bar-fill" style={{ width: `${progressPct}%` }} />
              </div>
            </div>
          </div>

          {/* YouTube MV / Audio Player (Standard embed URL) */}
          {song.youtubeId && (
            <div className="typing-video-wrapper">
              <iframe
                key={song.youtubeId}
                src={`https://www.youtube-nocookie.com/embed/${song.youtubeId}?rel=0&enablejsapi=1`}
                title={`${song.title} - Video`}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerPolicy="strict-origin-when-cross-origin"
                allowFullScreen
                className="typing-youtube-frame"
              />
            </div>
          )}

          {/* Part Selection Pill Bar & YouTube Direct Link */}
          <div className="part-selector-bar">
            <span className="part-selector-label">パート選択:</span>
            <div className="part-pills">
              {song.parts.map((p, idx) => (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => resetGame(song.id, idx)}
                  className={`part-pill ${idx === selectedPartIndex ? 'active' : ''}`}
                >
                  {p.name}
                </button>
              ))}
            </div>

            <div className="part-actions-right">
              <button
                type="button"
                className="show-lyrics-modal-btn"
                onClick={() => setShowAllLyricsModal(true)}
                title="곡의 전체 가사와 한국어 번역을 확인합니다"
              >
                📜 全歌詞を見る
              </button>

              {song.youtubeId && (
                <a
                  href={`https://www.youtube.com/watch?v=${song.youtubeId}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="youtube-direct-btn"
                  title="YouTube에서 직접 시청하기"
                >
                  ▶ YouTube ↗
                </a>
              )}
            </div>
          </div>

          {/* Lyrics Typing Display Area with Snappy Transition */}
          <div className={`typing-display-box ${isShaking ? 'shake-animation' : ''}`}>
            {currentLine ? (
              <div
                key={`${selectedPartIndex}_${currentLineIndex}`}
                className={`typing-line-active ${isLineEntering ? 'line-snappy-enter' : ''}`}
              >
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

          {/* Category & Album Tabs */}
          <div className="song-tabs">
            <button
              type="button"
              className={`song-tab ${categoryFilter === 'all' ? 'active' : ''}`}
              onClick={() => setCategoryFilter('all')}
            >
              全曲 ({SONGS.length})
            </button>
            <button
              type="button"
              className={`song-tab ${categoryFilter === 'album1' ? 'active' : ''}`}
              onClick={() => setCategoryFilter('album1')}
            >
              1st 迷跡波
            </button>
            <button
              type="button"
              className={`song-tab ${categoryFilter === 'album2' ? 'active' : ''}`}
              onClick={() => setCategoryFilter('album2')}
            >
              2nd 跡暖空
            </button>
            <button
              type="button"
              className={`song-tab ${categoryFilter === 'album3' ? 'active' : ''}`}
              onClick={() => setCategoryFilter('album3')}
            >
              3rd 致並跡
            </button>
            <button
              type="button"
              className={`song-tab ${categoryFilter === 'cover' ? 'active' : ''}`}
              onClick={() => setCategoryFilter('cover')}
            >
              カバー ({SONGS.filter(s => s.category === 'cover').length})
            </button>
          </div>

          {/* Song Card List */}
          <div className="song-list-scroll">
            {filteredSongs.map(s => {
              const isSelected = s.id === song.id;
              const recordKey = `${s.id}_part1`;
              const record = userStats.records[recordKey];

              return (
                <div
                  key={s.id}
                  onClick={() => resetGame(s.id, 0)}
                  className={`song-card ${isSelected ? 'selected' : ''}`}
                >
                  <div className="song-card-header">
                    <span className="song-name">{s.title}</span>
                    <span className="category-badge">{s.category === 'original' ? 'オリジナル' : 'カバー'}</span>
                  </div>
                  <div className="song-reading-row">{s.reading}</div>
                  <div className="song-album-row">
                    <span className="song-album-text">{s.album}</span>
                    <span className="song-parts-badge">{s.parts.length}パート</span>
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
              <span className="celebration-badge">🎉 PART FINISHED!</span>
              <h2>{song.title}</h2>
              <p className="song-album-desc">{activePart.name} 完奏！</p>
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
                onClick={() => resetGame(song.id, selectedPartIndex)}
              >
                もう一度挑戦
              </button>
              {selectedPartIndex + 1 < song.parts.length ? (
                <button
                  type="button"
                  className="modal-btn-next"
                  onClick={() => resetGame(song.id, selectedPartIndex + 1)}
                >
                  次のパート ({song.parts[selectedPartIndex + 1].name}) へ →
                </button>
              ) : (
                <button
                  type="button"
                  className="modal-btn-next"
                  onClick={() => {
                    const currentIndex = SONGS.findIndex(s => s.id === song.id);
                    const nextSong = SONGS[(currentIndex + 1) % SONGS.length];
                    resetGame(nextSong.id, 0);
                  }}
                >
                  次の曲へ →
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Full Lyrics Modal */}
      {showAllLyricsModal && (
        <div className="lyrics-modal-backdrop" onClick={() => setShowAllLyricsModal(false)}>
          <div className="lyrics-modal-card" onClick={e => e.stopPropagation()}>
            <div className="lyrics-modal-header">
              <div>
                <span className="category-badge">{song.category === 'original' ? 'オリジナル' : 'カバー'}</span>
                <h2 className="lyrics-modal-title">{song.title} <small>({song.reading})</small></h2>
                <p className="lyrics-modal-album">💿 {song.album}</p>
              </div>
              <button
                type="button"
                className="lyrics-modal-close"
                onClick={() => setShowAllLyricsModal(false)}
              >
                ✕ 閉じる (Esc)
              </button>
            </div>

            <div className="lyrics-modal-body">
              {song.parts.map((p, pIdx) => (
                <div key={p.id} className="lyrics-part-section">
                  <h3 className="lyrics-part-title">{p.name}</h3>
                  <div className="lyrics-lines-container">
                    {p.lines.map((line, lIdx) => (
                      <div key={lIdx} className="lyrics-line-item">
                        <span className="lyrics-line-num">{(pIdx === 0 ? 0 : song.parts[0].lines.length) + lIdx + 1}</span>
                        <div className="lyrics-line-text-group">
                          <div className="lyrics-ja">{line.ja}</div>
                          <div className="lyrics-romaji">{line.romaji}</div>
                          {showKorean && line.ko && (
                            <div className="lyrics-ko">{line.ko}</div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
