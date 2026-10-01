import subprocess

# Let's inspect silences below 108s in N2Q4
cmd = ['ffmpeg', '-i', 'references/official_vol2_listening/N2Q4_mondai4_sokuji.mp3', '-af', 'silencedetect=noise=-30dB:d=1.0', '-f', 'null', '-']
res = subprocess.run(cmd, capture_output=True, text=True, errors='replace')
for line in res.stderr.splitlines():
    if 'silence_start' in line or 'silence_end' in line:
        print(line)
