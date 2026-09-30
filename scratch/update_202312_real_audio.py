import re

REAL_AUDIO_PANEL_HTML = """            <!-- Listening ON-AIR Broadcast Status Panel (2교시 청해 시에만 노출) -->
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
                <span class="px-2 py-0.5 bg-emerald-600 text-white rounded text-[10px] font-bold">실제 음원 완본</span>
              </div>

              <!-- Real Exam Audio Player (Official 2023.12 Actual Recording) -->
              <div class="bg-neutral-900 text-white p-3.5 rounded-lg space-y-3">
                <div class="flex items-center justify-between text-xs">
                  <div class="flex items-center gap-2 font-bold text-emerald-400">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>2023.12 JLPT N2 本試験 公式 原本 聴解 音声 (42分 完本)</span>
                  </div>
                  <span class="text-[11px] text-neutral-400">실제 본시험 성우 녹음</span>
                </div>

                <!-- Embedded YouTube Player -->
                <div class="relative w-full rounded overflow-hidden aspect-video max-h-56 bg-black border border-neutral-700">
                  <iframe 
                    id="yt-actual-audio" 
                    src="https://www.youtube-nocookie.com/embed/q5lzCC2k8-0?enablejsapi=1&autoplay=0&rel=0" 
                    title="2023.12 JLPT N2 Listening Audio" 
                    class="w-full h-full border-0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
                  </iframe>
                </div>

                <!-- Fast Jump Section Markers -->
                <div class="flex flex-wrap items-center gap-1.5 pt-1 text-xs">
                  <span class="text-neutral-400 text-[11px] mr-1">대문항 바로가기:</span>
                  <button type="button" onclick="seekAudioTime(0)" class="px-2.5 py-1 rounded bg-neutral-800 hover:bg-neutral-700 text-neutral-200 border border-neutral-600 text-[11px] transition cursor-pointer">問題1 課題 (0:00)</button>
                  <button type="button" onclick="seekAudioTime(615)" class="px-2.5 py-1 rounded bg-neutral-800 hover:bg-neutral-700 text-neutral-200 border border-neutral-600 text-[11px] transition cursor-pointer">問題2 ポイント (10:15)</button>
                  <button type="button" onclick="seekAudioTime(1245)" class="px-2.5 py-1 rounded bg-neutral-800 hover:bg-neutral-700 text-neutral-200 border border-neutral-600 text-[11px] transition cursor-pointer">問題3 概要 (20:45)</button>
                  <button type="button" onclick="seekAudioTime(1730)" class="px-2.5 py-1 rounded bg-neutral-800 hover:bg-neutral-700 text-neutral-200 border border-neutral-600 text-[11px] transition cursor-pointer">問題4 即時 (28:50)</button>
                  <button type="button" onclick="seekAudioTime(2180)" class="px-2.5 py-1 rounded bg-neutral-800 hover:bg-neutral-700 text-neutral-200 border border-neutral-600 text-[11px] transition cursor-pointer">問題5 統合 (36:20)</button>
                </div>
              </div>

              <div class="text-[11px] text-neutral-600">
                ※ 기계식 브라우저 TTS가 아닌 2023.12 JLPT N2 실제 본시험 전문 성우 원본 음성입니다. 상단 플레이어로 음원을 재생하며 문제를 풀고 OMR에 마킹하세요.
              </div>
            </div>"""

JS_LISTENING_UPDATE = """    function seekAudioTime(seconds) {
      const iframe = document.getElementById('yt-actual-audio');
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
      }
    }

    function startContinuousListeningForQuestion(index) {
      const q = sessionQuestions[index];
      const phaseText = document.getElementById('listening-phase-text');

      // Cancel any synthetic browser TTS
      if (window.speechSynthesis) window.speechSynthesis.cancel();

      const meta = getListeningMeta(index);
      if (meta) {
        phaseText.textContent = `🎧 2023.12 본시험 공식 실제 음원: [問題${meta.probNo} ${meta.itemNo}番]`;
      } else {
        phaseText.textContent = '🎧 2023.12 본시험 공식 실제 음원 진행 중...';
      }

      // Allow navigation between listening questions freely
      document.getElementById('btn-prev').disabled = (index === 72);
    }
"""

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace intro screen references to TTS
    content = content.replace('(ブラウザTTS聴解演習)', '(2023.12 本試験 公式 原本 聴解 音声 実装)')
    content = content.replace('브라우저 TTS 음성으로 쉼 없이 자동 진행', '2023년 12월 본시험 공식 전문 성우 원본 음성(42분 완본)으로 진행')

    # 2. Replace listening status panel
    panel_pattern = r'<!-- Listening ON-AIR Broadcast Status Panel[\s\S]*?</div>\s*</div>\s*</div>\s*(?=<!-- Problem Header Badge -->)'
    if 'id="listening-status-panel"' in content:
        # replace from `<div id="listening-status-panel"` up to `<!-- Problem Header Badge -->`
        content = re.sub(r'<div id="listening-status-panel"[\s\S]*?(?=<!-- Problem Header Badge -->)', REAL_AUDIO_PANEL_HTML + "\n\n            ", content)

    # 3. Replace startContinuousListeningForQuestion logic
    # Find `function startContinuousListeningForQuestion(index) { ... }`
    func_pattern = r'function startContinuousListeningForQuestion\(index\) \{[\s\S]*?(?=function executeListeningFlowForQuestion)'
    if re.search(func_pattern, content):
        content = re.sub(func_pattern, JS_LISTENING_UPDATE + "\n", content)
    elif 'function seekAudioTime' not in content:
        content = content.replace('function startContinuousListeningForQuestion(index) {', JS_LISTENING_UPDATE + '\n    function old_startContinuousListeningForQuestion(index) {')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {path}")

for p in [
    'quiz_sites/n2-past-exam-202312-mock.html',
    'jlpt-calendar-site/public/exams/n2-past-exam-202312-mock.html'
]:
    update_file(p)
