import pdfplumber, sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open('references/official_vol2_listening/N2_listening_problems.pdf') as pdf:
    for idx, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"--- PROBLEM PAGE {idx+1} ---")
        print(text)
