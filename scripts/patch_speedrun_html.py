# -*- coding: utf-8 -*-
import sys, re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
FILE_PATH = ROOT / 'jlpt-calendar-site' / 'public' / 'exams' / 'n2-grammar-speedrun.html'
content = FILE_PATH.read_text(encoding='utf-8')

# 1. Update CSS
old_css = """@keyframes anchorBlinkPulse {
  0%, 100% {
    background-color: rgba(245, 158, 11, 0.4);
    box-shadow: 0 0 18px rgba(245, 158, 11, 0.9);
    border-color: #fbbf24;
    color: #fef08a;
    transform: scale(1.08);
  }
  50% {
    background-color: rgba(56, 189, 248, 0.45);
    box-shadow: 0 0 26px rgba(56, 189, 248, 0.95);
    border-color: #38bdf8;
    color: #e0f2fe;
    transform: scale(1.16);
  }
}
.anchor-blink {
  display: inline-block;
  padding: 1px 7px;
  margin: 0 3px;
  border-radius: 8px;
  border: 2px solid #f59e0b;
  font-weight: 900;
  animation: anchorBlinkPulse 0.85s infinite ease-in-out;
  vertical-align: middle;
}
.conn-anchor {
  display: inline;
}"""

new_css = """@keyframes anchorBlinkPulse {
  0%, 100% {
    background-color: rgba(245, 158, 11, 0.4);
    box-shadow: 0 0 18px rgba(245, 158, 11, 0.9);
    border-color: #fbbf24;
    color: #fef08a;
    transform: scale(1.08);
  }
  50% {
    background-color: rgba(56, 189, 248, 0.45);
    box-shadow: 0 0 26px rgba(56, 189, 248, 0.95);
    border-color: #38bdf8;
    color: #e0f2fe;
    transform: scale(1.16);
  }
}
@keyframes badgeBlinkPulse {
  0%, 100% {
    border-color: #fbbf24;
    color: #fef08a;
    background-color: rgba(120, 53, 15, 0.95);
    box-shadow: 0 0 12px rgba(245, 158, 11, 0.85);
    transform: translateX(-50%) scale(1.08);
  }
  50% {
    border-color: #38bdf8;
    color: #e0f2fe;
    background-color: rgba(12, 74, 110, 0.95);
    box-shadow: 0 0 18px rgba(56, 189, 248, 0.95);
    transform: translateX(-50%) scale(1.16);
  }
}
.anchor-blink {
  display: inline-block;
  padding: 1px 7px;
  margin: 0 3px;
  border-radius: 8px;
  border: 2px solid #f59e0b;
  font-weight: 900;
  animation: anchorBlinkPulse 0.85s infinite ease-in-out;
  vertical-align: middle;
}
.badge-blink {
  animation: badgeBlinkPulse 0.85s infinite ease-in-out !important;
}
.conn-anchor-wrapper {
  position: relative;
  display: inline-block;
  vertical-align: middle;
  margin: 14px 4px 4px 4px;
}
.conn-anchor-badge {
  position: absolute;
  top: -24px;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  pointer-events: none;
  z-index: 10;
  user-select: none;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.conn-anchor {
  display: inline-block;
}"""

assert old_css in content, "old_css not found!"
content = content.replace(old_css, new_css)

# 2. Add Toggle Button in Top Bar
old_top_bar = """      <button id="btnToggleKo" type="button" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 transition flex items-center gap-1.5 text-slate-300 text-xs font-semibold cursor-pointer select-none" title="앞면 한국어 해석 표시 ON/OFF (단축키: T)">
        <span id="koIcon">🌐</span> <span id="koLabel">해석 ON</span>
      </button>"""

new_top_bar = """      <button id="btnToggleBadge" type="button" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 transition flex items-center gap-1.5 text-cyan-300 text-xs font-semibold cursor-pointer select-none border border-cyan-500/40" title="앞 단어 품사/접속형 힌트 표시 ON/OFF (단축키: P 또는 C)">
        <span id="badgeIcon">🏷️</span> <span id="badgeLabel">품사 ON</span>
      </button>
      <button id="btnToggleKo" type="button" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 transition flex items-center gap-1.5 text-slate-300 text-xs font-semibold cursor-pointer select-none" title="앞면 한국어 해석 표시 ON/OFF (단축키: T)">
        <span id="koIcon">🌐</span> <span id="koLabel">해석 ON</span>
      </button>"""

assert old_top_bar in content, "old_top_bar not found!"
content = content.replace(old_top_bar, new_top_bar)

# 3. Increase Sentence Container Top Padding
old_sentence_div = '<div id="qSentenceJa" class="text-xl sm:text-2xl font-black text-white leading-relaxed break-keep tracking-wide font-sans">'
new_sentence_div = '<div id="qSentenceJa" class="text-xl sm:text-2xl font-black text-white leading-relaxed break-keep tracking-wide font-sans pt-3 sm:pt-4">'
assert old_sentence_div in content, "old_sentence_div not found!"
content = content.replace(old_sentence_div, new_sentence_div)

# 4. Add connBadgeVisible to state
old_state = "currentQKoRevealed: false,"
new_state = "currentQKoRevealed: false,\n  connBadgeVisible: true,"
assert old_state in content, "old_state not found!"
content = content.replace(old_state, new_state)

# 5. Update prepareQuestions blank/anchor rendering
old_prepare = """    // Construct Japanese blank HTML with anchor element for preceding word blinking
    const rawBlank = item.sentence_ja_blank || (item.sentence_ja + ' （　　）');
    let jaBlankHtml = '';
    const slotHtml = `<span id="blankSlot" class="slot-filled inline-block px-3 py-0.5 mx-1.5 rounded-lg border-2 border-dashed border-amber-400 bg-amber-400/20 text-amber-300 font-black tracking-wider text-lg sm:text-xl shadow-sm">（　　）</span>`;

    if (rawBlank.includes('（　　）')) {
      const parts = rawBlank.split('（　　）');
      const before = parts[0];
      const after = parts.slice(1).join('（　　）');
      const anchor = item.conn_anchor || '';

      let preAnchor = before;
      let anchorHtml = '';
      if (anchor && before.endsWith(anchor)) {
        preAnchor = before.slice(0, -anchor.length);
        anchorHtml = `<span id="connAnchor" class="conn-anchor transition-all duration-300">${anchor}</span>`;
      } else if (anchor && before.includes(anchor)) {
        const lastIdx = before.lastIndexOf(anchor);
        preAnchor = before.slice(0, lastIdx);
        const midText = before.slice(lastIdx + anchor.length);
        anchorHtml = `<span id="connAnchor" class="conn-anchor transition-all duration-300">${anchor}</span>${midText}`;
      } else {
        anchorHtml = `<span id="connAnchor" class="conn-anchor transition-all duration-300"></span>`;
      }

      jaBlankHtml = `${preAnchor}${anchorHtml}${slotHtml}${after}`;
    } else {
      jaBlankHtml = `${slotHtml} ${rawBlank}`;
    }"""

new_prepare = """    // Construct Japanese blank HTML with anchor element and floating part-of-speech badge
    const rawBlank = item.sentence_ja_blank || (item.sentence_ja + ' （　　）');
    let jaBlankHtml = '';
    const slotHtml = `<span id="blankSlot" class="slot-filled inline-block px-3 py-0.5 mx-1.5 rounded-lg border-2 border-dashed border-amber-400 bg-amber-400/20 text-amber-300 font-black tracking-wider text-lg sm:text-xl shadow-sm">（　　）</span>`;

    if (rawBlank.includes('（　　）')) {
      const parts = rawBlank.split('（　　）');
      const before = parts[0];
      const after = parts.slice(1).join('（　　）');
      const anchor = item.conn_anchor || '';
      const badge = item.conn_badge || item.conn_type || '접속';

      let preAnchor = before;
      let anchorHtml = '';
      const badgeDisplay = state.connBadgeVisible ? '' : 'hidden';
      const badgeHtml = `<span id="connAnchorBadge" class="conn-anchor-badge px-2 py-0.5 rounded-full text-[11px] font-extrabold tracking-wider bg-slate-900/95 text-cyan-300 border border-cyan-400/80 shadow-[0_0_10px_rgba(34,211,238,0.4)] ${badgeDisplay}">${badge}</span>`;

      if (anchor && before.endsWith(anchor)) {
        preAnchor = before.slice(0, -anchor.length);
        anchorHtml = `<span class="conn-anchor-wrapper inline-block mx-1.5">${badgeHtml}<span id="connAnchor" class="conn-anchor px-2.5 py-0.5 rounded-lg border-2 border-cyan-500/40 bg-cyan-500/10 text-cyan-100 font-black transition-all duration-300">${anchor}</span></span>`;
      } else if (anchor && before.includes(anchor)) {
        const lastIdx = before.lastIndexOf(anchor);
        preAnchor = before.slice(0, lastIdx);
        const midText = before.slice(lastIdx + anchor.length);
        anchorHtml = `<span class="conn-anchor-wrapper inline-block mx-1.5">${badgeHtml}<span id="connAnchor" class="conn-anchor px-2.5 py-0.5 rounded-lg border-2 border-cyan-500/40 bg-cyan-500/10 text-cyan-100 font-black transition-all duration-300">${anchor}</span></span>${midText}`;
      } else {
        anchorHtml = `<span id="connAnchor" class="conn-anchor transition-all duration-300"></span>`;
      }

      jaBlankHtml = `${preAnchor}${anchorHtml}${slotHtml}${after}`;
    } else {
      jaBlankHtml = `${slotHtml} ${rawBlank}`;
    }"""

assert old_prepare in content, "old_prepare not found!"
content = content.replace(old_prepare, new_prepare)

# 6. Add badge toggle functions
toggle_functions = """
function applyBadgeVisibility() {
  const btn = $('btnToggleBadge');
  const label = $('badgeLabel');
  const badgeEl = $('connAnchorBadge');
  if (state.connBadgeVisible) {
    if (btn) btn.className = 'px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 transition flex items-center gap-1.5 text-cyan-300 text-xs font-semibold cursor-pointer select-none border border-cyan-500/40';
    if (label) label.textContent = '품사 ON';
    if (badgeEl && !state.waitingConfirm) badgeEl.classList.remove('hidden');
  } else {
    if (btn) btn.className = 'px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 transition flex items-center gap-1.5 text-slate-400 text-xs font-semibold cursor-pointer select-none border border-slate-700';
    if (label) label.textContent = '품사 OFF';
    if (badgeEl && !state.waitingConfirm) badgeEl.classList.add('hidden');
  }
}

function toggleBadgeVisibility() {
  state.connBadgeVisible = !state.connBadgeVisible;
  applyBadgeVisibility();
}
"""

anchor_pos = content.find("function applyKoVisibility()")
assert anchor_pos != -1, "applyKoVisibility not found!"
content = content[:anchor_pos] + toggle_functions + "\n" + content[anchor_pos:]

# 7. Update renderQuestion() to handle connAnchorBadge
old_rq_anchor = """  const anchorEl = $('connAnchor');
  if (anchorEl) {
    anchorEl.classList.remove('anchor-blink');
  }"""

new_rq_anchor = """  const anchorEl = $('connAnchor');
  if (anchorEl) {
    anchorEl.classList.remove('anchor-blink');
  }
  const badgeEl = $('connAnchorBadge');
  if (badgeEl) {
    badgeEl.classList.remove('badge-blink');
    if (!state.connBadgeVisible) {
      badgeEl.classList.add('hidden');
    } else {
      badgeEl.classList.remove('hidden');
    }
  }"""

assert old_rq_anchor in content, "old_rq_anchor not found!"
content = content.replace(old_rq_anchor, new_rq_anchor)

# 8. Update checkAnswer() on correct
old_ca_correct = """    // Activate blinking highlight on preceding anchor word/particle (ます형, の, 명사 등)
    const anchorEl = $('connAnchor');
    if (anchorEl) {
      anchorEl.classList.add('anchor-blink');
    }"""

new_ca_correct = """    // Activate blinking highlight on preceding anchor word/particle and floating badge
    const anchorEl = $('connAnchor');
    if (anchorEl) {
      anchorEl.classList.add('anchor-blink');
    }
    const badgeEl = $('connAnchorBadge');
    if (badgeEl) {
      badgeEl.classList.remove('hidden');
      badgeEl.classList.add('badge-blink');
    }"""

assert old_ca_correct in content, "old_ca_correct not found!"
content = content.replace(old_ca_correct, new_ca_correct)

# 9. Update checkAnswer() on wrong
old_ca_wrong = """    const card = $('promptCard');
    card.classList.add('shake-wrong');"""

new_ca_wrong = """    const card = $('promptCard');
    card.classList.add('shake-wrong');

    const anchorEl = $('connAnchor');
    if (anchorEl) {
      anchorEl.classList.add('anchor-blink');
    }
    const badgeEl = $('connAnchorBadge');
    if (badgeEl) {
      badgeEl.classList.remove('hidden');
      badgeEl.classList.add('badge-blink');
    }"""

assert old_ca_wrong in content, "old_ca_wrong not found!"
content = content.replace(old_ca_wrong, new_ca_wrong)

# 10. Update keydown listener and button click listener
old_keydown = """    // Toggle translation with 't' / 'T' / 'ㅅ' (peek in OFF mode, turn off in ON mode)
    if (e.key === 't' || e.key === 'T' || e.key === 'ㅅ') {
      e.preventDefault();
      if (state.waitingConfirm) return;
      toggleCurrentQKo();
      return;
    }"""

new_keydown = """    // Toggle part-of-speech badge with 'p' / 'P' / 'ㅔ' or 'c' / 'C' / 'ㅊ'
    if (e.key === 'p' || e.key === 'P' || e.key === 'ㅔ' || e.key === 'c' || e.key === 'C' || e.key === 'ㅊ') {
      e.preventDefault();
      toggleBadgeVisibility();
      return;
    }

    // Toggle translation with 't' / 'T' / 'ㅅ' (peek in OFF mode, turn off in ON mode)
    if (e.key === 't' || e.key === 'T' || e.key === 'ㅅ') {
      e.preventDefault();
      if (state.waitingConfirm) return;
      toggleCurrentQKo();
      return;
    }"""

assert old_keydown in content, "old_keydown not found!"
content = content.replace(old_keydown, new_keydown)

# Wire up btnToggleBadge
old_btn_init = "  if ($('btnToggleKo')) {"
new_btn_init = """  if ($('btnToggleBadge')) {
    $('btnToggleBadge').onclick = () => toggleBadgeVisibility();
  }
  if ($('btnToggleKo')) {"""

assert old_btn_init in content, "old_btn_init not found!"
content = content.replace(old_btn_init, new_btn_init)

FILE_PATH.write_text(content, encoding='utf-8')
print("Updated jlpt-calendar-site/public/exams/n2-grammar-speedrun.html successfully!")
