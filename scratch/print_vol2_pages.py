import pdfplumber, sys

sys.stdout.reconfigure(encoding='utf-8')

pages_to_check = [1, 4, 10, 12, 13, 16]

with pdfplumber.open('references/official_vol2_listening/N2_listening_script.pdf') as pdf:
    for p in pages_to_check:
        print(f"\n==================== PAGE {p} ====================")
        page_text = pdf.pages[p-1].extract_text()
        print(page_text)
