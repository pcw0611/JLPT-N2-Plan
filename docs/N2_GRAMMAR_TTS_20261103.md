# 문형 스피드런 해설 TTS — 2026-11-03

## 적용

- 기존 프로젝트의 `n2-listening-practice.html`이 사용하는 브라우저 Web Speech API 방식을 재사용했다. 새 패키지·유료 API·서버 TTS·음원 저장소를 도입하지 않았다.
- 정답·오답·모름을 선택하고 완성 문장/해설이 공개된 직후에만 자동으로 1회 읽는다. 문제를 풀기 전에는 정답 문장 음성이나 재생 버튼을 노출하지 않는다.
- 해설에서 다시 듣기(0.95), 천천히(0.72), 중지, 자동 읽기 ON/OFF 제공. 자동 읽기 선호는 브라우저에 저장되며 OFF여도 수동 재생은 가능하다.
- 시작 화면에는 정답과 관계없는 일본어 샘플로 음성을 확인하는 버튼과 자동 읽기 설정을 제공한다.
- 현재 문장의 해설용 후리가나를 읽기 텍스트로 사용하므로 한자와 후리가나를 두 번 읽거나 한국어 해석을 읽지 않는다.
- 일시중지·종료 확인·다음 문제·새 세션·페이지 이탈 시 이전 음성과 대기 중 재생을 취소한다. 재개 후에는 필요할 때 수동으로 다시 듣는다. 듣는 동안의 활동 시간은 기존대로 세션 시간에 포함한다.
- 일본어 음성만 선택한다. 일본어 음성 없음, 지연 로딩, 재생 차단·오류를 안내하고 다른 언어로 잘못 읽지 않는다. 음성 실패로 답을 바꾸거나 오답 처리하지 않는다.
- 음원 출처는 브라우저 합성 음성. 공식 청해 음원이 아니며 이 퀴즈를 청해 시험으로 바꾸지 않았다.

## 변경 파일

- `scripts/grammar_tts_runtime.js`: 재생, 읽기 텍스트, 음성 선택, 취소·지연 이벤트 방지.
- `scripts/sync_grammar_speedrun_html.py`: 유지보수 원본 TTS 코드를 기존 인라인 실행기에 동기화.
- `jlpt-calendar-site/public/exams/n2-grammar-speedrun.html`, `quiz_sites/n2-grammar-speedrun.html`: 시작/해설 제어 및 기존 세션 흐름과 연동.
- `scripts/check_grammar_tts.mjs`: 메모리 음성 엔진/DOM으로 실제 실행기를 검사. 기존 학습 DB·일정·로그에는 쓰지 않음.

## 근거·검증

- [MDN rate](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/rate), [cancel](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/cancel), [기기별 음성 목록](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/getVoices)을 확인했다.
- `node scripts/check_grammar_tts.mjs` 통과: 답변 전 재생 차단, 정답/오답/모름 후 재생, 샘플, 반복/저속, 선호 저장, 중지/이동/종료, 지연 음성 로딩의 이전 문제 재생 방지, 일본어 음성 없음, 자동 재생 차단 안내, 1,400문항 읽기 텍스트 검사. 실제 네트워크·성적 쓰기 없음.
- `node scripts/check_grammar_daily.mjs` 통과: 기존 7요일 구성·전체 채점·일시중지·중간 종료 흐름 유지.
- 제출 반영 Python 테스트 3개 및 `pnpm build` 통과.
- 인앱 브라우저 로컬 검증: `Microsoft Haruka - Japanese (Japan)` 감지, 샘플 재생 완료, 정답 전 버튼 미노출, 정답 후 자동 재생 시작, 느리게 재생 시작, Enter 키로 느리게 재생해도 문제 유지, 일시중지 화면 확인. 실제 성적은 제출하지 않았다.

## 한계

음성과 음질은 기기·브라우저에 설치/제공된 음성에 따라 달라진다. 일본어 음성이 없는 기기에서는 해당 음성 설정이 필요하다. 브라우저 제공 온라인 음성이 선택될 수 있으므로 완전 오프라인을 보증하지 않는다. 재생 시작/완료 이벤트를 확인했으며, 스피커의 물리적 출력이나 1,400문장의 발음을 전수 청취·감수한 것은 아니다.
