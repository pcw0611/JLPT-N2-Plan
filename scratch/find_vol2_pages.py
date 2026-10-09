import pdfplumber, json, sys

sys.stdout.reconfigure(encoding='utf-8')

pages = []
with pdfplumber.open('references/official_vol2_listening/N2_listening_script.pdf') as pdf:
    for idx, page in enumerate(pdf.pages):
        pages.append((idx + 1, page.extract_text()))

checks = [
    ('1회_76', '休むときは'),
    ('1회_80', 'お茶の葉'),
    ('1회_90', '健康のため'),
    ('1회_94', '山田さん'),
    ('1회_97', 'プリンター'),
    ('1회_99', '壁の色'),
    ('1회_102', 'スキー'),
    ('1회_106', '交通安全')
]

for key, kw in checks:
    found = False
    for p_num, text in pages:
        if kw in text:
            print(f"{key} ({kw}) found on page {p_num}")
            found = True
            break
    if not found:
        print(f"{key} ({kw}) NOT FOUND!")
