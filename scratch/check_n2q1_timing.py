import subprocess, os

# Let's check the duration of N2Q1_mondai1_kadai.mp3
cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', 'references/official_vol2_listening/N2Q1_mondai1_kadai.mp3']
res = subprocess.run(cmd, capture_output=True, text=True)
print("N2Q1 total duration:", res.stdout.strip())

# In N2_listening_script.pdf:
# Page 1 has:
# 例: 授業で先生が話しています。学生は授業を休んだとき、どのように宿題を確認しますか。
# 1番: 会社で課長と男の人が話しています。男の人はこのあと何をしますか。
# Page 2 has: 2番, 3番
# Page 3 has: 4番
# Page 4 has: 5番 (うちのお茶の葉の品質管理のことで...)

# What did slice_vol2_clips.py do?
# It sliced:
# qid 76: start 156.0, duration 77.5
# qid 80: start 535.5, duration 96.0

print("Check slice_vol2_clips.py settings:")
print("qid 76 sliced from 156.0s to 233.5s")
print("qid 80 sliced from 535.5s to 631.5s")
