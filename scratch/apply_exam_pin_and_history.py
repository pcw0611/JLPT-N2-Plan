import json
import re

# Load 9/20 database result
with open('database/results/official-vol2-full-mock-20260920.json', 'r', encoding='utf-8') as f:
    res920 = json.load(f)

answers920 = [q['userAnswer'] for q in res920['questionsRecord']]
dwells920 = [q['dwellTimeSeconds'] for q in res920['questionsRecord']]

pin_modal_html = """
    <!-- ================================================================= -->
    <!-- PIN Auth Modal (응시 비밀번호: 6997) -->
    <!-- ================================================================= -->
    <div id="pin-modal" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-white border-2 border-neutral-900 rounded-2xl p-6 sm:p-8 max-w-sm w-full text-center space-y-4 shadow-2xl font-sans">
        <div class="w-14 h-14 rounded-full bg-neutral-100 text-neutral-900 flex items-center justify-center mx-auto text-3xl border border-neutral-300">
          🔒
        </div>
        <div>
          <h3 class="text-xl font-bold font-serif text-neutral-950">
            受験者 認証 (JLPT N2)
          </h3>
          <p class="text-xs text-neutral-600 mt-1.5 leading-relaxed">
            본 모의고사는 수험자 전용 비공개 시험입니다.<br>
            <strong>응시 비밀번호 (4자리)</strong>를 입력하세요.
          </p>
        </div>
        <div class="space-y-2">
          <input
            type="password"
            id="pin-input"
            maxlength="4"
            placeholder="••••"
            autocomplete="off"
            class="w-full text-center text-3xl font-mono tracking-[0.4em] py-3 px-4 border-2 border-neutral-400 focus:border-neutral-950 rounded-xl outline-none transition-all"
            onkeydown="if(event.key === 'Enter') submitPinAuth()"
          />
          <div id="pin-error" class="hidden text-xs text-red-600 font-bold">
            비밀번호가 올바르지 않습니다. 다시 입력해 주세요.
          </div>
        </div>
        <div class="flex gap-2 pt-2">
          <button onclick="closePinModal()" type="button" class="flex-1 py-3 border border-neutral-400 hover:bg-neutral-100 text-neutral-700 text-xs font-bold rounded-lg transition-colors cursor-pointer">
            취소
          </button>
          <button onclick="submitPinAuth()" type="button" class="flex-1 py-3 bg-neutral-950 hover:bg-neutral-800 text-white text-xs font-bold rounded-lg shadow transition-colors cursor-pointer">
            인증 및 시험 시작
          </button>
        </div>
      </div>
    </div>
"""

pin_js = """
    // =========================================================================
    // PIN Authentication (비밀번호: 6997)
    // =========================================================================
    let pendingExamStartCallback = null;

    function checkExamPin(callback) {
      if (sessionStorage.getItem('jlpt_exam_pin_auth') === '6997') {
        callback();
        return;
      }
      pendingExamStartCallback = callback;
      const modal = document.getElementById('pin-modal');
      modal.classList.remove('hidden');
      const input = document.getElementById('pin-input');
      input.value = '';
      input.classList.remove('border-red-600');
      document.getElementById('pin-error').classList.add('hidden');
      setTimeout(() => input.focus(), 150);
    }

    function closePinModal() {
      document.getElementById('pin-modal').classList.add('hidden');
      pendingExamStartCallback = null;
    }

    function submitPinAuth() {
      const input = document.getElementById('pin-input');
      const val = input.value.trim();
      if (val === '6997') {
        sessionStorage.setItem('jlpt_exam_pin_auth', '6997');
        document.getElementById('pin-modal').classList.add('hidden');
        if (pendingExamStartCallback) {
          const cb = pendingExamStartCallback;
          pendingExamStartCallback = null;
          cb();
        }
      } else {
        document.getElementById('pin-error').classList.remove('hidden');
        input.classList.add('border-red-600');
        input.value = '';
        input.focus();
      }
    }
"""

# ==============================================================================
# 1. Process 9/20 Exam: n2-midterm-mock-exam-20260920.html
# ==============================================================================
p920 = 'jlpt-calendar-site/public/exams/n2-midterm-mock-exam-20260920.html'
with open(p920, 'r', encoding='utf-8') as f:
    content920 = f.read()

# Add PIN modal if not present
if 'id="pin-modal"' not in content920:
    content920 = content920.replace('</body>', pin_modal_html + '\n</body>')

# Update Start Button to require PIN
content920 = content920.replace(
    'onclick="startSection1()" class="w-full sm:w-2/3 py-4 bg-neutral-950',
    'onclick="checkExamPin(() => startSection1())" class="w-full sm:w-2/3 py-4 bg-neutral-950'
)

# Add historical record banner to intro screen
banner920 = """
      <!-- 9/20 DB Historical Record & Wrong Questions Banner -->
      <div class="border-2 border-red-700 bg-red-50/90 p-5 rounded-xl space-y-3 font-sans my-4 shadow-md">
        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-red-200 pb-2.5">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-1 rounded bg-red-700 text-white font-bold text-xs">📊 9/20 응시 기록 (DB 보존)</span>
            <span class="font-extrabold text-neutral-950 text-sm sm:text-base">실전 환산: 119 / 180점 (정답 71 · 오답 36)</span>
          </div>
          <span class="text-xs text-neutral-600 font-mono font-bold">2026-09-20 응시 완료</span>
        </div>
        <p class="text-xs sm:text-sm text-neutral-800 leading-relaxed">
          지난 9월 20일 실전 모의고사에서 작성하신 107문항 답안 데이터가 원본 그대로 보존되어 있습니다.<br>
          아래 버튼을 누르면 <strong>당시 틀렸던 문제(36문항)와 내가 선택했던 오답, 정답 및 정밀 한국어 해설</strong>이 즉시 펼쳐집니다.
        </p>
        <div class="flex flex-wrap gap-2.5 pt-1">
          <button onclick="loadHistoricalExam20260920('wrong')" type="button" class="flex-1 py-3 px-4 bg-red-700 hover:bg-red-800 text-white text-xs sm:text-sm font-bold rounded-lg shadow transition-all flex items-center justify-center gap-2 cursor-pointer">
            <span>❌ 지난 시험 틀린 문제 (36문항) 오답노트 바로보기</span>
            <span>➔</span>
          </button>
          <button onclick="loadHistoricalExam20260920('all')" type="button" class="py-3 px-4 bg-neutral-900 hover:bg-neutral-800 text-white text-xs sm:text-sm font-bold rounded-lg shadow transition-all cursor-pointer">
            📊 전체 107문항 성적표 및 해설 보기
          </button>
        </div>
      </div>
"""

if '9/20 DB Historical Record' not in content920:
    content920 = content920.replace(
        '<!-- Start Button -->',
        banner920 + '\n      <!-- Start Button -->'
    )

# Add restart fresh button in results screen
if 'restartExamFresh' not in content920:
    content920 = content920.replace(
        '<button onclick="copyResultJSON()"',
        '<button onclick="restartExamFresh()" class="px-5 py-3 bg-neutral-700 hover:bg-neutral-800 text-white text-xs sm:text-sm font-bold rounded shadow transition-all mr-2">🔄 새 시험으로 다시 풀기</button>\n          <button onclick="copyResultJSON()"'
    )

# Embed Historical JS in 9/20
history920_js = f"""
    // =========================================================================
    // 9/20 Database Historical Result & Wrong Questions Auto-Loader
    // =========================================================================
    const DB_HISTORICAL_20260920 = {{
      examDate: "2026-09-20",
      totalQuestions: 107,
      correctCount: 71,
      wrongCount: 36,
      scaledScore: 119,
      section1ElapsedSeconds: 4320,
      section2ElapsedSeconds: 2616,
      answers: {json.dumps(answers920)},
      dwellTimes: {json.dumps(dwells920)}
    }};

    function loadHistoricalExam20260920(filterType = 'wrong') {{
      if (!sessionQuestions || sessionQuestions.length === 0) {{
        initExam();
      }}
      userAnswers = [...DB_HISTORICAL_20260920.answers];
      questionDwellTimes = [...DB_HISTORICAL_20260920.dwellTimes];
      section1ElapsedSeconds = DB_HISTORICAL_20260920.section1ElapsedSeconds;
      section2ElapsedSeconds = DB_HISTORICAL_20260920.section2ElapsedSeconds;

      document.getElementById('screen-intro').classList.add('hidden');
      document.getElementById('screen-quiz').classList.add('hidden');
      document.getElementById('screen-break').classList.add('hidden');
      document.getElementById('screen-listening-intro').classList.add('hidden');
      document.getElementById('screen-result').classList.remove('hidden');

      calculateAndRenderResults();
      renderAllExplanations(filterType);
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function restartExamFresh() {{
      checkExamPin(() => {{
        initExam();
        section1RemainingSeconds = 105 * 60;
        section1ElapsedSeconds = 0;
        section2ElapsedSeconds = 0;
        currentQuestionIndex = 0;
        startSection1();
      }});
    }}
"""

if 'DB_HISTORICAL_20260920' not in content920:
    content920 = content920.replace(
        'function initExam() {',
        pin_js + '\n' + history920_js + '\n    function initExam() {'
    )

with open(p920, 'w', encoding='utf-8') as f:
    f.write(content920)

with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'w', encoding='utf-8') as f:
    f.write(content920)

print('Updated 9/20 exam successfully!')

# ==============================================================================
# 2. Process 2023.12 Exam: n2-past-exam-202312-mock.html
# ==============================================================================
p2312 = 'jlpt-calendar-site/public/exams/n2-past-exam-202312-mock.html'
with open(p2312, 'r', encoding='utf-8') as f:
    content2312 = f.read()

# Add PIN modal if not present
if 'id="pin-modal"' not in content2312:
    content2312 = content2312.replace('</body>', pin_modal_html + '\n</body>')

# Update Start Button to require PIN
content2312 = content2312.replace(
    'onclick="startSection1()" class="w-full sm:w-2/3 py-4 bg-neutral-950',
    'onclick="checkExamPin(() => startSection1())" class="w-full sm:w-2/3 py-4 bg-neutral-950'
)

# Add local storage restore & restart button in 2023.12
banner2312 = """
      <!-- Local Storage Previous Result Banner -->
      <div id="local-history-banner" class="hidden border-2 border-emerald-700 bg-emerald-50/90 p-5 rounded-xl space-y-3 font-sans my-4 shadow-md">
        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-emerald-200 pb-2.5">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-1 rounded bg-emerald-700 text-white font-bold text-xs">📊 최근 응시 기록 보존됨</span>
            <span id="local-score-summary" class="font-extrabold text-neutral-950 text-sm sm:text-base"></span>
          </div>
          <span id="local-date-summary" class="text-xs text-neutral-600 font-mono font-bold"></span>
        </div>
        <p class="text-xs sm:text-sm text-neutral-800 leading-relaxed">
          이전에 응시하신 답안이 보존되어 있습니다. 아래 버튼을 눌러 틀린 문제의 오답 노트와 해설을 바로 확인하실 수 있습니다.
        </p>
        <div class="flex flex-wrap gap-2.5 pt-1">
          <button onclick="loadLocalExamResult('wrong')" type="button" class="flex-1 py-3 px-4 bg-red-700 hover:bg-red-800 text-white text-xs sm:text-sm font-bold rounded-lg shadow transition-all flex items-center justify-center gap-2 cursor-pointer">
            <span>❌ 최근 응시 틀린 문제 오답노트 바로보기</span>
            <span>➔</span>
          </button>
          <button onclick="loadLocalExamResult('all')" type="button" class="py-3 px-4 bg-neutral-900 hover:bg-neutral-800 text-white text-xs sm:text-sm font-bold rounded-lg shadow transition-all cursor-pointer">
            📊 전체 성적표 및 해설 보기
          </button>
        </div>
      </div>
"""

if 'id="local-history-banner"' not in content2312:
    content2312 = content2312.replace(
        '<!-- Start Button -->',
        banner2312 + '\n      <!-- Start Button -->'
    )

# Add restart fresh button in results screen for 2023.12
if 'restartExamFresh' not in content2312:
    content2312 = content2312.replace(
        '<button onclick="copyResultJSON()"',
        '<button onclick="restartExamFresh()" class="px-5 py-3 bg-neutral-700 hover:bg-neutral-800 text-white text-xs sm:text-sm font-bold rounded shadow transition-all mr-2">🔄 새 시험으로 다시 풀기</button>\n          <button onclick="copyResultJSON()"'
    )

# Local Storage JS for 2023.12
storage2312_js = """
    // =========================================================================
    // Local Storage Preservation for 2023.12 Mock Exam
    // =========================================================================
    function checkPreviousResult() {
      try {
        const raw = localStorage.getItem('n2_past_exam_202312_result');
        if (raw) {
          const data = JSON.parse(raw);
          const banner = document.getElementById('local-history-banner');
          if (banner) {
            document.getElementById('local-score-summary').textContent = `실전 환산: ${data.scoreScaledEstimate || 0} / 180점 (정답 ${data.correctCount || 0} · 오답 ${data.wrongCount || 0})`;
            document.getElementById('local-date-summary').textContent = `${data.examDate || ''} 응시`;
            banner.classList.remove('hidden');
          }
        }
      } catch (e) {
        console.warn('Could not load previous local result', e);
      }
    }

    function loadLocalExamResult(filterType = 'wrong') {
      try {
        const raw = localStorage.getItem('n2_past_exam_202312_result');
        if (!raw) return;
        const data = JSON.parse(raw);
        if (!sessionQuestions || sessionQuestions.length === 0) {
          initExam();
        }
        userAnswers = data.questionsRecord.map(q => q.userAnswer);
        questionDwellTimes = data.questionsRecord.map(q => q.dwellTimeSeconds || 0);
        section1ElapsedSeconds = data.elapsedSeconds ? Math.round(data.elapsedSeconds * 0.6) : 3600;
        section2ElapsedSeconds = data.elapsedSeconds ? (data.elapsedSeconds - section1ElapsedSeconds) : 2400;

        document.getElementById('screen-intro').classList.add('hidden');
        document.getElementById('screen-quiz').classList.add('hidden');
        document.getElementById('screen-break').classList.add('hidden');
        document.getElementById('screen-listening-intro').classList.add('hidden');
        document.getElementById('screen-result').classList.remove('hidden');

        calculateAndRenderResults();
        renderAllExplanations(filterType);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } catch (e) {
        console.error('Failed to load local result', e);
      }
    }

    function saveResultToLocal(payload) {
      try {
        localStorage.setItem('n2_past_exam_202312_result', JSON.stringify(payload));
      } catch (e) {
        console.warn('Failed to save to localStorage', e);
      }
    }

    function restartExamFresh() {
      checkExamPin(() => {
        initExam();
        section1RemainingSeconds = 105 * 60;
        section1ElapsedSeconds = 0;
        section2ElapsedSeconds = 0;
        currentQuestionIndex = 0;
        startSection1();
      });
    }
"""

if 'saveResultToLocal' not in content2312:
    content2312 = content2312.replace(
        'function initExam() {',
        pin_js + '\n' + storage2312_js + '\n    function initExam() {'
    )

# Also ensure copyResultJSON saves to localStorage in 2023.12
content2312 = content2312.replace(
    'const resultPayload = {',
    'saveResultToLocal(resultPayload);\n      const resultPayload = {'
)

# And call checkPreviousResult in DOMContentLoaded
content2312 = content2312.replace(
    'initExam();',
    'initExam();\n      checkPreviousResult();'
)

with open(p2312, 'w', encoding='utf-8') as f:
    f.write(content2312)

with open('quiz_sites/n2-past-exam-202312-mock.html', 'w', encoding='utf-8') as f:
    f.write(content2312)

print('Updated 2023.12 exam successfully!')
