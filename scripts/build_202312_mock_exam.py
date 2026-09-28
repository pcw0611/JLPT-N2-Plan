import json
import re

def build():
    # 1. Load 2023_12.json
    with open('database/past_exams/2023_12.json', 'r', encoding='utf-8') as f:
        data_2023_12 = json.load(f)

    questions = data_2023_12['questions']
    assert len(questions) == 104, f"Expected 104 questions, got {len(questions)}"

    # 2. Load base HTML template
    with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace title
    html = re.sub(
        r'<title>.*?</title>',
        '<title>JLPT N2 2023年 第2回 (12月) 本試験 全領域 実戦模試 (104問)</title>',
        html
    )

    # Replace header box titles
    html = html.replace(
        '日本語能力試験 公式問題集 第２集 原本対照 · 個人学習用 実戦模試',
        '2023年 第2回 (12月) JLPT N2 本試験 原本対照 · 個人学習用 実戦模試'
    )
    html = html.replace(
        'Official Practice Workbook Vol. 2 Base (ブラウザTTS聴解演習)',
        'December 2023 Official Exam Base (ブラウザTTS聴解演習)'
    )
    html = html.replace(
        '75 問<br><span class="text-[11px] font-normal text-neutral-500">(問1~75)</span>',
        '72 問<br><span class="text-[11px] font-normal text-neutral-500">(問1~72)</span>'
    )
    html = html.replace(
        '32 問<br><span class="text-[11px] font-normal text-neutral-500">(問76~107)</span>',
        '32 問<br><span class="text-[11px] font-normal text-neutral-500">(問73~104)</span>'
    )
    html = html.replace(
        '<li><strong>1교시(1~75문항)</strong>',
        '<li><strong>1교시(1~72문항)</strong>'
    )
    html = html.replace(
        '<li><strong>2교시 청해(76~107문항) 실전 규격</strong>:',
        '<li><strong>2교시 청해(73~104문항) 실전 규격</strong>:'
    )
    html = html.replace(
        '76번부터 107번까지',
        '73번부터 104번까지'
    )
    html = html.replace(
        '107번의 12초 마킹 카운트다운이 종료되는 순간',
        '104번의 12초 마킹 카운트다운이 종료되는 순간'
    )

    # Replace explanation filter button numbers
    html = html.replace('전체 (107)', '전체 (104)')
    html = html.replace('어휘 (32)', '어휘 (30)')
    html = html.replace('문법 (22)', '문법 (21)')
    html = html.replace('독해 (21)', '독해 (21)')
    html = html.replace('청해 (32)', '청해 (32)')

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
        "document.getElementById('q-total-period-num').textContent = '104';"
    )
    html = html.replace(
        "// 청해 첫 문제(75번 인덱스 = 76번 문항) 로드 및 자동 방송 개시\n      loadQuestion(75);",
        "// 청해 첫 문제(72번 인덱스 = 73번 문항) 로드 및 자동 방송 개시\n      loadQuestion(72);"
    )
    html = html.replace(
        "document.getElementById('q-side-badge').textContent = `問 ${index + 1} / 107`;",
        "document.getElementById('q-side-badge').textContent = `問 ${index + 1} / 104`;"
    )
    html = html.replace(
        "if (index === 74) {\n          btnNextText.textContent = '第1限 終了へ →';",
        "if (index === 71) {\n          btnNextText.textContent = '第1限 終了へ →';"
    )
    html = html.replace(
        "if (currentIndex < 74) {\n          loadQuestion(currentIndex + 1);",
        "if (currentIndex < 71) {\n          loadQuestion(currentIndex + 1);"
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
        "let startIdx = 0;\n      let endIdx = 72;\n\n      if (currentPhase === 'section2') {\n        startIdx = 72;\n        endIdx = 104;\n        document.getElementById('palette-period-title').textContent = '第2限 聴解パレット (73 ~ 104)';\n      } else {\n        document.getElementById('palette-period-title').textContent = '第1限 パレット (1 ~ 72)';\n      }"
    )
    html = html.replace(
        "let startIdx = currentPhase === 'section2' ? 75 : 0;\n      let endIdx = currentPhase === 'section2' ? 107 : 75;",
        "let startIdx = currentPhase === 'section2' ? 72 : 0;\n      let endIdx = currentPhase === 'section2' ? 104 : 72;"
    )

    # getListeningMeta logic replacement
    old_meta_pattern = re.compile(r'function getListeningMeta\(index\) \{.*?return null;\s*\}', re.DOTALL)
    new_meta_code = """function getListeningMeta(index) {
      const qNum = index + 1; // 73 ~ 104
      if (qNum >= 73 && qNum <= 77) {
        return { probNo: 1, itemNo: qNum - 72, isFirst: qNum === 73, name: "課題理解" };
      } else if (qNum >= 78 && qNum <= 83) {
        return { probNo: 2, itemNo: qNum - 77, isFirst: qNum === 78, name: "ポイント理解" };
      } else if (qNum >= 84 && qNum <= 88) {
        return { probNo: 3, itemNo: qNum - 83, isFirst: qNum === 84, name: "概要理解" };
      } else if (qNum >= 89 && qNum <= 100) {
        return { probNo: 4, itemNo: qNum - 88, isFirst: qNum === 89, name: "即時応答" };
      } else if (qNum >= 101 && qNum <= 104) {
        const map5 = { 101: 1, 102: 2, 103: 3, 104: 3 };
        const isPart3 = (qNum >= 103);
        return { 
          probNo: 5, 
          itemNo: map5[qNum], 
          qNum: qNum,
          isFirst: qNum === 101, 
          name: "統合理解",
          hasPrintedChoices: isPart3
        };
      }
      return null;
    }"""
    html = old_meta_pattern.sub(new_meta_code, html, count=1)

    # Half / Endurance stats replacement
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
      const secondPct = ((secondCorrect / 32) * 100).toFixed(1);

      const firstTime = section1ElapsedSeconds;
      const secondTime = section2ElapsedSeconds;

      document.getElementById('stat-first-half').textContent = `${firstCorrect} / 72 (${firstPct}%)`;
      document.getElementById('stat-first-half-time').innerHTML = `총 ${Math.round(firstTime/60)}분 · 문항당 ${((firstTime/72)).toFixed(1)}초`;

      document.getElementById('stat-second-half').textContent = `${secondCorrect} / 32 (${secondPct}%)`;
      document.getElementById('stat-second-half-time').innerHTML = `총 ${Math.round(secondTime/60)}분 · 문항당 ${((secondTime/32)).toFixed(1)}초`;"""
    html = html.replace(old_endurance, new_endurance)

    # Result JSON metadata replacement
    old_json_meta = """examType: "공식 문제집 제2집 기반 실전모의고사 (개인학습용 / TTS)",
        examTitle: "JLPT N2 実戦模試（公式問題集 第2集ベース / 個人学習用）",
        provenanceNote: "출제 원안: 日本語能力試験 公式問題集 第2集(2018) 대조 / 개인학습용 TTS 구현 / 비공식 정답률 추정","""

    new_json_meta = """examType: "official_past_mock",
        examTitle: "2023年 第2回 (12月) JLPT N2 本試験 全領域 実戦模試 (104問)",
        provenanceNote: "출제 원안: 2023年 第2回 (12月) JLPT N2 本試験 원문 대조 / 개인학습용 TTS 구현 / 비공식 정답률 추정",
        testId: "official-past-202312-full-mock-20261004","""
    html = html.replace(old_json_meta, new_json_meta)

    # Vocab/Grammar totals in result payload
    old_totals = """const vocabTotal = 32, grammarTotal = 22, readingTotal = 21, listeningTotal = 32;
      const langRate = (vocabCorrect + grammarCorrect) / 54;"""
    new_totals = """const vocabTotal = 30, grammarTotal = 21, readingTotal = 21, listeningTotal = 32;
      const langRate = (vocabCorrect + grammarCorrect) / 51;"""
    html = html.replace(old_totals, new_totals)

    target_path = 'quiz_sites/n2-past-exam-202312-mock.html'
    with open(target_path, 'w', encoding='utf-8') as out:
        out.write(html)

    print(f"Successfully generated {target_path} (length: {len(html)} bytes)")

if __name__ == '__main__':
    build()
