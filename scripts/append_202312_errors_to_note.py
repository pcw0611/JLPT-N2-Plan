import json

def generate_error_notes():
    with open('scratch/raw_submission.json', 'r', encoding='utf-8') as f:
        sub = json.load(f)

    with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
        exam = json.load(f)

    ref_map = {q['id']: q for q in exam['questions']}

    records = sub['questionsRecord']
    wrong_records = [r for r in records if not r['isCorrect']]

    out_lines = []
    out_lines.append("")
    out_lines.append("")
    out_lines.append("<!-- official-past-202312-full-mock-20260930-errors -->")
    out_lines.append("## 2026-09-30 — 2023年 第2回 (12月) JLPT N2 本試験 全領域 実戦模試 오답노트 (51문항)")
    out_lines.append("")
    out_lines.append("2023년 12월 JLPT N2 본시험 기출 완본 실전모의고사 102문항 중 오답 51문항에 대한 전수 정밀 해설 및 D+1(2026-10-01), D+3(2026-10-03), D+7(2026-10-07) 복습 관리 원장.")
    out_lines.append("")

    for r in wrong_records:
        qid = r['id']
        ref = ref_map.get(qid, {})
        user_ans = r['userAnswer']
        off_ans = r['officialAnswer']
        dwell = r.get('dwellTimeSeconds', 0)
        choices = ref.get('choices', [])

        user_text = choices[user_ans] if (user_ans is not None and user_ans < len(choices)) else str(user_ans)
        off_text = choices[off_ans] if (off_ans is not None and off_ans < len(choices)) else str(off_ans)

        section_name = ref.get('sectionName', '言語知識・読解')
        problem_no = ref.get('problemNo', r.get('problemNo', ''))
        subtype = ref.get('subtype', '')
        category = ref.get('category', r.get('category', ''))
        prompt = ref.get('prompt', '')
        translation = ref.get('translation', '')
        connection = ref.get('connection', '')
        meaning = ref.get('meaning', '')
        trap = ref.get('trap', '')
        contrast = ref.get('contrast', '')
        example = ref.get('example', '')

        out_lines.append(f"<!-- error-20260930-q{qid} -->")
        out_lines.append(f"### [2026-09-30] Q{qid} [오답 / D+1 신규 큐] {section_name} · {problem_no} ({subtype})")
        out_lines.append("")
        out_lines.append(f"**카테고리: {category}**")
        out_lines.append("")
        out_lines.append("1. **문제 원문**:")
        out_lines.append(f"{prompt}")
        out_lines.append(f"2. **자연스러운 번역**: {translation}")
        out_lines.append(f"3. **선택 답 ➔ 공식 정답**: `{user_text}` ➔ **`{off_ans + 1}番: {off_text}`**")
        out_lines.append(f"4. **접속·핵심 의미**: {connection} — {meaning}")
        out_lines.append(f"5. **사용자 상태 및 함정 분석**: {trap} (체류시간: {dwell}초)")
        out_lines.append(f"6. **유사 문형 및 표현 비교**: {contrast}")
        out_lines.append(f"7. **추가 예문**: {example}")
        out_lines.append("8. **다음 복습일**: **D+1(2026-10-01)**, **D+3(2026-10-03)**, **D+7(2026-10-07)**")
        out_lines.append("9. **다음번 풀이 절차**: 질문 및 문맥 키워드 포착 ➔ 핵심 문법/어휘 조건 대조 ➔ 매력적 오답 소거 ➔ 정답 확정.")
        out_lines.append("10. **제출 직전 체크**: 표기/음운/접속 형태의 미세한 함정에 낚이지 않고 정확한 기능어를 선택했는가?")
        out_lines.append("")

    with open('JLPT_ERROR_NOTE.md', 'a', encoding='utf-8') as f:
        f.write("\n".join(out_lines))

    print(f"Appended {len(wrong_records)} error notes to JLPT_ERROR_NOTE.md!")

if __name__ == '__main__':
    generate_error_notes()
