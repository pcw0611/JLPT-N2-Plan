import re
import json
import os
import sys

def verify():
    html_path = 'quiz_sites/n2-past-exam-202312-mock.html'
    assert os.path.exists(html_path), f"File not found: {html_path}"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    errors = []
    warnings = []

    # 1. Check title & headers
    if "2023年 第2回 (12月) JLPT N2 本試験 全領域 実戦模試 (104問)" not in html:
        errors.append("Title mismatch or missing in HTML")

    # 2. Extract RAW_QUESTIONS
    m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);\s*\n\s*// State Variables', html, re.DOTALL)
    if not m:
        errors.append("Could not extract RAW_QUESTIONS from HTML")
        questions = []
    else:
        try:
            questions = json.loads(m.group(1))
        except Exception as e:
            errors.append(f"JSON parse error in RAW_QUESTIONS: {e}")
            questions = []

    if len(questions) != 104:
        errors.append(f"Expected 104 questions, found {len(questions)}")

    # 3. Contiguity and field checks
    section1_count = 0
    section2_count = 0
    vocab_count = 0
    grammar_count = 0
    reading_count = 0
    listening_count = 0

    for idx, q in enumerate(questions):
        expected_id = idx + 1
        qid = q.get('id')
        if qid != expected_id:
            errors.append(f"Item {idx}: ID is {qid}, expected {expected_id}")

        sec = q.get('sectionName')
        part = q.get('part')
        prob = q.get('problemNo')
        choices = q.get('choices', [])
        ans = q.get('answer')
        prompt = q.get('prompt', '')
        cat = q.get('category', '')

        if q.get('section') == 1 or sec == '言語知識・読解':
            section1_count += 1
            if part == '文字・語彙': vocab_count += 1
            elif part == '文法': grammar_count += 1
            elif part == '読解': reading_count += 1
            else: errors.append(f"Q{qid}: Unknown part in section 1: {part}")
        elif q.get('section') == 2 or sec == '聴解':
            section2_count += 1
            if part == '聴解': listening_count += 1
            else: errors.append(f"Q{qid}: Unknown part in section 2: {part}")
        else:
            errors.append(f"Q{qid}: Unknown section: {sec}")

        # Choice and answer validity
        if not isinstance(choices, list) or len(choices) < 3:
            errors.append(f"Q{qid}: invalid choices len {len(choices)}")
        if not isinstance(ans, int) or ans < 0 or ans >= len(choices):
            errors.append(f"Q{qid}: invalid answer {ans} for {len(choices)} choices")

        # Category check
        if '→' not in cat:
            warnings.append(f"Q{qid}: category does not have '→': {cat}")

        # Prompt
        if not prompt.strip():
            errors.append(f"Q{qid}: empty prompt")

        # Listening audio check
        if sec == '聴解':
            audio = q.get('audio', [])
            if not audio or len(audio) == 0:
                errors.append(f"Q{qid}: listening question missing audio script")
            for line in audio:
                if 'text' not in line or not line['text'].strip():
                    errors.append(f"Q{qid}: audio line missing text")
                if 'speaker' not in line:
                    errors.append(f"Q{qid}: audio line missing speaker")

    # Count validations
    if section1_count != 72: errors.append(f"Section 1 count is {section1_count}, expected 72")
    if section2_count != 32: errors.append(f"Section 2 count is {section2_count}, expected 32")
    if vocab_count != 30: errors.append(f"Vocab count is {vocab_count}, expected 30")
    if grammar_count != 21: errors.append(f"Grammar count is {grammar_count}, expected 21")
    if reading_count != 21: errors.append(f"Reading count is {reading_count}, expected 21")
    if listening_count != 32: errors.append(f"Listening count is {listening_count}, expected 32")

    # 4. Check HTML script references
    if "loadQuestion(72)" not in html:
        errors.append("loadQuestion(72) not found in script (listening start)")
    if "index === 71" not in html:
        errors.append("index === 71 not found in script (section 1 boundary)")
    if "72 問" not in html:
        errors.append("Section 1 72 問 label not found")
    if "32 問" not in html:
        errors.append("Section 2 32 問 label not found")

    report_lines = [
        "=" * 60,
        "VERIFICATION REPORT FOR: n2-past-exam-202312-mock.html",
        "=" * 60,
        f"Total Questions: {len(questions)}",
        f"  - Section 1 (Language Knowledge & Reading): {section1_count} items",
        f"    * Vocab: {vocab_count} items (IDs 1~30)",
        f"    * Grammar: {grammar_count} items (IDs 31~51)",
        f"    * Reading: {reading_count} items (IDs 52~72)",
        f"  - Section 2 (Listening): {section2_count} items (IDs 73~104)",
        f"Errors: {len(errors)}"
    ]
    for e in errors:
        report_lines.append(f"  [ERROR] {e}")
    report_lines.append(f"Warnings: {len(warnings)}")
    for w in warnings[:5]:
        report_lines.append(f"  [WARN] {w}")
    report_lines.append("=" * 60)

    report_text = "\n".join(report_lines)
    with open("artifact_work/verification_report.txt", "w", encoding="utf-8") as out:
        out.write(report_text + "\n")
    print(report_text)

    if errors:
        sys.exit(1)
    else:
        print("SUCCESS: ALL INTEGRITY CHECKS PASSED PERFECTLY!")

if __name__ == '__main__':
    verify()
