import pypdf

reader = pypdf.PdfReader('references/official_vol2_listening/N2_listening_script.pdf')
print("Total pages:", len(reader.pages))
full_text = ""
for i, page in enumerate(reader.pages):
    full_text += f"\n--- Page {i+1} ---\n" + page.extract_text()

with open('scratch/vol2_script.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)

print("Saved scratch/vol2_script.txt, length:", len(full_text))
