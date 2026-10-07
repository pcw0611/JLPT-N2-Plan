# -*- coding: utf-8 -*-
"""Full generator for updated listening error note cards."""
import sys, json, re, html

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_25_listening_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

with open('scratch/translations_25.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Classify each card
# Returns (is_audio_only, problem_type_label, instruction_text)
def get_card_type_info(exam, qid):
    if exam == '1회':
        if qid in [76, 80]:
            return (False, '問題1 (課題理解)', '問題１では、まず質問を聞いてください。それから話を聞いて、問題用紙の１から４の中から、最もよいものを一つ選んでください。')
        elif qid == 90:
            return (True, '問題3 (概要理解)', '問題３では、問題用紙に何も印刷されていません。この問題は、全体としてどんな内容かを聞く問題です。話の前に質問はありません。まず話を聞いてください。それから、質問と選択肢を聞いて、１から４の中から、最もよいものを一つ選んでください。')
        elif qid in [94, 97, 99, 102]:
            return (True, '問題4 (即時応答)', '問題４では、問題用紙に何も印刷されていません。まず文を聞いてください。それから、その返事を聞いて、１から３の中から、最もよいものを一つ選んでください。')
        elif qid == 106:
            return (False, '問題5 (統合理解)', '問題５では、長めの話を聞きます。まず話を聞いてください。それから、質問を聞いて、問題用紙の１から４の中から、最もよいものを一つ選んでください。')
    else: # 2회
        if qid in [75, 76, 77]:
            return (False, '問題1 (課題理解)', '問題１では、まず質問を聞いてください。それから話を聞いて、問題用紙の１から４の中から、最もよいものを一つ選んでください。')
        elif qid in [78, 80, 82]:
            return (False, '問題2 (ポイント理解)', '問題２では、まず質問を聞いてください。そのあと、問題用紙の選択肢を読んでください。読む時間があります。それから話を聞いて、最もよいものを一つ選んでください。')
        elif qid in [85, 86, 88]:
            return (True, '問題3 (概要理解)', '問題３では、問題用紙に何も印刷されていません。この問題は、全体としてどんな内容かを聞く問題です。話の前に質問はありません。まず話を聞いてください。それから、質問と選択肢を聞いて、１から４の中から、最もよいものを一つ選んでください。')
        elif qid in [89, 90, 91, 95, 97, 98, 99]:
            return (True, '問題4 (即時応答)', '問題４では、問題用紙に何も印刷されていません。まず文を聞いてください。それから、その返事を聞いて、１から３の中から、最もよいものを一つ選んでください。')
        elif qid == 101:
            return (False, '問題5 (統合理解)', '問題５では、長めの話を聞きます。まず話を聞いてください。それから、質問を聞いて、問題用紙の１から４の中から、最もよいものを一つ選んでください。')
    return (False, '聴解', '')

# Extract components from old front
def extract_front_components(front_html):
    # Prompt text
    m_prompt = re.search(r'margin-bottom:16px; word-break:keep-all;">\s*(.*?)\s*</div>', front_html, re.DOTALL)
    if not m_prompt:
        m_prompt = re.search(r'font-size:18px;[^>]*>\s*(.*?)\s*</div>', front_html, re.DOTALL)
    prompt_text = m_prompt.group(1).strip() if m_prompt else ''

    # Choices (either format)
    # Format 1: flex column with items
    choices = []
    c_matches = re.findall(r'<div[^>]*padding:10px 14px;[^>]*>\s*<b[^>]*>([1-5]\.)</b>\s*([^<]+)</div>', front_html)
    if c_matches:
        for num, text in c_matches:
            choices.append(f"{num} {text.strip()}")
    else:
        # Format 2: margin:4px 0
        c_matches2 = re.findall(r"<div[^>]*font-size:15px;[^>]*>([1-5]\.\s*[^<]+)</div>", front_html)
        if c_matches2:
            choices = [c.strip() for c in c_matches2]
    
    return prompt_text, choices

# Test extraction for all 25 cards
print(f"{'Idx':>3} {'Exam':>4} {'Q':>4} {'AudioOnly':>10} {'PromptLen':>10} {'ChoicesCnt':>10}")
print("-" * 50)
for i, c in enumerate(cards):
    exam = c['exam']
    qid = c['qid']
    is_audio_only, ptype, instr = get_card_type_info(exam, qid)
    prompt, choices = extract_front_components(c['front'])
    print(f"{i+1:3d} {exam:>4} Q{qid:03d} {str(is_audio_only):>10} {len(prompt):>10} {len(choices):>10}")

