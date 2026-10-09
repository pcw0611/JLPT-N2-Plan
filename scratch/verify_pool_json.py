import json, sys

sys.stdout.reconfigure(encoding='utf-8')

for fp in ['jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html', 'quiz_sites/n2-mock-error-review-pool.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()

    start_marker = 'const ALL_ERROR_QUESTIONS = '
    start_idx = text.find(start_marker) + len(start_marker)

    bracket_depth = 0
    in_string = False
    escape = False
    quote_char = None
    end_idx = -1

    for i in range(start_idx, len(text)):
        c = text[i]
        if in_string:
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == quote_char:
                in_string = False
        else:
            if c in ('"', "'"):
                in_string = True
                quote_char = c
            elif c == '[':
                bracket_depth += 1
            elif c == ']':
                bracket_depth -= 1
                if bracket_depth == 0:
                    end_idx = i + 1
                    break

    questions = json.loads(text[start_idx:end_idx].strip())
    print(f"[{fp}] Successfully parsed {len(questions)} questions!")
    q10 = [q for q in questions if q['id'] == 'err-listen-10'][0]
    assert '動画は申請書の締め切り後、１週間以内の提出だったんだ' in q10['explanation_html']
    assert 'え、そうだったの？私もホームページ見たのに気がつかなかった。ごめんね。' in q10['explanation_html']
    assert '削除しちゃった？' in q10['explanation_html']
    assert '残してあるよ。' in q10['explanation_html']
    assert '締め切り明日だから提出任せるね。' in q10['explanation_html']
    assert '動画作成もすぐに取りかかんなきゃ。応募する以上は絶対出たいからね。' in q10['explanation_html']
    print(f"[{fp}] All assertions passed!")

print("\n>>> ALL VERIFICATIONS PASSED 100%! <<<")
