import pypdf
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
reader = pypdf.PdfReader('references/official_vol2_listening/N2_listening_script.pdf')
full_script = ''.join([page.extract_text() for page in reader.pages])
# Remove whitespace
clean_pdf = re.sub(r'\s+', '', full_script)

tests = [
    (76, "授業で先生が話しています"),
    (76, "宿題を確認しますか"),
    (80, "大阪出張"),
    (80, "ホテル"),
    (90, "屋上緑化"),
    (90, "環境フォーラム"),
    (94, "山田さんを除いて"),
    (97, "買い替えるしかない"),
    (97, "プリンター"),
    (99, "壁の色変えた"),
    (102, "サッカーの決勝戦"),
    (106, "旅行会社で夫婦"),
    (106, "温泉旅館")
]

for qid, phrase in tests:
    print(f"Q{qid:03d} '{phrase}': {'FOUND IN PDF' if phrase in clean_pdf else 'NOT FOUND'}")
