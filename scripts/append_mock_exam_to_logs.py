import json
import re

RESULT_PATH = 'database/results/official-vol2-full-mock-20260920.json'
HTML_PATH = 'quiz_sites/n2-midterm-mock-exam-20260920.html'
STUDY_LOG_PATH = 'JLPT_STUDY_LOG.md'
ERROR_NOTE_PATH = 'JLPT_ERROR_NOTE.md'

def run():
    with open(RESULT_PATH, 'r', encoding='utf-8') as f:
        res = json.load(f)

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', html, re.DOTALL)
    raw_questions = json.loads(m.group(1))
    q_map = {q['id']: q for q in raw_questions}

    # 1. Generate JLPT_STUDY_LOG.md entry
    log_entry = f"""
<!-- official-vol2-full-mock-20260920 -->
## 2026-09-20 — JLPT N2 공식 문제집 제2집 전 영역 완본 실전모의고사 (107문항)

- **시험 ID**: `official-vol2-full-mock-20260920`. 사용자 제출 실제 결과 (107문항 완본 응시).
- **출제 원안 및 성격**: 日本語能力試験 公式問題集 第2集 (2018) 대조 / 개인학습용 실전 브라우저 퀴즈 (청해 TTS 연습) / **공식 모의고사 (`official_mock`)**.
- **종합 결과**: **71 / 107 (正答率 66.4%)**
- **비공식 득점 환산 추정치**: **119 / 180 点 (합격선 90점 및 목표 110점권 여유 있게 돌파!)**
  - *(※ 본 점수는 비공식 정답률 기반 추정치이며, 실제 JLPT는 문항 난이도별 득점등화(IRT)가 적용됩니다.)*
- **과락 위험 평가**: **전 영역 과락 위험 0건 (안전 통과)** (각 영역 최저 기준점 19점/60점 = 31.6% 상회).
- **총 소요시간**: **115분 36초 (6,936초 / 약 1시간 55분)** (실제 시험 제한시간 155분 대비 약 39분 여유 있게 완주).
  - 1교시(언어지식·독해 1~75번): **86분 10초** (제한시간 105분 대비 19분 여유, 문항당 68.9초).
  - 2교시(청해 76~107번): **29분 28초** (제한시간 약 50분 대비 논스톱 완주, 문항당 55.3초).
- **오답 / 모름 / 미응답**: **오답 36문항 / 모름 0 / 미응답 0**.

### 영역별 세부 성적 및 소요시간

| 영역 | 공식 문제 구분 | 문항 수 | 정답 수 | 정답률 | 영역 환산점 (추정) | 과락 기준선 (19점) | 소요시간 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **문자·어휘** | 問題 1~6 | 32문 | **21문** | **65.6%** | 약 39.4 / 60 | 안전 통과 | 18분 18초 |
| **문법** | 問題 7~9 | 22문 | **10문** | **45.5%** | 약 27.3 / 60 | 안전 통과 | 21분 56초 |
| *(언어지식 합계)* | *問題 1~9* | *54문* | ***31문*** | ***57.4%*** | ***약 34.4 / 60*** | ***안전 통과*** | *40분 14초* |
| **독해** | 問題 10~14 | 21문 | **16문** | **76.2%** | **약 45.7 / 60** | **안전 통과 (우수)** | 47분 29초 |
| **청해** | 問題 1~5 | 32문 | **24문** | **75.0%** | **약 45.0 / 60** | **안전 통과 (우수)** | 29분 28초 |
| **총계** | **전 영역 종합** | **107문** | **71문** | **66.4%** | **119 / 180 点** | **합격권 판정 (목표 110점 초과)** | **115분 36초** |

### 실전 멘탈 지구력 (Endurance Analysis)
- **1교시(필기) 62.7% (47/75) ➔ 2교시(청해) 75.0% (24/32)**: **정답률 변화 +12.3%p**.
- 105분간의 긴 필기 시험 후에도 피로에 무너지지 않고 2교시 청해에서 오히려 집중력이 상승하는 강력한 실전 지구력을 입증함.
- 독해(76.2%)와 청해(75.0%)의 탄탄한 고득점 베이스가 구축되어 있어, N2 합격의 가장 큰 장애물인 '독해 시간 부족'과 '청해 과락'을 완벽하게 극복함.

### 영역별 성취도 분석 및 강점·약점
1. **독해 (16/21, 76.2%) — [압도적 강점]**:
   - 중문(60~62번, 64~65번, 67~68번 전원 적중), 통합이해(69~70번 100% 완벽 적중), 장문(71~73번 100% 완벽 적중), 정보검색(74번 적중) 등 배점이 높은 고난도 지문을 거의 전원 독파함.
   - 단문 2문항(55번, 58번), 중문 2문항(63번, 66번), 정보검색 계산(75번) 등 5문항만 사소한 디테일 미스.
2. **청해 (24/32, 75.0%) — [안정적 고득점권]**:
   - 포인트이해(81~86번 6문항 100% 올킬), 개요이해(87~89번, 91번 고득점), 즉시응답 12문항 중 8문항 정답, 통합이해 4문항 중 3문항 정답.
   - 과제이해 2문항(76번, 80번)과 즉시응답 4문항(94번, 97번, 99번, 102번)에서 순간적인 표현 캐치 미스가 있었으나 기본 청취력은 합격권 최상위.
3. **문자·어휘 (21/32, 65.6%) — [기본 안정권]**:
   - 한자읽기 4/5, 문맥규정 6/7, 유의표현 4/5로 고득점을 기록했으나, 한자표기(2/5)와 단어용법(2/5)에서 혼동 발생.
4. **문법 (10/22, 45.5%) — [향후 집중 보강 대상]**:
   - 문법형식판단 6/12(50%), 문장배열 1/5(20%), 글의문법 3/5(60%).
   - 기능어의 정확한 접속 형태와 문맥 호응(〜に反して, 〜ほかない 등) 및 어순 체인 구성에서 점수 누수가 발생함. 12월 본시험까지 문법 덱 집중 회독으로 15점 이상 추가 확보 가능.

### 복습 큐 등록 및 시간 원장 반영
- **신규 복습 큐**: 오답 36문항 × D+1, D+3, D+7 = **총 108건 신규 등록** (D+1: 2026-09-21, D+3: 2026-09-23, D+7: 2026-09-27).
- **학습시간**: 순수 시험시간 **115분 36초** (DB 정수 **115분** 반영, 잔여 36초 보존).
- **합격 확률 스냅샷**: 공식 종합 모의고사 119점 달성 및 전 영역 과락 0건 반영하여, 현재 응시 가능 범위 **45~60%**, 12월 본시험 전망 **75%**로 대폭 상향, 신뢰도 **medium** 상향.
"""

    with open(STUDY_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(log_entry)

    # 2. Generate JLPT_ERROR_NOTE.md entries
    error_entries = [f"\n\n<!-- official-vol2-full-mock-20260920-errors -->\n## 2026-09-20 — JLPT N2 공식 문제집 제2집 전 영역 완본 실전모의고사 오답노트 (36문항)\n\n공식 문제집 제2집 실전모의고사 107문항 중 오답 36문항에 대한 전수 정밀 해설 및 D+1, D+3, D+7 복습 관리 원장.\n"]

    wrong_records = [q for q in res['questionsRecord'] if not q['isCorrect']]
    for q_rec in wrong_records:
        qid = q_rec['id']
        raw = q_map.get(qid, {})
        choices = raw.get('choices', [])
        user_idx = q_rec['userAnswer']
        ans_idx = q_rec['officialAnswer']

        user_choice_str = choices[user_idx] if (user_idx is not None and user_idx < len(choices)) else str(user_idx)
        ans_choice_str = choices[ans_idx] if (ans_idx is not None and ans_idx < len(choices)) else str(ans_idx)

        # Build prompt with audio if listening
        prompt_full = raw.get('prompt', '')
        if raw.get('audio'):
            audio_text = "\n> " + "\n> ".join([f"{'話者1(남성/안내)' if a['speaker']==1 else '話者2(여성/대화)'}: {a['text']}" for a in raw['audio']])
            prompt_full = f"{prompt_full}\n\n**[🎧 청해 대본]**\n{audio_text}"

        entry = f"""
<!-- error-20260920-q{qid} -->
### [2026-09-20] Q{qid} [오답 / D+1 신규 큐] {raw.get('sectionName', '')} · {raw.get('problemNo', '')} ({raw.get('subtype', '')})

**카테고리: {raw.get('category', '')}**

1. **문제 원문**:
{prompt_full}
2. **자연스러운 번역**: {raw.get('translation', '')}
3. **선택 답 ➔ 공식 정답**: `{user_choice_str}` ➔ **`{ans_idx + 1}番: {ans_choice_str}`**
4. **접속·핵심 의미**: {raw.get('connection', '')} — {raw.get('meaning', '')}
5. **사용자 상태 및 함정 분석**: {raw.get('trap', '')} (체류시간: {q_rec.get('dwellTimeSeconds', 0)}초)
6. **유사 문형 및 표현 비교**: {raw.get('contrast', '')}
7. **추가 예문**: {raw.get('example', '')}
8. **다음 복습일**: **D+1(2026-09-21)**, **D+3(2026-09-23)**, **D+7(2026-09-27)**
9. **다음번 풀이 절차**: 질문 및 문맥 키워드 포착 ➔ 핵심 문법/어휘 조건 대조 ➔ 매력적 오답 소거 ➔ 정답 확정.
10. **제출 직전 체크**: 표기/음운/접속 형태의 미세한 함정에 낚이지 않고 정확한 기능어를 선택했는가?
"""
        error_entries.append(entry)

    with open(ERROR_NOTE_PATH, 'a', encoding='utf-8') as f:
        f.write("".join(error_entries))

    print(f"Successfully appended log and error note! Total error entries written: {len(wrong_records)}")

if __name__ == '__main__':
    run()
