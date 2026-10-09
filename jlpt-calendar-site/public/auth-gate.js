/**
 * JLPT N2 Codex - Universal PIN Auth Gate ('6997')
 * Enforces authentication across all pages, saving credentials in a 1-year cookie and localStorage.
 */
(function() {
  const PIN_EXPECTED = '6997';
  const COOKIE_NAME = 'jlpt_auth';
  const COOKIE_MAX_AGE = 31536000; // 365 days in seconds

  function isAuthed() {
    try {
      const cookieMatch = document.cookie.match(new RegExp('(?:^|;\\s*)' + COOKIE_NAME + '=(.*?)(?:;|$)'));
      if (cookieMatch && cookieMatch[1] === PIN_EXPECTED) {
        return true;
      }
      if (typeof localStorage !== 'undefined' && localStorage.getItem(COOKIE_NAME) === PIN_EXPECTED) {
        // Sync back to cookie
        document.cookie = `${COOKIE_NAME}=${PIN_EXPECTED}; path=/; max-age=${COOKIE_MAX_AGE}; SameSite=Lax`;
        return true;
      }
    } catch (e) {
      // Storage access exception fallback
    }
    return false;
  }

  function setAuthed() {
    try {
      document.cookie = `${COOKIE_NAME}=${PIN_EXPECTED}; path=/; max-age=${COOKIE_MAX_AGE}; SameSite=Lax`;
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(COOKIE_NAME, PIN_EXPECTED);
      }
    } catch (e) {}
  }

  // If already authenticated, do nothing and return immediately
  if (isAuthed()) {
    // Keep cookie refreshed
    setAuthed();
    return;
  }

  // Otherwise, block rendering and show PIN gate
  const styleEl = document.createElement('style');
  styleEl.id = 'jlpt-auth-gate-style';
  styleEl.textContent = `
    body > *:not(#jlpt-auth-gate-overlay) {
      display: none !important;
    }
    #jlpt-auth-gate-overlay {
      position: fixed !important;
      inset: 0 !important;
      z-index: 2147483647 !important;
      background: #0d120a !important;
      background: radial-gradient(circle at 50% 30%, #172213 0%, #0d120a 100%) !important;
      color: #e5f2dc !important;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      padding: 20px !important;
      box-sizing: border-box !important;
    }
    .jlpt-pin-box {
      background: rgba(22, 29, 20, 0.95) !important;
      border: 1px solid rgba(80, 100, 75, 0.5) !important;
      border-radius: 20px !important;
      padding: 36px 32px !important;
      max-width: 400px !important;
      width: 100% !important;
      text-align: center !important;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(180, 240, 100, 0.1) !important;
      backdrop-filter: blur(16px) !important;
    }
    .jlpt-pin-icon {
      font-size: 40px !important;
      margin-bottom: 12px !important;
      display: inline-block !important;
    }
    .jlpt-pin-title {
      font-size: 19px !important;
      font-weight: 800 !important;
      color: #e5f2dc !important;
      margin: 0 0 8px 0 !important;
      letter-spacing: -0.01em !important;
    }
    .jlpt-pin-desc {
      font-size: 13px !important;
      color: #9cb094 !important;
      margin: 0 0 24px 0 !important;
      line-height: 1.5 !important;
    }
    .jlpt-pin-input {
      width: 100% !important;
      box-sizing: border-box !important;
      background: #11170f !important;
      border: 2px solid #364433 !important;
      border-radius: 12px !important;
      color: #cdfb7a !important;
      font-size: 26px !important;
      font-weight: 800 !important;
      letter-spacing: 0.35em !important;
      text-align: center !important;
      padding: 12px 16px !important;
      margin-bottom: 14px !important;
      outline: none !important;
      transition: all 0.2s ease !important;
    }
    .jlpt-pin-input:focus {
      border-color: #cdfb7a !important;
      box-shadow: 0 0 16px rgba(205, 251, 122, 0.25) !important;
    }
    .jlpt-pin-btn {
      width: 100% !important;
      background: #cdfb7a !important;
      color: #0f150c !important;
      font-size: 14px !important;
      font-weight: 800 !important;
      padding: 13px !important;
      border-radius: 12px !important;
      border: none !important;
      cursor: pointer !important;
      transition: all 0.15s ease !important;
      letter-spacing: 0.02em !important;
    }
    .jlpt-pin-btn:hover {
      background: #ddfca0 !important;
      transform: translateY(-1px) !important;
      box-shadow: 0 4px 16px rgba(205, 251, 122, 0.3) !important;
    }
    .jlpt-pin-error {
      color: #ff6b81 !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      margin-top: 12px !important;
      display: none;
    }
    @keyframes jlpt-shake {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-6px); }
      40%, 80% { transform: translateX(6px); }
    }
    .jlpt-shake {
      animation: jlpt-shake 0.3s ease !important;
    }
  `;
  document.head.appendChild(styleEl);

  function createModal() {
    if (document.getElementById('jlpt-auth-gate-overlay')) return;

    const overlay = document.createElement('div');
    overlay.id = 'jlpt-auth-gate-overlay';
    overlay.innerHTML = `
      <div class="jlpt-pin-box" id="jlptPinBox">
        <div class="jlpt-pin-icon">🔐</div>
        <h2 class="jlpt-pin-title">JLPT N2 Codex Private Hub</h2>
        <p class="jlpt-pin-desc">학습자 전용 비공개 포털입니다.<br>접근을 위해 PIN 코드를 입력하세요.</p>
        <form id="jlptPinForm" autocomplete="off" onsubmit="return false;">
          <input
            type="password"
            id="jlptPinInput"
            class="jlpt-pin-input"
            inputmode="numeric"
            pattern="[0-9]*"
            maxlength="6"
            placeholder="••••"
            autocomplete="current-password"
            autofocus
          />
          <button type="submit" id="jlptPinSubmit" class="jlpt-pin-btn">확인 (Enter)</button>
          <div id="jlptPinError" class="jlpt-pin-error">⚠️ 올바른 PIN 코드가 아닙니다.</div>
        </form>
      </div>
    `;

    document.body.appendChild(overlay);

    const input = document.getElementById('jlptPinInput');
    const form = document.getElementById('jlptPinForm');
    const error = document.getElementById('jlptPinError');
    const box = document.getElementById('jlptPinBox');

    function tryAuth() {
      const val = input.value.trim();
      if (val === PIN_EXPECTED) {
        setAuthed();
        overlay.style.transition = 'opacity 0.25s ease';
        overlay.style.opacity = '0';
        setTimeout(() => {
          overlay.remove();
          styleEl.remove();
        }, 250);
      } else {
        error.style.display = 'block';
        box.classList.remove('jlpt-shake');
        void box.offsetWidth; // trigger reflow
        box.classList.add('jlpt-shake');
        input.value = '';
        input.focus();
      }
    }

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      tryAuth();
    });

    input.addEventListener('input', () => {
      error.style.display = 'none';
      if (input.value.length === 4 && input.value === PIN_EXPECTED) {
        tryAuth();
      }
    });

    setTimeout(() => {
      input.focus();
    }, 50);
  }

  if (document.body) {
    createModal();
  } else {
    document.addEventListener('DOMContentLoaded', createModal);
  }
})();
