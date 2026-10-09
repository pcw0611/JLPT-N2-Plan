import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/n2_2023_12_sub.ja.vtt', 'r', encoding='utf-8') as f:
    vtt_lines = f.readlines()

def to_sec(ts):
    parts = ts.split(':')
    return float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])

cues = []
current_start = None
current_end = None
current_text = []

for line in vtt_lines:
    m = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})', line)
    if m:
        if current_start is not None and current_text:
            cleaned = ' '.join(current_text)
            cues.append((current_start, current_end, cleaned))
        current_start = to_sec(m.group(1))
        current_end = to_sec(m.group(2))
        current_text = []
    elif current_start is not None and line.strip() and not line.startswith('NOTE') and not line.startswith('WEBVTT'):
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean:
            current_text.append(clean)

matched = []
for c_start, c_end, c_text in cues:
    if 185 <= c_start <= 280:
        lines = c_text.split('\n')
        for l in lines:
            l_s = l.strip()
            if l_s and (not matched or matched[-1] != l_s):
                matched.append(l_s)

print('Q75 AUDIO RAW:')
print(' '.join(matched))

with open('scratch/perfect_dialogues_25.json', 'r', encoding='utf-8') as f:
    dialogues = json.load(f)

print('\nQ75 CURRENT SCRIPT:')
for d in dialogues.get('2회_75', []):
    print(f"  {d['speaker']}: {d['ja']}")
