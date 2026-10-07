# -*- coding: utf-8 -*-
"""
Builder for N2 Grammar Speedrun Sniper Quiz.
Generates self-contained HTML file embedding all 143 N2 grammar patterns.
"""

import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / 'scripts' / 'n2_grammar_dataset.json'

with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    items = json.load(f)

json_data_str = json.dumps(items, ensure_ascii=False)

html_template = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>N2 文法 SPEED RUN — 문형 저격 퀴즈</title>
<script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
<style>
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Sans", "Yu Gothic UI", "Noto Sans JP", sans-serif;
  user-select: none;
}
.combo-pop {
  animation: pop 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
@keyframes pop {
  0% { transform: scale(0.8); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.flash-correct {
  animation: flashGreen 0.3s ease-out;
}
@keyframes flashGreen {
  0% { background-color: rgba(74, 222, 128, 0.25); }
  100% { background-color: transparent; }
}
.shake-wrong {
  animation: shake 0.35s ease-in-out;
}
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-8px); }
  40%, 80% { transform: translateX(8px); }
}
.slot-filled {
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}
</style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col items-center justify-center p-3 sm:p-5">

<!-- Main Wrapper -->
<div id="app" class="w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-5 sm:p-8 relative overflow-hidden">

  <!-- Top Bar -->
  <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-800 text-xs text-slate-400">
    <div class="flex items-center gap-2">
      <span class="inline-block w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></span>
      <span class="font-bold tracking-wider text-slate-300">JLPT N2 文法 SPEED RUN · 문형 저격</span>
    </div>
    <div class="flex items-center gap-3">
      <button id="btnSound" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 transition flex items-center gap-1.5 text-slate-300">
        <span id="soundIcon">🔊</span> <span id="soundLabel">Sound ON</span>
      </button>
      <a href="/" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 transition text-slate-300">
        🏠 캘린더
      </a>
    </div>
  </div>

  <!-- SCREEN 1: LOBBY -->
  <div id="screenLobby" class="space-y-6">
    <div class="text-center space-y-2 py-2">
      <h1 class="text-3xl sm:text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-orange-300 to-rose-400">
        N2 文法 SPEED RUN
      </h1>
      <p class="text-slate-400 text-sm">
        일본어 빈칸 <strong class="text-amber-300">（　　）</strong>과 한국어 뉘앙스를 보고 1초 만에 N2 문형을 저격하세요!
      </p>
    </div>

    <!-- Course Selection -->
    <div class="space-y-2">
      <label class="block text-xs font-bold text-slate-400 tracking-wider uppercase">1. 코스 선택</label>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3" id="courseList">
        <button data-course="c1" class="course-btn p-3.5 rounded-xl border border-amber-500 bg-amber-950/40 text-left hover:border-amber-400 transition relative">
          <div class="text-xs font-bold text-amber-400">★ 코스 1 (현재 수강 완료 완벽 굳히기)</div>
          <div class="font-bold text-white text-base mt-0.5">문법 001 〜 035 (35개 문형)</div>
          <div class="text-xs text-slate-400 mt-1">〜あげく, 〜あまり, 〜かねない, 〜きり 등</div>
          <div class="absolute top-3 right-3 text-amber-400 text-sm font-bold">🎯</div>
        </button>

        <button data-course="c2" class="course-btn p-3.5 rounded-xl border border-slate-700 bg-slate-800/60 text-left hover:border-slate-500 transition">
          <div class="text-xs font-bold text-indigo-400">코스 2 (중반부 핵심 문형)</div>
          <div class="font-bold text-white text-base mt-0.5">문법 036 〜 070 (35개 문형)</div>
          <div class="text-xs text-slate-400 mt-1">〜くせに, 〜げ, 〜こそ, 〜ざるを得ない 등</div>
        </button>

        <button data-course="c3" class="course-btn p-3.5 rounded-xl border border-slate-700 bg-slate-800/60 text-left hover:border-slate-500 transition">
          <div class="text-xs font-bold text-emerald-400">코스 3 (후반부 고난도 문형)</div>
          <div class="font-bold text-white text-base mt-0.5">문법 071 〜 105 (35개 문형)</div>
          <div class="text-xs text-slate-400 mt-1">〜に相違ない, 〜にほかならない 등</div>
        </button>

        <button data-course="all" class="course-btn p-3.5 rounded-xl border border-slate-700 bg-slate-800/60 text-left hover:border-slate-500 transition">
          <div class="text-xs font-bold text-rose-400">종합 그랑프리 143제</div>
          <div class="font-bold text-white text-base mt-0.5">문법 001 〜 150 전 범위 셔플</div>
          <div class="text-xs text-slate-400 mt-1">실전 시험 문법 1교시 완벽 정복</div>
        </button>
      </div>
    </div>

    <!-- Question Count -->
    <div>
      <label class="block text-xs font-bold text-slate-400 tracking-wider uppercase mb-2">2. 문제 수</label>
      <div class="grid grid-cols-4 gap-2" id="countList">
        <button data-count="20" class="count-btn p-2.5 rounded-lg border border-slate-700 bg-slate-800/60 text-center font-bold text-sm text-slate-300">
          20제<br><span class="text-[11px] font-normal text-slate-400">1분 컷</span>
        </button>
        <button data-count="35" class="count-btn p-2.5 rounded-lg border border-amber-500 bg-amber-950/40 text-center font-bold text-sm text-amber-200">
          35제 ★<br><span class="text-[11px] font-normal text-slate-400">1코스 완독</span>
        </button>
        <button data-count="50" class="count-btn p-2.5 rounded-lg border border-slate-700 bg-slate-800/60 text-center font-bold text-sm text-slate-300">
          50제<br><span class="text-[11px] font-normal text-slate-400">집중 러시</span>
        </button>
        <button data-count="100" class="count-btn p-2.5 rounded-lg border border-slate-700 bg-slate-800/60 text-center font-bold text-sm text-slate-300">
          100제 🔥<br><span class="text-[11px] font-normal text-slate-400">극한 타임어택</span>
        </button>
      </div>
    </div>

    <!-- Start Button -->
    <button id="btnStart" class="w-full py-4 rounded-xl bg-gradient-to-r from-amber-500 to-rose-600 hover:from-amber-400 hover:to-rose-500 font-black text-lg text-white shadow-lg shadow-amber-500/20 active:scale-[0.99] transition">
      문형 저격 스피드런 시작 (Space / Enter)
    </button>
  </div>

  <!-- SCREEN 2: ACTIVE GAME PLAY -->
  <div id="screenPlay" class="hidden space-y-5">
    <!-- Top HUD -->
    <div class="flex items-center justify-between text-sm">
      <div class="flex items-center gap-2">
        <span class="text-xs uppercase tracking-wider text-slate-400 font-bold">Question</span>
        <span id="hudQIndex" class="font-extrabold text-amber-400 text-lg">1</span>
        <span class="text-slate-500">/</span>
        <span id="hudQTotal" class="text-slate-400 font-semibold">35</span>
      </div>

      <div class="flex items-center gap-4">
        <div id="comboBadge" class="hidden px-2.5 py-0.5 rounded-full bg-amber-400/20 border border-amber-400/40 text-amber-300 font-black text-xs combo-pop">
          🔥 <span id="comboCount">0</span> COMBO!
        </div>
        <div class="font-mono text-base font-bold text-slate-300 flex items-center gap-1">
          ⏱️ <span id="hudTimer">00:00</span>
        </div>
      </div>
    </div>

    <!-- Progress bar -->
    <div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
      <div id="hudProgress" class="h-full bg-gradient-to-r from-amber-400 to-rose-500 transition-all duration-200" style="width: 1%"></div>
    </div>

    <!-- Center Prompt Card: Japanese Blank + Korean Nuance -->
    <div id="promptCard" class="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-5 sm:p-6 text-center space-y-4 relative">
      <!-- Top Badges -->
      <div class="flex items-center justify-between text-xs">
        <div class="flex items-center gap-2">
          <span id="qPatternNum" class="px-2 py-0.5 rounded text-[11px] font-extrabold bg-amber-500/20 text-amber-300 border border-amber-500/30">
            N2 문법 001
          </span>
          <span class="text-slate-400 text-[11px] hidden sm:inline">실전 문형 빈칸 완성</span>
        </div>
        <div id="qConnectionBadge" class="font-mono text-[11px] text-sky-300 bg-sky-950/60 px-2 py-0.5 rounded border border-sky-800/70 max-w-[200px] truncate">
          접속 정보
        </div>
      </div>

      <!-- 1. Japanese Blank Sentence (Primary Target) -->
      <div class="py-3 px-4 rounded-xl bg-slate-950/60 border border-slate-800/80 shadow-inner">
        <div id="qSentenceJa" class="text-xl sm:text-2xl font-black text-white leading-relaxed break-keep tracking-wide font-sans">
          <!-- Injected Japanese blank sentence -->
        </div>
      </div>

      <!-- 2. Korean Translation with Nuance Highlight (Context Support) -->
      <div class="py-1 px-2">
        <div id="qSentenceKo" class="text-sm sm:text-base font-semibold text-slate-300 leading-relaxed break-keep">
          <!-- Injected Korean translation -->
        </div>
      </div>

      <!-- Target Nuance Banner -->
      <div class="pt-3 border-t border-slate-700/60 flex items-center justify-center gap-2 text-xs">
        <span class="text-slate-400 font-semibold">저격 대상:</span>
        <span id="qTargetNuance" class="font-bold text-amber-300 text-sm">
          <!-- target nuance -->
        </span>
      </div>
    </div>

    <!-- 4-CHOICE GRID -->
    <div class="space-y-2">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5" id="choiceContainer">
        <!-- 4 choice buttons injected here -->
      </div>
      <div class="flex items-center justify-between text-xs text-slate-400 px-1 pt-1">
        <span>키보드 <strong>1, 2, 3, 4</strong> 키로 초고속 선택 가능</span>
        <button id="btnSkip" class="text-amber-400 hover:text-amber-300 underline font-semibold">모름 / 패스 (Space / Esc)</button>
      </div>
    </div>

    <!-- INSTANT 1-SECOND SNIPER FEEDBACK OVERLAY (On Wrong Answer) -->
    <div id="feedbackModal" class="hidden p-4 rounded-xl bg-red-950/80 border border-red-500/60 space-y-3">
      <div class="flex items-center justify-between">
        <div class="font-bold text-red-300 text-sm flex items-center gap-1.5">
          <span>❌ 오답! 1초 킬러 포인트 확인</span>
        </div>
        <div class="text-xs text-slate-400">잠시 후 재출제 큐에 추가됨</div>
      </div>
      
      <div class="bg-slate-900/90 p-3.5 rounded-lg border border-slate-800 space-y-2 text-xs">
        <div class="flex items-center justify-between">
          <div>
            <span class="text-slate-400">정답 문형: </span>
            <span id="fbPattern" class="text-lg font-black text-amber-300">〜あげく</span>
            <span id="fbMeaning" class="text-slate-300 font-bold ml-1.5">(~한 끝에)</span>
          </div>
          <div id="fbConnection" class="font-mono text-[11px] text-sky-300 bg-sky-950/60 px-2 py-0.5 rounded border border-sky-800">
            Vた＋あげく
          </div>
        </div>

        <!-- Full Example Sentence in Feedback -->
        <div class="pt-2 border-t border-slate-800 space-y-1">
          <div class="text-slate-300 font-bold text-sm" id="fbJaSentence"></div>
          <div class="text-slate-400 text-xs" id="fbKoSentence"></div>
        </div>

        <div class="text-slate-300 pt-1 border-t border-slate-800">
          <strong class="text-rose-400">핵심 뉘앙스:</strong> <span id="fbCore">오랜 과정 끝에 대체로 좋지 않거나 기대와 다른 결과</span>
        </div>

        <div id="fbDiffRow" class="text-slate-400">
          <strong class="text-amber-400">구별 함정:</strong> <span id="fbDiff">〜末に도 긴 과정 뒤의 결과지만 좋은 결과에도 쓴다</span>
        </div>
      </div>

      <button id="btnNextAfterMistake" class="w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 rounded-lg transition border border-slate-700">
        확인하고 다음 문제로 (Space / Enter)
      </button>
    </div>

  </div>

  <!-- SCREEN 3: RESULT -->
  <div id="screenResult" class="hidden space-y-6">
    <div class="text-center space-y-1 py-2">
      <div class="text-xs font-bold text-amber-400 tracking-widest uppercase">FINISH! 스피드런 완료</div>
      <h2 class="text-3xl sm:text-4xl font-black text-white" id="resTitle">
        문형 저격 완료!
      </h2>
      <p class="text-slate-400 text-sm" id="resSub">
        N2 핵심 문형의 뉘앙스 직관이 한층 더 날카로워졌습니다.
      </p>
    </div>

    <!-- Score Big Card -->
    <div class="grid grid-cols-3 gap-3 p-4 rounded-xl bg-slate-800/80 border border-slate-700 text-center">
      <div>
        <div class="text-xs text-slate-400">정답률</div>
        <div class="text-2xl sm:text-3xl font-black text-emerald-400 mt-1" id="resAccuracy">94%</div>
        <div class="text-[11px] text-slate-500" id="resScoreFraction">33 / 35</div>
      </div>
      <div>
        <div class="text-xs text-slate-400">총 소요 시간</div>
        <div class="text-2xl sm:text-3xl font-black text-amber-400 mt-1" id="resTotalTime">01:42</div>
        <div class="text-[11px] text-slate-500" id="resPace">문제당 2.9초</div>
      </div>
      <div>
        <div class="text-xs text-slate-400">최대 콤보</div>
        <div class="text-2xl sm:text-3xl font-black text-rose-400 mt-1" id="resMaxCombo">24</div>
        <div class="text-[11px] text-slate-500">연속 무오답</div>
      </div>
    </div>

    <!-- Review Mistake List -->
    <div id="resMistakeContainer" class="space-y-2">
      <h3 class="text-xs font-bold text-slate-400 tracking-wider uppercase">오늘의 오답 문형 목록 (<span id="resMistakeCount">0</span>)</h3>
      <div id="resMistakeList" class="max-h-56 overflow-y-auto space-y-1.5 pr-1 text-xs"></div>
    </div>

    <!-- Action Buttons -->
    <div class="flex flex-col sm:flex-row gap-3 pt-2">
      <button id="btnRetryWrong" class="hidden flex-1 py-3 bg-amber-500 hover:bg-amber-400 font-bold text-slate-950 rounded-xl transition text-sm">
        🔁 오답 문형만 다시 풀기
      </button>
      <button id="btnPlayAgain" class="flex-1 py-3 bg-sky-500 hover:bg-sky-400 font-bold text-slate-950 rounded-xl transition text-sm">
        🚀 새로운 세션 시작하기
      </button>
    </div>
  </div>

</div>

<script>
const ALL_PATTERNS = __JSON_DATA__;

class SoundEngine {
  constructor() {
    this.enabled = true;
    this.ctx = null;
  }
  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    }
  }
  playCorrect(combo = 1) {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const baseFreq = Math.min(920, 523.25 + (combo * 16));
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(baseFreq, now);
    osc.frequency.exponentialRampToValueAtTime(baseFreq * 1.5, now + 0.12);
    gain.gain.setValueAtTime(0.18, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(now);
    osc.stop(now + 0.18);
  }
  playWrong() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(180, now);
    osc.frequency.linearRampToValueAtTime(120, now + 0.22);
    gain.gain.setValueAtTime(0.2, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(now);
    osc.stop(now + 0.22);
  }
  playComboMilestone() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    [523.25, 659.25, 783.99, 1046.5].forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.12, now + idx * 0.05);
      gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.05 + 0.2);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now + idx * 0.05);
      osc.stop(now + idx * 0.05 + 0.2);
    });
  }
}
const sounds = new SoundEngine();

const state = {
  course: 'c1',
  targetCount: 35,
  questions: [],
  currentIndex: 0,
  score: 0,
  combo: 0,
  maxCombo: 0,
  startTime: null,
  timerInterval: null,
  elapsedSec: 0,
  waitingConfirm: false,
  mistakes: []
};

function generateQuestions(course, count) {
  let pool = [];
  if (course === 'c1') pool = ALL_PATTERNS.slice(0, 35);
  else if (course === 'c2') pool = ALL_PATTERNS.slice(35, 70);
  else if (course === 'c3') pool = ALL_PATTERNS.slice(70, 105);
  else pool = [...ALL_PATTERNS];

  const shuffledPool = [...pool].sort(() => 0.5 - Math.random());
  const selected = [];
  for (let i = 0; i < count; i++) {
    selected.push(shuffledPool[i % shuffledPool.length]);
  }

  return selected.map(item => {
    const distractors = new Set();
    
    // 1. Check if diff_point mentions another pattern
    if (item.diff_point) {
      const match = item.diff_point.match(/〜[^\\s、。ととは]+(?=[ととは]|\\s|\\b|$)/);
      if (match && match[0] !== item.pattern) {
        distractors.add(match[0]);
      }
    }

    // 2. Fill rest from pool
    while (distractors.size < 3) {
      const randomItem = ALL_PATTERNS[Math.floor(Math.random() * ALL_PATTERNS.length)];
      if (randomItem.pattern !== item.pattern) {
        distractors.add(randomItem.pattern);
      }
    }

    const choices = [item.pattern, ...Array.from(distractors).slice(0, 3)];
    for (let c = choices.length - 1; c > 0; c--) {
      const j = Math.floor(Math.random() * (c + 1));
      [choices[c], choices[j]] = [choices[j], choices[c]];
    }

    // Construct Japanese blank HTML
    let jaBlankHtml = item.sentence_ja_blank || (item.sentence_ja + ' （　　）');
    if (jaBlankHtml.includes('（　　）')) {
      jaBlankHtml = jaBlankHtml.replace(
        '（　　）',
        `<span id="blankSlot" class="slot-filled inline-block px-3 py-0.5 mx-1.5 rounded-lg border-2 border-dashed border-amber-400 bg-amber-400/20 text-amber-300 font-black tracking-wider text-lg sm:text-xl shadow-sm">（　　）</span>`
      );
    } else {
      jaBlankHtml = `<span id="blankSlot" class="slot-filled inline-block px-3 py-0.5 mx-1.5 rounded-lg border-2 border-dashed border-amber-400 bg-amber-400/20 text-amber-300 font-black tracking-wider text-lg sm:text-xl shadow-sm">（　　）</span> ${jaBlankHtml}`;
    }

    // Construct Korean HTML with highlight
    let koHtml = item.sentence_ko;
    const target = item.target_ko;
    if (target && koHtml.includes(target)) {
      koHtml = koHtml.replace(
        target,
        `<span class="text-amber-300 font-bold bg-amber-400/25 px-2 py-0.5 rounded border border-amber-400/40 underline decoration-amber-400 decoration-2">${target}</span>`
      );
    } else {
      koHtml = `<span class="text-amber-300 font-bold bg-amber-400/25 px-2 py-0.5 rounded border border-amber-400/40">[ ${item.meaning} ]</span> ${koHtml}`;
    }

    return {
      item,
      jaBlankHtml,
      koHtml,
      choices,
      answer: item.pattern
    };
  });
}

const $ = id => document.getElementById(id);

function initLobbyUI() {
  document.querySelectorAll('.course-btn').forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll('.course-btn').forEach(b => {
        b.classList.remove('border-amber-500', 'bg-amber-950/40');
        b.classList.add('border-slate-700', 'bg-slate-800/60');
      });
      btn.classList.add('border-amber-500', 'bg-amber-950/40');
      btn.classList.remove('border-slate-700', 'bg-slate-800/60');
      state.course = btn.dataset.course;
    };
  });

  document.querySelectorAll('.count-btn').forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll('.count-btn').forEach(b => {
        b.classList.remove('border-amber-500', 'bg-amber-950/40', 'text-amber-200');
        b.classList.add('border-slate-700', 'bg-slate-800/60', 'text-slate-300');
      });
      btn.classList.add('border-amber-500', 'bg-amber-950/40', 'text-amber-200');
      btn.classList.remove('border-slate-700', 'bg-slate-800/60', 'text-slate-300');
      state.targetCount = parseInt(btn.dataset.count, 10);
    };
  });

  $('btnStart').onclick = startGame;

  $('btnSound').onclick = () => {
    sounds.enabled = !sounds.enabled;
    $('soundIcon').textContent = sounds.enabled ? '🔊' : '🔇';
    $('soundLabel').textContent = sounds.enabled ? 'Sound ON' : 'Mute';
  };

  $('btnNextAfterMistake').onclick = advanceNext;
  $('btnSkip').onclick = () => checkAnswer('');

  window.addEventListener('keydown', e => {
    if (state.waitingConfirm) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        advanceNext();
      }
      return;
    }
    if (!$('screenPlay').classList.contains('hidden')) {
      if (['1', '2', '3', '4'].includes(e.key)) {
        const idx = parseInt(e.key, 10) - 1;
        const currentQ = state.questions[state.currentIndex];
        if (currentQ && currentQ.choices[idx]) {
          checkAnswer(currentQ.choices[idx]);
        }
      } else if (e.key === ' ' || e.key === 'Escape') {
        e.preventDefault();
        checkAnswer('');
      }
    }
  });

  $('btnPlayAgain').onclick = () => {
    clearInterval(state.timerInterval);
    $('screenResult').classList.add('hidden');
    $('screenLobby').classList.remove('hidden');
  };

  $('btnRetryWrong').onclick = () => {
    if (state.mistakes.length === 0) return;
    state.questions = state.mistakes.map(m => ({ ...m.q }));
    state.targetCount = state.questions.length;
    startSessionWithQuestions();
  };
}

function startGame() {
  state.questions = generateQuestions(state.course, state.targetCount);
  startSessionWithQuestions();
}

function startSessionWithQuestions() {
  state.currentIndex = 0;
  state.score = 0;
  state.combo = 0;
  state.maxCombo = 0;
  state.elapsedSec = 0;
  state.mistakes = [];
  state.waitingConfirm = false;

  $('screenLobby').classList.add('hidden');
  $('screenResult').classList.add('hidden');
  $('screenPlay').classList.remove('hidden');

  state.startTime = Date.now();
  clearInterval(state.timerInterval);
  state.timerInterval = setInterval(() => {
    state.elapsedSec = Math.floor((Date.now() - state.startTime) / 1000);
    const m = String(Math.floor(state.elapsedSec / 60)).padStart(2, '0');
    const s = String(state.elapsedSec % 60).padStart(2, '0');
    $('hudTimer').textContent = `${m}:${s}`;
  }, 1000);

  renderQuestion();
}

function renderQuestion() {
  state.waitingConfirm = false;
  $('feedbackModal').classList.add('hidden');
  const card = $('promptCard');
  card.classList.remove('flash-correct', 'shake-wrong');

  const q = state.questions[state.currentIndex];
  $('hudQIndex').textContent = state.currentIndex + 1;
  $('hudQTotal').textContent = state.questions.length;
  $('hudProgress').style.width = `${((state.currentIndex) / state.questions.length) * 100}%`;

  $('qPatternNum').textContent = `N2 문법 ${q.item.num}`;
  $('qConnectionBadge').textContent = q.item.connection ? `접속: ${q.item.connection}` : '접속: V/N연결';
  $('qSentenceJa').innerHTML = q.jaBlankHtml;
  $('qSentenceKo').innerHTML = q.koHtml;
  $('qTargetNuance').textContent = q.item.target_ko ? `[ ${q.item.target_ko} ] ➔ ${q.item.meaning}` : q.item.meaning;

  const container = $('choiceContainer');
  container.innerHTML = q.choices.map((c, idx) => `
    <button data-val="${c}" class="choice-item py-3.5 px-4 rounded-xl border border-slate-700 bg-slate-800/80 hover:border-amber-400 hover:bg-slate-700/80 transition text-left flex items-center justify-between font-bold text-white text-base">
      <span class="tracking-wide">${c}</span>
      <span class="w-6 h-6 rounded-full bg-slate-700 flex items-center justify-center text-xs text-slate-300 font-mono">${idx + 1}</span>
    </button>
  `).join('');

  container.querySelectorAll('.choice-item').forEach(btn => {
    btn.onclick = () => checkAnswer(btn.dataset.val);
  });
}

function checkAnswer(userAnswer) {
  if (state.waitingConfirm) return;
  const q = state.questions[state.currentIndex];
  const slot = $('blankSlot');

  if (userAnswer === q.answer) {
    state.score++;
    state.combo++;
    if (state.combo > state.maxCombo) state.maxCombo = state.combo;

    if (state.combo >= 5 && state.combo % 5 === 0) {
      sounds.playComboMilestone();
    } else {
      sounds.playCorrect(state.combo);
    }

    updateComboBadge();
    const card = $('promptCard');
    card.classList.add('flash-correct');

    if (slot) {
      slot.textContent = q.item.sentence_ja_target || q.item.pattern;
      slot.className = 'slot-filled inline-block px-3 py-0.5 mx-1.5 rounded-lg border-2 border-emerald-400 bg-emerald-500/30 text-emerald-300 font-black tracking-wider text-lg sm:text-xl shadow-md scale-105';
    }

    setTimeout(advanceNext, 220);
  } else {
    state.combo = 0;
    updateComboBadge();
    sounds.playWrong();

    const card = $('promptCard');
    card.classList.add('shake-wrong');

    if (slot) {
      slot.textContent = q.item.sentence_ja_target || q.item.pattern;
      slot.className = 'slot-filled inline-block px-3 py-0.5 mx-1.5 rounded-lg border-2 border-rose-500 bg-rose-500/30 text-rose-300 font-black tracking-wider text-lg sm:text-xl shadow-md';
    }

    state.mistakes.push({
      q,
      userAnswer: userAnswer || '(미선택/모름)'
    });

    state.questions.push({ ...q });

    state.waitingConfirm = true;
    $('fbPattern').textContent = q.item.pattern;
    $('fbMeaning').textContent = `(${ q.item.meaning })`;
    $('fbConnection').textContent = q.item.connection || 'V/N接続';
    $('fbJaSentence').textContent = q.item.sentence_ja;
    $('fbKoSentence').textContent = q.item.sentence_ko;
    $('fbCore').textContent = q.item.core_meaning;
    
    if (q.item.diff_point) {
      $('fbDiffRow').classList.remove('hidden');
      $('fbDiff').textContent = q.item.diff_point;
    } else {
      $('fbDiffRow').classList.add('hidden');
    }

    $('feedbackModal').classList.remove('hidden');
  }
}

function updateComboBadge() {
  const badge = $('comboBadge');
  if (state.combo >= 3) {
    badge.classList.remove('hidden');
    $('comboCount').textContent = state.combo;
  } else {
    badge.classList.add('hidden');
  }
}

function advanceNext() {
  state.currentIndex++;
  if (state.currentIndex >= state.questions.length) {
    finishGame();
  } else {
    renderQuestion();
  }
}

function finishGame() {
  clearInterval(state.timerInterval);
  $('screenPlay').classList.add('hidden');
  $('screenResult').classList.remove('hidden');

  const accuracy = Math.round((state.score / (state.score + state.mistakes.length)) * 100) || 0;
  $('resAccuracy').textContent = `${accuracy}%`;
  $('resScoreFraction').textContent = `${state.score} / ${state.score + state.mistakes.length} (정답수/총시도)`;

  const m = String(Math.floor(state.elapsedSec / 60)).padStart(2, '0');
  const s = String(state.elapsedSec % 60).padStart(2, '0');
  $('resTotalTime').textContent = `${m}:${s}`;

  const avgPace = ((state.elapsedSec / (state.score + state.mistakes.length)) || 0).toFixed(1);
  $('resPace').textContent = `문항당 평균 ${avgPace}초`;
  $('resMaxCombo').textContent = state.maxCombo;

  $('resMistakeCount').textContent = state.mistakes.length;
  const mistakeListEl = $('resMistakeList');
  if (state.mistakes.length === 0) {
    $('resMistakeContainer').classList.add('hidden');
    $('btnRetryWrong').classList.add('hidden');
  } else {
    $('resMistakeContainer').classList.remove('hidden');
    $('btnRetryWrong').classList.remove('hidden');
    mistakeListEl.innerHTML = state.mistakes.map(m => `
      <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1">
        <div class="flex items-center justify-between">
          <div>
            <span class="font-bold text-amber-300 text-sm">${m.q.item.pattern}</span>
            <span class="text-slate-400 text-xs ml-1">${m.q.item.meaning}</span>
          </div>
          <div>
            <span class="text-xs text-red-400 line-through">${m.userAnswer}</span>
            <span class="text-xs font-bold text-emerald-400 ml-1.5">✓ ${m.q.answer}</span>
          </div>
        </div>
        <div class="text-[11px] text-slate-300 font-sans">${m.q.item.sentence_ja}</div>
        <div class="text-[11px] text-slate-500">${m.q.item.sentence_ko}</div>
      </div>
    `).join('');
  }
}

window.addEventListener('DOMContentLoaded', initLobbyUI);
</script>
</body>
</html>
"""

final_html = html_template.replace('__JSON_DATA__', json_data_str)

target1 = ROOT / 'quiz_sites' / 'n2-grammar-speedrun.html'
target2 = ROOT / 'jlpt-calendar-site' / 'public' / 'exams' / 'n2-grammar-speedrun.html'
artifact_path = Path(r'C:\Users\pcw06\.gemini\antigravity\brain\bc5faace-29a7-4719-8d64-ead5d12a8c6d\grammar_speedrun.html')

for t in [target1, target2, artifact_path]:
    t.parent.mkdir(parents=True, exist_ok=True)
    with open(t, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f'Successfully built and wrote to {t}')
