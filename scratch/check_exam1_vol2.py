import pdfplumber, json, sys, re

sys.stdout.reconfigure(encoding='utf-8')

# Extract full text of PDF
pages_text = []
with pdfplumber.open('references/official_vol2_listening/N2_listening_script.pdf') as pdf:
    for page in pdf.pages:
        pages_text.append(page.extract_text())

full_pdf = "\n\n---PAGE---\n\n".join(pages_text)

# Clean out ruby/furigana artifacts from pdfplumber
# In Japanese official tests, the text has kanji with furigana on top
# Let's inspect pages where Q76, Q80, Q90, Q94, Q97, Q99, Q102, Q106 appear
# Let's see:
# Q76 is 問題1 1番 or 4番? In Vol 2:
# What are the question numbers in Vol 2?
# Let's find out how the 8 questions in Vol 2 map to mondai/number in N2_listening_script.pdf

with open('scratch/perfect_dialogues_25.json', 'r', encoding='utf-8') as f:
    dialogues = json.load(f)

for k in ['1회_76', '1회_80', '1회_90', '1회_94', '1회_97', '1회_99', '1회_102', '1회_106']:
    lines = dialogues[k]
    print(f"\n=== {k} ===")
    for l in lines[:2]:
        print(f"  {l['speaker']}: {l['ja']}")
