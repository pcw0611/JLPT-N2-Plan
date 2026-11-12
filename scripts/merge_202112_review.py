"""Publish the reviewed questions that were missed in the recorded 2021.12 run."""
import html
import json
import re
import sqlite3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'jlpt-calendar-site/public'
EXAMS = PUBLIC / 'exams'
SOURCE = '2021年12月 本試験資料'
SECTIONS = {'vocabulary': '言語知識 (文字・語彙)', 'grammar': '文法', 'reading': '読解', 'listening': '聴解'}
TYPES = {'漢字表記': '表記', '文法形式の判断': '文の文法1', '文の組み立て': '文の文法2'}

def make_item(question, attempt, dates):
    q = question
    number = q['id']
    assert q['answer'] == attempt['correct_index'] and q['itemTypeId'] == attempt['item_type_id']
    listening = q['section'] == 'listening'
    label = TYPES.get(q['part'], q['part'])
    if label == '統合理解':
        label = '統合理解（聴解）' if listening else '統合理解（読解）'
    passage, prompt, choices = q.get('passage', ''), q['prompt'], q['choices']
    audio_file = ''
    if listening:
        audio_file = f'n2-202112-q{number}.mp3'
        start, end = q['audioStart'], q['audioEnd']
        assert 0 <= start < end <= 2603
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(start), '-i',
                        str(EXAMS / 'assets/n2-202112-recording.mp3'), '-t', str(end-start),
                        '-c:a', 'libmp3lame', '-b:a', '80k', str(EXAMS / 'audio_clips' / audio_file)], check=True)
        if not q.get('printedChoices'):
            choices = [str(i + 1) for i in range(len(choices))]
        if not q.get('printedPrompt'):
            prompt = '音声を聞いて答えてください。'
        passage = ''
        if q.get('figure'):
            assert (PUBLIC / q['figure'].lstrip('/')).is_file()
            passage = f'<div><img src="{html.escape(q["figure"], quote=True)}" alt="座席表" style="max-width:100%"></div>'

    e = q['explanation']
    esc = html.escape
    explanation = [f'<h3>{esc(q["category"])}</h3>', f'<p>정답 {q["answer"]+1}번 · {esc(attempt["correct_text"])}</p>',
                   f'<p>원 시험 선택 {attempt["selected_index"]+1}번 · {esc(attempt["selected_text"])}</p>']
    if q.get('completeSentence'):
        explanation.append(f'<p>{esc(q["completeSentence"])}</p>')
    for title, key in [('번역', 'translation'), ('정답 근거', 'reason'), ('함정', 'trap'), ('유사 표현', 'contrast')]:
        explanation.append(f'<h4>{title}</h4><p>{esc(e[key])}</p>')
    explanation.append(f'<h4>예문</h4><p>{q["reviewExample"]}<br>{esc(e["exampleKo"])}</p>')
    if listening:
        explanation.append(f'<h4>청해 대본</h4><div style="white-space:pre-wrap">{q["reviewTranscript"]}</div><p>수험자 제공 녹음 구간 · 비TTS</p>')
    explanation.append(f'<p>원 시험 복습일 {" / ".join(dates)}</p>')
    return dict(id=f'err-202112-{number:03}', global_id=2000+number, is_listening=listening,
                section=SECTIONS[q['section']], exam_src=SOURCE, q_num=f'Q{number:02}',
                mondai_title=f'{q["problemNo"]} ({q["part"]})', category_detail=q['category'],
                type_label=label, instruction=q['instruction'], passage_text=passage,
                question_text=prompt, choices=choices, correct_num=q['answer']+1,
                correct_text=attempt['correct_text'], my_past_answer=attempt['selected_text'],
                audio_file=audio_file, explanation_html=''.join(explanation))

def main():
    page = EXAMS / 'n2-mock-error-review-pool.html'
    source = page.read_text(encoding='utf-8')
    start = re.search(r'const ALL_ERROR_QUESTIONS\s*=\s*', source).end()
    existing, length = json.JSONDecoder().raw_decode(source[start:])
    old = [item for item in existing if not item['id'].startswith('err-202112-')]
    exam = json.loads((ROOT / 'database/past_exams/2021_12_exam.json').read_text(encoding='utf-8'))
    db_uri = (ROOT / 'database/jlpt_learning.db').as_uri() + '?mode=ro'
    with sqlite3.connect(db_uri, uri=True) as connection:
        row = connection.execute('SELECT notes FROM tests WHERE id=?', ('online-sub-54',)).fetchone()
    result = json.loads(row[0])['submitted_result']
    details = result['details']
    assert details['test_id'] == exam['id'] and details['termination_reason'] == 'submitted'
    questions = {q['id']: q for q in exam['questions']}
    missed = [a for a in details['attempts'] if a['status'] == 'wrong']
    assert len(missed) == result['wrongCount'] == 43
    updated = old + [make_item(questions[a['item_no']], a, details['review_dates']) for a in missed]
    assert len(updated) == len({q['id'] for q in updated}) == len({q['global_id'] for q in updated})
    serialized = json.dumps(updated, ensure_ascii=False).replace('</script', '<\\/script')
    source = source[:start] + serialized + source[start+length:]
    source = source.replace('공식 제2집 36문항 · 2023.12 51문항 · 2023.07 52문항 = 총 139문항',
                            f'공식 제2집 36문항 · 2023.12 51문항 · 2023.07 52문항 · 2021.12 43문항 = 총 {len(updated)}문항')
    source = re.sub(r'139(?=問|문항|제)', str(len(updated)), source)
    page.write_text(source, encoding='utf-8')
    (ROOT / 'quiz_sites' / page.name).write_text(source, encoding='utf-8')
    print(f'{len(updated)} questions, {len(missed)} new errors, {sum(a["item_no"] >= 72 for a in missed)} new audio clips')

if __name__ == '__main__':
    main()
