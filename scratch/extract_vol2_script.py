import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

with pdfplumber.open('references/official_vol2_listening/N2_listening_script.pdf') as pdf:
    for page_idx, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"--- PAGE {page_idx + 1} ---")
        lines = text.split('\n')
        for line in lines[:15]:
            print(line)
        print(f"(Total lines on page: {len(lines)})")
