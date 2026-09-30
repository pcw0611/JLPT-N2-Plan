import json
import re

def verify():
    # 1. Verify JSON
    with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data['questions']
    assert len(questions) == 102, f"Expected 102 questions in JSON, got {len(questions)}"

    for i, q in enumerate(questions):
        assert q['id'] == i + 1, f"Question ID mismatch at index {i}: {q['id']}"
        assert len(q['choices']) in [3, 4], f"Invalid choice count at Q{q['id']}: {len(q['choices'])}"
        assert 0 <= q['answer'] < len(q['choices']), f"Invalid answer index at Q{q['id']}: {q['answer']}"
        assert len(q['prompt']) > 0, f"Empty prompt at Q{q['id']}"

    print("PASS: database/past_exams/2023_12.json verified successfully!")

    # 2. Verify HTML
    for target in ['quiz_sites/n2-past-exam-202312-mock.html', 'jlpt-calendar-site/public/exams/n2-past-exam-202312-mock.html']:
        with open(target, 'r', encoding='utf-8') as f:
            html = f.read()

        # Check total questions in RAW_QUESTIONS
        m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);\s*\n\s*// State Variables', html, re.DOTALL)
        assert m, f"RAW_QUESTIONS not found in {target}"
        raw_q = json.loads(m.group(1))
        assert len(raw_q) == 102, f"Expected 102 questions in HTML {target}, got {len(raw_q)}"

        # Check video is hidden
        assert 'left: -9999px' in html or 'opacity: 0' in html, f"Video not properly hidden in {target}"
        assert 'aspect-video max-h-56' not in html, f"Old visible video box still present in {target}"

        # Check audio controller exists
        assert 'btn-play-toggle' in html, f"Play toggle button missing in {target}"
        assert 'toggleAudioPlay' in html, f"toggleAudioPlay JS missing in {target}"
        assert 'seekAudioTime' in html, f"seekAudioTime JS missing in {target}"

        print(f"PASS: {target} verified successfully!")

if __name__ == '__main__':
    verify()
