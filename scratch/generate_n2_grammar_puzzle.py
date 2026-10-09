# -*- coding: utf-8 -*-
"""
Full Generator for JLPT N2 文法 接続パズル SPEED RUN
Creates:
- jlpt-calendar-site/public/exams/n2-grammar-puzzle.html
- jlpt-calendar-site/dist/client/exams/n2-grammar-puzzle.html
- quiz_sites/n2-grammar-puzzle.html
"""

import json
import os

from questions_data import QUESTIONS

HTML_TEMPLATE = r"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>N2 文法 接続パズル SPEED RUN — ブロック組み立て・文形攻略</title>
<script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
<style>
:root {
  --bg: #0b0f19;
  --surface: #131c2e;
  --surface-alt: #1e293b;
  --border: #334155;
  --text: #f8fafc;
  --muted: #94a3b8;
  --accent: #f59e0b;
  --accent-glow: rgba(245, 158, 11, 0.25);
  --green: #10b981;
  --red: #ef4444;
  --blue: #3b82f6;
  --indigo: #6366f1;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Sans", "Yu Gothic UI", "Noto Sans JP", sans-serif;
  user-select: none;
  background-color: var(--bg);
  color: var(--text);
  min-height: 100vh;
}
.glow-box {
  box-shadow: 0 0 25px var(--accent-glow);
}
.combo-pop {
  animation: pop 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
@keyframes pop {
  0% { transform: scale(0.8); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.flash-correct {
  animation: flashGreen 0.4s ease-out;
}
@keyframes flashGreen {
  0% { background-color: rgba(16, 185, 129, 0.25); }
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

/* Slot Styling */
.slot-box {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 90px;
  min-height: 44px;
  padding: 4px 12px;
  margin: 2px 4px;
  border-radius: 10px;
  font-size: 1.15rem;
  font-weight: 800;
  cursor: pointer;
  vertical-align: middle;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.slot-empty {
  border: 2px dashed #475569;
  background-color: rgba(30, 41, 59, 0.4);
  color: #64748b;
}
.slot-empty:hover {
  border-color: #f59e0b;
  background-color: rgba(245, 158, 11, 0.1);
  color: #fbbf24;
}
.slot-empty.dragover {
  border-color: #3b82f6;
  background-color: rgba(59, 130, 246, 0.2);
  transform: scale(1.05);
}
.slot-filled {
  border: 2px solid #3b82f6;
  background: linear-gradient(135deg, rgba(30, 58, 138, 0.8), rgba(59, 130, 246, 0.5));
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
  animation: pop 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.slot-filled:hover {
  border-color: #ef4444;
  background: linear-gradient(135deg, rgba(153, 27, 27, 0.8), rgba(239, 68, 68, 0.5));
}
.slot-filled:hover::after {
  content: " ✕";
  font-size: 0.85em;
  opacity: 0.8;
}

/* Block Chip Styling */
.block-chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 700;
  border: 1.5px solid #334155;
  background-color: #1e293b;
  color: #e2e8f0;
  cursor: grab;
  transition: all 0.18s ease;
  box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}
.block-chip:hover {
  border-color: #f59e0b;
  color: #ffffff;
  background-color: #334155;
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(245, 158, 11, 0.2);
}
.block-chip:active {
  cursor: grabbing;
  transform: scale(0.96);
}
.block-chip.used {
  opacity: 0.22;
  cursor: not-allowed;
  pointer-events: none;
  filter: grayscale(80%);
}

/* Press & Hold Button Styling */
.hold-hint-btn {
  transition: all 0.15s ease;
  user-select: none;
  -webkit-user-select: none;
}
.hold-hint-btn:active, .hold-hint-btn.holding {
  background-color: #4338ca !important;
  color: #ffffff !important;
  transform: scale(0.97);
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
}
</style>
</head>
<body class="flex flex-col items-center justify-center p-3 sm:p-5">

<!-- Main Game Wrapper -->
<div id="app" class="w-full max-w-2xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-5 sm:p-8 relative overflow-hidden">

  <!-- Top Bar -->
  <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-800 text-xs text-slate-400">
    <div class="flex items-center gap-2">
      <span class="inline-block w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></span>
      <span class="font-bold tracking-wider text-slate-300">JLPT N2 文法 接続パズル SPEED RUN</span>
    </div>
    <div class="flex items-center gap-2 sm:gap-3">
      <button id="btnSound" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 transition flex items-center gap-1.5 text-slate-300">
        <span id="soundIcon">🔊</span> <span id="soundLabel">Sound ON</span>
      </button>
      <a href="/" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 transition text-slate-300">
        🏠 캘린더
      </a>
      <a href="/exams/past-exams-portal.html" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 transition text-slate-300">
        📑 포털
      </a>
    </div>
  </div>

  <!-- SCREEN 1: LOBBY -->
  <div id="screenLobby" class="space-y-6">
    <div class="text-center space-y-2 py-2">
      <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 text-amber-400 text-xs font-semibold border border-amber-500/20 mb-1">
        🧩 ブロック組み立て・接続トラップ完全撃破
      </div>
      <h1 class="text-3xl sm:text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-orange-300 to-indigo-400">
        N2 文法 接続パズル
      </h1>
      <p class="text-slate-400 text-sm sm:text-base">
        문법 앞 <strong class="text-amber-300">단어의 활용형</strong>과 <strong class="text-indigo-300">문형 블록</strong>을 직접 끼워맞춰 완전한 문장을 조립하세요!
      </p>
    </div>

    <!-- Course Selection -->
    <div class="space-y-2">
      <label class="block text-xs font-bold text-slate-400 tracking-wider uppercase">1. 코스 선택</label>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3" id="courseList">
        <button data-course="c1" class="course-btn p-3.5 rounded-xl border border-amber-500 bg-amber-950/40 text-left hover:border-amber-400 transition relative">
          <div class="text-xs font-bold text-amber-400">★ 코스 1 (동사 접속 킬러 집중)</div>
          <div class="font-bold text-white text-base mt-0.5">動詞活用 接続トラップ (25제)</div>
          <div class="text-xs text-slate-400 mt-1">〜た上で, 〜がたい, 〜っこない, 〜ざるを得ない, 〜たところで 등</div>
          <div class="absolute top-3 right-3 text-amber-400 text-sm font-bold">🎯</div>
        </button>

        <button data-course="c2" class="course-btn p-3.5 rounded-xl border border-slate-700 bg-slate-800/60 text-left hover:border-slate-500 transition">
          <div class="text-xs font-bold text-indigo-400">코스 2 (명사·형용사 품사 결합)</div>
          <div class="font-bold text-white text-base mt-0.5">名詞・形容詞 接続トラップ (20제)</div>
          <div class="text-xs text-slate-400 mt-1">〜げ, 〜気味, 〜反面, 〜わりに, 〜にしては, 〜にほかならない 등</div>
        </button>

        <button data-course="c3" class="course-btn p-3.5 rounded-xl border border-slate-700 bg-slate-800/60 text-left hover:border-slate-500 transition">
          <div class="text-xs font-bold text-emerald-400">코스 3 (수강 완료 완벽 굳히기)</div>
          <div class="font-bold text-white text-base mt-0.5">N2 문법 001〜035 총정리 (25제)</div>
          <div class="text-xs text-slate-400 mt-1">다락원 강의 수강 완료 문형 접속 전수 조립</div>
        </button>

        <button data-course="all" class="course-btn p-3.5 rounded-xl border border-slate-700 bg-slate-800/60 text-left hover:border-slate-500 transition">
          <div class="text-xs font-bold text-rose-400">종합 그랑프리 (실전 풀 러시)</div>
          <div class="font-bold text-white text-base mt-0.5">全範囲 総合ランダム (30제)</div>
          <div class="text-xs text-slate-400 mt-1">N2 전범위 접속 셔플 실전 마스터 러시</div>
        </button>
      </div>
    </div>

    <!-- Question Count Options -->
    <div class="space-y-2">
      <label class="block text-xs font-bold text-slate-400 tracking-wider uppercase">2. 문항 수 선택</label>
      <div class="grid grid-cols-3 gap-2" id="countOptions">
        <button data-count="10" class="count-btn py-2 px-3 rounded-lg border border-slate-700 bg-slate-800 text-xs font-bold text-slate-300 hover:border-slate-500 transition">10문항 (쾌속)</button>
        <button data-count="20" class="count-btn py-2 px-3 rounded-lg border border-slate-700 bg-slate-800 text-xs font-bold text-slate-300 hover:border-slate-500 transition">20문항 (집중)</button>
        <button data-count="max" class="count-btn py-2 px-3 rounded-lg border border-amber-500 bg-amber-950/40 text-xs font-bold text-amber-300 transition">코스 전 문항</button>
      </div>
    </div>

    <!-- Instruction Card -->
    <div class="p-3.5 rounded-xl bg-slate-800/40 border border-slate-800 text-xs text-slate-300 space-y-1.5">
      <div class="font-bold text-amber-400 flex items-center gap-1.5">
        <span>💡 조작 및 학습 팁</span>
      </div>
      <ul class="list-disc list-inside space-y-1 text-slate-400 text-xs">
        <li><strong>블록 장착</strong>: 아래 블록을 클릭(터치)하거나 드래그하여 빈 슬롯 <span class="text-amber-300 font-bold">① / ②</span>에 넣으세요.</li>
        <li><strong>블록 해제</strong>: 장착된 슬롯을 클릭하면 다시 블록 뱅크로 복귀합니다.</li>
        <li><strong>번역 힌트 (Press & Hold)</strong>: <span class="text-indigo-400 font-bold">[👁️ 訳]</span> 버튼을 <strong>마우스로 꾹 누르고 있는 동안</strong>에만 한국어 번역이 잠깐 보입니다. 손을 떼면 즉시 숨겨집니다.</li>
      </ul>
    </div>

    <!-- Start Button -->
    <button id="btnStart" class="w-full py-4 rounded-xl bg-gradient-to-r from-amber-500 via-orange-500 to-rose-500 hover:from-amber-400 hover:to-rose-400 text-slate-950 font-black text-lg tracking-wider shadow-lg shadow-amber-500/25 transition active:scale-[0.98]">
      🧩 開始する (接続パズル スタート)
    </button>
  </div>

  <!-- SCREEN 2: GAMEPLAY -->
  <div id="screenGame" class="hidden space-y-5">
    <!-- Status Header -->
    <div class="flex items-center justify-between text-xs">
      <div class="flex items-center gap-2">
        <span id="badgeCategory" class="px-2 py-0.5 rounded bg-indigo-950 border border-indigo-700/60 text-indigo-300 font-bold text-[11px]">
          文法 接続
        </span>
        <span class="text-slate-400">Q. <strong id="qCurrent" class="text-amber-400 text-sm">1</strong> / <span id="qTotal">25</span></span>
      </div>
      <div class="flex items-center gap-3">
        <div id="comboBadge" class="hidden px-2 py-0.5 rounded-full bg-amber-500/20 border border-amber-500/40 text-amber-300 font-black text-xs combo-pop">
          🔥 <span id="comboCount">0</span> COMBO
        </div>
        <div class="text-slate-400 font-mono text-sm flex items-center gap-1">
          <span>⏱️</span> <span id="gameTimer" class="font-bold text-slate-200">00:00</span>
        </div>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
      <div id="progressBar" class="bg-gradient-to-r from-amber-500 to-orange-500 h-full w-0 transition-all duration-300"></div>
    </div>

    <!-- QUESTION CARD -->
    <div id="qCard" class="p-5 sm:p-6 rounded-2xl bg-slate-800/60 border border-slate-700/80 space-y-4">
      <div class="text-xs font-bold text-slate-400 tracking-wide uppercase flex items-center justify-between">
        <span>【 問題 】適切なブロックを組み立てて文を完成させなさい</span>
        <span class="text-slate-500 text-[11px]">※ スロットをクリックで解除</span>
      </div>

      <!-- Problem Sentence with Slots -->
      <div id="qSentence" class="text-lg sm:text-2xl font-bold text-slate-100 leading-relaxed sm:leading-loose tracking-wide">
        <!-- Injected via JS -->
      </div>

      <!-- Translation Hint Section (Zero Layout Shift Floating Tooltip) -->
      <div class="pt-2 border-t border-slate-700/50 flex items-center justify-between relative">
        <div class="relative inline-block">
          <button id="btnHoverTrans" type="button" class="px-3.5 py-1.5 rounded-lg bg-indigo-950/80 hover:bg-indigo-900 border border-indigo-700/70 text-indigo-300 hover:text-white font-bold text-xs flex items-center gap-2 shadow-sm transition cursor-pointer">
            <span>👁️ 訳・ヒント</span>
            <span class="text-[10px] text-indigo-400 bg-indigo-900/80 px-1.5 py-0.5 rounded">마우스 오버</span>
          </button>

          <!-- Floating Tooltip: Absolute positioning ensures ZERO layout shift! -->
          <div id="transTooltip" class="hidden absolute left-0 top-full mt-2 z-50 w-80 sm:w-[420px] p-3.5 rounded-xl bg-slate-900/95 backdrop-blur-md border border-indigo-500/80 shadow-2xl shadow-indigo-950 text-xs sm:text-sm text-slate-100 pointer-events-none transition-all">
            <div class="flex items-start gap-2">
              <span class="text-amber-400 font-bold shrink-0">💡 한국어 번역:</span>
              <span id="transTooltipText" class="text-slate-100 font-medium leading-relaxed"></span>
            </div>
            <div class="absolute left-6 bottom-full w-0 h-0 border-x-4 border-x-transparent border-b-4 border-b-indigo-500/80"></div>
          </div>
        </div>
        <span class="text-[11px] text-slate-500">※ 마우스를 올리면 번역이 뜨고 벗어나면 사라집니다</span>
      </div>
    </div>

    <!-- BLOCK BANK (Choices Pool) -->
    <div class="space-y-2">
      <div class="flex items-center justify-between text-xs text-slate-400 font-bold">
        <span>【 ブロック 選択肢 】<span class="text-slate-500 font-normal">クリックまたはドラッグして装着</span></span>
        <button id="btnClearSlots" class="text-slate-400 hover:text-amber-300 transition text-[11px] underline">
          🔄 スロットを空にする
        </button>
      </div>

      <!-- Block Pool Grid -->
      <div id="blockPool" class="flex flex-wrap gap-2 sm:gap-2.5 p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 min-h-[90px] items-center justify-center">
        <!-- Block chips injected via JS -->
      </div>
    </div>

    <!-- ACTION BUTTONS -->
    <div class="grid grid-cols-2 gap-3 pt-1">
      <button id="btnUnknown" class="py-3 px-4 rounded-xl border border-slate-700 bg-slate-800/80 hover:bg-slate-700 text-slate-300 font-bold text-sm transition">
        ❓ 分からない (スキップ)
      </button>
      <button id="btnCheck" class="py-3 px-4 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-sm tracking-wide shadow-lg shadow-amber-500/20 transition active:scale-[0.98]">
        ✅ 判定する (Enter)
      </button>
    </div>

    <!-- EXPLANATION SHEET (Revealed on Check/Unknown) -->
    <div id="explainSheet" class="hidden p-4 sm:p-5 rounded-2xl bg-slate-950 border border-slate-800 space-y-3.5">
      <!-- Result Banner -->
      <div id="explainBanner" class="flex items-center justify-between pb-3 border-b border-slate-800">
        <!-- Status text & icon injected -->
      </div>

      <!-- Full Japanese Sentence with Ruby/Highlight -->
      <div class="space-y-1">
        <div class="text-xs font-bold text-slate-400">【 完成文 】</div>
        <div id="explainSentence" class="text-base sm:text-lg font-bold text-amber-200 leading-relaxed"></div>
      </div>

      <!-- Korean Translation -->
      <div class="space-y-1">
        <div class="text-xs font-bold text-slate-400">【 韓国語訳 】</div>
        <div id="explainTranslation" class="text-sm text-slate-300"></div>
      </div>

      <!-- Formula & Connection Rule -->
      <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5 text-xs">
        <div class="font-bold text-emerald-400 flex items-center gap-1.5">
          <span>📌 핵심 접속 공식:</span> <span id="explainFormula" class="text-white font-mono"></span>
        </div>
        <div id="explainGrammarPoint" class="text-slate-300 font-semibold"></div>
      </div>

      <!-- Traps Analysis -->
      <div class="p-3 rounded-xl bg-rose-950/20 border border-rose-900/40 space-y-1 text-xs">
        <div class="font-bold text-rose-400 flex items-center gap-1.5">
          <span>⚠️ 함정 및 오답 분석:</span>
        </div>
        <div id="explainTraps" class="text-slate-300 whitespace-pre-line leading-relaxed"></div>
      </div>

      <!-- Extra Example -->
      <div class="p-3 rounded-xl bg-indigo-950/20 border border-indigo-900/40 space-y-1 text-xs">
        <div class="font-bold text-indigo-400 flex items-center gap-1.5">
          <span>📝 실전 예문:</span>
        </div>
        <div id="explainExample" class="text-slate-300 leading-relaxed font-japanese"></div>
      </div>

      <!-- Next Button -->
      <button id="btnNext" class="w-full py-3.5 rounded-xl bg-gradient-to-r from-indigo-500 to-blue-500 hover:from-indigo-400 hover:to-blue-400 text-white font-black text-sm tracking-wider shadow-lg transition active:scale-[0.98]">
        次の問題へ (Space / Enter) ➔
      </button>
    </div>
  </div>

  <!-- SCREEN 3: RESULT -->
  <div id="screenResult" class="hidden space-y-6">
    <div class="text-center space-y-2 py-3">
      <div id="resultRankBadge" class="inline-block text-4xl sm:text-5xl font-black px-4 py-2 rounded-2xl bg-slate-800 border border-amber-500/40 text-amber-400 glow-box">
        S RANK
      </div>
      <h2 class="text-2xl sm:text-3xl font-black text-white pt-2">
        パズル完走！お疲れ様でした
      </h2>
      <p id="resultComment" class="text-slate-400 text-xs sm:text-sm">
        문법 접속 규칙을 신속하게 분별해 냈습니다!
      </p>
    </div>

    <!-- Score Card -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
      <div class="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700 text-center">
        <div class="text-xs text-slate-400 font-bold">正解数</div>
        <div id="resScore" class="text-2xl font-black text-emerald-400 mt-0.5">0 / 0</div>
      </div>
      <div class="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700 text-center">
        <div class="text-xs text-slate-400 font-bold">正答率</div>
        <div id="resAccuracy" class="text-2xl font-black text-amber-400 mt-0.5">0%</div>
      </div>
      <div class="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700 text-center">
        <div class="text-xs text-slate-400 font-bold">所要時間</div>
        <div id="resTime" class="text-2xl font-black text-indigo-400 mt-0.5">00:00</div>
      </div>
      <div class="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700 text-center">
        <div class="text-xs text-slate-400 font-bold">MAX COMBO</div>
        <div id="resMaxCombo" class="text-2xl font-black text-rose-400 mt-0.5">0</div>
      </div>
    </div>

    <!-- Missed Items List (if any) -->
    <div id="missedBox" class="hidden space-y-2">
      <div class="text-xs font-bold text-slate-400">【 復習対象 문항 】</div>
      <div id="missedList" class="space-y-1.5 max-h-48 overflow-y-auto pr-1 text-xs">
        <!-- Injected -->
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="space-y-2.5 pt-2">
      <button id="btnCopyResult" class="w-full py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-sm tracking-wide shadow-lg transition flex items-center justify-center gap-2">
        <span>📋 学習結果をコピーする (클립보드 복사)</span>
      </button>

      <div class="grid grid-cols-2 gap-3">
        <button id="btnRetryWrong" class="hidden py-3 rounded-xl border border-rose-500/50 bg-rose-950/30 hover:bg-rose-900/50 text-rose-300 font-bold text-xs transition">
          🔁 오답/모름만 다시 풀기
        </button>
        <button id="btnBackLobby" class="py-3 rounded-xl border border-slate-700 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs transition">
          🏠 コース選択へ戻る
        </button>
      </div>
    </div>
  </div>

</div>

<!-- Sound Synthesis & Game Logic -->
<script>
const QUESTIONS = """ + json.dumps(QUESTIONS, ensure_ascii=False) + r""";

// --- WEB AUDIO API SYNTHESIZER ---
class SoundManager {
  constructor() {
    this.ctx = null;
    this.enabled = true;
  }
  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) this.ctx = new AudioCtx();
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }
  playClick() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(600, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(300, this.ctx.currentTime + 0.04);
    gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.04);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.05);
  }
  playCorrect() {
    if (!this.enabled) return;
    this.init();
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now + i * 0.06);
      gain.gain.setValueAtTime(0.15, now + i * 0.06);
      gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.06 + 0.3);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now + i * 0.06);
      osc.stop(now + i * 0.06 + 0.32);
    });
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
    osc.frequency.exponentialRampToValueAtTime(110, now + 0.25);
    gain.gain.setValueAtTime(0.18, now);
    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(now);
    osc.stop(now + 0.26);
  }
}
const sound = new SoundManager();

// --- STATE MANAGEMENT ---
let currentCourse = 'c1';
let questionLimit = 'max';
let sessionQuestions = [];
let currentIndex = 0;
let currentQ = null;
let currentSlots = [null, null]; // slot 0, slot 1
let isAnswered = false;

let timerInterval = null;
let startTime = 0;
let elapsedSeconds = 0;
let correctCount = 0;
let combo = 0;
let maxCombo = 0;
let userAnswers = []; // { q, userSlots, isCorrect, isUnknown }

// --- DOM ELEMENTS ---
const screenLobby = document.getElementById('screenLobby');
const screenGame = document.getElementById('screenGame');
const screenResult = document.getElementById('screenResult');

const btnSound = document.getElementById('btnSound');
const soundIcon = document.getElementById('soundIcon');
const soundLabel = document.getElementById('soundLabel');

const btnStart = document.getElementById('btnStart');
const qCurrent = document.getElementById('qCurrent');
const qTotal = document.getElementById('qTotal');
const progressBar = document.getElementById('progressBar');
const gameTimer = document.getElementById('gameTimer');
const comboBadge = document.getElementById('comboBadge');
const comboCount = document.getElementById('comboCount');

const qSentence = document.getElementById('qSentence');
const btnHoverTrans = document.getElementById('btnHoverTrans');
const transTooltip = document.getElementById('transTooltip');
const transTooltipText = document.getElementById('transTooltipText');
const blockPool = document.getElementById('blockPool');
const btnClearSlots = document.getElementById('btnClearSlots');
const btnUnknown = document.getElementById('btnUnknown');
const btnCheck = document.getElementById('btnCheck');

const explainSheet = document.getElementById('explainSheet');
const explainBanner = document.getElementById('explainBanner');
const explainSentence = document.getElementById('explainSentence');
const explainTranslation = document.getElementById('explainTranslation');
const explainFormula = document.getElementById('explainFormula');
const explainGrammarPoint = document.getElementById('explainGrammarPoint');
const explainTraps = document.getElementById('explainTraps');
const explainExample = document.getElementById('explainExample');
const btnNext = document.getElementById('btnNext');

// Sound toggle
btnSound.addEventListener('click', () => {
  sound.enabled = !sound.enabled;
  soundIcon.textContent = sound.enabled ? '🔊' : '🔇';
  soundLabel.textContent = sound.enabled ? 'Sound ON' : 'Sound OFF';
});

// Lobby course selection
document.querySelectorAll('.course-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.course-btn').forEach(b => {
      b.classList.remove('border-amber-500', 'bg-amber-950/40');
      b.classList.add('border-slate-700', 'bg-slate-800/60');
    });
    btn.classList.add('border-amber-500', 'bg-amber-950/40');
    btn.classList.remove('border-slate-700', 'bg-slate-800/60');
    currentCourse = btn.dataset.course;
  });
});

// Lobby count options
document.querySelectorAll('.count-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.count-btn').forEach(b => {
      b.classList.remove('border-amber-500', 'bg-amber-950/40', 'text-amber-300');
      b.classList.add('border-slate-700', 'bg-slate-800', 'text-slate-300');
    });
    btn.classList.add('border-amber-500', 'bg-amber-950/40', 'text-amber-300');
    btn.classList.remove('border-slate-700', 'bg-slate-800', 'text-slate-300');
    questionLimit = btn.dataset.count;
  });
});

// --- HOVER TRANSLATION TOOLTIP (Zero Layout Shift) ---
function showTooltip() {
  if (!currentQ) return;
  transTooltipText.textContent = currentQ.translation;
  transTooltip.classList.remove('hidden');
  btnHoverTrans.classList.add('border-indigo-400', 'bg-indigo-800', 'text-white');
}
function hideTooltip() {
  transTooltip.classList.add('hidden');
  btnHoverTrans.classList.remove('border-indigo-400', 'bg-indigo-800', 'text-white');
}

// Mouse hover: show on enter, hide on leave
btnHoverTrans.addEventListener('mouseenter', showTooltip);
btnHoverTrans.addEventListener('mouseleave', hideTooltip);

// Touch / click toggle support
btnHoverTrans.addEventListener('click', (e) => {
  e.preventDefault();
  if (transTooltip.classList.contains('hidden')) {
    showTooltip();
  } else {
    hideTooltip();
  }
});

// --- START GAME ---
btnStart.addEventListener('click', () => {
  startQuiz();
});

function shuffleArray(arr) {
  const res = [...arr];
  for (let i = res.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [res[i], res[j]] = [res[j], res[i]];
  }
  return res;
}

function startQuiz(customQuestions = null) {
  sound.init();
  if (customQuestions) {
    sessionQuestions = [...customQuestions];
  } else {
    let pool = QUESTIONS.filter(q => q.course.includes(currentCourse));
    if (pool.length === 0) pool = QUESTIONS;
    pool = shuffleArray(pool);
    if (questionLimit !== 'max') {
      const limit = parseInt(questionLimit, 10);
      sessionQuestions = pool.slice(0, limit);
    } else {
      sessionQuestions = pool;
    }
  }

  currentIndex = 0;
  correctCount = 0;
  combo = 0;
  maxCombo = 0;
  userAnswers = [];
  elapsedSeconds = 0;
  startTime = Date.now();

  screenLobby.classList.add('hidden');
  screenResult.classList.add('hidden');
  screenGame.classList.remove('hidden');

  qTotal.textContent = sessionQuestions.length;

  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(updateTimer, 1000);

  renderQuestion();
}

function updateTimer() {
  elapsedSeconds = Math.floor((Date.now() - startTime) / 1000);
  const m = String(Math.floor(elapsedSeconds / 60)).padStart(2, '0');
  const s = String(elapsedSeconds % 60).padStart(2, '0');
  gameTimer.textContent = `${m}:${s}`;
}

// --- RENDER CURRENT QUESTION ---
function renderQuestion() {
  currentQ = sessionQuestions[currentIndex];
  currentSlots = [null, null];
  isAnswered = false;

  qCurrent.textContent = currentIndex + 1;
  const progressPercent = ((currentIndex) / sessionQuestions.length) * 100;
  progressBar.style.width = `${progressPercent}%`;

  explainSheet.classList.add('hidden');
  hideTooltip();

  btnCheck.disabled = false;
  btnUnknown.disabled = false;

  // Build sentence HTML with 2 slots
  qSentence.innerHTML = `
    <span>${escapeHtml(currentQ.prompt_prefix)}</span>
    <span class="slot-box slot-empty" data-slot="0" id="slot-0">① 選択</span>
    <span class="slot-box slot-empty" data-slot="1" id="slot-1">② 選択</span>
    <span>${escapeHtml(currentQ.prompt_suffix)}</span>
  `;

  // Bind slot click to unslot
  document.querySelectorAll('.slot-box').forEach(slotEl => {
    const slotIdx = parseInt(slotEl.dataset.slot, 10);
    slotEl.addEventListener('click', () => {
      if (isAnswered) return;
      if (currentSlots[slotIdx] !== null) {
        unslotItem(slotIdx);
      }
    });

    // Drag-over handlers
    slotEl.addEventListener('dragover', (e) => {
      e.preventDefault();
      if (!isAnswered) slotEl.classList.add('dragover');
    });
    slotEl.addEventListener('dragleave', () => {
      slotEl.classList.remove('dragover');
    });
    slotEl.addEventListener('drop', (e) => {
      e.preventDefault();
      slotEl.classList.remove('dragover');
      if (isAnswered) return;
      const text = e.dataTransfer.getData('text/plain');
      if (text) {
        slotItem(text, slotIdx);
      }
    });
  });

  // Render block pool
  renderBlockPool();
}

function renderBlockPool() {
  blockPool.innerHTML = '';
  const blocks = shuffleArray(currentQ.blocks);

  blocks.forEach(text => {
    const chip = document.createElement('div');
    chip.className = 'block-chip';
    chip.textContent = text;
    chip.draggable = true;

    // Check if already placed in a slot
    if (currentSlots.includes(text)) {
      chip.classList.add('used');
    }

    // Click handler: puts in first empty slot
    chip.addEventListener('click', () => {
      if (isAnswered) return;
      if (chip.classList.contains('used')) return;
      sound.playClick();
      const emptyIdx = currentSlots.findIndex(s => s === null);
      if (emptyIdx !== -1) {
        slotItem(text, emptyIdx);
      }
    });

    // Drag handler
    chip.addEventListener('dragstart', (e) => {
      if (isAnswered || chip.classList.contains('used')) return;
      e.dataTransfer.setData('text/plain', text);
    });

    blockPool.appendChild(chip);
  });
}

function slotItem(text, slotIdx) {
  // If text already in another slot, clear that slot first
  const existingIdx = currentSlots.indexOf(text);
  if (existingIdx !== -1) {
    currentSlots[existingIdx] = null;
    updateSlotEl(existingIdx);
  }

  currentSlots[slotIdx] = text;
  sound.playClick();
  updateSlotEl(slotIdx);
  updateBlockChipsUsedState();
}

function unslotItem(slotIdx) {
  currentSlots[slotIdx] = null;
  sound.playClick();
  updateSlotEl(slotIdx);
  updateBlockChipsUsedState();
}

function updateSlotEl(slotIdx) {
  const el = document.getElementById(`slot-${slotIdx}`);
  if (!el) return;
  const val = currentSlots[slotIdx];
  if (val) {
    el.className = 'slot-box slot-filled';
    el.textContent = val;
  } else {
    el.className = 'slot-box slot-empty';
    el.textContent = slotIdx === 0 ? '① 選択' : '② 選択';
  }
}

function updateBlockChipsUsedState() {
  document.querySelectorAll('.block-chip').forEach(chip => {
    if (currentSlots.includes(chip.textContent)) {
      chip.classList.add('used');
    } else {
      chip.classList.remove('used');
    }
  });
}

// Clear both slots
btnClearSlots.addEventListener('click', () => {
  if (isAnswered) return;
  sound.playClick();
  currentSlots = [null, null];
  updateSlotEl(0);
  updateSlotEl(1);
  updateBlockChipsUsedState();
});

// Unknown / Skip button
btnUnknown.addEventListener('click', () => {
  if (isAnswered) return;
  submitAnswer(true);
});

// Check answer button
btnCheck.addEventListener('click', () => {
  if (isAnswered) return;
  submitAnswer(false);
});

function submitAnswer(isUnknown = false) {
  isAnswered = true;
  btnCheck.disabled = true;
  btnUnknown.disabled = true;

  const correctSlot0 = currentQ.slots[0].answer;
  const correctSlot1 = currentQ.slots[1].answer;

  const userSlot0 = currentSlots[0];
  const userSlot1 = currentSlots[1];

  const isCorrect = !isUnknown && (userSlot0 === correctSlot0 && userSlot1 === correctSlot1);

  if (isCorrect) {
    correctCount++;
    combo++;
    if (combo > maxCombo) maxCombo = combo;
    sound.playCorrect();
    triggerCorrectAnimation();
  } else {
    combo = 0;
    sound.playWrong();
    triggerWrongAnimation();
  }

  updateComboUI();

  userAnswers.push({
    q: currentQ,
    userSlots: [...currentSlots],
    isCorrect: isCorrect,
    isUnknown: isUnknown
  });

  // Always auto-fill correct answer in slots for clear visual confirmation
  const el0 = document.getElementById('slot-0');
  const el1 = document.getElementById('slot-1');
  if (el0) el0.textContent = correctSlot0;
  if (el1) el1.textContent = correctSlot1;

  if (isCorrect) {
    if (el0) el0.className = 'slot-box slot-filled border-emerald-500 bg-emerald-950/80 text-emerald-300';
    if (el1) el1.className = 'slot-box slot-filled border-emerald-500 bg-emerald-950/80 text-emerald-300';
  } else {
    if (el0) el0.className = 'slot-box slot-filled border-rose-500 bg-rose-950/80 text-rose-300';
    if (el1) el1.className = 'slot-box slot-filled border-rose-500 bg-rose-950/80 text-rose-300';
  }

  // Show full explanation sheet
  showExplanation(isCorrect, isUnknown);
}

function triggerCorrectAnimation() {
  const card = document.getElementById('qCard');
  card.classList.add('flash-correct');
  setTimeout(() => card.classList.remove('flash-correct'), 400);
}

function triggerWrongAnimation() {
  const card = document.getElementById('qCard');
  card.classList.add('shake-wrong');
  setTimeout(() => card.classList.remove('shake-wrong'), 350);
}

function updateComboUI() {
  if (combo >= 2) {
    comboBadge.classList.remove('hidden');
    comboCount.textContent = combo;
  } else {
    comboBadge.classList.add('hidden');
  }
}

function showExplanation(isCorrect, isUnknown) {
  explainSheet.classList.remove('hidden');
  hideTooltip();

  if (isCorrect) {
    explainBanner.innerHTML = `
      <div class="flex items-center gap-2 text-emerald-400 font-black text-base">
        <span>🎉 正解！ (EXCELLENT)</span>
      </div>
      <div class="text-xs text-slate-400 font-bold">正答率: ${Math.round((correctCount / (currentIndex + 1)) * 100)}%</div>
    `;
  } else {
    const reason = isUnknown ? '分からない (スキップ)' : '不正解';
    explainBanner.innerHTML = `
      <div class="flex items-center gap-2 text-rose-400 font-black text-base">
        <span>❌ ${reason}</span>
      </div>
      <div class="text-xs text-slate-400 font-bold">정답 블록 확인 후 복습</div>
    `;
  }

  explainSentence.innerHTML = highlightSlotsInSentence(currentQ);
  explainTranslation.textContent = currentQ.translation;
  explainFormula.textContent = currentQ.formula;
  explainGrammarPoint.textContent = `${currentQ.grammar_point} — ${currentQ.meaning}`;
  explainTraps.textContent = currentQ.trap_analysis;
  explainExample.textContent = currentQ.extra_example;

  btnNext.focus();
}

function highlightSlotsInSentence(q) {
  return `${escapeHtml(q.prompt_prefix)} <span class="text-amber-400 font-black underline decoration-2 underline-offset-4">${escapeHtml(q.slots[0].answer)}</span> <span class="text-indigo-400 font-black underline decoration-2 underline-offset-4">${escapeHtml(q.slots[1].answer)}</span> ${escapeHtml(q.prompt_suffix)}`;
}

// Next question
btnNext.addEventListener('click', () => {
  nextQuestion();
});

function nextQuestion() {
  currentIndex++;
  if (currentIndex < sessionQuestions.length) {
    renderQuestion();
  } else {
    finishQuiz();
  }
}

// Key shortcuts (Enter / Space)
window.addEventListener('keydown', (e) => {
  if (screenGame.classList.contains('hidden')) return;

  if (e.key === 'Enter') {
    if (!isAnswered) {
      // Only submit if at least one slot filled
      if (currentSlots[0] || currentSlots[1]) {
        submitAnswer(false);
      }
    } else {
      nextQuestion();
    }
  } else if (e.key === ' ' && isAnswered) {
    e.preventDefault();
    nextQuestion();
  }
});

// --- FINISH QUIZ / RESULTS SCREEN ---
function finishQuiz() {
  clearInterval(timerInterval);
  progressBar.style.width = '100%';

  screenGame.classList.add('hidden');
  screenResult.classList.remove('hidden');

  const total = sessionQuestions.length;
  const accuracy = Math.round((correctCount / total) * 100);

  const m = String(Math.floor(elapsedSeconds / 60)).padStart(2, '0');
  const s = String(elapsedSeconds % 60).padStart(2, '0');
  const timeFormatted = `${m}:${s}`;

  document.getElementById('resScore').textContent = `${correctCount} / ${total}`;
  document.getElementById('resAccuracy').textContent = `${accuracy}%`;
  document.getElementById('resTime').textContent = timeFormatted;
  document.getElementById('resMaxCombo').textContent = maxCombo;

  // Grade badge
  const badgeEl = document.getElementById('resultRankBadge');
  const commentEl = document.getElementById('resultComment');
  if (accuracy >= 95) {
    badgeEl.textContent = 'S+ RANK';
    badgeEl.className = 'inline-block text-4xl sm:text-5xl font-black px-4 py-2 rounded-2xl bg-amber-950 border border-amber-400 text-amber-300 glow-box';
    commentEl.textContent = '🏆 압도적인 마스터! N2 문법 접속 함정을 완벽히 간파하고 있습니다.';
  } else if (accuracy >= 85) {
    badgeEl.textContent = 'A RANK';
    badgeEl.className = 'inline-block text-4xl sm:text-5xl font-black px-4 py-2 rounded-2xl bg-indigo-950 border border-indigo-400 text-indigo-300';
    commentEl.textContent = '✨ 훌륭한 성적입니다! 사소한 접속 형태만 보완하면 만점권입니다.';
  } else if (accuracy >= 70) {
    badgeEl.textContent = 'B RANK';
    badgeEl.className = 'inline-block text-4xl sm:text-5xl font-black px-4 py-2 rounded-2xl bg-slate-800 border border-slate-600 text-slate-200';
    commentEl.textContent = '👍 기본기는 충분합니다. 동사 ます형 어간과 た형 접속 차이를 점검하세요.';
  } else {
    badgeEl.textContent = 'C RANK';
    badgeEl.className = 'inline-block text-4xl sm:text-5xl font-black px-4 py-2 rounded-2xl bg-rose-950 border border-rose-500 text-rose-300';
    commentEl.textContent = '💪 오답 복습을 통해 문형 앞의 단어 활용 형태를 집중적으로 훈련해보세요.';
  }

  // Missed items
  const missed = userAnswers.filter(a => !a.isCorrect);
  const missedBox = document.getElementById('missedBox');
  const missedList = document.getElementById('missedList');
  const btnRetryWrong = document.getElementById('btnRetryWrong');

  if (missed.length > 0) {
    missedBox.classList.remove('hidden');
    btnRetryWrong.classList.remove('hidden');
    missedList.innerHTML = '';
    missed.forEach(item => {
      const row = document.createElement('div');
      row.className = 'p-2 rounded-lg bg-slate-800 border border-slate-700/80 flex items-center justify-between';
      row.innerHTML = `
        <div class="truncate pr-2">
          <span class="text-rose-400 font-bold">[${item.q.id}]</span>
          <span class="text-slate-200">${escapeHtml(item.q.grammar_point)}</span>
          <span class="text-slate-400 text-[11px] block truncate">${escapeHtml(item.q.full_sentence)}</span>
        </div>
        <span class="text-amber-400 font-mono font-bold text-xs whitespace-nowrap">
          正解: ${item.q.slots[0].answer} + ${item.q.slots[1].answer}
        </span>
      `;
      missedList.appendChild(row);
    });
  } else {
    missedBox.classList.add('hidden');
    btnRetryWrong.classList.add('hidden');
  }
}

// Copy results to clipboard
document.getElementById('btnCopyResult').addEventListener('click', () => {
  const total = sessionQuestions.length;
  const accuracy = Math.round((correctCount / total) * 100);
  const m = Math.floor(elapsedSeconds / 60);
  const s = elapsedSeconds % 60;
  const timeStr = `${m}분 ${s}초`;

  const missed = userAnswers.filter(a => !a.isCorrect);
  let missedDetails = '없음 (전 문항 정답)';
  if (missed.length > 0) {
    missedDetails = missed.map(m => `${m.q.id} (${m.q.grammar_point})`).join(', ');
  }

  const courseNames = {
    c1: '動詞活用 接続トラップ (25제)',
    c2: '名詞・形容詞 接続トラップ (20제)',
    c3: 'N2 文法 001~035 총정리 (25제)',
    all: '全範囲 総合ランダム (30제)'
  };
  const cName = courseNames[currentCourse] || currentCourse;

  const todayStr = new Date().toISOString().slice(0, 10);
  const reportText = `[${todayStr} N2 文法 接続パズル SPEED RUN] 학습 시간: ${timeStr} (코스: ${cName}, 정답: ${correctCount}/${total}, 정답률: ${accuracy}%)\n- 오답/모름 문항 (${missed.length}건): ${missedDetails}`;

  navigator.clipboard.writeText(reportText).then(() => {
    const btn = document.getElementById('btnCopyResult');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span>✅ 클립보드에 복사 완료! (채팅창에 붙여넣기 가능)</span>';
    setTimeout(() => {
      btn.innerHTML = originalText;
    }, 2500);
  });
});

// Retry wrong button
document.getElementById('btnRetryWrong').addEventListener('click', () => {
  const missedQuestions = userAnswers.filter(a => !a.isCorrect).map(a => a.q);
  if (missedQuestions.length > 0) {
    startQuiz(missedQuestions);
  }
});

// Back to lobby
document.getElementById('btnBackLobby').addEventListener('click', () => {
  screenResult.classList.add('hidden');
  screenGame.classList.add('hidden');
  screenLobby.classList.remove('hidden');
});

function escapeHtml(text) {
  if (!text) return '';
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
</script>
</body>
</html>
"""

# Targets to write
targets = [
    "jlpt-calendar-site/public/exams/n2-grammar-puzzle.html",
    "jlpt-calendar-site/dist/client/exams/n2-grammar-puzzle.html",
    "quiz_sites/n2-grammar-puzzle.html"
]

for t in targets:
    os.makedirs(os.path.dirname(t), exist_ok=True)
    with open(t, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    print(f"Generated: {t} (Bytes: {len(HTML_TEMPLATE.encode('utf-8'))})")
