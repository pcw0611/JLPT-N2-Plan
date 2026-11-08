"""Merge the verified actual July submission into the existing review pool."""
import json, re, html, subprocess, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html'
s = p.read_text(encoding='utf-8')
pattern = r'const ALL_ERROR_QUESTIONS\s*=\s*(\[.*?\]);'
old = json.loads(re.search(pattern, s, re.S)[1])
questions = [q for q in old if not q['id'].startswith('err-202307-')]
exam = json.loads((ROOT/'database/past_exams/2023_07_exam.json').read_text(encoding='utf-8'))
import sqlite3
with sqlite3.connect(ROOT/'database/jlpt_learning.db') as c:
    payload = json.loads(c.execute("select notes from tests where id='online-sub-37'").fetchone()[0])['submitted_result']
attempts = {a['item_no']:a for a in payload['details']['attempts']}
timeline = {q['id']:q for q in json.loads((ROOT/'scripts/n2_202307_complete_audio_timeline.json').read_text(encoding='utf-8'))['items']}
audio_dir = ROOT/'jlpt-calendar-site/public/exams/audio_clips'
audio_dir.mkdir(exist_ok=True)
sections = {'vocabulary':'言語知識 (文字・語彙)', 'grammar':'文法', 'reading':'読解', 'listening':'聴解'}
for q in exam['questions']:
    a = attempts[q['id']]
    if a['status'] != 'wrong': continue
    e = q['explanation']; listening = q['section']=='listening'
    audio = ''
    if listening:
        t = timeline[q['id']]; start=t['startSeconds']; end=t['nextBoundarySeconds']
        if q['id'] in (100,101): start=timeline[100]['startSeconds']; end=timeline[101]['nextBoundarySeconds']
        audio=f'n2-202307-q{q["id"]}.mp3'
        if not (audio_dir/audio).exists():
            subprocess.run([shutil.which('ffmpeg'),'-v','error','-ss',str(start),'-i',str(ROOT/'jlpt-calendar-site/public/exams/assets/n2-202307-recording.mp3'),'-t',str(end-start),'-c:a','libmp3lame','-b:a','80k',str(audio_dir/audio)],check=True)
    def esc(v): return html.escape(str(v))
    explanation=f'<h3>{esc(q["category"])}</h3><p>검토한 기출 자료 기준 정답: {q["answer"]+1}번 · {esc(a["correct_text"])}</p><p>원 시험 선택: {a["selected_index"]+1}번 · {esc(a["selected_text"])}</p>'
    for title,key in [('핵심 번역','translation'),('정답 근거·접속·의미','reason'),('함정','trap'),('유사 표현 비교','contrast')]:
        explanation+=f'<h4>{title}</h4><p>{esc(e.get(key,""))}</p>'
    explanation+='<h4>예문</h4><p>'+q.get('reviewExample',esc(e.get('exampleJa','')))+'<br>'+esc(e.get('exampleKo',''))+'</p>'
    if listening: explanation+='<h4>청해 대본 (제출 후 공개)</h4><div style="white-space:pre-wrap">'+q.get('reviewTranscript',esc(q.get('transcript','')))+'</div><p>비TTS 보완 녹음 · Ánh sensei 공개 자료 기반. 원음 구간 분할, 공식 배포 음원이라는 보증은 없음.</p>'
    explanation+='<p>원 시험 오답 복습일: 2026-11-09 / 11-11 / 11-15. 이 화면의 복습 상태는 브라우저에 별도 보존됩니다.</p>'
    choices=q['choices']; prompt=q['prompt']; passage=q.get('passage','')
    if listening:
        if not q.get('printedChoices'): choices=[str(i+1) for i in range(len(choices))]
        if not q.get('printedPrompt'): prompt='音声を聞いて答えてください。'
        passage=''
    questions.append(dict(id=f'err-202307-{q["id"]:03}',global_id=1000+q['id'],is_listening=listening,section=sections[q['section']],exam_src='2023年7月 本試験資料',q_num=f'Q{q["id"]:02}',mondai_title=f'{q["problemNo"]} ({q["part"]})',category_detail=q['category'],type_label=q['part'],instruction=q['instruction'],passage_text=passage,question_text=prompt,choices=choices,correct_num=q['answer']+1,correct_text=a['correct_text'],my_past_answer=a['selected_text'],audio_file=audio,explanation_html=explanation))
assert len(questions)==139 and len({q['id'] for q in questions})==139
for q in questions:
    q.setdefault('type_label',re.sub(r'^問題\d+\s*','',q['mondai_title']).strip(' ()（）'))
s=re.sub(pattern,lambda m:'const ALL_ERROR_QUESTIONS = '+json.dumps(questions,ensure_ascii=False)+';',s,flags=re.S)
s=s.replace('87문항','139문항').replace('87問','139問').replace('87개','139개').replace('전영역 87제','전영역 139제')
s=s.replace('★ 2023.12 기출 본시험 & 공식 제2집 모의고사 오답노트 전수 수록 (139문항 완비) ★','공식 제2집 36문항 · 2023.12 51문항 · 2023.07 52문항 = 총 139문항')
# One scope is used by the lobby, counts and the question browser.
for fn in ['updateLobbyMasteredUI','updateAnkiDeckUI','startExam']:
    start=s.index('  function '+fn+'('); end=s.find('\n  function ',start+5)
    s=s[:start]+s[start:end].replace('ALL_ERROR_QUESTIONS','getScopedQuestions()')+s[end:]
s=s.replace("return ALL_ERROR_QUESTIONS.filter(q => {", "return getScopedQuestions().filter(q => {")
s=s.replace("if (state.ankiFilter === 'due' && srs.status !== 'due') return false;", "if (state.ankiFilter === 'due' && !(state.srsData[q.id]?.nextReviewDate <= getTodayStr())) return false;")
s=s.replace("    let pool = [];\n    if (state.course", "    let pool = [];\n    if (state.course")
# Freeze the first instant-feedback answer; batch answers remain editable without auto-navigation.
s=s.replace('  function selectAnswer(choiceNum) {','  function selectAnswer(choiceNum) {\n    if (state.submitted || (state.feedbackMode === \'instant\' && state.currentAnswered)) return;')
a=s.index('  function selectAnswer('); b=s.index('  function showInstantFeedback(',a)
s=s[:a]+s[a:b].replace("      if (state.currentIndex < state.activeQuestions.length - 1) {\n        state.currentIndex++;\n        renderQuestion();\n      }",'')+s[b:]
s=s.replace('  function finishExam(isPartial = false) {','  function finishExam(isPartial = false) {\n    if (state.submitted) return;\n    state.elapsedSec = Math.floor((Date.now() - state.startTime) / 1000);')
s=s.replace("    state.startTime = Date.now();", "    $('hudTimer').textContent = '00:00';\n    state.startTime = Date.now();")
s=s.replace("      const key =", "      const key =")
s=s.replace("      if (state.submitted || $('screenExam').classList.contains('hidden')) return;", "      if (state.submitted || $('screenExam').classList.contains('hidden')) return;\n      if (['INPUT','SELECT','TEXTAREA'].includes(e.target.tagName)) return;\n      if (['partialSubmitModal','fullSubmitModal'].some(id => $(id) && !$(id).classList.contains('hidden'))) return;")
# Stop old playback even when moving to another listening item; report load errors.
s=s.replace("    const audioPlayer = $('audioPlayer');", "    const audioPlayer = $('audioPlayer');\n    audioPlayer.pause();\n    audioPlayer.onerror = () => $('audioStatusText').textContent = '音声を読み込めません。接続を確認して再生してください。';")
s=s.replace('공식 정답:', '자료 기준 정답:')
s=s.replace('<span>分からない (모름 / 확실하지 않음)</span>','<span>分からない</span>')
# Exact source text stays without ruby until grading.
s=s.replace("    $('qQuestionSentence').innerHTML = q.question_text;", "    $('qQuestionSentence').innerHTML = withoutRuby(q.question_text);\n    passageBox.querySelectorAll('rt,rp').forEach(n=>n.remove());")
s=s.replace('${choiceText}</span>', '${withoutRuby(choiceText)}</span>')
if '/exams/mock-review-filters.js' not in s: s=s.replace('</body>','<script src="/exams/mock-review-filters.js"></script>\n</body>')
p.write_text(s,encoding='utf-8')
(ROOT/'quiz_sites/n2-mock-error-review-pool.html').write_text(s,encoding='utf-8')
print('Merged139 questions, including52 July errors and17 listening clips')
