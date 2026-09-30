import re

MODAL_HTML = """
  <!-- Exam Structure Guide Modal -->
  <div id="examStructureModal" class="fixed inset-0 z-50 hidden bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-3 sm:p-6 transition-all">
    <div class="bg-slate-900 border border-slate-700/80 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
      <!-- Modal Header -->
      <div class="p-5 sm:p-6 border-b border-slate-800 flex items-center justify-between bg-slate-900/90 sticky top-0 z-10">
        <div>
          <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-semibold mb-1 border border-indigo-500/20">
            <span>📋 JLPT N2 공식 시험 규격 & 출제 스펙</span>
          </div>
          <h2 class="text-xl sm:text-2xl font-black text-white">JLPT N2 전 영역 출제 유형 및 시간 배분 가이드</h2>
        </div>
        <button type="button" onclick="closeExamStructureModal()" class="w-9 h-9 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center font-bold text-lg transition-colors" aria-label="닫기">
          ✕
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-5 sm:p-6 overflow-y-auto space-y-6 text-sm text-slate-300">
        
        <!-- Quick Overview Alert -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="bg-slate-800/80 border border-slate-700/60 p-3.5 rounded-xl text-center">
            <div class="text-xs text-slate-400">1교시 시험시간</div>
            <div class="text-xl sm:text-2xl font-bold text-blue-400 mt-0.5">105분</div>
            <div class="text-[11px] text-slate-400">언어지식·독해 72~75문항</div>
          </div>
          <div class="bg-slate-800/80 border border-slate-700/60 p-3.5 rounded-xl text-center">
            <div class="text-xs text-slate-400">2교시 시험시간</div>
            <div class="text-xl sm:text-2xl font-bold text-sky-400 mt-0.5">50분</div>
            <div class="text-[11px] text-slate-400">청해 31~32문항</div>
          </div>
          <div class="bg-slate-800/80 border border-slate-700/60 p-3.5 rounded-xl text-center">
            <div class="text-xs text-slate-400">합격 기준 / 만점</div>
            <div class="text-xl sm:text-2xl font-bold text-emerald-400 mt-0.5">90 / 180점</div>
            <div class="text-[11px] text-slate-400">최우선 목표 110점 이상</div>
          </div>
          <div class="bg-slate-800/80 border border-slate-700/60 p-3.5 rounded-xl text-center">
            <div class="text-xs text-slate-400">과락 기준</div>
            <div class="text-xl sm:text-2xl font-bold text-amber-400 mt-0.5">각 19점 미만</div>
            <div class="text-[11px] text-slate-400">3개 영역 모두 19점 이상</div>
          </div>
        </div>

        <!-- Section 1: 文字・語彙 -->
        <div class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4 sm:p-5 space-y-3">
          <div class="flex items-center justify-between border-b border-slate-700/60 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded text-xs font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30">1교시 언어지식</span>
              <h3 class="text-base font-bold text-white">문자·어휘 (文字・語彙) · 총 30~32문항</h3>
            </div>
            <span class="text-xs font-semibold text-emerald-400">⏱ 권장 소요시간: 15~18분</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <strong class="text-blue-300 block mb-0.5">문제 1: 한자 읽기 (漢字読み) [5문항]</strong>
              <p class="text-slate-400">밑줄 친 한자의 히라가나 읽기 찾기 (음독/훈독, 탁음/촉음/장음 구별이 핵심 함정)</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <strong class="text-blue-300 block mb-0.5">문제 2: 표기 (表記) [5문항]</strong>
              <p class="text-slate-400">히라가나 문맥에 알맞은 올바른 한자 표기 찾기 (동음이의어 및 모양 유사 한자 구별)</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <strong class="text-blue-300 block mb-0.5">문제 3: 어형성 (語形成) [5문항]</strong>
              <p class="text-slate-400">접두사(無, 非, 不, 未, 総 등) 및 접미사(~的, ~性, ~感, ~風 등), 파생어/복합어 결합</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <strong class="text-blue-300 block mb-0.5">문제 4: 문맥 규정 (文脈規定) [7문항]</strong>
              <p class="text-slate-400">문장의 문맥과 의미 흐름상 가장 적합한 명사, 동사, 형용사, 부사, 의태어/의성어 선택</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <strong class="text-blue-300 block mb-0.5">문제 5: 유의 표현 (類義表現) [5문항]</strong>
              <p class="text-slate-400">밑줄 친 단어/표현과 의미가 가장 가까운 바꿔쓰기(패러프레이징) 표현 고르기</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <strong class="text-blue-300 block mb-0.5">문제 6: 용법 (用法) [5문항]</strong>
              <p class="text-slate-400">주어진 단어가 가장 자연스럽고 문법적으로 바르게 쓰인 1개 문장 찾기 (연어/공기관계)</p>
            </div>
          </div>
        </div>

        <!-- Section 2: 文法 -->
        <div class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4 sm:p-5 space-y-3">
          <div class="flex items-center justify-between border-b border-slate-700/60 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">1교시 언어지식</span>
              <h3 class="text-base font-bold text-white">문법 (文法) · 총 21~22문항</h3>
            </div>
            <span class="text-xs font-semibold text-emerald-400">⏱ 권장 소요시간: 15~17분</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <strong class="text-indigo-300 block mb-0.5">문제 7: 문법형식 판단 [12문항]</strong>
              <p class="text-slate-400">N2 핵심 기능어, 문형 접속, 존경어/겸양어 등 문맥에 가장 적합한 문법 형식 선택</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <strong class="text-indigo-300 block mb-0.5">문제 8: 문맥 배열 (★ 별표) [5문항]</strong>
              <p class="text-slate-400">4개의 어구를 논리적 문장으로 조립하여 ★ 위치에 들어갈 어구의 번호 선택</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <strong class="text-indigo-300 block mb-0.5">문제 9: 글의 문법 [5문항]</strong>
              <p class="text-slate-400">1편의 완성된 글 속 빈칸에 들어갈 접속사, 지시어, 서술어 호응, 화자의 의도 판단</p>
            </div>
          </div>
        </div>

        <!-- Section 3: 読解 -->
        <div class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4 sm:p-5 space-y-3">
          <div class="flex items-center justify-between border-b border-slate-700/60 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">1교시 독해</span>
              <h3 class="text-base font-bold text-white">독해 (読解) · 총 21문항</h3>
            </div>
            <span class="text-xs font-semibold text-emerald-400">⏱ 권장 소요시간: 65~70분</span>
          </div>
          <div class="space-y-2 text-xs">
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <strong class="text-amber-300">문제 10: 단문 독해 (短文読解) [5지문, 각 1문항 = 총 5문항]</strong>
                <p class="text-slate-400 mt-0.5">150~200자 내외 공지, 서신, 설명문. 핵심 요지와 알림 내용 신속 파악</p>
              </div>
              <span class="text-slate-400 text-[11px] whitespace-nowrap bg-slate-700/60 px-2 py-1 rounded">지문당 1.5~2분 (총 10분)</span>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <strong class="text-amber-300">문제 11: 중문 독해 (中文読解) [3지문, 각 3문항 = 총 9문항]</strong>
                <p class="text-slate-400 mt-0.5">500자 내외 해설문, 수필, 논설문. 인과관계, 이유, 필자의 핵심 관점</p>
              </div>
              <span class="text-slate-400 text-[11px] whitespace-nowrap bg-slate-700/60 px-2 py-1 rounded">지문당 8분 (총 24~25분)</span>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <strong class="text-amber-300">문제 12: 통합 이해 (統合理解) [1지문 2개 글, 총 2문항]</strong>
                <p class="text-slate-400 mt-0.5">동일한 테마에 대한 두 사람의 다른 의견/문서 비교 (공통점 및 차이점 대조)</p>
              </div>
              <span class="text-slate-400 text-[11px] whitespace-nowrap bg-slate-700/60 px-2 py-1 rounded">총 8~10분</span>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <strong class="text-amber-300">문제 13: 장문 독해 (長文読解) [1지문, 총 3문항]</strong>
                <p class="text-slate-400 mt-0.5">900~1,000자 장문 논설/에세이. 전체 전개 구조와 필자가 궁극적으로 말하고자 하는 주장</p>
              </div>
              <span class="text-slate-400 text-[11px] whitespace-nowrap bg-slate-700/60 px-2 py-1 rounded">총 12~14분</span>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <strong class="text-amber-300">문제 14: 정보 검색 (情報検索) [1지문(표·공지), 총 2문항]</strong>
                <p class="text-slate-400 mt-0.5">신청 자격, 할인 조건, 일정 안내문 등 제시된 조건에 정확히 부합하는 항목 신속 검색</p>
              </div>
              <span class="text-slate-400 text-[11px] whitespace-nowrap bg-slate-700/60 px-2 py-1 rounded">총 4~5분</span>
            </div>
          </div>
        </div>

        <!-- Section 4: 聴解 -->
        <div class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-4 sm:p-5 space-y-3">
          <div class="flex items-center justify-between border-b border-slate-700/60 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded text-xs font-bold bg-sky-500/20 text-sky-300 border border-sky-500/30">2교시 청해</span>
              <h3 class="text-base font-bold text-white">청해 (聴解) · 총 31~32문항</h3>
            </div>
            <span class="text-xs font-semibold text-sky-400">⏱ 정규 시험시간: 50분</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs">
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <div class="flex items-center justify-between mb-1">
                <strong class="text-sky-300">문제 1: 과제 이해 (課題理解) [5문항]</strong>
                <span class="px-1.5 py-0.5 bg-emerald-500/20 text-emerald-400 rounded text-[10px]">보기 인쇄 O</span>
              </div>
              <p class="text-slate-400">상황과 질문 선제시 → 대화 청취 → "이 다음 먼저 해야 할 행동" 파악 (조건 변경 주의)</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <div class="flex items-center justify-between mb-1">
                <strong class="text-sky-300">문제 2: 포인트 이해 (ポイント理解) [6문항]</strong>
                <span class="px-1.5 py-0.5 bg-emerald-500/20 text-emerald-400 rounded text-[10px]">보기 인쇄 O</span>
              </div>
              <p class="text-slate-400">질문 선제시 + 20초 읽기 시간 → 대화 청취 → 이유, 원인, 핵심 근거 파악</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <div class="flex items-center justify-between mb-1">
                <strong class="text-sky-300">문제 3: 개요 이해 (概要理解) [5문항]</strong>
                <span class="px-1.5 py-0.5 bg-rose-500/20 text-rose-400 rounded text-[10px]">보기 인쇄 X (백지)</span>
              </div>
              <p class="text-slate-400">문제지에 아무것도 쓰여있지 않음! 발화자의 입장, 강연의 핵심 주제와 의도 메모 필수</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40">
              <div class="flex items-center justify-between mb-1">
                <strong class="text-sky-300">문제 4: 즉시 응답 (即時応答) [11~12문항]</strong>
                <span class="px-1.5 py-0.5 bg-rose-500/20 text-rose-400 rounded text-[10px]">보기 인쇄 X (음성만)</span>
              </div>
              <p class="text-slate-400">짧은 발화 1문장 직후 가장 자연스러운 대답(1~3번) 즉시 선택 (경어, 관용구, 맞장구 빈출)</p>
            </div>
            <div class="bg-slate-800/60 p-2.5 rounded-lg border border-slate-700/40 sm:col-span-2">
              <div class="flex items-center justify-between mb-1">
                <strong class="text-sky-300">문제 5: 통합 이해 (統合理解) [총 3문항]</strong>
                <span class="px-1.5 py-0.5 bg-emerald-500/20 text-emerald-400 rounded text-[10px]">보기 인쇄 O</span>
              </div>
              <p class="text-slate-400">1번·2번: 4가지 대안 조건 제시 후 남녀 2명이 각자 최종 선택하는 방안 매칭 / 3번: 장문 인터뷰 사실관계 파악</p>
            </div>
          </div>
        </div>

        <!-- Strategy Box -->
        <div class="bg-gradient-to-r from-blue-900/30 to-indigo-900/30 border border-blue-500/30 rounded-xl p-4 text-xs space-y-2">
          <strong class="text-blue-300 flex items-center gap-1.5 text-sm">
            <span>💡</span> 실전 합격 골든룰
          </strong>
          <ul class="list-disc list-inside space-y-1 text-slate-300">
            <li><strong>시간 사수:</strong> 언어지식(문자·어휘·문법)은 반드시 30~35분 이내에 끝내야 독해 65~70분을 확보할 수 있습니다. 모르는 어휘는 30초 이상 끌지 말고 즉시 체크 후 통과!</li>
            <li><strong>독해 진입 순서:</strong> 문제 10(단문)과 문제 14(정보검색)를 먼저 확실히 득점하고 중문/장문으로 넘어가면 심리적 안정감이 큽니다.</li>
            <li><strong>청해 시선 선점:</strong> 문제 1, 2는 방송 시작 전 20초 동안 선택지의 핵심 키워드(차이점)에 동그라미를 쳐둡니다. 문제 3, 4는 한 번 지나간 문제는 미련을 버리고 다음 문제에 집중합니다.</li>
          </ul>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-4 sm:p-5 border-t border-slate-800 bg-slate-900 flex justify-end">
        <button type="button" onclick="closeExamStructureModal()" class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl text-sm transition-colors shadow-lg">
          확인 완료 (가이드 닫기)
        </button>
      </div>
    </div>
  </div>

  <script>
    function openExamStructureModal() {
      const modal = document.getElementById('examStructureModal');
      if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
      }
    }
    function closeExamStructureModal() {
      const modal = document.getElementById('examStructureModal');
      if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
      }
    }
    // Close on backdrop click
    document.addEventListener('DOMContentLoaded', function() {
      const modal = document.getElementById('examStructureModal');
      if (modal) {
        modal.addEventListener('click', function(e) {
          if (e.target === modal) closeExamStructureModal();
        });
      }
    });
  </script>
"""

VOL2_CARD_HTML = """        <div class="bg-slate-800/60 hover:bg-slate-800 border border-blue-500/40 rounded-2xl p-5 shadow-lg transition-all space-y-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="font-bold text-base text-white">日本語能力試験 公式問題集 第2集 (N2 完本)</span>
              <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30">1차 실전응시 완료 · 119점 합격</span>
            </div>
            <div class="flex items-center gap-2">
              <a href="official-vol2-listening-player.html" class="px-2.5 py-1.5 bg-sky-600/80 hover:bg-sky-500 text-white text-xs font-bold rounded-lg transition-colors flex items-center gap-1">🎧 음원</a>
              <a href="n2-midterm-mock-exam-20260920.html" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-lg transition-colors flex items-center gap-1">결과·오답 해설 보기 →</a>
            </div>
          </div>
          <div class="flex items-center gap-4 text-xs text-slate-400">
            <span>응시일: 2026-09-20 (공식 제2집)</span>
            <span>문항수: 107문항</span>
            <span>실전 결과: 119 / 180점 (정답 71/107, 66.4% · 합격선 90점 및 목표 110점 돌파)</span>
          </div>
          <div class="space-y-1.5 pt-1 border-t border-slate-700/60 text-xs">
            <div>
              <span class="text-slate-400 font-semibold">핵심 어휘: </span>
              <div class="inline-flex flex-wrap gap-1 mt-0.5"><span class="px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-300 text-[11px] border border-blue-500/20">抱負</span><span class="px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-300 text-[11px] border border-blue-500/20">慎重</span><span class="px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-300 text-[11px] border border-blue-500/20">契機</span><span class="px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-300 text-[11px] border border-blue-500/20">催促</span><span class="px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-300 text-[11px] border border-blue-500/20">ぎっしり</span></div>
            </div>
            <div>
              <span class="text-slate-400 font-semibold">빈출 문법: </span>
              <div class="inline-flex flex-wrap gap-1 mt-0.5"><span class="px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-300 text-[11px] border border-indigo-500/20">〜にほかならない</span><span class="px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-300 text-[11px] border border-indigo-500/20">〜を契機に</span><span class="px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-300 text-[11px] border border-indigo-500/20">〜ざるを得ない</span><span class="px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-300 text-[11px] border border-indigo-500/20">〜からといって</span><span class="px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-300 text-[11px] border border-indigo-500/20">〜っこない</span></div>
            </div>
            <div class="text-slate-400">
              <span class="font-semibold text-slate-300">독해 테마: </span>
              <span>AI 번역과 인간 사유의 본질, 도심 생태계 공존, 직장 내 의사결정 프로세스</span>
            </div>
            <div class="text-slate-400">
              <span class="font-semibold text-slate-300">청해 트릭: </span>
              <span>조건부 변경에 따른 우선행동 전환(과제이해), 경어 관용표현 즉시응답</span>
            </div>
          </div>
        </div>
"""

HEADER_BUTTONS_REPLACEMENT = """      <div class="flex flex-wrap items-center gap-3">
        <a href="/" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs sm:text-sm font-bold rounded-xl border border-slate-600 shadow-lg transition-all flex items-center gap-2">
          <span>🏠 学習カレンダー</span>
        </a>
        <button type="button" onclick="openExamStructureModal()" class="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs sm:text-sm font-bold rounded-xl shadow-lg transition-all flex items-center gap-2 border border-indigo-400/40 cursor-pointer">
          <span>📋 N2 출제 유형 & 시간 배분 가이드</span>
          <span class="text-xs bg-indigo-800 px-1.5 py-0.5 rounded">상기</span>
        </button>
      </div>"""

def update_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the header buttons group
    # Search from `<div class="flex flex-wrap items-center gap-3">` up to `</header>`
    header_regex = r'<div class="flex flex-wrap items-center gap-3">[\s\S]*?</div>\s*</header>'
    new_header = HEADER_BUTTONS_REPLACEMENT + "\n    </header>"
    content = re.sub(header_regex, new_header, content)

    # 2. Update Stats bar "TTS 청해" -> "실전 규격"
    content = content.replace('TTS 청해 & 지구력 정밀 분석', '실전 규격 & 지구력 정밀 분석')

    # 3. In the Grid, insert VOL2_CARD_HTML right before the 2023.12 card if not already inserted
    if '日本語能力試験 公式問題集 第2集 (N2 完本)' not in content:
        grid_start = '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">'
        content = content.replace(grid_start, grid_start + "\n\n" + VOL2_CARD_HTML)

    # 4. Remove the old duplicate stub at the bottom: `<span class="font-bold text-base text-white">JLPT N2 公式問題集 第2集 (2018)</span>`
    old_stub_regex = r'<div class="bg-slate-800/60 hover:bg-slate-800 border border-slate-700 rounded-2xl p-5 shadow transition-all space-y-3">\s*<div class="flex items-center justify-between">\s*<div class="flex items-center gap-2">\s*<span class="font-bold text-base text-white">JLPT N2 公式問題集 第2集 \(2018\)</span>[\s\S]*?</div>\s*</div>\s*</div>\s*(?=\s*</div>\s*</div>\s*</div>\s*</body>)'
    content = re.sub(old_stub_regex, '', content)

    # 5. Insert MODAL_HTML before `</body>` if not already present
    if 'id="examStructureModal"' not in content:
        content = content.replace('</body>', MODAL_HTML + '\n</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {path}")

for p in [
    'jlpt-calendar-site/public/exams/past-exams-portal.html',
    'jlpt-calendar-site/public/exams/index.html',
    'quiz_sites/past-exams-portal.html'
]:
    update_file(p)
