import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('scratch/reconstructed_transcript.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Join all lines without timestamps
raw_full = "".join([l.split('] ', 1)[1] if '] ' in l else l for l in lines])

# Let's locate the 17 questions in raw_full:
# Q75: M1-3
# Q76: M1-4
# Q77: M1-5
# Q78: M2-1
# Q80: M2-3
# Q82: M2-5
# Q85: M3-2
# Q86: M3-3
# Q88: M3-5
# Q89: M4-1
# Q90: M4-2
# Q91: M4-3
# Q95: M4-7
# Q97: M4-9
# Q98: M4-10
# Q99: M4-11
# Q101: M5-2

print("Length of full raw text:", len(raw_full))

# Let's write a script that searches for snippets of each question
keywords = [
    (75, "日本語のクラスで先生が留学生に"),
    (76, "青葉市の市民文化祭"),
    (77, "うちで育てている"),
    (78, "あるアナウンサーについて"),
    (80, "服のリサイクルについて"),
    (82, "ビーチコーミングの話"),
    (85, "南村に来ています"),
    (86, "りんごの木"),
    (87, "医療器具"),
    (88, "ワシ伝統的な日本の紙"),
    (89, "明日もアルバイトに来てもらえると"),
    (90, "僕、泣かずにはいられなかったよ"),
    (91, "本日本社から専務がお越しになると"),
    (95, "今日の作業はこの辺で切り上げましょうか"),
    (97, "今日の花火大会は延期にしましょう"),
    (98, "明日の会議、課長の代わりに進行役"),
    (99, "先日ご依頼いただいた件ですが"),
    (101, "語学研修の宿泊先")
]

for qid, kw in keywords:
    pos = raw_full.find(kw.replace(' ', ''))
    if pos == -1:
        # try shorter kw
        kw_short = kw[:6]
        pos = raw_full.find(kw_short)
    print(f"Q{qid} ('{kw[:10]}...'): found at {pos}")
    if pos != -1:
        start = max(0, pos - 80)
        end = min(len(raw_full), pos + 350)
        print(f"  Snippet: {raw_full[start:end]}\n")
    else:
        print(f"  NOT FOUND: {kw}\n")
