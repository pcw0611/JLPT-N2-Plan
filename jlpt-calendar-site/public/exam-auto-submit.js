/**
 * JLPT N2 Codex - Automated Exam & Quiz Result Submitter
 * Automatically submits elapsed time, score, accuracy, and questions directly to the calendar API.
 */
(function() {
  function showSubmitToast(message, isSuccess = true) {
    let toast = document.getElementById('jlpt-submit-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'jlpt-submit-toast';
      toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%) translateY(100px);
        background: rgba(18, 26, 16, 0.96);
        border: 1px solid #4ade80;
        color: #f0fdf4;
        padding: 14px 24px;
        border-radius: 99px;
        font-size: 13px;
        font-weight: 800;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(74, 222, 128, 0.25);
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 999999;
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease;
        opacity: 0;
        pointer-events: none;
        white-space: nowrap;
      `;
      document.body.appendChild(toast);
    }

    if (!isSuccess) {
      toast.style.borderColor = '#fb7185';
      toast.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(251, 113, 133, 0.25)';
    } else {
      toast.style.borderColor = '#4ade80';
      toast.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(74, 222, 128, 0.25)';
    }

    toast.innerHTML = isSuccess ? `<span>✅</span> <span>${message}</span>` : `<span>⚠️</span> <span>${message}</span>`;
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(-50%) translateY(100px)';
    }, 4500);
  }

  async function autoSubmitExamResult(data) {
    if (!data) return;

    // Default Seoul date
    if (!data.date) {
      data.date = new Intl.DateTimeFormat('sv-SE', {
        timeZone: 'Asia/Seoul',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      }).format(new Date());
    }

    const sec = Number(data.elapsedSeconds || 0);
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    const timeStr = m > 0 ? `${m}분 ${s}초` : `${s}초`;
    const scoreStr = `${data.correctCount}/${data.totalQuestions}`;
    const accStr = `${data.accuracy}%`;

    try {
      const res = await fetch('/api/submit-exam', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const json = await res.json();
      if (res.ok && json.ok) {
        showSubmitToast(`[자동 기록 완료] ${data.title} (${timeStr}, ${scoreStr}, ${accStr})`, true);

        // Update any copy button text if present
        ['btnCopyTime', 'btnCopyResult', 'btnCopyHudTime'].forEach(btnId => {
          const btn = document.getElementById(btnId);
          if (btn) {
            btn.innerHTML = `✓ 캘린더 자동 저장 완료! <span style="opacity:0.75;font-size:11px;">(클립보드 복사 가능)</span>`;
          }
        });

        // Store last submitted payload in localStorage
        try {
          localStorage.setItem('jlpt_last_submission', JSON.stringify({
            id: json.id,
            title: data.title,
            submittedAt: new Date().toISOString(),
          }));
        } catch (e) {}

        return json;
      } else {
        throw new Error(json.error || 'submission_failed');
      }
    } catch (err) {
      console.warn('Auto submit warning:', err);
      showSubmitToast(`자동 저장 일시 실패 (로컬 보관됨): ${timeStr}, ${scoreStr}`, false);
      try {
        const queue = JSON.parse(localStorage.getItem('jlpt_pending_submissions') || '[]');
        queue.push({ data, timestamp: Date.now() });
        localStorage.setItem('jlpt_pending_submissions', JSON.stringify(queue));
      } catch (e) {}
    }
  }

  window.autoSubmitExamResult = autoSubmitExamResult;
  window.showSubmitToast = showSubmitToast;
})();
