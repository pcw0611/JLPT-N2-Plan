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
    
    meaning = divs[0].get_text(strip=True) if divs else ''
    connection = ''
    core_meaning = ''
    ex1_ja = ''
    ex1_ko = ''
    ex1_ko_target = ''
    diff_point = ''
    exam_signal = ''
    
    for i, d in enumerate(divs):
        txt = d.get_text(strip=True)
        if txt == '접속' and i + 1 < len(divs):
            connection = divs[i+1].get_text(strip=True)
        elif txt == '핵심 의미' and i + 1 < len(divs):
            core_meaning = divs[i+1].get_text(strip=True)
        elif txt == '구별 포인트' and i + 1 < len(divs):
            diff_point = divs[i+1].get_text(strip=True)
        elif txt == '시험 신호' and i + 1 < len(divs):
            exam_signal = divs[i+1].get_text(strip=True)
        elif txt == '예문 1' and i + 1 < len(divs):
            ex1_div = divs[i+1]
            # find japanese part and korean part
            spans = ex1_div.find_all('span')
            # Korean span is typically the one with color:#6b7280
            ko_span = None
            for s in spans:
                style = s.get('style', '')
                if '#6b7280' in style:
                    ko_span = s
                    break
            
            if ko_span:
                # Highlighted keyword in korean
                hl_span = ko_span.find('span')
                if hl_span:
                    ex1_ko_target = hl_span.get_text(strip=True)
                ex1_ko = ko_span.get_text(strip=True)
            
            # Japanese sentence: remove the korean span to get ja sentence
            ex1_clone = BeautifulSoup(str(ex1_div), 'html.parser')
            for s in ex1_clone.find_all('span'):
                if getattr(s, 'attrs', None) and '#6b7280' in s.attrs.get('style', ''):
                    s.decompose()
            ex1_ja = ex1_clone.get_text(strip=True)

    parsed_items.append({
        'id': f'n2-grammar-{num}',
        'num': num,
        'pattern': pattern,
        'meaning': meaning,
        'connection': connection,
        'core_meaning': core_meaning,
        'sentence_ko': ex1_ko,
        'target_ko': ex1_ko_target or meaning.replace('~', '').strip(),
        'sentence_ja': ex1_ja,
        'diff_point': diff_point,
        'exam_signal': exam_signal
    })

print(f'Total parsed items: {len(parsed_items)}')
out_path = Path(__file__).resolve().parent / 'n2_grammar_dataset.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(parsed_items, f, ensure_ascii=False, indent=2)

print(f'Saved dataset to {out_path}')
