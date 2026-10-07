# -*- coding: utf-8 -*-
import sqlite3, json, sys, re
from pathlib import Path
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

TEMP_DB = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_inspect_1007\collection.anki2')
con = sqlite3.connect(TEMP_DB)
cur = con.cursor()
cur.execute('SELECT n.flds FROM cards c JOIN notes n ON c.nid = n.id WHERE c.did = 1788792649376 ORDER BY n.id')
rows = cur.fetchall()

parsed_items = []
for idx, r in enumerate(rows):
    parts = r[0].split('\x1f')
    front_raw, back_raw = parts[0], parts[1]
    
    # parse front: number, pattern
    m_num = re.search(r'>(\d{3})<', front_raw)
    num = m_num.group(1) if m_num else f'{idx+1:03d}'
    
    m_pat = re.search(r'margin:8px 0 14px">([^<]+)<', front_raw)
    pattern = m_pat.group(1).strip() if m_pat else ''
    if not pattern:
        m_pat2 = re.search(r'〜[^<]+', front_raw)
        pattern = m_pat2.group(0).strip() if m_pat2 else f'문형 {num}'

    soup = BeautifulSoup(back_raw, 'html.parser')
    divs = soup.find_all('div')
    
    meaning = ''
    connection = ''
    core_meaning = ''
    diff_point = ''
    exam_signal = ''
    
    ex1_ja = ''
    ex1_ja_target = ''
    ex1_ko = ''
    ex1_ko_target = ''
    
    for i, d in enumerate(divs):
        txt = d.get_text(strip=True)
        if txt.startswith('접속') or txt == '접속':
            c_val = txt.replace('접속', '').strip()
            connection = c_val if c_val else (divs[i+1].get_text(strip=True) if i + 1 < len(divs) else '')
        elif txt.startswith('핵심 의미') or txt == '핵심 의미':
            c_val = txt.replace('핵심 의미', '').strip()
            core_meaning = c_val if c_val else (divs[i+1].get_text(strip=True) if i + 1 < len(divs) else '')
        elif txt.startswith('구별 포인트') or txt == '구별 포인트':
            c_val = txt.replace('구별 포인트', '').strip()
            diff_point = c_val if c_val else (divs[i+1].get_text(strip=True) if i + 1 < len(divs) else '')
        elif txt.startswith('시험 신호') or txt == '시험 신호':
            c_val = txt.replace('시험 신호', '').strip()
            exam_signal = c_val if c_val else (divs[i+1].get_text(strip=True) if i + 1 < len(divs) else '')

    for d in divs[:4]:
        style = d.get('style', '')
        if '#52606d' in style and ('font-size:20px' in style or 'font-size:21px' in style):
            meaning = d.get_text(strip=True)
            break
    if not meaning and divs:
        meaning = divs[0].get_text(strip=True)

    # 1. Look for '예문 1'
    ex1_div = None
    for i, d in enumerate(divs):
        if d.get_text(strip=True) == '예문 1' and i + 1 < len(divs):
            ex1_div = divs[i+1]
            break

    # 2. If no '예문 1' (e.g. cards 026-035), find div with font-size:20px after header
    if not ex1_div:
        for d in divs:
            style = d.get('style', '')
            if 'font-size:20px' in style and ('margin-top:16px' in style or 'margin-top:15px' in style):
                ex1_div = d
                # Korean sentence is the following div
                next_div = d.find_next_sibling('div')
                if next_div:
                    raw_s = str(next_div)
                    cleaned = re.sub(r'<[^>]+>', ' ', raw_s)
                    ex1_ko = ' '.join(cleaned.split())
                    hl_k = next_div.find('span')
                    if hl_k:
                        ex1_ko_target = hl_k.get_text(strip=True)
                break

    if ex1_div:
        # Check if ex1_div contains korean span inside it
        ko_span = None
        for s in ex1_div.find_all('span'):
            style = s.get('style', '')
            if '#6b7280' in style:
                ko_span = s
                break
        
        if ko_span:
            # Preserve spacing between tags
            raw_s = str(ko_span)
            cleaned = re.sub(r'<[^>]+>', ' ', raw_s)
            ex1_ko = ' '.join(cleaned.split())
            hl_k = ko_span.find('span')
            if hl_k:
                ex1_ko_target = hl_k.get_text(strip=True)

        # Find Japanese target: highlighted span (yellow)
        for s in ex1_div.find_all('span'):
            style = s.get('style', '')
            if ('250, 204, 21' in style or '#fef08a' in style) and s != ko_span and not (ko_span and s in ko_span.descendants):
                ex1_ja_target = s.get_text(strip=True)
                break

        # Clone and decompose korean to get pure japanese sentence
        clone = BeautifulSoup(str(ex1_div), 'html.parser')
        for s in clone.find_all('span'):
            style = s.attrs.get('style', '') if getattr(s, 'attrs', None) else ''
            if '#6b7280' in style:
                s.decompose()
        # Also decompose br
        for br in clone.find_all('br'):
            br.decompose()
        ex1_ja = clone.get_text(strip=True)

    # Fallback for target if not explicitly highlighted in Japanese span (e.g., cards 012, 039, 044, 053)
    if not ex1_ja_target and ex1_ja:
        if num == '012':
            ex1_ja_target = '読みかけ'
        elif num == '039':
            ex1_ja_target = 'ざるを得なかった'
        elif num == '044':
            ex1_ja_target = '食べずに'
        elif num == '053':
            ex1_ja_target = '開けたとたんに'
        else:
            # Try to match cleaned pattern
            clean_p = pattern.replace('〜', '').split('／')[0].split('（')[0].strip()
            if clean_p and clean_p in ex1_ja:
                ex1_ja_target = clean_p

    # Construct sentence_ja_blank
    sentence_ja_blank = ''
    if ex1_ja and ex1_ja_target and ex1_ja_target in ex1_ja:
        sentence_ja_blank = ex1_ja.replace(ex1_ja_target, '（　　）', 1)
    elif ex1_ja:
        # Fallback search
        clean_p = pattern.replace('〜', '').split('／')[0].split('（')[0].strip()
        if clean_p and clean_p in ex1_ja:
            sentence_ja_blank = ex1_ja.replace(clean_p, '（　　）', 1)
            ex1_ja_target = clean_p
        else:
            sentence_ja_blank = ex1_ja + ' （　　）'

    parsed_items.append({
        'id': f'n2-grammar-{num}',
        'num': num,
        'pattern': pattern,
        'meaning': meaning,
        'connection': connection,
        'core_meaning': core_meaning,
        'sentence_ja': ex1_ja,
        'sentence_ja_target': ex1_ja_target,
        'sentence_ja_blank': sentence_ja_blank,
        'sentence_ko': ex1_ko,
        'target_ko': ex1_ko_target or meaning.replace('~', '').strip(),
        'diff_point': diff_point,
        'exam_signal': exam_signal
    })

print(f'Total parsed items: {len(parsed_items)}')
out_path = Path(__file__).resolve().parent / 'n2_grammar_dataset.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(parsed_items, f, ensure_ascii=False, indent=2)

print(f'Saved dataset to {out_path}')
