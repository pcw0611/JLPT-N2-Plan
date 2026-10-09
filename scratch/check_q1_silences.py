import subprocess

# Let's inspect silences between 0 and 200
cmd = ['ffmpeg', '-ss', '0', '-t', '250', '-i', 'references/official_vol2_listening/N2Q1_mondai1_kadai.mp3', '-af', 'silencedetect=noise=-30dB:d=1.0', '-f', 'null', '-']
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stderr)
