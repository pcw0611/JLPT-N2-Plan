# -*- coding: utf-8 -*-
"""Classify listening cards by JLPT listening problem type and identify front issues."""
import sys, sqlite3, re, html
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

dst = Path(r'C:\Users\pcw06\AppData\Local\Temp\anki_listening_check')
con = sqlite3.connect(dst / 'collection.anki2')
cur = con.cursor()

DECK_ID = 1790835146324

cur.execute('''
    SELECT c.id, c.nid, n.flds, n.tags
    FROM cards c
    JOIN notes n ON c.nid = n.id
    WHERE c.did = ?
    ORDER BY c.id
''', (DECK_ID,))

rows = cur.fetchall()

def strip_html(text):
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    return text.strip()

# Classify by problem type
for i, (cid, nid, flds, tags) in enumerate(rows):
    field_values = flds.split(chr(0x1f))
    front = field_values[0]
    back = field_values[1] if len(field_values) > 1 else ''
    
    front_text = strip_html(front)
    
    q_match = re.search(r'Q(\d+)', tags)
    q_num = f'Q{q_match.group(1)}' if q_match else '?'
    
    # Determine problem type from front text
    ptype = 'unknown'
    if '問題1' in front_text or '問題１' in front_text or '課題理解' in front_text:
        ptype = '問題1(課題理解)'
    elif '問題2' in front_text or '問題２' in front_text or 'ポイント理解' in front_text:
        ptype = '問題2(ポイント理解)'
    elif '問題3' in front_text or '問題３' in front_text or '概要理解' in front_text:
        ptype = '問題3(概要理解)'
    elif '問題4' in front_text or '問題４' in front_text or '即時応答' in front_text:
        ptype = '問題4(即時応答)'
    elif '問題5' in front_text or '問題５' in front_text or '統合理解' in front_text:
        ptype = '問題5(統合理解)'
    
    # What's on the front?
    front_has_question = bool(re.search(r'質問|何を|何が|どう|何について|いつ|どこ|だれ|どの', front_text))
    front_has_choices = bool(re.search(r'[1-4]\s*[\.．]|1番|2番|3番|4番', front_text))
    
    # For 問題3 and 問題4: front should NOT show question/choices (they come from audio)
    # For 問題1 and 問題2: question is printed on paper, choices may be printed
    should_hide_from_front = ptype in ['問題3(概要理解)', '問題4(即時応答)']
    
    # Check back for Korean translation of script
    back_text = strip_html(back)
    has_korean_translation = bool(re.search(r'해석|번역|한국어 해석|의미', back_text))
    
    # Audio location
    front_audio = re.findall(r'\[sound:([^\]]+)\]', front)
    back_audio = re.findall(r'\[sound:([^\]]+)\]', back)
    
    exam = '1회' if '1회' in tags else '2회' if '2회' in tags else '?'
    
    issue = ''
    if should_hide_from_front and front_has_question:
        issue += ' ⚠️FRONT_SHOWS_QUESTION'
    if should_hide_from_front and front_has_choices:
        issue += ' ⚠️FRONT_SHOWS_CHOICES'
    if not should_hide_from_front and front_has_choices:
        # For 問題1/2, choices on front is OK (printed on test paper)
        pass
    
    print(f"{i+1:2d} {exam} {q_num:>5} {ptype:<20} audio_front={bool(front_audio)} Q_front={front_has_question} C_front={front_has_choices}{issue}")

# Summary
print("\n=== JLPT Listening Problem Types ===")
print("問題1(課題理解): Question printed, choices 1-4 printed on paper → OK to show on front")  
print("問題2(ポイント理解): Question printed, choices 1-4 printed → OK to show on front")
print("問題3(概要理解): NOTHING printed (何も印刷されていません) → question & choices from audio only → HIDE from front")
print("問題4(即時応答): NOTHING printed → audio only → HIDE from front")
print("問題5(統合理解): Question printed, choices printed → OK to show on front")

con.close()
