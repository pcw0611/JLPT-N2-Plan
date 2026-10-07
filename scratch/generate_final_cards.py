# -*- coding: utf-8 -*-
"""Generate final Front and Back HTML using perfect dialogues."""
import sys, json, re, html

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_25_listening_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

with open('scratch/perfect_dialogues_25.json', 'r', encoding='utf-8') as f:
    perfect_dialogues = json.load(f)

def get_card_type_info(exam, qid):
    if exam == '1회':
        exam_title = '제1회 실전 모의고사 (공식 제2집)'
        if qid in [76, 80]:
            return (False, '問題1 (課題理解)', '問題１では、まず質問を聞いてください。それから話を聞いて、問題用紙の１から４の中から、最もよいものを一つ選んでください。', exam_title)
        elif qid == 90:
            return (True, '問題3 (概要理解)', '問題３では、問題用紙に何も印刷されていません。この問題は、全体としてどんな内容かを聞く問題です。話の前に質問はありません。まず話を聞いてください。それから、質問と選択肢を聞いて、１から４の中から、最もよいものを一つ選んでください。', exam_title)
        elif qid in [94, 97, 99, 102]:
            return (True, '問題4 (即時応答)', '問題４では、問題用紙に何も印刷されていません。まず文を聞いてください。それから、その返事を聞いて、１から３の中から、最もよいものを一つ選んでください。', exam_title)
        elif qid == 106:
            return (False, '問題5 (統合理解)', '問題５では、長めの話を聞きます。まず話を聞いてください。それから、質問を聞いて、問題用紙の１から４の中から、最もよいものを一つ選んでください。', exam_title)
    else: # 2회
        exam_title = '제2회 실전 모의고사 (2023.12 기출 완본)'
        if qid in [75, 76, 77]:
            return (False, '問題1 (課題理解)', '問題１では、まず質問を聞いてください。それから話を聞いて、問題用紙の１から４の中から、最もよいものを一つ選んでください。', exam_title)
        elif qid in [78, 80, 82]:
            return (False, '問題2 (ポイント理解)', '問題２では、まず質問を聞いてください。そのあと、問題用紙の選択肢を読んでください。読む時間があります。それから話を聞いて、最もよいものを一つ選んでください。', exam_title)
        elif qid in [85, 86, 88]:
            return (True, '問題3 (概要理解)', '問題３では、問題用紙に何も印刷されていません。この問題は、全体としてどんな内容かを聞く問題です。話の前に質問はありません。まず話を聞いてください。それから、質問と選択肢を聞いて、１から４の中から、最もよいものを一つ選んでください。', exam_title)
        elif qid in [89, 90, 91, 95, 97, 98, 99]:
            return (True, '問題4 (即時応答)', '問題４では、問題用紙に何も印刷されていません。まず文を聞いてください。それから、その返事を聞いて、１から３の中から、最もよいものを一つ選んでください。', exam_title)
        elif qid == 101:
            return (False, '問題5 (統合理解)', '問題５では、長めの話を聞きます。まず話を聞いてください。それから、質問を聞いて、問題用紙の１から４の中から、最もよいものを一つ選んでください。', exam_title)
    return (False, '聴解', '', '')

def extract_front_components(front_html):
    m_prompt = re.search(r'margin-bottom:16px; word-break:keep-all;">\s*(.*?)\s*</div>', front_html, re.DOTALL)
    if not m_prompt:
        m_prompt = re.search(r'font-size:18px;[^>]*>\s*(.*?)\s*</div>', front_html, re.DOTALL)
    prompt_text = m_prompt.group(1).strip() if m_prompt else ''

    choices = []
    c_matches = re.findall(r'<div[^>]*padding:10px 14px;[^>]*>\s*<b[^>]*>([1-5]\.)</b>\s*([^<]+)</div>', front_html)
    if c_matches:
        for num, text in c_matches:
            choices.append(f"{num} {text.strip()}")
    else:
        c_matches2 = re.findall(r"<div[^>]*font-size:15px;[^>]*>([1-5]\.\s*[^<]+)</div>", front_html)
        if c_matches2:
            choices = [c.strip() for c in c_matches2]
    
    return prompt_text, choices

def render_bilingual_script_html(turns):
    items = []
    for t in turns:
        spk = t.get('speaker', '')
        ja = t.get('ja', '')
        ko = t.get('ko', '')
        
        # Color coding speaker
        if spk in ['1', '2', '3', '4']:
            is_correct = '正解' in ja
            num_color = '#16a34a' if is_correct else '#64748b'
            j_html = f"<b style='color:{num_color}; margin-right:6px;'>{spk}.</b> {html.escape(ja)}"
        elif spk:
            color = "#2563eb" if any(w in spk for w in ["女", "妻", "学生（女"]) else "#0284c7" if "先生" in spk else "#475569"
            j_html = f"<b style='color:{color};'>{html.escape(spk)}：</b>{html.escape(ja)}"
        else:
            j_html = html.escape(ja)
            
        k_html = html.escape(ko)
        
        item_html = f"""<div style="margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;">
  <div style="font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;">{j_html}</div>
  <div style="font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;">↳ {k_html}</div>
</div>"""
        items.append(item_html)
        
    return "\n".join(items)

def generate_all():
    final_cards = []
    
    for i, c in enumerate(cards):
        cid = c['cid']
        nid = c['nid']
        exam = c['exam']
        qid = c['qid']
        sound_fn = c['sound']
        old_front = c['front']
        old_back = c['back']
        
        is_audio_only, ptype_label, instr_text, exam_title = get_card_type_info(exam, qid)
        prompt_text, choices = extract_front_components(old_front)
        
        audio_box_label = "🎧 일본 공식 문제집 제2집 본시험 성우 녹음" if exam == '1회' else "🎧 2023.12 JLPT N2 본시험 성우 원본 음원"
        
        # -------------------------------------------------------------
        # FRONT
        # -------------------------------------------------------------
        if is_audio_only:
            front_html = f"""<div style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Hiragino Sans', sans-serif; max-width:620px; margin:0 auto; padding:6px 2px;">
  <!-- Header -->
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:8px; margin-bottom:12px;">
    <span style="font-size:12px; font-weight:700; color:#2563eb; background:#eff6ff; padding:3px 8px; border-radius:6px;">{exam_title} · Q{qid}</span>
    <span style="font-size:12px; font-weight:600; color:#475569;">{ptype_label}</span>
  </div>

  <!-- Instruction -->
  <div style="font-size:13px; color:#64748b; margin-bottom:12px; line-height:1.4;">{instr_text}</div>

  <!-- Audio Player Box -->
  <div style="margin:12px 0 16px 0; padding:14px 12px; background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px; text-align:center;">
    <div style="font-size:12px; font-weight:700; color:#1e40af; margin-bottom:6px;">{audio_box_label}</div>
    [sound:{sound_fn}]
  </div>

  <!-- Real Exam Notice Banner -->
  <div style="padding:14px 16px; background:#f8fafc; border:1.5px dashed #cbd5e1; border-radius:8px; text-align:center; margin-top:12px;">
    <div style="font-size:13px; font-weight:700; color:#475569; margin-bottom:4px;">📝 問題用紙に何も印刷されていません</div>
    <div style="font-size:12px; color:#64748b; line-height:1.5;">음성을 끝까지 주의 깊게 들은 후 정답을 떠올려보세요.<br><span style="color:#2563eb; font-weight:600;">(질문 및 선택지는 음성에서 주어지며, 카드 뒷면에서 확인하실 수 있습니다)</span></div>
  </div>
</div>"""
        else:
            choices_html_list = []
            for ch in choices:
                m_ch = re.match(r'^([1-5]\.?\s*)(.*)$', ch)
                if m_ch:
                    num_part = m_ch.group(1).strip()
                    txt_part = m_ch.group(2).strip()
                    choices_html_list.append(f"""<div style="padding:10px 14px; border:1px solid #e2e8f0; border-radius:8px; font-size:16px; color:#1e293b; background:#f8fafc; line-height:1.45;">
  <b style="color:#64748b; margin-right:8px;">{num_part}</b> {txt_part}
</div>""")
                else:
                    choices_html_list.append(f"""<div style="padding:10px 14px; border:1px solid #e2e8f0; border-radius:8px; font-size:16px; color:#1e293b; background:#f8fafc; line-height:1.45;">{ch}</div>""")
            
            choices_html = "\n".join(choices_html_list)
            
            front_html = f"""<div style="font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Hiragino Sans', sans-serif; max-width:620px; margin:0 auto; padding:6px 2px;">
  <!-- Header -->
  <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:8px; margin-bottom:12px;">
    <span style="font-size:12px; font-weight:700; color:#2563eb; background:#eff6ff; padding:3px 8px; border-radius:6px;">{exam_title} · Q{qid}</span>
    <span style="font-size:12px; font-weight:600; color:#475569;">{ptype_label}</span>
  </div>

  <!-- Instruction -->
  <div style="font-size:13px; color:#64748b; margin-bottom:12px; line-height:1.4;">{instr_text}</div>

  <!-- Audio Player Box -->
  <div style="margin:12px 0 16px 0; padding:12px; background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px; text-align:center;">
    <div style="font-size:12px; font-weight:700; color:#1e40af; margin-bottom:6px;">{audio_box_label}</div>
    [sound:{sound_fn}]
  </div>

  <!-- Question Prompt -->
  <div style="font-size:18px; font-weight:700; color:#0f172a; line-height:1.6; margin-bottom:16px; word-break:keep-all;">
    {prompt_text}
  </div>

  <!-- Choices -->
  <div style="display:flex; flex-direction:column; gap:8px;">
    {choices_html}
  </div>
</div>"""

        # -------------------------------------------------------------
        # BACK
        # -------------------------------------------------------------
        question_choices_back_box = ""
        if is_audio_only:
            b_choices_items = []
            for ch in choices:
                b_choices_items.append(f"<div style='margin:3px 0; font-size:14px; color:#334155;'>• {ch}</div>")
            b_choices_html = "".join(b_choices_items)
            
            question_choices_back_box = f"""<!-- Audio Question & Choices Box -->
<div style="background:#f1f5f9; border:1px solid #cbd5e1; border-radius:8px; padding:12px 14px; margin-bottom:12px;">
  <div style="font-size:12px; font-weight:700; color:#334155; margin-bottom:4px;">🎧 음성 질문 및 선택지 (실전 음성 출제 내용)</div>
  {f'<div style="font-size:15px; font-weight:700; color:#0f172a; margin-bottom:8px; line-height:1.5;">{prompt_text}</div>' if prompt_text else ''}
  <div style="padding-left:4px;">
    {b_choices_html}
  </div>
</div>"""

        dialogue_turns = perfect_dialogues.get(f"{exam}_{qid}", [])
        bilingual_script_content = render_bilingual_script_html(dialogue_turns)
        bilingual_script_box = f"""<!-- Listening Script & Korean Translation Box -->
<div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #0284c7; border-radius:4px 8px 8px 4px; padding:12px 14px; margin-bottom:12px;">
  <div style="font-size:12px; font-weight:700; color:#0369a1; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
    <span>📜 청해 대본 및 한국어 완본 번역 (発話スクリプト・対訳)</span>
    <span style="font-size:11px; font-weight:600; color:#0284c7; background:#e0f2fe; padding:2px 6px; border-radius:4px;">문장별 완벽 대조</span>
  </div>
  <div style="background:#ffffff; padding:10px 12px; border-radius:6px; border:1px solid #e2e8f0;">
    {bilingual_script_content}
  </div>
</div>"""

        new_back = old_back
        p1 = new_back.find('📜')
        if p1 != -1:
            box_start = new_back.rfind('<div style="', 0, p1)
            box_end = new_back.find('<!-- User Mistake', p1)
            if box_end == -1:
                box_end = new_back.find('<!-- Connection', p1)
            if box_end == -1:
                box_end = new_back.rfind('</div>')
            
            replacement = question_choices_back_box + "\n\n" + bilingual_script_box if question_choices_back_box else bilingual_script_box
            new_back = new_back[:box_start] + replacement + "\n\n" + new_back[box_end:]

        final_cards.append({
            'cid': cid,
            'nid': nid,
            'exam': exam,
            'qid': qid,
            'is_audio_only': is_audio_only,
            'ptype': ptype_label,
            'front': front_html,
            'back': new_back
        })

    with open('scratch/final_updated_cards.json', 'w', encoding='utf-8') as f:
        json.dump(final_cards, f, ensure_ascii=False, indent=2)

    print(f"Generated all {len(final_cards)} final cards into scratch/final_updated_cards.json")

if __name__ == '__main__':
    generate_all()
