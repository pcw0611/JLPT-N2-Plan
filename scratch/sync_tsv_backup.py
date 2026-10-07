# -*- coding: utf-8 -*-
"""Update scratch/anki_error_notes_listening_25.tsv backup with latest updated cards."""
import sys, json

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/final_updated_cards.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

with open('scratch/anki_error_notes_listening_25.tsv', 'w', encoding='utf-8') as out:
    for c in cards:
        exam_tag = '1회_공식제2집' if c['exam'] == '1회' else '2회_202312'
        tags = f"{exam_tag} JLPT_N2 Q{c['qid']} 오답노트 음원포함 청해"
        f_val = c['front'].replace('"', '""')
        b_val = c['back'].replace('"', '""')
        out.write(f'"{f_val}"\t"{b_val}"\t{tags}\n')

print(f"Synchronized scratch/anki_error_notes_listening_25.tsv backup with {len(cards)} updated cards!")
