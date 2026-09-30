import json
import re

AUDIO_PANEL_HTML = """            <!-- Listening ON-AIR Broadcast Status Panel (2교시 청해 시에만 노출) -->
            <div id="listening-status-panel" class="hidden border-2 border-neutral-900 bg-neutral-100 p-4 space-y-3 font-sans rounded">
              <div class="flex items-center justify-between border-b border-neutral-300 pb-2">
                <div class="flex items-center gap-2 text-neutral-900 font-bold text-xs">
                  <div class="flex items-end gap-0.5 h-4 text-neutral-900">
                    <span class="sound-bar"></span>
                    <span class="sound-bar"></span>
                    <span class="sound-bar"></span>
                    <span class="sound-bar"></span>
                    <span class="sound-bar"></span>
                  </div>
                  <span id="listening-phase-text">🎧 2023.12 本試験 公式 原本 聴解 音声</span>
                </div>
                <span class="px-2 py-0.5 bg-emerald-600 text-white rounded text-[10px] font-bold">실제 음원 완본 (영상 숨김 모드)</span>
              </div>

              <!-- Pure Exam Audio Controller (Video Frame Hidden for Authentic Exam Practice) -->
              <div class="bg-neutral-900 text-white p-4 rounded-lg space-y-3">
                <div class="flex items-center justify-between text-xs">
                  <div class="flex items-center gap-2 font-bold text-emerald-400">
                    <span id="audio-pulse-indicator" class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>2023.12 JLPT N2 本試験 公式 聴解 原本 音声 (42分 完本)</span>
                  </div>
                  <span class="text-[11px] text-neutral-400">실제 본시험 전문 성우 녹음</span>
                </div>

                <!-- Hidden YouTube Player (Audio Stream Only) -->
                <div style="position: absolute; width: 1px; height: 1px; opacity: 0.001; pointer-events: none; overflow: hidden; left: -9999px;">
                  <iframe 
                    id="yt-actual-audio" 
                    src="https://www.youtube-nocookie.com/embed/q5lzCC2k8-0?enablejsapi=1&autoplay=0&rel=0&controls=0" 
                    title="2023.12 JLPT N2 Listening Audio" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
                  </iframe>
                </div>

                <!-- Custom Audio Control Bar -->
                <div class="flex flex-wrap items-center gap-3 bg-neutral-800 p-3 rounded border border-neutral-700">
                  <button 
                    type="button" 
                    id="btn-play-toggle" 
                    onclick="toggleAudioPlay()" 
                    class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded text-xs transition cursor-pointer flex items-center gap-1.5 shadow">
                    <span id="btn-play-label">▶ 聴解 音声 再生</span>
                  </button>

                  <div class="text-[11px] text-neutral-300">
                    실제 시험장과 동일하게 <span class="text-amber-300 font-bold">영상 화면은 가려져 있으며, 오디오 음성만 방송</span>됩니다.
                  </div>
                </div>

                <!-- Fast Jump Section Markers -->
                <div class="flex flex-wrap items-center gap-1.5 pt-1 text-xs">
                  <span class="text-neutral-400 text-[11px] mr-1">대문항 바로가기:</span>
                  <button type="button" onclick="seekAudioTime(0)" class="px-2.5 py-1 rounded bg-neutral-800 hover:bg-neutral-700 text-neutral-200 border border-neutral-600 text-[11px] transition cursor-pointer">問題1 課題 (0:00)</button>
                  <button type="button" onclick="seekAudioTime(460)" class="px-2.5 py-1 rounded bg-neutral-800 hover:bg-neutral-700 text-neutral-200 border border-neutral-600 text-[11px] transition cursor-pointer">問題2 ポイント (7:40)</button>
                  <button type="button" onclick="seekAudioTime(1130)" class="px-2.5 py-1 rounded bg-neutral-800 hover:bg-neutral-700 text-neutral-200 border border-neutral-600 text-[11px] transition cursor-pointer">問題3 概要 (18:50)</button>
                  <button type="button" onclick="seekAudioTime(1755)" class="px-2.5 py-1 rounded bg-neutral-800 hover:bg-neutral-700 text-neutral-200 border border-neutral-600 text-[11px] transition cursor-pointer">問題4 即時 (29:15)</button>
                  <button type="button" onclick="seekAudioTime(2155)" class="px-2.5 py-1 rounded bg-neutral-800 hover:bg-neutral-700 text-neutral-200 border border-neutral-600 text-[11px] transition cursor-pointer">問題5 統合 (35:55)</button>
                </div>
              </div>

              <div class="text-[11px] text-neutral-600">
                ※ 기계식 브라우저 TTS가 아닌 2023.12 JLPT N2 실제 본시험 전문 성우 원본 음성입니다. 상단 플레이어로 음원을 재생하며 문제를 풀고 OMR에 마킹하세요.
              </div>
            </div>"""

AUDIO_JS = """let isYtPlaying = false;

    function toggleAudioPlay() {
      const iframe = document.getElementById('yt-actual-audio');
      const label = document.getElementById('btn-play-label');
      const pulse = document.getElementById('audio-pulse-indicator');
      
      if (!iframe || !iframe.contentWindow) return;

      if (isYtPlaying) {
        iframe.contentWindow.postMessage(JSON.stringify({
          event: 'command',
          func: 'pauseVideo',
          args: []
        }), '*');
        isYtPlaying = false;
        if (label) label.textContent = '▶ 聴解 音声 再生';
        if (pulse) {
          pulse.classList.remove('bg-emerald-400', 'animate-pulse');
          pulse.classList.add('bg-neutral-500');
        }
      } else {
        iframe.contentWindow.postMessage(JSON.stringify({
          event: 'command',
          func: 'playVideo',
          args: []
        }), '*');
        isYtPlaying = true;
        if (label) label.textContent = '⏸ 一時停止 (Pause)';
        if (pulse) {
          pulse.classList.add('bg-emerald-400', 'animate-pulse');
          pulse.classList.remove('bg-neutral-500');
        }
      }
    }

    function seekAudioTime(seconds) {
      const iframe = document.getElementById('yt-actual-audio');
      const label = document.getElementById('btn-play-label');
      const pulse = document.getElementById('audio-pulse-indicator');
      if (iframe && iframe.contentWindow) {
        iframe.contentWindow.postMessage(JSON.stringify({
          event: 'command',
          func: 'seekTo',
          args: [seconds, true]
        }), '*');
        iframe.contentWindow.postMessage(JSON.stringify({
          event: 'command',
          func: 'playVideo',
          args: []
        }), '*');
        isYtPlaying = true;
        if (label) label.textContent = '⏸ 一時停止 (Pause)';
        if (pulse) {
          pulse.classList.add('bg-emerald-400', 'animate-pulse');
          pulse.classList.remove('bg-neutral-500');
        }
      }
    }

    function startContinuousListeningForQuestion(index) {
      const phaseText = document.getElementById('listening-phase-text');
      if (window.speechSynthesis) window.speechSynthesis.cancel();

      const meta = getListeningMeta(index);
      if (meta) {
        phaseText.textContent = `🎧 2023.12 본시험 공식 실제 음원: [問題${meta.probNo} ${meta.itemNo}番]`;
      } else {
        phaseText.textContent = '🎧 2023.12 본시험 공식 실제 음원 진행 중...';
      }

      document.getElementById('btn-prev').disabled = (index === 72);
    }
"""

CLEAN_SECTION1_START_JS = """    function restartExamFresh() {
      initExam();
      section1RemainingSeconds = 105 * 60;
      section1ElapsedSeconds = 0;
      section2ElapsedSeconds = 0;
      currentIndex = 0;
      startSection1();
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
    // Phase 1: Section 1 (言語知識・読解 1~72번, 105분)
    // =========================================================================
    function startSection1() {
      if (!sessionQuestions || sessionQuestions.length === 0) {
        initExam();
      }
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
      document.getElementById('q-total-period-num').textContent = '72';

      // 105분 카운트다운 타이머
      updateSection1TimerDisplay();
      if (section1TimerInterval) clearInterval(section1TimerInterval);
      section1TimerInterval = setInterval(() => {
        section1RemainingSeconds--;
        section1ElapsedSeconds++;
        updateSection1TimerDisplay();

        if (section1RemainingSeconds <= 0) {
          clearInterval(section1TimerInterval);
          alert('第1限（言語知識・読解）の試験時間(105分)が終了しました。休憩時間に入ります。\\n(1교시 105분이 종료되었습니다. 휴식 시간으로 이동합니다.)');
          finishSection1();
        }
      }, 1000);

      if (questionTimerInterval) clearInterval(questionTimerInterval);
      questionTimerInterval = setInterval(() => {
        if (!isExamFinished && currentPhase !== 'break') {
          questionDwellTimes[currentIndex] = (questionDwellTimes[currentIndex] || 0) + 1;
        }
      }, 1000);

      renderPaletteGrid();
      loadQuestion(0);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }"""

CLEAN_SECTION2_START_JS = """    // =========================================================================
    // Phase 3: Section 2 (聴解 実戦 公式 音声 本試験)
    // =========================================================================
    function startSection2() {
      if (breakTimerInterval) clearInterval(breakTimerInterval);
      currentPhase = 'section2';

      document.getElementById('screen-break').classList.add('hidden');
      document.getElementById('screen-listening-intro').classList.add('hidden');
      document.getElementById('screen-quiz').classList.remove('hidden');

      document.getElementById('badge-period-name').textContent = '第2限 (2교시)';
      document.getElementById('badge-section-title').textContent = '聴解 (실시간 방송 진행)';
      document.getElementById('badge-listening-onair').classList.remove('hidden');
      document.getElementById('listening-status-panel').classList.remove('hidden');
      document.getElementById('section1-actions').classList.add('hidden');
      document.getElementById('section2-actions').classList.remove('hidden');
      document.getElementById('timer-icon').textContent = '⏱️ 진행시간';
      document.getElementById('q-total-period-num').textContent = '102';

      section2StartTime = Date.now();
      if (section2TimerInterval) clearInterval(section2TimerInterval);
      section2TimerInterval = setInterval(() => {
        section2ElapsedSeconds = Math.floor((Date.now() - section2StartTime) / 1000);
        const m = String(Math.floor(section2ElapsedSeconds / 60)).padStart(2, '0');
        const s = String(section2ElapsedSeconds % 60).padStart(2, '0');
        document.getElementById('period-timer').textContent = `${m}:${s}`;
      }, 1000);

      renderPaletteGrid();
      // 청해 첫 문제(72번 인덱스 = 73번 문항) 로드 및 자동 방송 개시
      loadQuestion(72);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function skipListeningIntro() {
      startSection2();
    }"""

def build():
    # 1. Load 2023_12.json
    with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
        data_2023_12 = json.load(f)

    questions = data_2023_12['questions']
    assert len(questions) == 102, f"Expected 102 questions, got {len(questions)}"

    # 2. Load base HTML template
    with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace title
    html = re.sub(
        r'<title>.*?</title>',
        '<title>JLPT N2 2023年 第2回 (12月) 本試験 全領域 実戦模試 (102問)</title>',
        html
    )

    # Replace header box titles
    html = html.replace(
        '日本語能力試験 公式問題集 第２集 原本対照 · 個人学習用 実戦模試',
        '2023年 第2回 (12月) JLPT N2 本試験 原本対照 · 個人学習用 実戦模試'
    )
    html = html.replace(
        'Official Practice Workbook Vol. 2 Base (ブラウザTTS聴解演習)',
        'December 2023 Official Exam Base (2023.12 本試験 公式 原本 聴解 音声 実装)'
    )
    html = html.replace(
        '브라우저 TTS 음성으로 쉼 없이 자동 진행',
        '2023년 12월 본시험 공식 전문 성우 원본 음성(42분 완본, 영상 숨김 순수 청해 모드)으로 진행'
    )
    html = html.replace(
        '75 問<br><span class="text-[11px] font-normal text-neutral-500">(問1~75)</span>',
        '72 問<br><span class="text-[11px] font-normal text-neutral-500">(問1~72)</span>'
    )
    html = html.replace(
        '32 問<br><span class="text-[11px] font-normal text-neutral-500">(問76~107)</span>',
        '30 問<br><span class="text-[11px] font-normal text-neutral-500">(問73~102)</span>'
    )
    html = html.replace(
        '<li><strong>1교시(1~75문항)</strong>',
        '<li><strong>1교시(1~72문항)</strong>'
    )
    html = html.replace(
        '<li><strong>2교시 청해(76~107문항) 실전 규격</strong>:',
        '<li><strong>2교시 청해(73~102문항) 실전 규격</strong>:'
    )
    html = html.replace(
        '76번부터 107번까지',
        '73번부터 102번까지'
    )
    html = html.replace(
        '107번의 12초 마킹 카운트다운이 종료되는 순간',
        '102번의 마킹이 종료되는 순간'
    )

    # Remove 9/20 historical banner from HTML
    hist_start = html.find('<!-- 9/20 DB Historical Record & Wrong Questions Banner -->')
    if hist_start != -1:
        hist_end = html.find('<!-- Start Button -->')
        if hist_end != -1:
            html = html[:hist_start] + html[hist_end:]

    # Remove PIN modal from HTML
    pin_modal_start = html.find('<!-- ================================================================= -->\n    <!-- PIN Auth Modal')
    if pin_modal_start == -1:
        pin_modal_start = html.find('<!-- PIN Auth Modal')
    if pin_modal_start != -1:
        pin_modal_end = html.find('</body>')
        if pin_modal_end != -1:
            html = html[:pin_modal_start] + html[pin_modal_end:]

    # Fix Start Button in HTML: direct startSection1, cursor-pointer, full width styling
    html = html.replace(
        '<button id="btn-start-exam" onclick="checkExamPin(() => startSection1())" class="w-full sm:w-2/3 py-4 bg-neutral-950 hover:bg-neutral-800 text-white font-serif font-bold text-lg rounded border-2 border-neutral-950 shadow-md transition-all tracking-widest">',
        '<button id="btn-start-exam" onclick="startSection1()" class="w-full sm:w-2/3 py-4 bg-neutral-950 hover:bg-neutral-800 text-white font-serif font-bold text-lg rounded border-2 border-neutral-950 shadow-md transition-all tracking-widest cursor-pointer">'
    )
    html = html.replace(
        'onclick="checkExamPin(() => startSection1())"',
        'onclick="startSection1()"'
    )

    # Replace explanation filter button numbers
    html = html.replace('전체 (107)', '전체 (102)')
    html = html.replace('어휘 (32)', '어휘 (30)')
    html = html.replace('문법 (22)', '문법 (21)')
    html = html.replace('독해 (21)', '독해 (21)')
    html = html.replace('청해 (32)', '청해 (30)')

    # Replace RAW_QUESTIONS
    questions_json_str = json.dumps(questions, ensure_ascii=False)
    m = re.search(r'const RAW_QUESTIONS = \[.*?\];\s*\n\s*// State Variables', html, re.DOTALL)
    assert m, "Could not find RAW_QUESTIONS in template"
    html = html[:m.start()] + f'const RAW_QUESTIONS = {questions_json_str};\n\n    // State Variables' + html[m.end() - len('// State Variables'):]

    # Replace JavaScript constants and counts
    html = html.replace(
        "document.getElementById('q-total-period-num').textContent = '75';",
        "document.getElementById('q-total-period-num').textContent = '72';"
    )
    html = html.replace(
        "const s1Answers = userAnswers.slice(0, 75);\n      const markedCount = s1Answers.filter(a => a !== null).length;\n      document.getElementById('break-stat-marked').textContent = `${markedCount} / 75 問`;",
        "const s1Answers = userAnswers.slice(0, 72);\n      const markedCount = s1Answers.filter(a => a !== null).length;\n      document.getElementById('break-stat-marked').textContent = `${markedCount} / 72 問`;"
    )
    html = html.replace(
        "document.getElementById('q-total-period-num').textContent = '107';",
        "document.getElementById('q-total-period-num').textContent = '102';"
    )
    html = html.replace(
        "document.getElementById('q-side-badge').textContent = `問 ${index + 1} / 107`;",
        "document.getElementById('q-side-badge').textContent = `問 ${index + 1} / 102`;"
    )
    # Unblock nextQuestion and prevQuestion across Section 1 and Section 2
    old_nav = """    function prevQuestion() {
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
        alert('※ 聴解試験では、放送の進行に合わせて自動的に次の問題へ進みます。手動でのスキップはできません。\\n(청해 시험에서는 방송 흐름에 맞춰 자동 전환됩니다. 수동 건너뛰기는 불가합니다.)');
      }
    }"""

    new_nav = """    function prevQuestion() {
      if (currentPhase === 'section1' && currentIndex > 0) {
        loadQuestion(currentIndex - 1);
      } else if (currentPhase === 'section2' && currentIndex > 72) {
        loadQuestion(currentIndex - 1);
      }
    }

    function nextQuestion() {
      if (currentPhase === 'section1') {
        if (currentIndex < 71) {
          loadQuestion(currentIndex + 1);
        } else {
          confirmFinishSection1();
        }
      } else if (currentPhase === 'section2') {
        if (currentIndex < sessionQuestions.length - 1) {
          loadQuestion(currentIndex + 1);
        } else {
          confirmSubmitAll();
        }
      }
    }"""
    html = html.replace(old_nav, new_nav)

    # Next button text at end of Section 1
    html = html.replace(
        "if (index === 74) {\n          btnNextText.textContent = '第1限 終了へ →';",
        "if (index === 71) {\n          btnNextText.textContent = '第1限 終了へ →';"
    )

    # Unblock palette dot clicks in Section 2
    old_dot_click = """        if (currentPhase === 'section2') {
          // 청해 중에는 임의 점프/되돌아가기 불가!
          dot.onclick = () => {
            alert('※ 聴解試験では、問題の再聴取や自由移動はできません。放送順に従って解答してください。\\n(청해 시험에서는 임의 이동 및 다시듣기가 불가능합니다. 방송 순서에 따라 풀어주세요.)');
          };
        } else {
          dot.onclick = () => loadQuestion(idx);
        }"""
    new_dot_click = """        dot.onclick = () => loadQuestion(idx);"""
    html = html.replace(old_dot_click, new_dot_click)

    # Allow Previous button in Section 2 (disabled only on first question index 72)
    html = html.replace(
        "document.getElementById('btn-prev').disabled = true; // 청해는 이전 문제 복귀 불가",
        "document.getElementById('btn-prev').disabled = (index === 72);"
    )
    html = html.replace(
        "const s1Answers = userAnswers.slice(0, 75);\n      const nextUnans = s1Answers.findIndex((ans, idx) => idx > currentIndex && ans === null);",
        "const s1Answers = userAnswers.slice(0, 72);\n      const nextUnans = s1Answers.findIndex((ans, idx) => idx > currentIndex && ans === null);"
    )
    html = html.replace(
        "alert('第1限(1~75問)のすべての問題にマークされています。(1교시 모든 문항에 마킹하셨습니다.)');",
        "alert('第1限(1~72問)のすべての問題にマークされています。(1교시 모든 문항에 마킹하셨습니다.)');"
    )
    html = html.replace(
        "let startIdx = 0;\n      let endIdx = 75;\n\n      if (currentPhase === 'section2') {\n        startIdx = 75;\n        endIdx = 107;\n        document.getElementById('palette-period-title').textContent = '第2限 聴解パレット (76 ~ 107)';\n      } else {\n        document.getElementById('palette-period-title').textContent = '第1限 パレット (1 ~ 75)';\n      }",
        "let startIdx = 0;\n      let endIdx = 72;\n\n      if (currentPhase === 'section2') {\n        startIdx = 72;\n        endIdx = 102;\n        document.getElementById('palette-period-title').textContent = '第2限 聴解パレット (73 ~ 102)';\n      } else {\n        document.getElementById('palette-period-title').textContent = '第1限 パレット (1 ~ 72)';\n      }"
    )
    html = html.replace(
        "let startIdx = currentPhase === 'section2' ? 75 : 0;\n      let endIdx = currentPhase === 'section2' ? 107 : 75;",
        "let startIdx = currentPhase === 'section2' ? 72 : 0;\n      let endIdx = currentPhase === 'section2' ? 102 : 72;"
    )

    # Clean replace PIN JS + 9/20 historical JS + old startSection1
    # Locate from '// PIN Authentication' (or '// 9/20 Database Historical Result') down to 'function updateSection1TimerDisplay()'
    p_start = html.find('// PIN Authentication')
    if p_start == -1:
        p_start = html.find('// 9/20 Database Historical Result')
    if p_start == -1:
        p_start = html.find('function restartExamFresh()')
    else:
        # back up to comment line
        line_start = html.rfind('// =', 0, p_start)
        if line_start != -1:
            p_start = line_start

    p_end = html.find('function updateSection1TimerDisplay()')
    assert p_start != -1 and p_end != -1, "Could not find startSection1 replacement bounds"
    html = html[:p_start] + CLEAN_SECTION1_START_JS + "\n\n    " + html[p_end:]

    # Clean replace Section 2 start (remove TTS intro & speechSynthesis)
    s2_start = html.find('function startSection2() {')
    if s2_start != -1:
        s2_end = html.find('function loadQuestion(index) {')
        assert s2_end != -1, "Could not find loadQuestion marker"
        html = html[:s2_start] + CLEAN_SECTION2_START_JS + "\n\n    " + html[s2_end:]

    # getListeningMeta logic replacement
    old_meta_pattern = re.compile(r'function getListeningMeta\(index\) \{.*?return null;\s*\}', re.DOTALL)
    new_meta_code = """function getListeningMeta(index) {
      const qNum = index + 1; // 73 ~ 102
      if (qNum >= 73 && qNum <= 77) {
        return { probNo: 1, itemNo: qNum - 72, isFirst: qNum === 73, name: "課題理解" };
      } else if (qNum >= 78 && qNum <= 83) {
        return { probNo: 2, itemNo: qNum - 77, isFirst: qNum === 78, name: "ポイント理解" };
      } else if (qNum >= 84 && qNum <= 88) {
        return { probNo: 3, itemNo: qNum - 83, isFirst: qNum === 84, name: "概要理解" };
      } else if (qNum >= 89 && qNum <= 99) {
        return { probNo: 4, itemNo: qNum - 88, isFirst: qNum === 89, name: "即時応答" };
      } else if (qNum >= 100 && qNum <= 102) {
        const itemLabels = { 100: "1番", 101: "2番 質問1", 102: "2番 質問2" };
        return { 
          probNo: 5, 
          itemNo: itemLabels[qNum], 
          qNum: qNum,
          isFirst: qNum === 100, 
          name: "統合理解",
          hasPrintedChoices: true
        };
      }
      return null;
    }"""
    html = old_meta_pattern.sub(new_meta_code, html, count=1)

    # Fix Problem 5 Question 1 & 2 label comparison
    html = html.replace(
        "meta.qNum === 106 ? '1' : '2'",
        "meta.qNum === 101 ? '1' : '2'"
    )

    # Endurance stats replacement
    old_endurance = """const firstAnswers = userAnswers.slice(0, 75);
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
      document.getElementById('stat-second-half-time').innerHTML = `총 ${Math.round(secondTime/60)}분 · 문항당 ${((secondTime/32)).toFixed(1)}초`;"""

    new_endurance = """const firstAnswers = userAnswers.slice(0, 72);
      const secondAnswers = userAnswers.slice(72);

      const firstCorrect = firstAnswers.filter((a, i) => a === sessionQuestions[i].sessionAnswer).length;
      const secondCorrect = secondAnswers.filter((a, i) => a === sessionQuestions[72 + i].sessionAnswer).length;

      const firstPct = ((firstCorrect / 72) * 100).toFixed(1);
      const secondPct = ((secondCorrect / 30) * 100).toFixed(1);

      const firstTime = section1ElapsedSeconds;
      const secondTime = section2ElapsedSeconds;

      document.getElementById('stat-first-half').textContent = `${firstCorrect} / 72 (${firstPct}%)`;
      document.getElementById('stat-first-half-time').innerHTML = `총 ${Math.round(firstTime/60)}분 · 문항당 ${((firstTime/72)).toFixed(1)}초`;

      document.getElementById('stat-second-half').textContent = `${secondCorrect} / 30 (${secondPct}%)`;
      document.getElementById('stat-second-half-time').innerHTML = `총 ${Math.round(secondTime/60)}분 · 문항당 ${((secondTime/30)).toFixed(1)}초`;"""
    html = html.replace(old_endurance, new_endurance)

    # Result JSON metadata replacement
    old_json_meta = """examType: "공식 문제집 제2집 기반 실전모의고사 (개인학습용 / TTS)",
        examTitle: "JLPT N2 実戦模試（公式問題集 第2集ベース / 個人学習用）",
        provenanceNote: "출제 원안: 日本語能力試験 公式問題集 第2集(2018) 대조 / 개인학습용 TTS 구현 / 비공식 정답률 추정","""

    new_json_meta = """examType: "official_past_mock",
        examTitle: "2023年 第2回 (12月) JLPT N2 本試験 全領域 実戦模試 (102問)",
        provenanceNote: "출제 원안: 2023年 第2回 (12月) JLPT N2 本試験 원문 대조 / 실제 본시험 전문 성우 원음(영상 숨김 순수 청해) / 공식 정답 일치",
        testId: "official-past-202312-full-mock-20261004","""
    html = html.replace(old_json_meta, new_json_meta)

    # Vocab/Grammar totals in result payload
    old_totals = """const vocabTotal = 32, grammarTotal = 22, readingTotal = 21, listeningTotal = 32;
      const langRate = (vocabCorrect + grammarCorrect) / 54;"""
    new_totals = """const vocabTotal = 30, grammarTotal = 21, readingTotal = 21, listeningTotal = 30;
      const langRate = (vocabCorrect + grammarCorrect) / 51;"""
    html = html.replace(old_totals, new_totals)

    # 3. Replace listening status panel HTML with hidden video player
    panel_start = html.find('<!-- Listening ON-AIR Broadcast Status Panel')
    panel_end = html.find('<!-- Problem Header Badge -->')
    assert panel_start != -1 and panel_end != -1, "Could not find listening panel markers"
    html = html[:panel_start] + AUDIO_PANEL_HTML + "\n\n            " + html[panel_end:]

    # 4. Cleanly replace the entire old TTS block with AUDIO_JS
    tts_start = html.find('function startContinuousListeningForQuestion(index) {')
    tts_end = html.find('function confirmSubmitAll() {')
    assert tts_start != -1 and tts_end != -1, "Could not find TTS block markers"
    html = html[:tts_start] + AUDIO_JS + "\n    " + html[tts_end:]

    # 5. Fix end-of-exam triggers (index == 101 instead of 106)
    html = html.replace("if (index === 106)", "if (index === 101)")
    html = html.replace("if (currentIndex === 106)", "if (currentIndex === 101)")
    html = html.replace("index === 103", "index === 101")
    html = html.replace("currentIndex === 103", "currentIndex === 101")

    # 5.1 Clean replace finishAllExams (remove SpeechSynthesisUtterance, cleanly pause YouTube player)
    old_finish = """    function finishAllExams() {
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
    }"""
    new_finish = """    function finishAllExams() {
      isExamFinished = true;
      if (section1TimerInterval) clearInterval(section1TimerInterval);
      if (breakTimerInterval) clearInterval(breakTimerInterval);
      if (section2TimerInterval) clearInterval(section2TimerInterval);
      if (questionTimerInterval) clearInterval(questionTimerInterval);
      if (listeningCountdownTimer) clearInterval(listeningCountdownTimer);
      if (window.speechSynthesis) window.speechSynthesis.cancel();

      // Stop audio playback
      const iframe = document.getElementById('yt-actual-audio');
      if (iframe && iframe.contentWindow) {
        iframe.contentWindow.postMessage(JSON.stringify({
          event: 'command',
          func: 'pauseVideo',
          args: []
        }), '*');
      }
      isYtPlaying = false;

      document.getElementById('screen-quiz').classList.add('hidden');
      document.getElementById('screen-break').classList.add('hidden');
      document.getElementById('screen-result').classList.remove('hidden');

      renderResults();
    }"""
    html = html.replace(old_finish, new_finish)

    # 6. Ensure robust DOMContentLoaded start button binding
    auto_init_old = """    // Auto-init on load
    window.addEventListener('DOMContentLoaded', () => {
      initExam();
    });"""
    auto_init_new = """    // Auto-init on load and robust button wiring
    window.addEventListener('DOMContentLoaded', () => {
      initExam();
      const startBtn = document.getElementById('btn-start-exam');
      if (startBtn) {
        startBtn.addEventListener('click', (e) => {
          e.preventDefault();
          startSection1();
        });
      }
    });"""
    html = html.replace(auto_init_old, auto_init_new)

    # 7. Save to both destinations
    destinations = [
        'quiz_sites/n2-past-exam-202312-mock.html',
        'jlpt-calendar-site/public/exams/n2-past-exam-202312-mock.html'
    ]
    for dest in destinations:
        with open(dest, 'w', encoding='utf-8') as out:
            out.write(html)
        print(f"Successfully generated {dest} (length: {len(html)} bytes)")

if __name__ == '__main__':
    build()
