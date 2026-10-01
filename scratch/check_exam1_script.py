import pypdf
import sys

sys.stdout.reconfigure(encoding='utf-8')
reader = pypdf.PdfReader('references/official_vol2_listening/N2_listening_script.pdf')
full_script = '\n'.join([page.extract_text() for page in reader.pages])

exam1_prompts = [
    (76, "授業で先生が話しています。学生は授業を休んだとき、どのように宿題を確認しますか。"),
    (80, "会社で上司と女性社員が話しています。女の人はこのあと、何をしなければなりませんか。"),
    (90, "環境フォーラムで研究者が話しています。女の人は何について報告していますか。"),
    (94, "部長、社内アンケート、山田さんを除いて全員から回答を得ました。"),
    (97, "課長、プリンター、修理に出したんですが、もう買い替えるしかないって言われました。"),
    (99, "この会議室、壁の色変えたせいか、広く見えるんじゃない？"),
    (102, "昨日のサッカーの決勝戦、見逃しちゃったんだ。"),
    (106, "旅行会社で夫婦が店員からツアーの説明を聞いています。")
]

print("=== CHECKING EXAM 1 WRONG QUESTIONS AGAINST OFFICIAL SCRIPT PDF ===")
for qid, p in exam1_prompts:
    keywords = [k for k in ["宿題", "大阪出張", "緑化", "山田さん", "プリンター", "壁の色", "サッカー", "旅行会社"] if k in p or (qid==80 and k=="大阪出張") or (qid==90 and k=="緑化")]
    in_pdf = any(kw in full_script for kw in keywords)
    print(f"Q{qid:03d}: in official script? {in_pdf} (Keywords searched: {keywords})")
