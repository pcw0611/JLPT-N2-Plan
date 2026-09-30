import json
import re

def update_portal():
    with open('database/past_exams/exam_index.json', 'r', encoding='utf-8') as f:
        exams = json.load(f)

    exam_map = {e['examId']: e for e in exams}

    title_to_id = {
        "日本語能力試験 公式問題集 第2集 (N2 完本)": "OFFICIAL-VOL2",
        "2023年 第2回 (12月) JLPT N2 本試験 (完本 102問)": "2023-12",
        "2023年 第2回 (12月) JLPT N2 本試験": "2023-12",
    }
    for e in exams:
        title_to_id[e['title']] = e['examId']

    html_path = 'jlpt-calendar-site/public/exams/past-exams-portal.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Badge HTML mapping
    badge_templates = {
        '최상': '<span class="px-2 py-0.5 rounded text-[11px] font-extrabold bg-rose-500/20 text-rose-300 border border-rose-500/40 flex items-center gap-1 shadow-sm"><span>🔥</span> 난이도 최상 (불시험)</span>',
        '상': '<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center gap-1 shadow-sm"><span>⚡</span> 난이도 상</span>',
        '중상': '<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-yellow-500/20 text-yellow-300 border border-yellow-500/30 flex items-center gap-1 shadow-sm"><span>⚖️</span> 난이도 중상</span>',
        '중': '<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1 shadow-sm"><span>📘</span> 난이도 중 (표준)</span>'
    }

    # Delineate strictly the grid section
    split_str_1 = '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">'
    split_str_2 = '<!-- Exam Structure Guide Modal -->'

    before_grid, rest = html.split(split_str_1, 1)
    cards_section, after_grid = rest.split(split_str_2, 1)

    # Split cards_section by the card pattern
    # Each card starts with `<div class="bg-slate-800/60`
    card_chunks = cards_section.split('<div class="bg-slate-800/60')
    prefix = card_chunks[0]
    raw_cards = card_chunks[1:]

    print(f"Total raw exam cards found: {len(raw_cards)}")

    processed_cards = []
    diff_counts = {'최상': 0, '상': 0, '중상': 0, '중': 0}

    for idx, card in enumerate(raw_cards):
        # find title
        m_title = re.search(r'<span class="font-bold text-base text-white">(.*?)</span>', card)
        title = m_title.group(1).strip() if m_title else ""

        eid = title_to_id.get(title)
        if not eid:
            for k, v in title_to_id.items():
                if k in title or title in k:
                    eid = v
                    break

        exam_info = exam_map.get(eid, {})
        diff_grade = exam_info.get('difficultyGrade', '중')
        diff_desc = exam_info.get('difficulty', f'{diff_grade} 난이도')
        diff_counts[diff_grade] = diff_counts.get(diff_grade, 0) + 1

        badge_html = badge_templates.get(diff_grade, badge_templates['중'])

        # Card container tag construction
        m_header_tag = re.match(r'^([^>]*)>', card)
        orig_tag_content = m_header_tag.group(1) if m_header_tag else ""
        rest_of_card = card[len(orig_tag_content)+1:]

        # Cleanly build open div tag
        clean_tag_content = orig_tag_content.replace(' exam-card', '')
        clean_tag_content = re.sub(r'\s*data-difficulty="[^"]*"', '', clean_tag_content)
        
        full_open_tag = f'<div class="exam-card bg-slate-800/60{clean_tag_content} data-difficulty="{diff_grade}">'

        # Insert difficulty badge into title header
        # Pattern: <span class="font-bold text-base text-white">...</span> (badges here) </div>
        title_box_match = re.search(r'(<div class="flex items-center gap-2">\s*<span class="font-bold text-base text-white">.*?</span>)(.*?)(</div>)', rest_of_card, re.DOTALL)
        if title_box_match:
            title_part = title_box_match.group(1)
            badges_part = title_box_match.group(2)
            close_div = title_box_match.group(3)

            # remove any old difficulty badge
            clean_badges = re.sub(r'<span class="[^"]*">[^<]*난이도[^<]*</span>', '', badges_part)
            new_title_box = f'{title_part}{clean_badges}\n              {badge_html}{close_div}'
            rest_of_card = rest_of_card[:title_box_match.start()] + new_title_box + rest_of_card[title_box_match.end():]

        # Update metadata line
        meta_match = re.search(r'(<div class="flex [^"]*text-xs text-slate-400">)(.*?)(</div>)', rest_of_card, re.DOTALL)
        if meta_match:
            open_div = meta_match.group(1)
            meta_inner = meta_match.group(2)
            end_div = meta_match.group(3)

            # Clean any old difficulty spans
            meta_inner_clean = re.sub(r'<span>\s*난이도:\s*[^<]*</span>', '', meta_inner)
            meta_inner_clean = re.sub(r'<span class="[^"]*">\s*난이도:\s*[^<]*</span>', '', meta_inner_clean)

            diff_color = "text-rose-400 font-bold" if diff_grade == '최상' else "text-amber-400 font-semibold" if diff_grade == '상' else "text-yellow-400 font-semibold" if diff_grade == '중상' else "text-emerald-400 font-semibold"
            diff_span = f'<span class="{diff_color}">난이도: {diff_desc}</span>'

            # Reconstruct clean metadata
            items = [item.strip() for item in re.findall(r'<span[^>]*>.*?</span>', meta_inner_clean, re.DOTALL)]
            items.append(diff_span)

            new_meta_inner = "\n            " + "\n            ".join(items) + "\n          "
            rest_of_card = rest_of_card[:meta_match.start()] + f'<div class="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-400">{new_meta_inner}</div>' + rest_of_card[meta_match.end():]

        processed_cards.append(f'{full_open_tag}{rest_of_card}')

    print(f"Processed cards: {len(processed_cards)}, Difficulty counts: {diff_counts}")

    # Build Filter Bar
    filter_bar = f'''      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-slate-700/60">
        <h2 class="text-xl font-bold flex items-center gap-2">
          <span>📚 회차별 기출 상세 목록 및 출제 스펙</span>
          <span class="text-xs font-normal text-slate-400">(2010〜2023 전 28회분)</span>
        </h2>
        <div class="flex flex-wrap items-center gap-1.5" id="difficultyFilterBar">
          <button type="button" onclick="setDiffFilter('all', this)" class="diff-btn active px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-600 text-white transition-all shadow cursor-pointer">전체 (28회)</button>
          <button type="button" onclick="setDiffFilter('최상', this)" class="diff-btn px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-rose-300 border border-rose-500/40 transition-all cursor-pointer">🔥 최상 ({diff_counts.get('최상', 0)}회)</button>
          <button type="button" onclick="setDiffFilter('상', this)" class="diff-btn px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-amber-300 border border-amber-500/30 transition-all cursor-pointer">⚡ 상 ({diff_counts.get('상', 0)}회)</button>
          <button type="button" onclick="setDiffFilter('중상', this)" class="diff-btn px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-yellow-300 border border-yellow-500/30 transition-all cursor-pointer">⚖️ 중상 ({diff_counts.get('중상', 0)}회)</button>
          <button type="button" onclick="setDiffFilter('중', this)" class="diff-btn px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-emerald-300 border border-emerald-500/30 transition-all cursor-pointer">📘 중 ({diff_counts.get('중', 0)}회)</button>
        </div>
      </div>'''

    before_grid_updated = re.sub(
        r'<div class="flex items-center justify-between">\s*<h2 class="text-xl font-bold flex items-center gap-2">.*?</h2>\s*</div>',
        filter_bar,
        before_grid,
        flags=re.DOTALL
    )

    filter_script = '''
  <script>
    function setDiffFilter(diff, btn) {
      document.querySelectorAll('#difficultyFilterBar .diff-btn').forEach(b => {
        b.classList.remove('bg-blue-600', 'text-white', 'shadow');
        b.classList.add('bg-slate-800');
      });
      btn.classList.remove('bg-slate-800');
      btn.classList.add('bg-blue-600', 'text-white', 'shadow');

      const cards = document.querySelectorAll('.exam-card');
      cards.forEach(card => {
        if (diff === 'all' || card.getAttribute('data-difficulty') === diff) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    }
  </script>
</body>'''

    new_cards_section = prefix + "".join(processed_cards)
    
    if 'function setDiffFilter' not in after_grid:
        after_grid = after_grid.replace('</body>', filter_script)

    final_html = before_grid_updated + split_str_1 + new_cards_section + split_str_2 + after_grid

    with open('jlpt-calendar-site/public/exams/past-exams-portal.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
    with open('quiz_sites/past-exams-portal.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

    print("Portal HTML updated successfully in both public and quiz_sites!")

if __name__ == '__main__':
    update_portal()
