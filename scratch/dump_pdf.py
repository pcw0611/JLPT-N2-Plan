import pypdf
import sys

sys.stdout.reconfigure(encoding='utf-8')
reader = pypdf.PdfReader('references/official_vol2_listening/N2_listening_script.pdf')

with open('scratch/official_vol2_full_script.txt', 'w', encoding='utf-8') as f:
    for idx, page in enumerate(reader.pages):
        f.write(f"\n\n=== PAGE {idx+1} ===\n\n")
        f.write(page.extract_text())

print(f"Dumped {len(reader.pages)} pages to scratch/official_vol2_full_script.txt")
