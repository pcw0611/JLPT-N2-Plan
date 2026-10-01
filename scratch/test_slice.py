import subprocess

def test_slice(infile, start, dur, outfile):
    cmd = ['ffmpeg', '-y', '-ss', str(start), '-t', str(dur), '-i', infile, outfile]
    subprocess.run(cmd, capture_output=True)

# Test Q76
test_slice('references/official_vol2_listening/N2Q1_mondai1_kadai.mp3', 156, 78, 'scratch/test_q76.mp3')
print("Sliced test_q76.mp3")

# Check Mondai 4: let's verify what question starts at each interval
# In Mondai 4, let's test 116~143, 151~177, etc.
