# -*- coding: utf-8 -*-
"""Full generator for updated listening error note cards - robust replacement for all templates."""
import sys, json, re, html

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_25_listening_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

with open('scratch/translations_25.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

with open('scratch/extracted_scripts.json', 'r', encoding='utf-8') as f:
    extracted_scripts = json.load(f)

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

def build_bilingual_script_html(script_lines, trans_lines):
    html_items = []
    t_texts = [t[1] if isinstance(t, (list, tuple)) else t for t in trans_lines]
    
    for i, j_line in enumerate(script_lines):
        k_line = t_texts[i] if i < len(t_texts) else ""
        
        j_formatted = j_line
        m_spk = re.match(r'^([^：:]+[：:])(.*)$', j_line)
        if m_spk:
            spk, rest = m_spk.group(1), m_spk.group(2)
            color = "#2563eb" if "女" in spk or "妻" in spk or "生徒" in spk or "学生（女" in spk else "#0284c7" if "先生" in spk else "#475569"
            j_formatted = f"<b style='color:{color};'>{html.escape(spk)}</b>{html.escape(rest)}"
        else:
            j_formatted = html.escape(j_line)
            
        k_formatted = html.escape(k_line)
        
        item_html = f"""<div style="margin-bottom:10px; padding-bottom:8px; border-bottom:1px dashed #e2e8f0;">
  <div style="font-size:14px; line-height:1.7; color:#0f172a; word-break:keep-all;">{j_formatted}</div>
  {f'<div style="font-size:13px; line-height:1.6; color:#475569; margin-top:3px; word-break:keep-all;">↳ {k_formatted}</div>' if k_formatted else ''}
</div>"""
        html_items.append(item_html)
        
    return "\n".join(html_items)

def build_cards():
    results = []
    
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
        
        trans_key = f"{exam}_{qid}"
        trans_list = translations.get(trans_key, [])
        script_data = extracted_scripts[i]
        script_lines = script_data['script_lines']
        
        audio_box_label = "🎧 일본 공식 문제집 제2집 본시험 성우 녹음" if exam == '1회' else "🎧 2023.12 JLPT N2 본시험 성우 원본 음원"
        
        # -------------------------------------------------------------
        # BUILD FRONT
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
        # BUILD BACK
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

        # Bilingual Script Box
        bilingual_script_content = build_bilingual_script_html(script_lines, trans_list)
        bilingual_script_box = f"""<!-- Listening Script & Korean Translation Box -->
<div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #0284c7; border-radius:4px 8px 8px 4px; padding:12px 14px; margin-bottom:12px;">
  <div style="font-size:12px; font-weight:700; color:#0369a1; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
    <span>📜 청해 대본 및 한국어 완본 번역 (発話スクリプト・対訳)</span>
    <span style="font-size:11px; font-weight:600; color:#0284c7; background:#e0f2fe; padding:2px 6px; border-radius:4px;">정밀 대조</span>
  </div>
  <div style="background:#ffffff; padding:10px 12px; border-radius:6px; border:1px solid #e2e8f0;">
    {bilingual_script_content}
  </div>
</div>"""

        # Replace in Back
        new_back = old_back
        
        # Check if card has a script section
        p1 = new_back.find('📜')
        if p1 != -1:
            box_start = new_back.rfind('<div style="', 0, p1)
            
            # Look for boundary after script box
            # Case A: has <!-- User Mistake
            box_end = new_back.find('<!-- User Mistake', p1)
            if box_end == -1:
                # Case B: has <!-- Connection
                box_end = new_back.find('<!-- Connection', p1)
            if box_end == -1:
                # Case C: Cards 2, 3, 7, 8 (which end after the script box div)
                # Find the closing </div> of the script box
                # In cards 2, 3, 7, 8: script box is followed immediately by </div> (outer container close)
                box_end = new_back.rfind('</div>')
            
            if box_start != -1 and box_end != -1 and box_start < box_end:
                replacement = question_choices_back_box + "\n\n" + bilingual_script_box if question_choices_back_box else bilingual_script_box
                new_back = new_back[:box_start] + replacement + "\n\n" + new_back[box_end:]
                print(f"Card {i+1:2d} ({exam} Q{qid:03d}): successfully updated back")
            else:
                print(f"WARN: could not determine box bounds for card {i+1}")
        else:
            print(f"WARN: no script marker in back for card {i+1}")

        results.append({
            'index': i,
            'cid': cid,
            'nid': nid,
            'exam': exam,
            'qid': qid,
            'is_audio_only': is_audio_only,
            'ptype': ptype_label,
            'front': front_html,
            'back': new_back
        })

    with open('scratch/updated_cards_preview.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully generated updated cards for all {len(results)} cards!")

if __name__ == '__main__':
    build_cards()
