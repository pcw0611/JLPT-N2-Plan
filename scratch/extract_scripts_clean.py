# -*- coding: utf-8 -*-
"""Extract script section HTML and text from all 25 cards."""
import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_25_listening_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

extracted = []

for i, c in enumerate(cards):
    back = c['back']
    pos = back.find('📜')
    script_html = ''
    if pos != -1:
        sub = back[pos:pos+4000]
        # Look for the inner div containing the dialogue
        # Pattern 1: has inner div
        m = re.search(r'📜[^\n<]+(?:</span>)?\s*</div>\s*<div[^>]*>(.*?)</div>\s*</div>', sub, re.DOTALL)
        if m:
            script_html = m.group(1).strip()
        else:
            # Pattern 2: older structure
            m2 = re.search(r'📜[^\n<]+(?:</span>)?\s*</div>\s*(<div.*?)<!--', sub, re.DOTALL)
            if m2:
                script_html = m2.group(1).strip()
            else:
                script_html = "ERROR_NOT_FOUND"
    
    clean_text = re.sub(r'<[^>]+>', '\n', script_html)
    clean_lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
    
    print(f"CARD {i+1:2d} ({c['exam']} Q{c['qid']:03d}): {len(clean_lines)} lines, {len(' '.join(clean_lines))} chars")
    extracted.append({
        'index': i,
        'cid': c['cid'],
        'nid': c['nid'],
        'exam': c['exam'],
        'qid': c['qid'],
        'sound': c['sound'],
        'script_lines': clean_lines,
        'script_html': script_html
    })

with open('scratch/extracted_scripts.json', 'w', encoding='utf-8') as out:
    json.dump(extracted, out, ensure_ascii=False, indent=2)

print("\nSaved all extracted scripts to scratch/extracted_scripts.json")
