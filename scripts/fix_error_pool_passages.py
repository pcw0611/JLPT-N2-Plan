# -*- coding: utf-8 -*-
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

# 1. Load midterm 20260920
with open(ROOT / 'jlpt-calendar-site/public/exams/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    text_mid = f.read()
m_mid = re.search(r'const (?:QUESTIONS|RAW_QUESTIONS|examData|questions)\s*=\s*(\[.*?\]);\s*\n', text_mid, re.DOTALL)
mid_questions = {q['id']: q for q in json.loads(m_mid.group(1))}

# 2. Load past 202312
with open(ROOT / 'jlpt-calendar-site/public/exams/n2-past-exam-202312-mock.html', 'r', encoding='utf-8') as f:
    text_past = f.read()
m_past = re.search(r'const (?:QUESTIONS|RAW_QUESTIONS|examData|questions)\s*=\s*(\[.*?\]);\s*\n', text_past, re.DOTALL)
past_questions = {q['id']: q for q in json.loads(m_past.group(1))}

# Common passage for 20260920 問題9 (Q50~54)
passage_toilet = """【日本発のトイレマーク】<br>
公衆トイレの入り口に描かれている男女の絵のマーク。そのマークがあれば、文字で「トイレ」と書かれていなくても、そこがトイレであることがわかる。世界のあちこちで使われているこのトイレマークが実は日本で生まれたものだということを（ 50 ）。<br>
トイレマークが生まれたのは、１９６４年の東京オリンピックがきっかけだ。この東京オリンピックは、アルファベットを使わない国での初めての開催であったため、特に問題になったのが、言葉の壁だった。当時、日本国内の案内板は「お手洗い」などと日本語で書かれているものがほとんどだった。（ 51 ）、それでは世界９０数か国から来日する選手たちに理解してもらえない。かといって、参加国すべての国の言葉で書くわけにもいかない。<br>
そこで考え出されたのが、文字の代わりに絵を使って情報を伝える方法だった。デザイナーたちが集まり、知恵を出し合って、一目で意味が伝わるマークが次々と生み出された。トイレマークも（ 52 ）一つである。<br>
このマークの優れた点は、誰にでも直感的に伝わるわかりやすさだけでなく、社会の共有財産として（ 53 ）ように、デザイナーたちが著作権を放棄したことである。そのおかげで、マークは急速に世界中へと広まっていった。<br>
現在、私たちが日常的に目にするピクトグラム（絵文字）の原点は、まさにこの東京オリンピックの挑戦に（ 54 ）。"""

# Common passage for 202312 問題9 (Q48~51)
passage_rest = """【文章】<br>
日々の仕事で高いパフォーマンスを発揮するためには、適度な休息が不可欠である。（ 48 ）、多くのビジネスパーソンは休むことに罪悪感を抱きがちである。しかし、適切なタイミングでリフレッシュを（ 49 ）。短時間の散歩や軽いストレッチに時間を（ 50 ）。限界まで（ 51 ）は、回復に何倍もの時間がかかってしまうからである。"""

def extract_passage(instruction_text):
    # Split instruction text into prompt and passage
    # Usually starts with 【文章...】 or 【社内通知】 or 【ミハマホテル...】
    for marker in ['【文章', '【社内通知', '【ミハマホテル', '【日本発']:
        if marker in instruction_text:
            idx = instruction_text.find(marker)
            passage = instruction_text[idx:].strip()
            # replace newlines with <br>
            return passage.replace('\r\n', '<br>').replace('\n', '<br>')
    return instruction_text.replace('\r\n', '<br>').replace('\n', '<br>')

def fix_pool_file(filepath):
    print(f"Fixing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    m_pool = re.search(r'const ALL_ERROR_QUESTIONS = (\[.*?\]);\s*\n', content)
    if not m_pool:
        print(f"  ALL_ERROR_QUESTIONS not found in {filepath}")
        return False

    pool_questions = json.loads(m_pool.group(1))
    fixed_count = 0

    for q in pool_questions:
        qid = q['id']
        qnum = int(q['q_num'].replace('Q', ''))
        exam_src = q['exam_src']

        # Fix 問題9
        if qid in ['err-lang-22', 'err-lang-23']:
            q['passage_text'] = passage_toilet
            q['question_text'] = f"（ {qnum} ）に入る最もよいものを選んでください。"
            fixed_count += 1
        elif qid in ['err-lang-51', 'err-lang-52', 'err-lang-53', 'err-lang-54']:
            q['passage_text'] = passage_rest
            q['question_text'] = f"（ {qnum} ）に入る最もよいものを選んでください。"
            fixed_count += 1
        # Fix reading comprehension without passage
        elif len(q.get('passage_text', '')) == 0 and ('読解' in q.get('section', '') or '情報検索' in q.get('mondai_title', '') or '読解' in q.get('mondai_title', '')):
            if '第2集' in exam_src:
                orig = mid_questions.get(qnum)
            else:
                orig = past_questions.get(qnum)

            if orig:
                orig_instr = orig.get('instruction', '')
                extracted_passage = extract_passage(orig_instr)
                q['passage_text'] = extracted_passage
                if orig.get('prompt'):
                    q['question_text'] = orig.get('prompt')
                fixed_count += 1
                print(f"  Fixed reading {qid} ({q['q_num']}) with passage len {len(extracted_passage)}")
            else:
                print(f"  Warning: orig not found for {qid}")

    # Format JSON
    new_json_str = json.dumps(pool_questions, ensure_ascii=False)
    # Replace in content
    new_content = content[:m_pool.start(1)] + new_json_str + content[m_pool.end(1):]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  Done fixing {filepath}, {fixed_count} questions updated.")
    return True

target_files = [
    ROOT / 'jlpt-calendar-site/public/exams/n2-mock-error-review-pool.html',
    ROOT / 'jlpt-calendar-site/dist/client/exams/n2-mock-error-review-pool.html',
    ROOT / 'quiz_sites/n2-mock-error-review-pool.html'
]

for tf in target_files:
    if tf.exists():
        fix_pool_file(tf)
