import subprocess
import re

def get_silences(filepath):
    cmd = ['ffmpeg', '-i', filepath, '-af', 'silencedetect=noise=-35dB:d=1.5', '-f', 'null', '-']
    res = subprocess.run(cmd, capture_output=True, text=True, errors='replace')
    out = res.stderr
    
    silences = []
    starts = re.findall(r'silence_start: ([\d\.]+)', out)
    ends = re.findall(r'silence_end: ([\d\.]+)', out)
    durs = re.findall(r'silence_duration: ([\d\.]+)', out)
    
    for s, e, d in zip(starts, ends, durs):
        silences.append((float(s), float(e), float(d)))
    return silences

print("--- N2Q3 (Mondai 3) ---")
for s, e, d in get_silences('references/official_vol2_listening/N2Q3_mondai3_gaiyou.mp3'):
    if d > 4.0:
        print(f"Long silence: {s:.1f}s ~ {e:.1f}s ({d:.1f}s)")

print("--- N2Q4 (Mondai 4 - check Q10, Q11, Q12) ---")
for s, e, d in get_silences('references/official_vol2_listening/N2Q4_mondai4_sokuji.mp3'):
    if d > 6.0:
        print(f"Answer silence: {s:.1f}s ~ {e:.1f}s ({d:.1f}s)")

print("--- N2Q5 (Mondai 5) ---")
for s, e, d in get_silences('references/official_vol2_listening/N2Q5_mondai5_tougou.mp3'):
    if d > 4.0:
        print(f"Long silence: {s:.1f}s ~ {e:.1f}s ({d:.1f}s)")
