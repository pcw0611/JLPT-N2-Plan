// State Variables
    let sessionQuestions = [];
    let currentIndex = 0;
    let userAnswers = []; // null: unans, 0..3: index
    let questionDwellTimes = [];
    
    // Exam Phases: 'intro' -> 'section1' -> 'break' -> 'section2' -> 'result'
    let currentPhase = 'intro';

    // Section 1 Timer (105 minutes countdown)
    let section1TimeLimitSeconds = 105 * 60; // 105분
    let section1RemainingSeconds = section1TimeLimitSeconds;
    let section1TimerInterval = null;
    let section1ElapsedSeconds = 0;

    // Break Timer (10 minutes countdown)
    let breakRemainingSeconds = 10 * 60;
    let breakTimerInterval = null;

    // Section 2 Continuous Listening Timer
    let section2StartTime = 0;
    let section2ElapsedSeconds = 0;
    let section2TimerInterval = null;

    let questionTimerInterval = null;
    let isExamFinished = false;

    // Continuous Listening Engine State
    let isListeningPaused = false;
    let listeningCountdownTimer = null;
    let remainingCountdownSeconds = 12;

    function toggleTheme() {
      document.body.classList.toggle('dark-theme');
    }

    function initExam() {
      sessionQuestions = RAW_QUESTIONS.map(q => ({
        ...q,
        sessionChoices: [...q.choices],
        sessionAnswer: q.answer
      }));

      userAnswers = new Array(sessionQuestions.length).fill(null);
      questionDwellTimes = new Array(sessionQuestions.length).fill(0);
    }

    // =========================================================================
    // Phase 1: Section 1 (言語知識・読解 1~75번, 105분)
    // =========================================================================
    function startSection1() {
      currentPhase = 'section1';
      document.getElementById('screen-intro').classList.add('hidden');
      document.getElementById('screen-break').classList.add('hidden');
      document.getElementById('screen-quiz').classList.remove('hidden');

      document.getElementById('badge-period-name').textContent = '第1限 (1교시)';
      document.getElementById('badge-section-title').textContent = '言語知識（文字・語彙・文法）・読解';
      document.getElementById('badge-listening-onair').classList.add('hidden');
      document.getElementById('listening-status-panel').classList.add('hidden');
      document.getElementById('section1-actions').classList.remove('hidden');
      document.getElementById('section2-actions').classList.add('hidden');
      document.getElementById('q-total-period-num').textContent = '75';

      // 105분 카운트다운 타이머
      updateSection1TimerDisplay();
      section1TimerInterval = setInterval(() => {
        section1RemainingSeconds--;
        section1ElapsedSeconds++;
        updateSection1TimerDisplay();

        if (section1RemainingSeconds <= 0) {
          clearInterval(section1TimerInterval);
          alert('第1限（言語知識・読解）の試験時間(105分)が終了しました。休憩時間に入ります。\n(1교시 105분이 종료되었습니다. 휴식 시간으로 이동합니다.)');
          finishSection1();
        }
      }, 1000);

      questionTimerInterval = setInterval(() => {
        if (!isExamFinished && currentPhase !== 'break') {
          questionDwellTimes[currentIndex] = (questionDwellTimes[currentIndex] || 0) + 1;
        }
      }, 1000);

      renderPaletteGrid();
      loadQuestion(0);
    }

    function updateSection1TimerDisplay() {
      const m = String(Math.floor(section1RemainingSeconds / 60)).padStart(2, '0');
      const s = String(section1RemainingSeconds % 60).padStart(2, '0');
      document.getElementById('period-timer').textContent = `${m}:${s}`;
    }

    function confirmFinishSection1() {
      finishSection1();
    }

    function finishSection1() {
      if (section1TimerInterval) clearInterval(section1TimerInterval);
      showBreakScreen();
    }

    function resumeSection1() {
      if (breakTimerInterval) clearInterval(breakTimerInterval);
      currentPhase = 'section1';
      document.getElementById('screen-break').classList.add('hidden');
      document.getElementById('screen-quiz').classList.remove('hidden');

      // Restart section 1 timer interval
      updateSection1TimerDisplay();
      section1TimerInterval = setInterval(() => {
        section1RemainingSeconds--;
        section1ElapsedSeconds++;
        updateSection1TimerDisplay();

        if (section1RemainingSeconds <= 0) {
          clearInterval(section1TimerInterval);
          finishSection1();
        }
      }, 1000);

      renderPaletteGrid();
      loadQuestion(currentIndex);
    }

    // =========================================================================
    // Phase 2: Intermission (휴식 시간)
    // =========================================================================
    function showBreakScreen() {
      currentPhase = 'break';
      document.getElementById('screen-quiz').classList.add('hidden');
      document.getElementById('screen-break').classList.remove('hidden');

      // 1교시 통계 요약
      const s1Answers = userAnswers.slice(0, 75);
      const markedCount = s1Answers.filter(a => a !== null).length;
      document.getElementById('break-stat-marked').textContent = `${markedCount} / 75 問`;

      const m = String(Math.floor(section1ElapsedSeconds / 60)).padStart(2, '0');
      const s = String(section1ElapsedSeconds % 60).padStart(2, '0');
      document.getElementById('break-stat-time').textContent = `${m}:${s}`;

      // 10분 휴식 타이머
      breakRemainingSeconds = 10 * 60;
      updateBreakTimerDisplay();
      breakTimerInterval = setInterval(() => {
        breakRemainingSeconds--;
        updateBreakTimerDisplay();

        if (breakRemainingSeconds <= 0) {
          clearInterval(breakTimerInterval);
          alert('休憩時間が終了しました。第2限（聴解）を開始します。\n(휴식 시간이 종료되었습니다. 2교시 청해 시험을 시작합니다.)');
          startSection2();
        }
      }, 1000);
    }

    function updateBreakTimerDisplay() {
      const m = String(Math.floor(breakRemainingSeconds / 60)).padStart(2, '0');
      const s = String(breakRemainingSeconds % 60).padStart(2, '0');
      document.getElementById('break-countdown-timer').textContent = `${m}:${s}`;
    }

    // =========================================================================
    // Phase 3: Section 2 (聴解 公式 オープニング イントロ & 本試験)
    // =========================================================================
    function startSection2() {
      if (breakTimerInterval) clearInterval(breakTimerInterval);
      currentPhase = 'listening_intro';

      document.getElementById('screen-break').classList.add('hidden');
      document.getElementById('screen-quiz').classList.add('hidden');
      document.getElementById('screen-listening-intro').classList.remove('hidden');

      playListeningIntroAudio();
    }

    function playListeningIntroAudio() {
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();

      const voices = window.speechSynthesis.getVoices().filter(v => v.lang.startsWith('ja'));
      const introScript = [
        "これより、日本語能力試験、エヌにの、聴解試験を始めます。",
        "問題用紙を開けてください。問題用紙に汚れや破れがある場合、または印刷がはっきりしない場合は、手を挙げてください。",
        "音の大きさを確かめます。音が聞こえにくい場合は、手を挙げてください。…… 天気がいいから、散歩しましょう。…… いかがですか。よろしいですか。",
        "それでは、始めます。"
      ];

      let idx = 0;
      function speakLine() {
        if (currentPhase !== 'listening_intro') return;
        if (idx >= introScript.length) {
          setTimeout(() => {
            if (currentPhase === 'listening_intro') {
              startListeningQuestions();
            }
          }, 1200);
          return;
        }

        const utter = new SpeechSynthesisUtterance(introScript[idx]);
        utter.lang = 'ja-JP';
        utter.rate = 0.95;
        utter.pitch = 0.95;
        if (voices.length > 0) utter.voice = voices[0];

        utter.onend = () => {
          idx++;
          setTimeout(speakLine, 700);
        };
        utter.onerror = () => {
          idx++;
          speakLine();
        };

        window.speechSynthesis.speak(utter);
      }

      speakLine();
    }

    function skipListeningIntro() {
      window.speechSynthesis && window.speechSynthesis.cancel();
      startListeningQuestions();
    }

    function startListeningQuestions() {
      currentPhase = 'section2';
      document.getElementById('screen-listening-intro').classList.add('hidden');
      document.getElementById('screen-quiz').classList.remove('hidden');

      document.getElementById('badge-period-name').textContent = '第2限 (2교시)';
      document.getElementById('badge-section-title').textContent = '聴解 (실시간 방송 진행)';
      document.getElementById('badge-listening-onair').classList.remove('hidden');
      document.getElementById('listening-status-panel').classList.remove('hidden');
      document.getElementById('section1-actions').classList.add('hidden');
      document.getElementById('section2-actions').classList.remove('hidden');
      document.getElementById('timer-icon').textContent = '⏱️ 진행시간';
      document.getElementById('q-total-period-num').textContent = '107';

      section2StartTime = Date.now();
      section2TimerInterval = setInterval(() => {
        section2ElapsedSeconds = Math.floor((Date.now() - section2StartTime) / 1000);
        const m = String(Math.floor(section2ElapsedSeconds / 60)).padStart(2, '0');
        const s = String(section2ElapsedSeconds % 60).padStart(2, '0');
        document.getElementById('period-timer').textContent = `${m}:${s}`;
      }, 1000);

      renderPaletteGrid();
      // 청해 첫 문제(75번 인덱스 = 76번 문항) 로드 및 자동 방송 개시
      loadQuestion(75);
    }

    // =========================================================================
    // Question Loader & Renderer
    // =========================================================================
    function loadQuestion(index) {
      currentIndex = index;
      const q = sessionQuestions[index];

      // Reset any active listening countdown
      if (listeningCountdownTimer) {
        clearInterval(listeningCountdownTimer);
        listeningCountdownTimer = null;
      }
      window.speechSynthesis && window.speechSynthesis.cancel();

      // Header info
      document.getElementById('badge-problem-no').textContent = q.problemNo || '問題';
      document.getElementById('badge-part-name').textContent = `(${ q.part || '' })`;
      document.getElementById('q-curr-num').textContent = index + 1;
      document.getElementById('q-side-badge').textContent = `問 ${index + 1} / 107`;

      // Instruction & Prompt Rendering (공식 고사장 문제지 N2L.pdf와 100% 동일한 완벽 싱크로)
      const instBox = document.getElementById('q-instruction');
      const promptEl = document.getElementById('q-prompt');
      const isListening = currentPhase === 'section2';

      if (isListening) {
        const meta = getListeningMeta(index);

        // 1. Instruction: 개별 질문 문장을 절대 노출하지 않고 대문항 공통 공식 지시문만 표시!
        if (meta.probNo === 1) {
          instBox.textContent = '問題１では、まず質問を聞いてください。それから話を聞いて、問題用紙の１から４の中から、最もよいものを一つ選んでください。';
        } else if (meta.probNo === 2) {
          instBox.textContent = '問題２では、まず質問を聞いてください。そのあと、問題用紙の選択肢を読んでください。読む時間があります。それから話を聞いて、問題用紙の１から４の中から、最もよいものを一つ選んでください。';
        } else if (meta.probNo === 3) {
          instBox.textContent = '問題３では、問題用紙に何も印刷されていません。この問題は、全体としてどんな内容かを聞く問題です。話の前に質問はありません。まず話を聞いてください。それから、質問と選択肢を聞いて、１から４の中から、最もよいものを一つ選んでください。';
        } else if (meta.probNo === 4) {
          instBox.textContent = '問題４では、問題用紙に何も印刷されていません。まず文を聞いてください。それから、その返事を聞いて、１から３の中から、最もよいものを一つ選んでください。';
        } else if (meta.probNo === 5) {
          instBox.textContent = '問題５では、長めの話を聞きます。この問題には、練習はありません。メモをとってもかまいません。';
        }
        instBox.classList.remove('hidden');

        // 2. Prompt (문제지 좌측 시험지): 실제 시험지에 맞게 본문/질문/상황문 일절 블라인드 처리
        if (meta.probNo === 1) {
          // 문제 1: 시험지에는 질문도 대화도 없고 메모란만 제공 (선택지만 우측에 인쇄)
          promptEl.innerHTML = `
            <div class="py-8 px-4 text-center border border-dashed border-neutral-300 rounded bg-neutral-50 space-y-3">
              <div class="font-serif font-bold text-neutral-800 text-sm tracking-wide">
                問題１（${meta.itemNo}番）
              </div>
              <div class="text-xs text-neutral-500 leading-relaxed max-w-md mx-auto">
                ※ 質問および会話文は問題用紙に印刷されていません。<br>
                音声を聞き、右側の【解答欄（選択肢）】から最もよいものを一つ選んでください。
              </div>
              <div class="pt-6 mt-4 border-t border-neutral-200 text-xs text-neutral-400 font-mono">
                【 メモ欄 (MEMO) 】
              </div>
            </div>
          `;
        } else if (meta.probNo === 2) {
          // 문제 2: 시험지에는 질문도 대화도 없고 메모란만 제공 (선택지는 14초간 읽을 수 있게 인쇄)
          promptEl.innerHTML = `
            <div class="py-8 px-4 text-center border border-dashed border-neutral-300 rounded bg-neutral-50 space-y-3">
              <div class="font-serif font-bold text-neutral-800 text-sm tracking-wide">
                問題２（${meta.itemNo}番）
              </div>
              <div class="text-xs text-neutral-500 leading-relaxed max-w-md mx-auto">
                ※ まず質問を聞き、右側の【解答欄（選択肢）】を読む時間（約14秒）のあとに話を聞いてください。
              </div>
              <div class="pt-6 mt-4 border-t border-neutral-200 text-xs text-neutral-400 font-mono">
                【 メモ欄 (MEMO) 】
              </div>
            </div>
          `;
        } else if (meta.probNo === 3) {
          // 문제 3: 시험지 완전 백지! 상황설명·질문·선택지 모두 음성으로만 청취!
          promptEl.innerHTML = `
            <div class="py-8 px-4 text-center border-2 border-dashed border-neutral-300 rounded bg-neutral-50 space-y-3">
              <div class="font-serif font-bold text-neutral-800 text-sm sm:text-base tracking-wide">
                問題３（${meta.itemNo}番）では、問題用紙に何も印刷されていません。
              </div>
              <div class="text-xs text-neutral-500 leading-relaxed max-w-md mx-auto">
                状況説明・話・質問・選択肢はすべて音声でのみ放送されます。<br>
                メモ欄を活用し、放送を聞いて１から４の中から選んでください。
              </div>
              <div class="pt-6 mt-4 border-t border-neutral-200 text-xs text-neutral-400 font-mono">
                【 メモ欄 (MEMO) 】
              </div>
            </div>
          `;
        } else if (meta.probNo === 4) {
          // 문제 4: 시험지 완전 백지! 발화 및 선택지 모두 음성으로만 청취!
          promptEl.innerHTML = `
            <div class="py-8 px-4 text-center border-2 border-dashed border-neutral-300 rounded bg-neutral-50 space-y-3">
              <div class="font-serif font-bold text-neutral-800 text-sm sm:text-base tracking-wide">
                問題４（${meta.itemNo}番）では、問題用紙に何も印刷されていません。
              </div>
              <div class="text-xs text-neutral-500 leading-relaxed max-w-md mx-auto">
                短い文を聞いたあと、音声で流れる返事を聞いて、１から３の中から最もよいものを選んでください。
              </div>
              <div class="pt-6 mt-4 border-t border-neutral-200 text-xs text-neutral-400 font-mono">
                【 メモ欄 (MEMO) 】
              </div>
            </div>
          `;
        } else if (meta.probNo === 5 && !meta.hasPrintedChoices) {
          // 문제 5의 1번, 2번: 시험지 완전 백지! 질문과 선택지 모두 음성 청취!
          promptEl.innerHTML = `
            <div class="py-8 px-4 text-center border-2 border-dashed border-neutral-300 rounded bg-neutral-50 space-y-3">
              <div class="font-serif font-bold text-neutral-800 text-sm sm:text-base tracking-wide">
                問題５（${meta.itemNo}番）では、問題用紙に何も印刷されていません。
              </div>
              <div class="text-xs text-neutral-500 leading-relaxed max-w-md mx-auto">
                長めの話を聞きます。話のあとに質問と選択肢がすべて音声で放送されます。<br>
                メモをとってもかまいません。１から４の中から最もよいものを一つ選んでください。
              </div>
              <div class="pt-6 mt-4 border-t border-neutral-200 text-xs text-neutral-400 font-mono">
                【 メモ欄 (MEMO) 】
              </div>
            </div>
          `;
        } else if (meta.probNo === 5 && meta.hasPrintedChoices) {
          // 문제 5의 3번: 시험지에 質問1, 質問2와 각각의 1~4번 선택지가 인쇄됨
          promptEl.innerHTML = `
            <div class="py-6 px-4 text-center border border-dashed border-neutral-300 rounded bg-neutral-50 space-y-2">
              <div class="font-serif font-bold text-neutral-700 text-sm">
                問題５（3番 - 質問${meta.qNum === 106 ? '1' : '2'}）
              </div>
              <div class="text-xs text-neutral-500 leading-relaxed">
                右側の【解答欄（選択肢）】に印刷された選択肢を見ながら、放送される質問に答えてください。
              </div>
              <div class="pt-6 mt-4 border-t border-neutral-200 text-xs text-neutral-400 font-mono">
                【 メモ欄 (MEMO) 】
              </div>
            </div>
          `;
        }
      } else {
        // 1교시(언어지식·독해)
        if (q.instruction) {
          instBox.textContent = q.instruction;
          instBox.classList.remove('hidden');
        } else {
          instBox.classList.add('hidden');
        }
        promptEl.textContent = q.prompt;
      }

      // Listening vs Section 1 controls
      if (isListening) {
        document.getElementById('btn-prev').disabled = true; // 청해는 이전 문제 복귀 불가
        startContinuousListeningForQuestion(index);
      } else {
        document.getElementById('btn-prev').disabled = index === 0;
      }

      // Render OMR Choices in Right Column
      renderChoices(index);

      // Next / Submit button text
      const btnNextText = document.getElementById('btn-next-text');
      if (currentPhase === 'section1') {
        if (index === 74) {
          btnNextText.textContent = '第1限 終了へ →';
        } else {
          btnNextText.textContent = '次の問題 →';
        }
      } else {
        if (index === sessionQuestions.length - 1) {
          btnNextText.textContent = '全試験 提出 →';
        } else {
          btnNextText.textContent = '次へ (即時移動) →';
        }
      }

      updatePaletteStatus();
    }

    function renderChoices(index) {
      const q = sessionQuestions[index];
      const choicesContainer = document.getElementById('q-choices');
      choicesContainer.innerHTML = '';

      const isListening = currentPhase === 'section2';
      const meta = isListening ? getListeningMeta(index) : null;
      // 문제 3과 문제 4: 실제 시험지에도 선택지가 인쇄되지 않고 오직 음성으로만 나옴 (번호만 마킹)
      const hideChoiceText = isListening && meta && (
        meta.probNo === 3 || 
        meta.probNo === 4 || 
        (meta.probNo === 5 && !meta.hasPrintedChoices)
      );

      q.sessionChoices.forEach((choiceText, cIdx) => {
        const btn = document.createElement('button');
        const isSelected = userAnswers[index] === cIdx;
        btn.className = `omr-choice-btn w-full p-3.5 rounded text-left text-xs sm:text-sm flex items-center justify-between ${isSelected ? 'selected' : ''}`;
        
        let labelHtml = '';
        if (hideChoiceText) {
          labelHtml = `
            <div class="flex items-center gap-3">
              <span class="omr-circle font-bold">${cIdx + 1}</span>
              <span class="text-xs text-neutral-400 font-serif italic tracking-wide">（音声を聞いてマーク）</span>
            </div>
          `;
        } else {
          labelHtml = `
            <div class="flex items-center gap-3">
              <span class="omr-circle">${cIdx + 1}</span>
              <span class="leading-relaxed">${escapeHtml(choiceText)}</span>
            </div>
          `;
        }

        btn.innerHTML = `
          ${labelHtml}
          ${isSelected ? '<span class="text-xs font-bold font-mono">● 記入済</span>' : ''}
        `;
        btn.onclick = () => selectAnswer(cIdx);
        choicesContainer.appendChild(btn);
      });

      // [？ 分からない] ボタン (PROJECT_GUIDE 規約遵守: 誤答・分からない・未回答の3者厳密分離)
      const unkBtn = document.createElement('button');
      const isUnknown = userAnswers[index] === 'unknown';
      unkBtn.className = `w-full p-2.5 mt-2 rounded border border-dashed text-xs font-sans text-center transition-all ${
        isUnknown ? 'bg-amber-100 border-amber-500 font-bold text-amber-900 shadow-inner' : 'bg-neutral-50 hover:bg-neutral-100 text-neutral-600 border-neutral-400'
      }`;
      unkBtn.innerHTML = isUnknown ? '❓ 分からない (マーク済 · D+1 復習対象)' : '？ 分からない (모름)';
      unkBtn.onclick = () => selectAnswer('unknown');
      choicesContainer.appendChild(unkBtn);
    }

    function selectAnswer(ans) {
      if (userAnswers[currentIndex] === ans) {
        userAnswers[currentIndex] = null; // Toggle unselect
      } else {
        userAnswers[currentIndex] = ans;
      }
      updatePaletteStatus();
      renderChoices(currentIndex);
    }

    function prevQuestion() {
      if (currentPhase === 'section1' && currentIndex > 0) {
        loadQuestion(currentIndex - 1);
      }
    }

    function nextQuestion() {
      if (currentPhase === 'section1') {
        if (currentIndex < 74) {
          loadQuestion(currentIndex + 1);
        } else {
          confirmFinishSection1();
        }
      } else if (currentPhase === 'section2') {
        // 청해 시험 중에는 방송 진행에 따라 자동 전환되므로 임의 건너뛰기 차단
        alert('※ 聴解試験では、放送の進行に合わせて自動的に次の問題へ進みます。手動でのスキップはできません。\n(청해 시험에서는 방송 흐름에 맞춰 자동 전환됩니다. 수동 건너뛰기는 불가합니다.)');
      }
    }

    function goToNextUnansweredInSection1() {
      const s1Answers = userAnswers.slice(0, 75);
      const nextUnans = s1Answers.findIndex((ans, idx) => idx > currentIndex && ans === null);
      if (nextUnans !== -1) {
        loadQuestion(nextUnans);
        return;
      }
      const anyUnans = s1Answers.findIndex(ans => ans === null);
      if (anyUnans !== -1) {
        loadQuestion(anyUnans);
      } else {
        alert('第1限(1~75問)のすべての問題にマークされています。(1교시 모든 문항에 마킹하셨습니다.)');
      }
    }

    // =========================================================================
    // Palette Rendering (교시별 분리: 1교시는 1~75만, 2교시는 76~107만)
    // =========================================================================
    function renderPaletteGrid() {
      const grid = document.getElementById('palette-grid');
      grid.innerHTML = '';

      let startIdx = 0;
      let endIdx = 75;

      if (currentPhase === 'section2') {
        startIdx = 75;
        endIdx = 107;
        document.getElementById('palette-period-title').textContent = '第2限 聴解パレット (76 ~ 107)';
      } else {
        document.getElementById('palette-period-title').textContent = '第1限 パレット (1 ~ 75)';
      }

      for (let idx = startIdx; idx < endIdx; idx++) {
        const dot = document.createElement('button');
        dot.id = `palette-dot-${idx}`;
        dot.textContent = idx + 1;
        dot.className = 'text-[10px] font-mono h-5 rounded border border-neutral-400 flex items-center justify-center font-bold bg-white text-neutral-600';
        
        if (currentPhase === 'section2') {
          // 청해 중에는 임의 점프/되돌아가기 불가!
          dot.onclick = () => {
            alert('※ 聴解試験では、問題の再聴取や自由移動はできません。放送順に従って解答してください。\n(청해 시험에서는 임의 이동 및 다시듣기가 불가능합니다. 방송 순서에 따라 풀어주세요.)');
          };
        } else {
          dot.onclick = () => loadQuestion(idx);
        }

        grid.appendChild(dot);
      }

      updatePaletteStatus();
    }

    function updatePaletteStatus() {
      let startIdx = currentPhase === 'section2' ? 75 : 0;
      let endIdx = currentPhase === 'section2' ? 107 : 75;
      let answeredCount = 0;

      for (let idx = startIdx; idx < endIdx; idx++) {
        const dot = document.getElementById(`palette-dot-${idx}`);
        const ans = userAnswers[idx];
        const isCur = idx === currentIndex;

        if (typeof ans === 'number' || ans === 'unknown') answeredCount++;

        if (!dot) continue;

        let base = 'text-[10px] font-mono h-5 rounded border flex items-center justify-center font-bold ';
        if (isCur) {
          base += 'ring-2 ring-neutral-900 ';
        }

        if (typeof ans === 'number') {
          dot.className = base + 'bg-neutral-950 text-white border-neutral-950';
        } else if (ans === 'unknown') {
          dot.className = base + 'bg-amber-400 text-neutral-950 border-amber-500 font-bold';
        } else {
          dot.className = base + 'bg-white text-neutral-500 border-neutral-300';
        }
      }

      const totalPeriodQuestions = endIdx - startIdx;
      document.getElementById('palette-summary-count').textContent = `${answeredCount} / ${totalPeriodQuestions} 回答済`;
    }

    // =========================================================================
    // Continuous Listening Engine (실제 시험 100% 싱크로 공식 시퀀스 완벽 탑재)
    // =========================================================================
    function getListeningMeta(index) {
      const qNum = index + 1; // 76 ~ 107
      if (qNum >= 76 && qNum <= 80) {
        return { probNo: 1, itemNo: qNum - 75, isFirst: qNum === 76, name: "課題理解" };
      } else if (qNum >= 81 && qNum <= 86) {
        return { probNo: 2, itemNo: qNum - 80, isFirst: qNum === 81, name: "ポイント理解" };
      } else if (qNum >= 87 && qNum <= 91) {
        return { probNo: 3, itemNo: qNum - 86, isFirst: qNum === 87, name: "概要理解" };
      } else if (qNum >= 92 && qNum <= 103) {
        return { probNo: 4, itemNo: qNum - 91, isFirst: qNum === 92, name: "即時応答" };
      } else if (qNum >= 104 && qNum <= 107) {
        const map5 = { 104: 1, 105: 2, 106: 3, 107: 3 };
        const isPart3 = (qNum >= 106);
        return { 
          probNo: 5, 
          itemNo: map5[qNum], 
          qNum: qNum,
          isFirst: qNum === 104, 
          name: "統合理解",
          hasPrintedChoices: isPart3
        };
      }
      return null;
    }

    function extractPromptText(q) {
      let raw = (q.prompt || '').replace(/【[^】]+】\s*/g, '').trim();
      raw = raw.replace(/^(女性|男性|男の人|女の人|店員|客|先生|学生)：\s*/, '');
      return raw;
    }

    function extractOnlyQuestion(q) {
      const raw = extractPromptText(q);
      const parts = raw.split('。').map(s => s.trim()).filter(Boolean);
      if (parts.length > 1) {
        return parts[parts.length - 1] + '。';
      }
      return raw;
    }

    function startContinuousListeningForQuestion(index) {
      const q = sessionQuestions[index];
      if (!q.audio || q.audio.length === 0) return;

      const phaseText = document.getElementById('listening-phase-text');
      const progressBox = document.getElementById('countdown-container');
      const progressBar = document.getElementById('countdown-progress-bar');
      const countdownTimerText = document.getElementById('countdown-timer-text');

      progressBox.classList.add('opacity-40');
      progressBar.style.width = '100%';
      countdownTimerText.textContent = '待機中';

      if (!('speechSynthesis' in window)) {
        phaseText.textContent = '이 브라우저는 웹 음성(TTS)을 지원하지 않습니다.';
        return;
      }

      window.speechSynthesis.cancel();
      const voices = window.speechSynthesis.getVoices().filter(v => v.lang.startsWith('ja'));

      const meta = getListeningMeta(index);
      if (!meta) return;

      // 1. Prepare Announcement Speech (실제 시험 지시문 및 번호 호명)
      let announceText = '';
      if (meta.isFirst) {
        if (meta.probNo === 1) announceText = '問題1。では、まず質問を聞いてください。それから話を聞いて、1から4の中から、最もよいものを一つ選んでください。…… 1番。';
        else if (meta.probNo === 2) announceText = '問題2。では、まず質問を聞いてください。そのあと、選択肢を見てください。読む時間があります。…… 1番。';
        else if (meta.probNo === 3) announceText = '問題3。では、まず話を聞いてください。それから、質問と選択肢を聞いて、最もよいものを一つ選んでください。…… 1番。';
        else if (meta.probNo === 4) announceText = '問題4。まず文を聞いてください。それから、返事を聞いて、1から3の中から選んでください。…… 1番。';
        else if (meta.probNo === 5) announceText = '問題5。長めの話を聞きます。メモをとってもかまいません。…… 1番。';
      } else {
        announceText = `${meta.itemNo}番。`;
      }

      const labelText = meta.isFirst ? ('問題' + meta.probNo + ' 開始') : (meta.itemNo + '番');
      phaseText.textContent = `📢 放送案内: ${labelText}`;

      const utterAnnounce = new SpeechSynthesisUtterance(announceText);
      utterAnnounce.lang = 'ja-JP';
      utterAnnounce.rate = 0.95;
      utterAnnounce.pitch = 0.95;
      if (voices.length > 0) utterAnnounce.voice = voices[0];

      utterAnnounce.onend = () => {
        if (isListeningPaused) return;

        // 2초 숨고르기 준비 텀
        phaseText.textContent = '⏱️ 問題を聞く準備をしてください (2초 숨고르기)...';
        setTimeout(() => {
          if (isListeningPaused) return;
          executeListeningFlowForQuestion(q, meta, voices);
        }, 2000);
      };

      utterAnnounce.onerror = () => {
        executeListeningFlowForQuestion(q, meta, voices);
      };

      window.speechSynthesis.speak(utterAnnounce);
    }

    function executeListeningFlowForQuestion(q, meta, voices) {
      const phaseText = document.getElementById('listening-phase-text');

      if (meta.probNo === 1) {
        // [문제1: 과제이해] 질문 먼저 방송 -> 본문 대화 -> 질문 다시 방송 -> 12초 답변
        phaseText.textContent = '❓ 質問放送中 (먼저 질문을 들으세요)...';
        const qText = extractPromptText(q);
        const uQ = new SpeechSynthesisUtterance(qText);
        uQ.lang = 'ja-JP';
        uQ.rate = 0.95;
        if (voices.length > 0) uQ.voice = voices[0];
        uQ.onend = () => {
          setTimeout(() => {
            playAudioLines(q.audio, voices, () => {
              // 질문 반복 재낭독
              phaseText.textContent = '❓ 質問再放送中...';
              const repQ = new SpeechSynthesisUtterance(extractOnlyQuestion(q));
              repQ.lang = 'ja-JP';
              repQ.rate = 0.95;
              if (voices.length > 0) repQ.voice = voices[0];
              repQ.onend = () => startAnswerCountdown(12);
              repQ.onerror = () => startAnswerCountdown(12);
              window.speechSynthesis.speak(repQ);
            });
          }, 800);
        };
        uQ.onerror = () => {
          playAudioLines(q.audio, voices, () => startAnswerCountdown(12));
        };
        window.speechSynthesis.speak(uQ);

      } else if (meta.probNo === 2) {
        // [문제2: 포인트이해] 질문 먼저 방송 -> 14초 선택지 읽는 시간 -> "それから話を聞いてください" -> 대화 -> 질문 다시 방송 -> 12초 답변
        phaseText.textContent = '❓ 質問放送中 (먼저 질문을 들으세요)...';
        const qText = extractPromptText(q);
        const uQ = new SpeechSynthesisUtterance(qText);
        uQ.lang = 'ja-JP';
        uQ.rate = 0.95;
        if (voices.length > 0) uQ.voice = voices[0];
        uQ.onend = () => {
          startProblem2ChoiceReadingInterval(q, voices);
        };
        uQ.onerror = () => {
          startProblem2ChoiceReadingInterval(q, voices);
        };
        window.speechSynthesis.speak(uQ);

      } else if (meta.probNo === 3) {
        // [문제3: 개요이해] 본문 강연/독백 -> 질문 방송 -> 선택지 1~4번 음성 낭독 -> 12초 답변
        phaseText.textContent = '📻 話をよく聞いてください (본문 강연/독백)...';
        playAudioLines(q.audio, voices, () => {
          phaseText.textContent = '❓ 質問放送中...';
          const qText = extractOnlyQuestion(q);
          const uQ = new SpeechSynthesisUtterance('質問。' + qText);
          uQ.lang = 'ja-JP';
          uQ.rate = 0.95;
          if (voices.length > 0) uQ.voice = voices[0];
          uQ.onend = () => {
            speakChoicesSequence(q.choices, voices, 12);
          };
          uQ.onerror = () => {
            speakChoicesSequence(q.choices, voices, 12);
          };
          window.speechSynthesis.speak(uQ);
        });

      } else if (meta.probNo === 4) {
        // [문제4: 즉시응답] 질문 발화 1문장 -> 선택지 1~3번 음성 낭독 -> 6초 빠른 답변!
        phaseText.textContent = '📻 文を聞いてください (발화 듣기)...';
        playAudioLines(q.audio, voices, () => {
          speakChoicesSequence(q.choices, voices, 6);
        });

      } else if (meta.probNo === 5) {
        // [문제5: 통합이해] 1·2번은 선택지까지 전부 음성 낭독, 3번은 인쇄된 선택지 보고 풀기
        phaseText.textContent = '📻 総合的な会話を聞いてください (메モ可能)...';
        playAudioLines(q.audio, voices, () => {
          phaseText.textContent = '❓ 質問放送中...';
          const qText = extractPromptText(q);
          const uQ = new SpeechSynthesisUtterance(qText);
          uQ.lang = 'ja-JP';
          uQ.rate = 0.95;
          if (voices.length > 0) uQ.voice = voices[0];

          if (!meta.hasPrintedChoices) {
            // 1번, 2번 (104, 105): 질문 방송 후 선택지 1~4번 음성 낭독
            uQ.onend = () => {
              speakChoicesSequence(q.choices, voices, 12);
            };
            uQ.onerror = () => {
              speakChoicesSequence(q.choices, voices, 12);
            };
          } else {
            // 3번 (106, 107): 질문 방송 후 시험지 인쇄 선택지 보고 답변 12초
            uQ.onend = () => startAnswerCountdown(12);
            uQ.onerror = () => startAnswerCountdown(12);
          }
          window.speechSynthesis.speak(uQ);
        });
      }
    }

    function playAudioLines(audioList, voices, onComplete) {
      const phaseText = document.getElementById('listening-phase-text');
      phaseText.textContent = '📻 会話・問題 放送中...';

      let lineIdx = 0;
      function speakNextLine() {
        if (isListeningPaused) return;
        if (lineIdx >= audioList.length) {
          if (onComplete) onComplete();
          return;
        }

        const line = audioList[lineIdx];
        const utter = new SpeechSynthesisUtterance(line.text);
        utter.lang = 'ja-JP';
        utter.rate = 0.98;

        if (line.speaker === 2) {
          utter.pitch = 1.22;
        } else if (line.speaker === 3) {
          utter.pitch = 0.85;
        } else {
          utter.pitch = 1.0;
        }

        if (voices.length > 0) {
          utter.voice = voices[line.speaker % voices.length] || voices[0];
        }

        utter.onend = () => {
          lineIdx++;
          setTimeout(speakNextLine, 350);
        };

        utter.onerror = (e) => {
          console.error("Audio playback error:", e);
          phaseText.textContent = '⚠️ 音声の再生中にエラーが発生しました。ブラウザの音声設定を確認してください。';
          lineIdx++;
          setTimeout(speakNextLine, 500);
        };

        window.speechSynthesis.speak(utter);
      }

      speakNextLine();
    }

    function speakChoicesSequence(choices, voices, countdownSeconds) {
      const phaseText = document.getElementById('listening-phase-text');
      phaseText.textContent = '📢 選択肢を放送中 (선택지 낭독)...';

      let cIdx = 0;
      function speakNextChoice() {
        if (isListeningPaused) return;
        if (cIdx >= choices.length) {
          startAnswerCountdown(countdownSeconds);
          return;
        }

        const utter = new SpeechSynthesisUtterance(`${cIdx + 1}番、${choices[cIdx]}`);
        utter.lang = 'ja-JP';
        utter.rate = 0.96;
        if (voices.length > 0) utter.voice = voices[0];

        utter.onend = () => {
          cIdx++;
          setTimeout(speakNextChoice, 400);
        };

        utter.onerror = () => {
          cIdx++;
          speakNextChoice();
        };

        window.speechSynthesis.speak(utter);
      }

      speakNextChoice();
    }

    function startProblem2ChoiceReadingInterval(q, voices) {
      const phaseText = document.getElementById('listening-phase-text');
      const progressBox = document.getElementById('countdown-container');
      const progressBar = document.getElementById('countdown-progress-bar');
      const countdownTimerText = document.getElementById('countdown-timer-text');

      phaseText.textContent = '📖 選択肢を読む時間 (우측 선택지를 미리 읽으세요)...';
      progressBox.classList.remove('opacity-40');

      let readSeconds = 14;
      const totalRead = 14;
      countdownTimerText.textContent = `${readSeconds}秒`;
      progressBar.style.width = '100%';

      listeningCountdownTimer = setInterval(() => {
        if (isListeningPaused) return;
        readSeconds--;
        countdownTimerText.textContent = `${readSeconds}秒`;
        progressBar.style.width = `${(readSeconds / totalRead) * 100}%`;

        if (readSeconds <= 0) {
          clearInterval(listeningCountdownTimer);
          listeningCountdownTimer = null;
          progressBox.classList.add('opacity-40');

          const cue = new SpeechSynthesisUtterance('それから、話を聞いてください。');
          cue.lang = 'ja-JP';
          cue.rate = 0.95;
          if (voices.length > 0) cue.voice = voices[0];
          cue.onend = () => {
            playAudioLines(q.audio, voices, () => {
              phaseText.textContent = '❓ 質問再放送中...';
              const repQ = new SpeechSynthesisUtterance(extractOnlyQuestion(q));
              repQ.lang = 'ja-JP';
              repQ.rate = 0.95;
              if (voices.length > 0) repQ.voice = voices[0];
              repQ.onend = () => startAnswerCountdown(12);
              repQ.onerror = () => startAnswerCountdown(12);
              window.speechSynthesis.speak(repQ);
            });
          };
          window.speechSynthesis.speak(cue);
        }
      }, 1000);
    }

    function startAnswerCountdown(seconds = 12) {
      const phaseText = document.getElementById('listening-phase-text');
      const progressBox = document.getElementById('countdown-container');
      const progressBar = document.getElementById('countdown-progress-bar');
      const countdownTimerText = document.getElementById('countdown-timer-text');

      const isQuick = seconds <= 6;
      phaseText.textContent = isQuick 
        ? '⚡ 即時解答時間 (빠른 답변! 6초 후 바로 다음 번호로 넘어갑니다)' 
        : '⏳ 解答時間 (답을 선택하세요 - 시간 종료 시 다음 문제 자동 진행)';
      progressBox.classList.remove('opacity-40');

      remainingCountdownSeconds = seconds;
      const totalSeconds = seconds;
      countdownTimerText.textContent = `${remainingCountdownSeconds}秒`;
      progressBar.style.width = '100%';

      listeningCountdownTimer = setInterval(() => {
        if (isListeningPaused) return;

        remainingCountdownSeconds--;
        countdownTimerText.textContent = `${remainingCountdownSeconds}秒`;
        const pct = (remainingCountdownSeconds / totalSeconds) * 100;
        progressBar.style.width = `${pct}%`;

        if (remainingCountdownSeconds <= 0) {
          clearInterval(listeningCountdownTimer);
          listeningCountdownTimer = null;
          if (currentIndex < sessionQuestions.length - 1) {
            loadQuestion(currentIndex + 1);
          } else {
            finishAllExams();
          }
        }
      }, 1000);
    }

    function confirmSubmitAll() {
      finishAllExams();
    }

    function finishAllExams() {
      isExamFinished = true;
      if (section1TimerInterval) clearInterval(section1TimerInterval);
      if (breakTimerInterval) clearInterval(breakTimerInterval);
      if (section2TimerInterval) clearInterval(section2TimerInterval);
      if (questionTimerInterval) clearInterval(questionTimerInterval);
      if (listeningCountdownTimer) clearInterval(listeningCountdownTimer);
      window.speechSynthesis && window.speechSynthesis.cancel();

      // 방송 종료 아나운스 멘트
      const finishUtter = new SpeechSynthesisUtterance('これで、レベルN2の聴解試験を終わります。');
      finishUtter.lang = 'ja-JP';
      window.speechSynthesis && window.speechSynthesis.speak(finishUtter);

      document.getElementById('screen-quiz').classList.add('hidden');
      document.getElementById('screen-break').classList.add('hidden');
      document.getElementById('screen-result').classList.remove('hidden');

      renderResults();
    }

    // =========================================================================
    // Score & Explanations Renderer
    // =========================================================================
    function renderResults() {
      let correct = 0;
      let wrong = 0;
      let unknown = 0;
      let unanswered = 0;

      let vocabCorrect = 0, vocabTotal = 0, vocabTime = 0;
      let grammarCorrect = 0, grammarTotal = 0, grammarTime = 0;
      let readingCorrect = 0, readingTotal = 0, readingTime = 0;
      let listeningCorrect = 0, listeningTotal = 0, listeningTime = 0;

      sessionQuestions.forEach((q, idx) => {
        const userAns = userAnswers[idx];
        const time = questionDwellTimes[idx] || 0;

        if (q.part === '文字・語彙') {
          vocabTotal++;
          vocabTime += time;
          if (userAns === q.sessionAnswer) vocabCorrect++;
        } else if (q.part === '文法') {
          grammarTotal++;
          grammarTime += time;
          if (userAns === q.sessionAnswer) grammarCorrect++;
        } else if (q.part === '読解') {
          readingTotal++;
          readingTime += time;
          if (userAns === q.sessionAnswer) readingCorrect++;
        } else if (q.part === '聴解') {
          listeningTotal++;
          listeningTime += time;
          if (userAns === q.sessionAnswer) listeningCorrect++;
        }

        if (userAns === q.sessionAnswer) {
          correct++;
        } else if (userAns === 'unknown') {
          unknown++;
        } else if (userAns === null) {
          unanswered++;
        } else {
          wrong++;
        }
      });

      const total = sessionQuestions.length;
      const pct = ((correct / total) * 100).toFixed(1);

      document.getElementById('stat-total-score').textContent = `${correct} / ${total}`;
      document.getElementById('stat-total-percent').textContent = `正答率 ${pct}%`;

      const totalElapsed = section1ElapsedSeconds + section2ElapsedSeconds;
      const m = String(Math.floor(totalElapsed / 60)).padStart(2, '0');
      const s = String(totalElapsed % 60).padStart(2, '0');
      document.getElementById('stat-total-time').textContent = `${m}:${s}`;
      document.getElementById('stat-wrong-unanswered').textContent = `오답 ${wrong} / 모름 ${unknown} / 미응답 ${unanswered}`;
      document.getElementById('stat-review-count').textContent = `${wrong + unknown + unanswered} 問 (D+1 복습 대상)`;

      // Sectional stats
      document.getElementById('stat-section-vocab').textContent = `${vocabCorrect} / ${vocabTotal} (${vocabTotal ? ((vocabCorrect/vocabTotal)*100).toFixed(0) : 0}%)`;
      document.getElementById('stat-section-vocab-time').textContent = `${Math.round(vocabTime/60)}分 ${Math.round(vocabTime%60)}秒`;

      document.getElementById('stat-section-grammar').textContent = `${grammarCorrect} / ${grammarTotal} (${grammarTotal ? ((grammarCorrect/grammarTotal)*100).toFixed(0) : 0}%)`;
      document.getElementById('stat-section-grammar-time').textContent = `${Math.round(grammarTime/60)}分 ${Math.round(grammarTime%60)}秒`;

      document.getElementById('stat-section-reading').textContent = `${readingCorrect} / ${readingTotal} (${readingTotal ? ((readingCorrect/readingTotal)*100).toFixed(0) : 0}%)`;
      document.getElementById('stat-section-reading-time').textContent = `${Math.round(readingTime/60)}分 ${Math.round(readingTime%60)}秒`;

      document.getElementById('stat-section-listening').textContent = `${listeningCorrect} / ${listeningTotal} (${listeningTotal ? ((listeningCorrect/listeningTotal)*100).toFixed(0) : 0}%)`;
      document.getElementById('stat-section-listening-time').textContent = `${Math.round(listeningTime/60)}分 ${Math.round(listeningTime%60)}秒`;

      // Pass projection (110 / 180 points scaled approx: >= 61.1%)
      const passBadge = document.getElementById('stat-pass-status');
      const passDetail = document.getElementById('stat-pass-detail');
      const scaledScore = Math.round((correct / total) * 180);
      document.getElementById('stat-scaled-score').textContent = `${scaledScore} / 180 点`;

      // Sectional cutoff evaluation (각 영역 31.6% = 19/60점 미만 시 과락)
      const vocabRate = vocabTotal ? (vocabCorrect / vocabTotal) : 0;
      const grammarRate = grammarTotal ? (grammarCorrect / grammarTotal) : 0;
      const readingRate = readingTotal ? (readingCorrect / readingTotal) : 0;
      const listeningRate = listeningTotal ? (listeningCorrect / listeningTotal) : 0;
      const langRate = (vocabTotal + grammarTotal) ? ((vocabCorrect + grammarCorrect) / (vocabTotal + grammarTotal)) : 0;

      const hasCutoffRisk = (langRate < 0.316) || (readingRate < 0.316) || (listeningRate < 0.316);

      if (hasCutoffRisk) {
        passBadge.textContent = `기준점 미달 위험 (${scaledScore}点 추정)`;
        passBadge.className = 'text-2xl sm:text-3xl font-black font-serif text-red-600';
        passDetail.textContent = '특정 영역 득점률이 과락선(31.6%) 미만입니다. 영역별 최저점(19점) 보강이 최우선입니다.';
      } else if (scaledScore >= 110) {
        passBadge.textContent = `합격권 추정 (${scaledScore}点)`;
        passBadge.className = 'text-2xl sm:text-3xl font-black font-serif text-neutral-900';
        passDetail.textContent = '정답률 기준 목표 110점권 도달 · (※ 본 점수는 비공식 정답률 환산치이며 실제 시험은 득점등화가 적용됩니다)';
      } else if (scaledScore >= 90) {
        passBadge.textContent = `경계선 추정 (${scaledScore}点)`;
        passBadge.className = 'text-2xl sm:text-3xl font-black font-serif text-neutral-800';
        passDetail.textContent = '합격선(90점) 근접 · 110점 안정권까지 취약 영역 보강 필요';
      } else {
        passBadge.textContent = `보강 필요 (${scaledScore}点)`;
        passBadge.className = 'text-2xl sm:text-3xl font-black font-serif text-neutral-700';
        passDetail.textContent = '개념 누수 점검 및 어휘·문법 반복 복습 권고';
      }

      // First period (1~75) vs Second period (76~107)
      const firstAnswers = userAnswers.slice(0, 75);
      const secondAnswers = userAnswers.slice(75);

      const firstCorrect = firstAnswers.filter((a, i) => a === sessionQuestions[i].sessionAnswer).length;
      const secondCorrect = secondAnswers.filter((a, i) => a === sessionQuestions[75 + i].sessionAnswer).length;

      const firstPct = ((firstCorrect / 75) * 100).toFixed(1);
      const secondPct = ((secondCorrect / 32) * 100).toFixed(1);

      const firstTime = section1ElapsedSeconds;
      const secondTime = section2ElapsedSeconds;

      document.getElementById('stat-first-half').textContent = `${firstCorrect} / 75 (${firstPct}%)`;
      document.getElementById('stat-first-half-time').innerHTML = `총 ${Math.round(firstTime/60)}분 · 문항당 ${((firstTime/75)).toFixed(1)}초`;

      document.getElementById('stat-second-half').textContent = `${secondCorrect} / 32 (${secondPct}%)`;
      document.getElementById('stat-second-half-time').innerHTML = `총 ${Math.round(secondTime/60)}분 · 문항당 ${((secondTime/32)).toFixed(1)}초`;

      const diff = (secondPct - firstPct).toFixed(1);
      let commentary = `<strong>지구력 분석:</strong> 1교시(필기) 대비 2교시(청해) 정답률 변화 <strong>${diff > 0 ? '+' + diff : diff}%p</strong>. `;
      if (diff < -15) {
        commentary += "1교시(105분) 후반부 및 2교시 청해에서 집중력 피로가 나타났습니다. 휴식 시간 동안의 이완 및 당분 보충 루틴이 권장됩니다.";
      } else if (diff >= -5) {
        commentary += "1교시와 2교시 청해의 집중도가 균형 있게 유지되었습니다. 155분 전 영역 시험을 완주할 수 있는 실전 멘탈을 갖추고 있습니다.";
      } else {
        commentary += "2교시 청해에서 약간의 체력 저하가 감지되었으나 실전 평균 수준입니다.";
      }
      document.getElementById('endurance-commentary').innerHTML = commentary;

      renderAllExplanations('all');
    }

    function renderAllExplanations(filterType) {
      const container = document.getElementById('explanations-list');
      container.innerHTML = '';

      sessionQuestions.forEach((q, idx) => {
        const userAns = userAnswers[idx];
        const isCorrect = userAns === q.sessionAnswer;
        const isUnknown = userAns === 'unknown'; const isUnanswered = userAns === null;

        if (filterType === 'wrong' && isCorrect) return;
        if (filterType === 'unknown' && !isUnknown) return;
        if (filterType === 'vocab' && q.part !== '文字・語彙') return;
        if (filterType === 'grammar' && q.part !== '文法') return;
        if (filterType === 'reading' && q.part !== '読解') return;
        if (filterType === 'listening' && q.part !== '聴解') return;

        const card = document.createElement('div');
        card.className = `jlpt-paper rounded-lg p-5 sm:p-6 space-y-4 ${
          isCorrect ? 'border-neutral-700' : 'border-neutral-950 bg-neutral-50'
        }`;

        const selectedText = typeof userAns === 'number' ? q.sessionChoices[userAns] : "未回答 (미마킹/모름)";
        const correctText = q.sessionChoices[q.sessionAnswer];

        let badgeStatus = '';
        if (isCorrect) {
          badgeStatus = '<span class="px-2 py-0.5 border border-neutral-900 bg-neutral-900 text-white font-bold text-xs rounded">○ 正解 (정답)</span>';
        } else if (isUnanswered) {
          badgeStatus = '<span class="px-2 py-0.5 border border-neutral-600 bg-neutral-200 text-neutral-800 font-bold text-xs rounded">- 未回答 (미마킹)</span>';
        } else {
          badgeStatus = '<span class="px-2 py-0.5 border border-neutral-900 text-neutral-900 font-bold text-xs rounded">✕ 誤答 (오답)</span>';
        }

        // Script block for listening
        let scriptHtml = '';
        if (q.audio && q.audio.length > 0) {
          scriptHtml = `
            <div class="p-3.5 rounded border border-neutral-400 bg-white space-y-1.5 text-xs">
              <div class="font-bold text-neutral-900 uppercase tracking-wider">🎧 聴解 大本 (스크립트 전문)</div>
              <div class="space-y-1 text-neutral-800 leading-relaxed font-sans">
                ${q.audio.map(a => `<div><strong class="text-neutral-950">${a.speaker === 1 ? '話者1(남/교사/안내)' : a.speaker === 2 ? '話者2(여/학생/손님)' : '解説'}:</strong> ${escapeHtml(a.text)}</div>`).join('')}
              </div>
            </div>
          `;
        }

        card.innerHTML = `
          <!-- Header -->
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-neutral-300 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="text-xs font-mono font-bold px-2 py-0.5 bg-neutral-900 text-white rounded">
                問 ${q.id}
              </span>
              <span class="text-xs font-bold text-neutral-900">
                ${escapeHtml(q.category || '')}
              </span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-[11px] text-neutral-500 font-mono">체류 ${questionDwellTimes[idx] || 0}초</span>
              ${badgeStatus}
            </div>
          </div>

          <!-- Problem & Reading Passage -->
          <div class="space-y-2 text-xs sm:text-sm leading-relaxed">
            ${q.instruction && q.instruction.length > 50 ? `<div class="p-3 bg-neutral-100 rounded border border-neutral-300 text-xs text-neutral-700 whitespace-pre-wrap">${escapeHtml(q.instruction)}</div>` : ''}
            <div class="font-medium text-neutral-950 whitespace-pre-wrap font-serif">${escapeHtml(q.prompt)}</div>
          </div>

          ${scriptHtml}

          <!-- Choices & Comparison -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs bg-white p-3 rounded border border-neutral-300">
            <div>
              <span class="text-neutral-500 block mb-0.5">사용자 마킹</span>
              <span class="font-bold text-neutral-900">
                ${escapeHtml(selectedText)}
              </span>
            </div>
            <div>
              <span class="text-neutral-500 block mb-0.5">공식 정답</span>
              <span class="font-bold text-neutral-950">
                ${q.sessionAnswer + 1}番: ${escapeHtml(correctText)}
              </span>
            </div>
          </div>

          <!-- Korean Detailed Explanations -->
          <div class="text-xs space-y-2 pt-1 text-neutral-700 leading-relaxed border-t border-neutral-200">
            <div>
              <strong class="text-neutral-950">【한국어 번역 및 핵심 해설】</strong><br>
              <span>${q.translation || ''}</span>
            </div>
            ${q.connection ? `<div><strong class="text-neutral-950">【접속·어휘 분석】</strong> <span>${q.connection}</span></div>` : ''}
            ${q.meaning ? `<div><strong class="text-neutral-950">【핵심 의미】</strong> <span>${q.meaning}</span></div>` : ''}
            ${q.trap ? `<div><strong class="text-neutral-950">【함정 분석】</strong> <span>${q.trap}</span></div>` : ''}
            ${q.contrast ? `<div><strong class="text-neutral-950">【유사 표현 비교】</strong> <span>${q.contrast}</span></div>` : ''}
            ${q.example ? `<div><strong class="text-neutral-950">【추가 예문】</strong> <span>${q.example}</span></div>` : ''}
            <div class="flex items-center justify-between pt-1.5 text-[11px] text-neutral-500 border-t border-neutral-200">
              <span>복습 주기: <strong>${q.nextReview || 'D+1: 2026-09-21'}</strong></span>
              <span class="font-mono">${q.sectionName} · ${q.problemNo}</span>
            </div>
          </div>
        `;

        container.appendChild(card);
      });
    }

    function copyResultJSON() {
      const total = sessionQuestions.length;
      let correct = 0, wrong = 0, unknown = 0, unanswered = 0;
      let vocabCorrect = 0, grammarCorrect = 0, readingCorrect = 0, listeningCorrect = 0;

      sessionQuestions.forEach((q, idx) => {
        const userAns = userAnswers[idx];
        if (userAns === q.sessionAnswer) {
          correct++;
          if (q.part === '文字・語彙') vocabCorrect++;
          if (q.part === '文法') grammarCorrect++;
          if (q.part === '読解') readingCorrect++;
          if (q.part === '聴解') listeningCorrect++;
        } else if (userAns === 'unknown') {
          unknown++;
        } else if (userAns === null) {
          unanswered++;
        } else {
          wrong++;
        }
      });

      const pct = ((correct / total) * 100).toFixed(1);
      const vocabTotal = 32, grammarTotal = 22, readingTotal = 21, listeningTotal = 32;
      const langRate = (vocabCorrect + grammarCorrect) / 54;
      const readingRate = readingCorrect / 21;
      const listeningRate = listeningCorrect / 32;
      const hasCutoffRisk = (langRate < 0.316) || (readingRate < 0.316) || (listeningRate < 0.316);

      const resultPayload = {
        examDate: new Date().toISOString().split('T')[0],
        examType: "공식 문제집 제2집 기반 실전모의고사 (개인학습용 / TTS)",
        examTitle: "JLPT N2 実戦模試（公式問題集 第2集ベース / 個人学習用）",
        provenanceNote: "출제 원안: 日本語能力試験 公式問題集 第2集(2018) 대조 / 개인학습용 TTS 구현 / 비공식 정답률 추정",
        totalQuestions: total,
        correctCount: correct,
        wrongCount: wrong,
        unknownCount: unknown,
        unansweredCount: unanswered,
        accuracyPercent: Number(pct),
        scoreScaledEstimate: Math.round((correct / total) * 180),
        hasSectionalCutoffRisk: hasCutoffRisk,
        elapsedSeconds: (typeof section1ElapsedSeconds !== 'undefined' ? section1ElapsedSeconds : 0) + (typeof section2ElapsedSeconds !== 'undefined' ? section2ElapsedSeconds : 0),
        sections: {
          vocab: { total: 32, correct: vocabCorrect },
          grammar: { total: 22, correct: grammarCorrect },
          reading: { total: 21, correct: readingCorrect },
          listening: { total: 32, correct: listeningCorrect }
        },
        questionsRecord: sessionQuestions.map((q, idx) => ({
          id: q.id,
          problemNo: q.problemNo,
          category: q.category,
          userAnswer: userAnswers[idx],
          officialAnswer: q.sessionAnswer,
          isCorrect: userAnswers[idx] === q.sessionAnswer,
          dwellTimeSeconds: questionDwellTimes[idx] || 0,
          nextReview: q.nextReview
        }))
      };

      navigator.clipboard.writeText(JSON.stringify(resultPayload, null, 2)).then(() => {
        alert('채점 결과 JSON이 클립보드에 복사되었습니다!\n대화창에 붙여넣어 주시면 학습 원장에 즉시 동기화 기록됩니다.');
      }).catch(err => {
        console.error(err);
        prompt('아래 JSON을 복사하세요:', JSON.stringify(resultPayload));
      });
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    // Auto-init on load
    window.addEventListener('DOMContentLoaded', () => {
      initExam();
    });
  </script>
</body>
</html>