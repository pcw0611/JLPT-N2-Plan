import json
import re
import sys
from pathlib import Path
import pypdf

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load 9/20 exam questions
with open('quiz_sites/n2-midterm-mock-exam-20260920.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);\s*\n', html, re.DOTALL)
if not m:
    m = re.search(r'const RAW_QUESTIONS = (\[.*?\]);', html, re.DOTALL)
exam_qs = json.loads(m.group(1))

# 2. Extract texts from official PDFs
def get_pdf_text(path):
    reader = pypdf.PdfReader(path)
    return '\n'.join([p.extract_text() for p in reader.pages])

vocab_text = get_pdf_text('references/official_vol2/N2V_vocab.pdf')
grammar_text = get_pdf_text('references/official_vol2/N2G_grammar.pdf')
reading_text = get_pdf_text('references/official_vol2/N2R_reading.pdf')
listening_script = get_pdf_text('references/official_vol2_listening/N2_listening_script.pdf')
listening_problems = get_pdf_text('references/official_vol2_listening/N2_listening_problems.pdf')

all_official = vocab_text + '\n' + grammar_text + '\n' + reading_text + '\n' + listening_script + '\n' + listening_problems
# Normalize whitespace
all_official_clean = re.sub(r'\s+', '', all_official)

def clean_str(s):
    if not s: return ''
    # remove 【...】 and parentheses
    s = re.sub(r'【.*?】', '', s)
    s = re.sub(r'[（）\(\)\s]', '', s)
    return s

results = []

for q in exam_qs:
    qid = q['id']
    sec = q.get('sectionName', '')
    part = q.get('part', '')
    prob = q.get('problemNo', '')
    prompt = q.get('prompt', '')
    choices = q.get('choices', [])
    passage = q.get('passage', '')
    
    # Check matching in official clean text
    # 1. Check prompt snippet
    clean_p = clean_str(prompt)
    clean_pass = clean_str(passage)
    
    # Try finding longest contiguous substrings
    matched = False
    match_type = 'None'
    match_detail = ''
    
    # Check if prompt appears
    if len(clean_p) > 6 and clean_p[:12] in all_official_clean:
        matched = True
        match_type = 'Exact_or_Close_Prompt'
    elif len(clean_p) > 10 and any(clean_p[i:i+10] in all_official_clean for i in range(0, min(20, len(clean_p)-9), 5)):
        matched = True
        match_type = 'Partial_Prompt'
    elif clean_pass and len(clean_pass) > 20 and clean_pass[:20] in all_official_clean:
        matched = True
        match_type = 'Passage_Match'
    else:
        # Check choices
        matching_choices = 0
        for c in choices:
            cc = clean_str(c)
            if len(cc) > 3 and cc in all_official_clean:
                matching_choices += 1
        if matching_choices >= 3:
            matched = True
            match_type = f'Choices_Match_{matching_choices}'
        elif matching_choices >= 1 and len(clean_p) > 4 and any(clean_p[i:i+6] in all_official_clean for i in range(len(clean_p)-5)):
            matched = True
            match_type = 'Weak_Match'
        else:
            match_type = 'Different_or_Custom'

    results.append({
        'id': qid,
        'section': sec,
        'part': part,
        'problemNo': prob,
        'match_type': match_type,
        'prompt': prompt[:60].replace('\n', ' '),
        'choices': choices[:2]
    })

# Summary by section
by_section = {}
for r in results:
    key = f"{r['section']} - {r['part']} ({r['problemNo']})"
    if key not in by_section:
        by_section[key] = {'total': 0, 'official_matched': 0, 'different': 0}
    by_section[key]['total'] += 1
    if r['match_type'] in ['Exact_or_Close_Prompt', 'Passage_Match', 'Choices_Match_3', 'Choices_Match_4']:
        by_section[key]['official_matched'] += 1
    else:
        by_section[key]['different'] += 1

print("\n=== 섹션별 공식 문제집 제2집 일치도 집계 ===")
total_all = len(results)
matched_all = sum(s['official_matched'] for s in by_section.values())
diff_all = sum(s['different'] for s in by_section.values())

for k, v in by_section.items():
    print(f"{k}: 총 {v['total']}문항 | 공식 일치 {v['official_matched']}문항 | 상이/대체 {v['different']}문항")

print(f"\n전체 종합: 총 {total_all}문항 중 공식 제2집 일치 {matched_all}문항, 상이/대체 {diff_all}문항")
