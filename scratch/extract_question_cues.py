import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    text = f.read()

blocks = re.split(r'\n\n+', text)
cues = []
for b in blocks:
    lines = [l.strip() for l in b.splitlines() if l.strip()]
    if len(lines) >= 2 and '-->' in lines[0]:
        time_range = lines[0]
        cue_text = ' '.join(lines[1:])
        cue_text = re.sub(r'<[^>]+>', '', cue_text)
        if cue_text:
            cues.append((time_range, cue_text))

def deduplicate_text(cue_list):
    # YouTube VTT often has rolling lines: "A B", "B C", "C D"
    # Let's extract unique sentences / phrases
    combined = " ".join([c[1] for c in cue_list])
    # split words/phrases or clean repetitions
    return combined

print("--- Searching for Question markers ---")
markers = [
    ("Q75 (M1-3)", "3番", "4番"),
    ("Q76 (M1-4)", "4番", "5番"),
    ("Q77 (M1-5)", "5番", "問題 2"),
    ("Q78 (M2-1)", "21番", "2番"),
    ("Q80 (M2-3)", "3番", "4番"),
    ("Q82 (M2-5)", "5番", "6番"),
    ("Q85 (M3-2)", "2番", "3番"),
    ("Q86 (M3-3)", "3番", "4番"),
    ("Q88 (M3-5)", "5番", "問題 4"),
    ("Q89 (M4-1)", "1番", "2番"),
    ("Q90 (M4-2)", "2番", "3番"),
    ("Q91 (M4-3)", "3番", "4番"),
    ("Q95 (M4-7)", "7番", "8番"),
    ("Q97 (M4-9)", "9番", "10番"),
    ("Q98 (M4-10)", "10番", "11番"),
    ("Q99 (M4-11)", "11番", "問題 5"),
    ("Q101 (M5-2)", "2番", "3番")
]

for i, (t, c) in enumerate(cues):
    # Print cues that contain question numbers
    for label, start_k, _ in markers:
        if start_k in c:
            pass # we can do more specific print
